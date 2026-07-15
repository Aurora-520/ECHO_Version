# 性能与稳定性指标

## 每次回放/实测至少记录

- 输入数据集/录像 ID、版本、路径、SHA-256 和配置哈希。
- 平台、系统、Python/MaixPy、OpenCV、模型版本和相机配置。
- 输入帧数、处理帧数、采集 drop、Pipeline drop 和录像 drop。
- FPS、处理延迟 p50/p95/max、端到端延迟和结果年龄。
- 误检、漏检、precision、recall；没有标注时明确写“未评估”。
- CPU/NPU、内存、温度、存储余量和连续运行时长。
- UART 有效帧、CRC 错误、sequence gap、超时、重连和最大结果年龄。
- 相机断开、低置信度、坏帧、队列满、网络断开和恢复时间。

## 定义

- 采集延迟：CameraSource 得到帧时间减传感器/驱动采集时间，能力不足时标记 unknown。
- 处理延迟：VisionResult 产生时间减 Frame 采集单调时间。
- 结果年龄：MCU 使用结果时刻减 Frame 采集时间；视觉侧字段只是发送时估计。
- FPS：在明确时间窗口内的成功处理帧数，不使用瞬时单帧倒数冒充稳定 FPS。
- drop：必须区分采集、latest-frame 覆盖、Pipeline、UART 和录像 drop。

所有数字必须来自机器可读摘要、日志或健康快照。
