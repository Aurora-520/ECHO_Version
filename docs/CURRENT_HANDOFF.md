# ECHO_Vision 当前交接

更新时间：2026-07-15，Asia/Shanghai

## 新任务先做什么

1. 确认当前目录为 `E:\ECHO_Version`，不要使用 `E:\ECHO-Vision`。
2. 读取 `AGENTS.md` 和 `docs/PROJECT_STATUS.md`。
3. 读取本文件和 `docs/DOCUMENTATION_SYSTEM.md`。
4. 读取 `docs/ROBUSTNESS.md`。
5. 读取 `docs/CURRENT_WORKFLOW.md` 和当前阶段文档 `docs/phases/V1_ACQUISITION.md`。
6. 读取 `docs/CAPABILITY_CATALOG.md`、`docs/debuglogs/README.md` 和
   `docs/learning/README.md`，再读取本任务相关条目。
7. 执行：

```powershell
git status --short --branch
git diff
git diff --cached
```

8. 保留用户已有修改，不自动暂存、提交或 push；用户明确要求上传时仍需先检查暂存清单和远端。

## 当前断点

- 只读资料调查和架构判断已经完成，不需要从头重做。
- V0 第一版工程骨架和纯软件验收已经完成；V1.0 MaixCAM 首次连接只读发现已完成。
- Git 分支为 `main`，V0 基线使用标签 `vision-v0-baseline`；`origin` 为
  `https://github.com/Aurora-520/ECHO_Version.git`，首次 push 已完成。
- 本机 Codex Python 为 3.12.13，已有 NumPy/Pillow，没有 OpenCV、pytest、PyYAML 或 pyserial。
- 标准库 `unittest` 为 14/14 通过；Pillow 文件回放 2 帧、0 failure。
- MaixCAM USB/SSH 发现已通过；实时相机、IMU、部署、树莓派、UART 和整机路径尚未执行。
- 已建立 worklog、debuglog、learning 和 capability 分工；新任务必须按上述顺序读取索引和
  相关记录。
- 已建立 `docs/ROBUSTNESS.md`；任何检测能力必须覆盖分场景切片和最差切片，超出能力范围时
  安全拒绝，不能持续输出猜测坐标。

## 已冻结决定

- 唯一正式视觉目录是 `E:\ECHO_Version`。
- MaixCAM Pro 暂定主平台，树莓派 4B 为开发/采集/备用，A/B 测试前不最终冻结。
- MaixCAM Pro 官方资料和实机文件确认板载六轴 IMU；实时读取尚未验证，必须通过 `ImuSource`。
- 视觉不控制执行器；MSPM0G3507 是电机、底盘和云台的唯一最终输出者。
- 传统视觉与几何标定优先，跟踪其次，神经网络第三。
- 鲁棒性是正式能力硬门禁；R1 离线结果不能替代 R2 实机台架或 R4 整车赛场演练。
- 模型 `model_262872.mud`、`model_271670.mud` 及标签/训练数据当前缺失。

## 当前禁止事项

- 不修改 `E:\ECHO`、`E:\电赛相关资料`、`E:\电赛开源` 或 `E:\version`。
- 不连接运动输出，不刷 MaixCAM 系统，不操作未知 USB 磁盘。
- 不宣称 MaixCAM、UART 或整机测试通过。

## 下一步：V1.1 最小相机采集

1. 设备当前在 Settings 应用；先由用户正常退出到启动器，或使用 MaixVision 正常 Connect 接管。
2. 不再用 `import maix` 做版本探测；它会自动打开 UART0。
3. 记录并修正设备时间来源，避免错误墙钟污染数据集和日志。
4. 按 MaixPy 4.12.5 API 实现最小 MaixCAM CameraSource，首次部署不加载模型、不发送 UART。
5. 抓取 raw、相机配置和 health 快照，核对 GC4653 图像方向、曝光、清晰度和实际 FPS。
6. 第一批采集覆盖 nominal、dim、bright、backlight、glare、blur 和 negative。

设备事实见 `docs/evidence/2026-07-15_maixcam_discovery.json`。本轮没有写设备文件、改系统时间、
改 SSH 密码、停止进程或刷系统。
