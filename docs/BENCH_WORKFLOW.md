# MaixCAM/树莓派台架工作流

## 1. 无硬件开发

1. 在 `datasets` 外部路径保存图片或录像，登记索引和 SHA-256。
2. 使用 `tools/replay.py` 回放固定输入并保存 JSONL 摘要。
3. 每次只修改一个主要参数，比较误检、漏检、FPS 和延迟。
4. 失败帧单独登记，不覆盖原始数据。

## 2. MaixCAM 首次连接，只读发现

用户完成 USB-C 连接后：

1. 运行 `tools/discover_devices.ps1`，记录 USB 网卡、IP 和串口候选。
2. 用户确认设备 IP 后，通过 SSH 读取 hostname、系统版本、uptime、存储、内存、温度和进程。
3. 读取相机节点、支持格式、分辨率和 MaixPy/MaixCDK 版本。
4. 只读检查 `/root/models`、`/maixapp` 和旧模型路径，不移动或删除文件。
5. 更新 `docs/HARDWARE.md` 和 `PROJECT_STATUS.md`。

不得在发现阶段刷系统或写未知 USB 磁盘。

## 3. 普通应用部署

目标闭环：

```text
discover -> deploy app/config/model -> start -> status
-> capture raw/overlay -> tune config -> replay failures -> redeploy
```

应用部署应使用独立版本目录或可回滚软链接，上传完成后再切换。正式工具需要提供 deploy、
start、stop、status、capture、logs、set-config 和 download-failures。V0 的工具仅生成操作计划，
实际 SSH/SCP 执行在设备信息确认后实现。

## 4. 调试服务契约

MaixCAM 端至少提供：

- `raw.jpg`：最近原图，原子替换。
- `overlay.jpg`：检测框、中心、ROI、FPS、延迟、模式和故障。
- `status.json`：版本、序号、结果、FPS、p50/p95、drop、内存、温度和故障。
- `config.json`：当前生效配置及版本。
- 参数更新：校验、pending、边界应用和 ACK。
- 失败帧保存和有界短时录像。

调试服务故障不得影响相机采集和 UART 结果输出。

## 5. UART 台架

1. 确认 USB-TTL 为 3.3 V，先做本地回环。
2. TX/RX 交叉并可靠共地，不连接 5 V。
3. 先由电脑模拟 MCU，测试合法帧、坏 CRC、截断、粘包、噪声、超时和重连。
4. 再连接 MSPM0G3507，保持执行器禁止，验证 SET_MODE/START/STOP/PING。
5. 最后才在 MCU 安全门通过后做动作联调。

## 6. 系统镜像烧录门禁

仅当系统不兼容、文件系统损坏或用户明确要求升级时考虑：

1. 备份 `/root`、`/maixapp` 和重要配置，并记录哈希。
2. 确认镜像名称属于 MaixCAM Pro：`maixcam-pro_os_...`。
3. 记录下载来源、版本和 SHA-256。
4. 用户现场按 USER 键上电、连接 USB 并确认目标磁盘。
5. 在用户明确批准目标磁盘后才执行写镜像。
6. 烧录后验证启动、网络、存储、相机和恢复数据。

系统烧录会清空数据，任何一步不确定都必须停止。
