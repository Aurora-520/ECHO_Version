# ECHO_Vision 硬件清单与接线状态

## 1. 当前已知设备

| 设备 | 当前事实 | 未确认项 |
| --- | --- | --- |
| MaixCAM Pro | 设备在手，暂定比赛主视觉 | 系统/固件、MaixPy API、相机接口、IP、存储、温度接口 |
| Raspberry Pi 4B | 开发、采集、回放和备用平台 | 系统、位数、Python/OpenCV、存储、电源 |
| 独立相机 | 不假设为 MaixCAM 内置相机 | 型号、传感器、USB/CSI/DVP、镜头、分辨率、帧率 |
| MSPM0G3507 | 正式电控主控，独立 UART 接收视觉 | UART 实例、引脚、波特率和 MCU 解析实现 |
| USB-TTL | 用于读/模拟视觉 UART | 芯片、COM 号、电平和线序 |

MaixCAM Pro 不假设内置陀螺仪。若以后增加 MPU6050、ICM42688、BMI088 等外接 IMU，必须
记录模块、电压、总线、坐标轴、安装方向、采样率和标定，并通过独立 `ImuSource` 接入。

## 2. USB-C 调试链

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

## 3. UART 接线红线

- USB-TTL 和 MaixCAM/MSPM0 均使用 3.3 V 逻辑。
- TX 接 RX，RX 接 TX，GND 必须可靠共地。
- 禁止把 USB-TTL 5 V 接到 UART 或 3.3 V 电源轨。
- COM 号是本机运行参数，不得写死为工程事实。
- 连接 MCU 前先用 USB-TTL 做回环和协议模拟。

## 4. 烧录与部署

普通应用开发通过 SSH/SCP/SFTP 上传并运行应用、模型和配置。只有系统不兼容、文件系统损坏
或用户明确要求升级时才考虑系统镜像。系统烧录会清空数据，必须执行备份、镜像来源和哈希
核对，并由用户现场确认目标 USB 磁盘。
