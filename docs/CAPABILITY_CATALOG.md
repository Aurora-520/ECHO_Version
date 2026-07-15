# 可复用能力目录

本目录是正式比赛任务选择已有能力的入口。Mission 不应复制模块内部实现，而应通过稳定接口、
配置和 Pipeline 组合复用。状态含义：

- `reusable`：固定数据、鲁棒性切片和适用平台实测通过，可按文档直接复用。
- `host-validated`：电脑纯软件验证通过，硬件仍需验收。
- `experimental`：接口或算法仍可能变化。
- `deferred`：只有边界或占位，不能使用。

## 当前能力

| 能力 | 稳定入口 | 状态 | 说明 |
| --- | --- | --- | --- |
| 核心结构化类型 | `echo_vision.core` | host-validated | Frame/Detection/Track/Result/Health |
| JSON 配置加载 | `echo_vision.config.load_config` | host-validated | 支持默认配置和本机覆盖 |
| 文件图像源 | `FileImageSource` | host-validated | Pillow/NumPy，支持循环和单调 frame_id |
| JSONL 结果输出 | `JsonlResultSink` | host-validated | 离线证据，不用于控制协议 |
| latest-frame 槽 | `LatestValueSlot` | host-validated | 容量 1，记录覆盖和 high-water |
| no-op Pipeline | `NoopPipeline` | host-validated | 仅验证数据流，始终 valid=false |
| 协议帧/CRC/流解析 | `echo_vision.protocol` | host-validated | UART 尚未实测 |
| 树莓派 OpenCV 相机 | `OpenCvCameraSource` | experimental | 当前主机无 OpenCV，未接相机 |
| MaixCAM 相机 | `MaixCamCameraSource` | deferred | 等待真实固件/API 发现 |
| 圆/矩形/光斑/黑线算法 | 待建立 | deferred | V2 逐模块实现和评测 |

详细快速复用说明见 `docs/capabilities/V0_RUNTIME_FOUNDATION.md`。任何状态升级必须同步修改本表、
对应能力文档、测试证据和当前 Phase。

每项能力还必须记录 `docs/ROBUSTNESS.md` 定义的 R0-R4 等级。当前 V0 运行底座不做检测，
鲁棒性等级为 R1（仅数据流和故障报告的宿主机验证），不能外推为目标识别鲁棒性。

## 比赛任务接入原则

1. 从本表选择状态和平台满足要求的能力。
2. 读取能力文档中的输入、输出、配置、故障和性能边界。
3. 在新 Mission 中组合接口，不复制源码或创建第二个设备所有者。
4. 使用比赛数据回放现有回归测试，确认没有退化。
5. 新参数进入集中配置，不能在 Mission 内写魔法数字。
6. 新场景需要修改模块内部时，先补测试和 debuglog，再升级能力版本。
7. 检查比赛环境是否落在能力文档声明的光照、尺度、运动和遮挡范围内；超出范围使用安全回退。
