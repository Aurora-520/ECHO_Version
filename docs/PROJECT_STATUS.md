# ECHO_Vision 当前状态

最后核对：2026-07-15，Asia/Shanghai

## 1. 权威位置

- 唯一正式视觉工程：`E:\ECHO_Version`
- 当前分支：`main`
- V0 基线提交：`71d827a`
- 当前阶段：V1 设备、采集、曝光、时间戳和录像，进行中
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

- MaixCAM Pro：USB NCM/RNDIS 和 SSH 只读发现完成；MaixPy 4.12.5、GC4653、板载六轴 IMU、
  存储/内存/温度和服务端口已记录；实时采集尚未执行。
- 树莓派 4B：系统版本和软件环境待确认。
- 独立相机：型号、传感器、镜头、接口和安装方式待确认。
- MSPM0G3507：正式电控主控，视觉使用独立 UART 与其通信。
- USB-TTL：型号待确认；只允许 3.3 V TTL，必须可靠共地。

当前 MaixCAM Pro 已连接。设备 Settings 应用正在使用相机/显示并初始化默认 UART 通信监听，
不能并行启动第二个相机或 UART 所有者。

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
| MaixCAM USB/SSH 发现 | 通过 | NCM/RNDIS 双网卡、SSH、系统、资源、相机配置和模型路径只读发现 |
| MaixCAM 实时相机采集 | 未执行 | 只读取配置和最近日志，尚未抓取新帧 |
| MaixCAM IMU 实时读取 | 未执行 | 官方说明、应用和校准文件存在，未调用传感器 |
| MaixCAM 部署 | 未执行 | 已连接但未上传或启动正式工程应用 |
| 树莓派相机实测 | 未执行 | 系统和相机未知 |
| UART 实测 | 未执行 | 未接线 |
| 整机联调 | 未执行 | 不属于当前 V1.0 只读发现 |

## 6. 下一步

1. 正常退出设备 Settings 应用或由 MaixVision 接管，释放相机和默认通信资源。
2. 校正设备时间来源并记录前后状态，不刷系统。
3. 基于 MaixPy 4.12.5 实现最小 CameraSource 和单帧 raw/status 抓取，不加载模型、不发送 UART。
4. 确认曝光、增益、白平衡和实际帧率 API，保存第一批固定原图。
5. 确认独立相机型号/接口和树莓派系统，再准备同场景 A/B 采集。

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
- V0 当时未连接设备，`tools/discover_devices.ps1` 未发现候选；该历史结果不代表当前状态。

## 8. V1.0 首次连接证据

- Windows 主机：NCM `10.5.66.100`、RNDIS `10.5.67.100`；设备端分别为 `.1`。
- 设备：`maixcam-0542`，镜像 `maixcam-pro-2026-01-24-maixpy-v4.12.5`。
- GC4653 配置存在，最近运行日志为 1280x720@60fps；本轮没有实时抓图。
- `/root/models/my_model` 只有 `model_282919`，旧 `model_262872`/`model_271670` 仍缺失。
- 改进后的发现脚本在实机上输出双网卡、两个 `.1` 设备地址、SSH=true、COM4 和空错误列表。
- 机器可读快照：`docs/evidence/2026-07-15_maixcam_discovery.json`。
