# V1：设备、采集、曝光、时间戳和录像

状态：进行中；V1.0 首次连接只读发现已完成，实时相机采集和部署尚未执行

## 目标

在 MaixCAM Pro 和树莓派上建立可重复、单所有者、带相机元数据的采集与调试链，能够保存原图、
短时录像、失败帧和机器可读性能摘要，并为同场景鲁棒性 A/B 测试提供输入。

## 范围

- MaixCAM/树莓派系统、相机和接口发现。
- CameraSource 的实际平台适配。
- 曝光、增益、白平衡、分辨率、帧率和单调时间戳。
- latest-frame、有界录像旁路、原图/overlay/status/config 调试输出。
- nominal/boundary/adverse/negative/recovery 采集流程。
- 相机断开、坏帧、磁盘满、网络断开和恢复测试。

## 非目标

- 不实现完整比赛 Mission。
- 不冻结 MaixCAM 与树莓派最终平台选择。
- 不刷系统镜像。
- 不连接电机、底盘或云台动作。
- 不用旧模型缺失问题阻塞传统视觉和采集底座。

## V1.0 首次连接实际结果

- Windows 11 同时识别 NCM `10.5.66.100` 和 RNDIS `10.5.67.100`，设备端均为 `.1`。
- SSH 22、FTP 21、MaixVision 7899 可见；使用官方默认 SSH 账户完成只读发现。
- 确认产品 `MaixCAM-Pro`，镜像 `maixcam-pro-2026-01-24-maixpy-v4.12.5`。
- 确认 Python 3.11.6、MaixPy 4.12.5、maixcam lib 1.24.0。
- 确认 GC4653，相机配置文件标识 4M/30fps，最近运行日志为 1280x720@60fps。
- 确认板载六轴 IMU 的官方说明、设备应用和校准文件；尚未执行实时读取。
- Linux 可见单核、约 128MiB 内存、无 swap、根分区约 58GB，温度快照约 55.3°C。
- 设备时钟明显落后于电脑，Wi-Fi 未连接；在校时前不能信任墙钟日志。
- 旧模型 `model_262872.mud`、`model_271670.mud` 在搜索路径中仍缺失。
- 发现另一个 `model_282919`，标签为 10 类动物，未证明与旧比赛任务有关。
- 发现 `import maix` 会注册默认通信监听并打开 UART0，版本发现必须改用包元数据/文件。

机器可读证据见 `docs/evidence/2026-07-15_maixcam_discovery.json`。

## V1 验收标准

- CameraSource 能稳定启动、读取、超时、停止和恢复，且同一相机只有一个所有者。
- 每帧包含单调时间、分辨率、像素格式及设备可读的曝光/增益/白平衡元数据。
- raw、overlay、status、config、失败帧和短时录像旁路不会阻塞采集。
- 固定相机配置下记录 FPS、p50/p95、drop、内存、温度和连续运行时间。
- 完成至少 nominal、dim、bright、backlight、glare、blur、negative 场景采集。
- MaixCAM 与树莓派使用同一 Frame/CameraSource 契约和同一批离线回放数据。
- 所有硬件与故障测试有日志；未执行项目明确 `deferred`。

## 下一步：V1.1 MaixCAM 最小采集

1. 先退出设备 Settings 应用或通过 MaixVision 正常接管，避免第二个相机/UART 所有者。
2. 修正设备时间来源，记录校时前后结果，不刷系统。
3. 使用 MaixPy 4.12.5 正式 API 实现最小 CameraSource 和单帧抓取。
4. 首次部署只输出 raw、相机元数据和健康状态，不加载旧模型、不发送 UART。
5. 保存一组固定场景原图并回传电脑，验证方向、镜像、曝光、清晰度和实际 FPS。
