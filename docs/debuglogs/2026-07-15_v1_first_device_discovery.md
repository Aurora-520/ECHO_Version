# 2026-07-15 V1 MaixCAM 首次设备发现

## 背景与影响

V1 第一次连接必须先证明电脑识别了正确设备、系统和接口，再写适配器或部署程序。若直接根据
旧代码猜 MaixPy API，可能抢占相机/UART、误判模型状态或把系统问题当算法问题。

## 现象

- 初次运行 `tools/discover_devices.ps1` 被 Windows ExecutionPolicy 拒绝。
- 沙箱内直接调用 `Get-NetAdapter`、CIM 和 PnP 查询返回“拒绝访问”。
- Windows 同时出现 NCM 和 RNDIS 两张 USB 网卡，不清楚是否是两个设备。
- SSH 无密钥登录被拒绝，尚未确认默认账户。
- 两条远端查询因 PowerShell/远端 shell 的引号冲突在本机提前解析。
- 设备墙钟比电脑滞后近一个月。
- 顶层 `import maix` 在版本探测时自动打开 UART0。
- 旧应用启动日志报告模型缺失。

## 初始假设

- 发现脚本返回空列表可能表示设备没有被 Windows 识别。
- 两张 USB 网卡可能来自不同设备或驱动冲突。
- 直接导入 `maix` 读取 `__version__` 应当是无副作用操作。

## 调查与 A/B 证据

- 使用提升权限且仅绕过脚本策略后，脚本立即读到 NCM/RNDIS 和 COM4，证明原空结果是权限问题。
- `ipconfig`、路由、ARP 和设备 DHCP 配置共同证明：主机 `.100`、设备 `.1`，两条 MAC 相邻，
  NCM/RNDIS 是同一台 MaixCAM 的双网卡。
- 两条设备 IP 的 TCP 22 均开放，SSH banner 为 OpenSSH 9.6。
- 官方 MaixPy 快速入门确认默认 SSH 账户 `root/root`，单次使用后只读登录成功。
- `/boot/ver`、dist-info、`version.py` 分别确认镜像与 MaixPy 4.12.5，避免继续导入包探测。
- `/maixapp/tmp/last_run.log` 确认 GC4653 1280x720@60fps，并记录
  `model_262872.mud not exists` 的真实堆栈。

## 根因

- Windows 网络/CIM 枚举需要当前环境没有默认授予的权限，ExecutionPolicy 又禁止直接执行 ps1。
- Windows 11 按官方设计同时支持 NCM 和 RNDIS，并非重复设备。
- `maix/__init__.py` 会执行 `add_default_comm_listener()`，因此导入包本身具有 UART 副作用。
- 设备 Wi-Fi 没有连接，时间同步守护进程无法获得网络，墙钟未更新。
- 旧应用在模块顶层同时初始化相机、UART 和两个模型，任一模型缺失都会直接退出。

## 修复

- 改进发现脚本：权限错误显式进入 `DiscoveryErrors`，推导 `.1` 设备地址，并支持 `-ProbeSsh`。
- 版本探测固定读取 `/boot/ver`、Python dist-info 或 `maix/version.py`。
- 把相机/UART 单所有者和 `import maix` 副作用写入硬件、阶段、风险和交接文档。
- 保存脱敏机器可读快照，不记录 Wi-Fi 密码或正式凭据。
- 旧模型保持 missing，不用无关 `model_282919` 替换。

## 验证

- NCM `10.5.66.100 -> 10.5.66.1`，RNDIS `10.5.67.100 -> 10.5.67.1`。
- SSH 22、FTP 21、MaixVision 7899 可见；只读 SSH 查询成功。
- 实机镜像、Python/MaixPy、相机、存储、内存、温度、服务、模型和 IMU 证据已记录。
- 改进脚本的实机运行返回双网卡、SSH=true、COM4、`DiscoveryErrors=[]`。
- 同一脚本在受限环境返回明确权限错误，验证失败路径不会伪装成“未发现设备”。
- 宿主机 Python 3.12 回归测试 14/14 通过，evidence JSON 解析通过。
- 没有写设备文件、改时间、改密码、停止进程、实时抓图或发送 UART。

## 如何避免复发

- 空发现结果必须同时检查 `DiscoveryErrors`，不能直接下结论“没有硬件”。
- 首次连接先对照官方 DHCP 规则，Windows 11 双网卡选择一条主链路即可。
- 设备元数据探测不导入会启动硬件监听的顶层包。
- SSH/远端命令使用脚本化转义或固定小命令，避免三层 shell 引号混杂。
- 设备日志同时保存单调时间和校准后的墙钟，校时前不进入正式数据集。

## 对真实视觉任务的影响

如果算法进程和探测脚本都自动打开 UART0，可能产生多个写入者；如果 Settings/MaixVision 仍占用
相机又启动采集程序，会破坏唯一相机所有者。V1.1 部署前必须先正常释放现有应用资源。

## 可复用结论

首次设备发现应分为 Windows 枚举、IP/端口、SSH 系统快照、相机/模型/服务证据四层，每层都只
读并保留错误分类。

## 仍未解决

- 设备时间尚未修正。
- 实时相机、曝光/增益、IMU、UART 和连续运行尚未测试。
- 默认 SSH 凭据尚未替换为正式密钥/密码管理。
- COM4 尚未确认是哪个物理设备，不能作为视觉 UART 使用。
