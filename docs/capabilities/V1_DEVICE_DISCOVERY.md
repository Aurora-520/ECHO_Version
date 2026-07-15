# V1 Windows MaixCAM 设备发现

状态：experimental

鲁棒性等级：R1；在一台 Windows 11 电脑和一台 MaixCAM Pro 上实测，尚未覆盖其他驱动/电脑。

## 用途

只读枚举 Windows USB NCM/RNDIS 网卡、推导 MaixCAM 设备 IP、可选探测 SSH 22，并列出串口
VID/PID。用于第一次连接和赛场换电脑后的快速定位，不执行 SSH 登录、部署或串口写入。

## 稳定入口

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\discover_devices.ps1 -ProbeSsh
```

输出为 JSON，包含主机时间、管理员状态、USB 网卡、主机/设备 IP、SSH 状态、串口和错误。

## 所有权与安全

- 只读取 Windows 网络和 CIM 状态，不打开相机或串口。
- `-ProbeSsh` 只做 TCP 22 连接测试，不认证、不执行远端命令。
- 串口候选不能仅凭 COM 号认定，必须核对适配器、电平和接线。
- 脚本不处理系统烧录或 USB 磁盘。

## 故障行为

- 缺少管理员/CIM 权限时输出 `DiscoveryErrors`，不能把空列表解释为“没有设备”。
- 非 `/24` 地址不自动推导 `.1`，`ExpectedDeviceIPv4` 为 null。
- SSH 未开或超时时输出 false，不自动尝试密码。

## 验证证据

- 2026-07-15 实机识别 NCM `10.5.66.100 -> 10.5.66.1`。
- 同时识别 RNDIS `10.5.67.100 -> 10.5.67.1`。
- 两条设备 IP 的 SSH 22 均开放。
- 识别 COM4 `VID_0D28&PID_0204`，但未错误标记为视觉 UART。
- 在受限环境下再次运行时返回两条 `DiscoveryErrors`，而不是静默输出空设备列表。

## 限制与回退

- 当前依赖 Windows `Get-NetAdapter`、`Get-NetIPAddress` 和 CIM，通常需要提升权限。
- 其他子网、旧 Windows 或手工静态 IP 尚未测试。
- 脚本失败时回退到 `ipconfig /all`、`route print -4`、`arp -a` 和设备管理器人工核对。
