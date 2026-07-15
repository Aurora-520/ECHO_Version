# ECHO_Vision 硬件清单与接线状态

## 1. 当前已知设备

| 设备 | 当前事实 | 未确认项 |
| --- | --- | --- |
| MaixCAM Pro | 已通过 USB-C/SSH 只读发现，暂定比赛主视觉 | 实时采集、曝光 API、连续运行和部署 |
| Raspberry Pi 4B | 开发、采集、回放和备用平台 | 系统、位数、Python/OpenCV、存储、电源 |
| 相机 | MaixCAM 当前日志确认 GC4653 MIPI；另有独立相机信息待补 | 独立相机型号/镜头/接口 |
| MSPM0G3507 | 正式电控主控，独立 UART 接收视觉 | UART 实例、引脚、波特率和 MCU 解析实现 |
| USB-TTL | 用于读/模拟视觉 UART | 实际适配器尚未确认；COM4 不是已确认的视觉 UART |

MaixCAM Pro 官方硬件资料明确标注板载六轴 IMU，设备存在 `imu_ahrs` 应用和陀螺仪校准文件。
当前尚未执行实时读取。板载或外接 IMU 都必须记录总线、坐标轴、安装方向、采样率和标定，并
通过独立 `ImuSource` 接入。

## 2. 2026-07-15 MaixCAM Pro 实机快照

| 项目 | 实测/只读发现结果 |
| --- | --- |
| 主机名 | `maixcam-0542` |
| USB NCM | 电脑 `10.5.66.100`，设备 `10.5.66.1` |
| USB RNDIS | 电脑 `10.5.67.100`，设备 `10.5.67.1` |
| 系统镜像 | `maixcam-pro-2026-01-24-maixpy-v4.12.5` |
| 内核/系统 | Linux 5.10.4-tag，RISC-V 64，Buildroot 2023.11.2 |
| Python/MaixPy | Python 3.11.6，MaixPy 4.12.5，maixcam lib 1.24.0 |
| Linux CPU/内存 | 1 核，约 128MiB 可见内存，无 swap |
| 存储 | 根分区 57.6GB，发现时可用约 53.3GB |
| 温度 | 单次快照约 55.3°C；不是连续运行结论 |
| 相机 | GC4653，配置标识 4M/30fps，最近日志运行 1280x720@60fps |
| 服务 | SSH 22、FTP 21、MaixVision 7899 |
| 设备时间 | 比电脑明显滞后，校时前墙钟日志不可作为准确时间证据 |

当前设备 Settings 应用正在运行并初始化相机、显示和默认通信监听。进行采集部署前必须先通过
正常 UI/MaixVision 流程释放资源，禁止直接启动第二个相机或 UART 所有者。

## 3. USB-C 调试链

目标拓扑：

```text
电脑/Codex <-- USB-C 虚拟网卡 --> MaixCAM Pro
电脑/Codex <-- USB-TTL 3.3V ---> MaixCAM UART
MaixCAM Pro <-- camera interface --> 独立相机
```

首次连接只允许发现设备，不刷系统：

- 枚举 USB/RNDIS 网卡、MAC、IP 和路由。
- 枚举串口、VID/PID 和 COM 号。
- 通过 SSH 读取设备名、系统版本、uptime、存储、内存、温度和进程。
- 记录相机节点、支持格式和分辨率。

## 4. UART 接线红线

- USB-TTL 和 MaixCAM/MSPM0 均使用 3.3 V 逻辑。
- TX 接 RX，RX 接 TX，GND 必须可靠共地。
- 禁止把 USB-TTL 5 V 接到 UART 或 3.3 V 电源轨。
- COM 号是本机运行参数，不得写死为工程事实。
- 连接 MCU 前先用 USB-TTL 做回环和协议模拟。
- MaixPy 4.12.5 的顶层 `import maix` 会注册默认通信监听并打开 UART0；设备探测和纯算法测试
  不得用无必要的顶层导入占用串口。

## 5. 烧录与部署

普通应用开发通过 SSH/SCP/SFTP 上传并运行应用、模型和配置。只有系统不兼容、文件系统损坏
或用户明确要求升级时才考虑系统镜像。系统烧录会清空数据，必须执行备份、镜像来源和哈希
核对，并由用户现场确认目标 USB 磁盘。
