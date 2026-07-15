# ECHO_Vision 当前状态

最后核对：2026-07-15，Asia/Shanghai

## 1. 权威位置

- 唯一正式视觉工程：`E:\ECHO_Version`
- 当前分支：`main`
- V0 基线提交：`71d827a`
- 当前阶段：V0 工具链与可运行基线已完成纯软件验收
- 阶段标签：`vision-v0-baseline`
- 远端：`origin` -> `https://github.com/Aurora-520/ECHO_Version.git`
- 分支跟踪：`main` -> `origin/main`
- 首次 push：2026-07-15 已完成；当前同步状态以 `git status --short --branch` 为准

`E:\ECHO-Vision` 是旧笔误，不得使用。所有长期事实必须写入本仓库文档。

## 2. 已完成调查

- 已读取 `E:\ECHO` 的 AGENTS、PROJECT_STATUS、CURRENT_WORKFLOW、架构边界、工程红线、
  Phase 1F 和 worklog 规则。
- 已盘点 `E:\电赛相关资料\赛题` 的 6 张往年题目截图。
- 已检查 `E:\version` 的全部 8 个 Python 文件，并重点逐段审查
  `version 4.4.0(1).py`。
- 已审查 `E:\电赛开源` 中的通用电控框架、云台视觉接收/卡尔曼代码和逐飞相机示例。
- 未找到旧代码引用的 `model_262872.mud`、`model_271670.mud`、标签文件、训练数据或说明。

详细证据见 `docs/SOURCES.md` 和 `docs/LEGACY_CODE_AUDIT.md`。

## 3. 已知硬件

- MaixCAM Pro：设备在手；系统/固件版本、存储和接口尚未读取；不假设内置陀螺仪。
- 树莓派 4B：系统版本和软件环境待确认。
- 独立相机：型号、传感器、镜头、接口和安装方式待确认。
- MSPM0G3507：正式电控主控，视觉使用独立 UART 与其通信。
- USB-TTL：型号待确认；只允许 3.3 V TTL，必须可靠共地。

当前未连接或未自动识别任何视觉硬件。本文件不得把“设备在手”写成“硬件测试通过”。

## 4. 当前实现状态

V0 第一版工程骨架已经实现：

- 工程规则、交接、阶段、架构、硬件、协议、台架流程和风险文档。
- `Frame`、`Detection`、`Track`、`VisionResult`、`HealthSnapshot` 等结构化类型。
- JSON 配置加载、文件图像源、无硬件离线回放入口。
- MaixCAM/树莓派适配器边界和设备工具占位。
- 视觉-MCU 帧格式与 CRC 参考实现。
- 标准库单元测试和设备只读发现工具。
- 五类长期记录：状态/交接、worklog、debuglog、learning 和 capability；阶段完成与模块复用
  均有明确文档门禁。
- 已建立跨阶段鲁棒性规范，覆盖赛场光照、曝光、反光、模糊、遮挡、背景、设备差异、故障恢复、
  数据集切片和 R0-R4 验证等级。

## 5. 验证状态

| 验证层级 | 状态 | 说明 |
| --- | --- | --- |
| 资料审查 | 完成 | 本地只读来源已调查 |
| 代码实现 | 完成 | V0 结构、类型、文件源、回放、协议和工具 |
| 本机单元测试 | 通过 | Python 3.12.13，14/14 unittest 通过 |
| 本机 Pillow 文件回放 | 通过 | 两张只读赛题截图，2 帧、0 failure |
| 本机 OpenCV 回放 | 未执行 | 当前 bundled Python 无 OpenCV |
| 目标识别鲁棒性 | 未执行 | 当前没有正式矩形/圆/光斑算法和鲁棒性数据集 |
| MaixCAM 部署 | 未执行 | 未连接设备 |
| 树莓派相机实测 | 未执行 | 系统和相机未知 |
| UART 实测 | 未执行 | 未接线 |
| 整机联调 | 未执行 | 不属于 V0 |

## 6. 下一步

1. 用户连接 MaixCAM Pro 后，先只读发现系统、USB 网卡、IP、存储、相机和串口，不刷系统。
2. 更新硬件清单并确认 MaixPy/MaixCDK API，再实现 MaixCAM CameraSource。
3. 确认独立相机型号/接口和树莓派系统，再做同场景采集准备。
4. 建立第一批固定图片数据集，开始矩形、圆和中心点的纯算法实现与评测。
5. 同场景采集 nominal/boundary/adverse/negative/recovery 切片，冻结 test 集后再调参。

开始以上任何任务前，必须先按 `AGENTS.md` 和 `docs/DOCUMENTATION_SYSTEM.md` 读取状态、交接、
能力目录、相关调试日志和学习日志。

## 7. V0 本机证据

- Python：3.12.13；NumPy：2.3.5；Pillow：12.2.0。
- `python -m unittest discover -s tests -v`：14 tests，全部通过。
- JSON/schema 解析：5 个文件通过；包模块导入：26 个通过。
- CLI 回放输入：`E:\电赛相关资料\赛题` 中前两张截图。
- CLI 回放结果：2 帧、0 failure；输出为 ignored
  `artifacts/v0-smoke/results.jsonl`。
- 本次 no-op 回放只验证数据流，FPS/0 ms 延迟不代表真实算法性能。
- `tools/discover_devices.ps1` 在当前环境未发现 USB 网卡或串口候选，不代表硬件不存在。
