# Tools

- `replay.py`：文件图像源离线回放。
- `discover_devices.ps1`：Windows 只读枚举 USB 网卡、IP 和串口。
- `device_cli.py`：V0 设备操作计划生成器，不执行 SSH/SCP 或重启。

V1 确认 MaixCAM 系统和接口后，再实现带明确 `--execute` 门禁的部署、启动、停止、抓图、日志、
参数和失败样本工具。系统镜像烧录不进入普通设备 CLI。
