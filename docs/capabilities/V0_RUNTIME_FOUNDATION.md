# V0 运行底座快速复用

状态：host-validated

基线：`71d827a` / `vision-v0-baseline`

## 1. 用途

在没有真实相机时从文件读取图片，经过 Pipeline 生成结构化结果，并可输出 JSONL 或编码为
视觉-MCU 协议帧。以后圆、矩形、光斑、黑线和棋盘算法都应接入这条数据流。

## 2. 稳定接口

开发 checkout 尚未执行 editable install 时，PowerShell 先设置：

```powershell
$env:PYTHONPATH = (Resolve-Path 'src').Path
```

正式虚拟环境推荐执行 `python -m pip install -e .`，避免依赖临时环境变量。

```python
from echo_vision.adapters import FileImageSource, JsonlResultSink
from echo_vision.pipelines import NoopPipeline
from echo_vision.runtime import run_replay

source = FileImageSource.from_path("path/to/images")
summary = run_replay(
    source,
    NoopPipeline(),
    sink=JsonlResultSink("artifacts/results.jsonl"),
)
```

正式算法只需实现：

```python
process(frame: Frame) -> VisionResult
```

不得在 `process()` 内打开相机、串口、HTTP 或录像文件。

## 3. 输入与输出

- 输入：不可变 `Frame`，包含 uint8 图像、单调时间、来源和像素格式。
- 输出：`VisionResult`，包含 sequence、mode、valid、类别、坐标系、坐标、置信度和故障。
- 文件源支持 PNG/JPEG/BMP/NPY，默认 RGB8，可配置 GRAY8。

## 4. 所有权与实时性

- CameraSource 是图像唯一生产者。
- 实时采集接入 `LatestValueSlot`，满时覆盖旧帧并计数，不阻塞相机。
- JSONL 是离线旁路，不能代替 UART 控制协议。
- no-op Pipeline 仅用于检查数据流，不代表识别算法。

## 5. 故障行为

- 输入路径不存在或没有图片：明确抛出 CameraSourceError。
- 图片无法解码：记录具体文件和错误。
- Pipeline/输出异常：ReplaySummary 增加 failure 和 failure_messages。
- 无目标：`valid=false`，不能使用合法坐标表示。

## 6. 新算法的安全接入步骤

1. 在 `algorithms` 中写纯函数，输入图像和参数，返回候选结果。
2. 在 `pipelines` 中把候选转换为 Detection/VisionResult。
3. 为固定图片增加单元测试和离线回放测试。
4. 在 `configs` 登记阈值、ROI 和模式参数，不写死到 Mission。
5. 更新能力目录、debuglog、learning 日志和性能证据。
6. 硬件部署后再把状态从 host-validated 升级，不能提前写 reusable。

## 7. 验证证据

- Python 3.12.13，NumPy 2.3.5，Pillow 12.2.0。
- 使用明确的 Python 3.12.13 路径和 `PYTHONPATH=src`，标准库单元测试 14/14 通过。
- 两张只读赛题截图完成回放：2 帧、0 failure。
- OpenCV、MaixCAM、树莓派相机、UART 和整机均未验证。

## 8. 已知限制与回退

- 当前没有真实检测 Pipeline。
- 当前实时相机适配器没有完成设备验收。
- 协议仅有 Python 参考实现，MCU golden vector 和 UART 实测待 V3。
- 出现设备问题时退回 FileImageSource，先证明算法和配置是否正常。
