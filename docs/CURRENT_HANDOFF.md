# ECHO_Vision 当前交接

更新时间：2026-07-15，Asia/Shanghai

## 新任务先做什么

1. 确认当前目录为 `E:\ECHO_Version`，不要使用 `E:\ECHO-Vision`。
2. 读取 `AGENTS.md` 和 `docs/PROJECT_STATUS.md`。
3. 读取本文件和 `docs/DOCUMENTATION_SYSTEM.md`。
4. 读取 `docs/ROBUSTNESS.md`。
5. 读取 `docs/CURRENT_WORKFLOW.md` 和当前阶段文档 `docs/phases/V0_BASELINE.md`。
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
- V0 第一版工程骨架和纯软件验收已经完成。
- Git 分支为 `main`，V0 基线使用标签 `vision-v0-baseline`；`origin` 为
  `https://github.com/Aurora-520/ECHO_Version.git`，首次 push 已完成。
- 本机 Codex Python 为 3.12.13，已有 NumPy/Pillow，没有 OpenCV、pytest、PyYAML 或 pyserial。
- 标准库 `unittest` 为 14/14 通过；Pillow 文件回放 2 帧、0 failure。
- OpenCV、MaixCAM、树莓派相机、UART 和整机路径均未执行。
- 已建立 worklog、debuglog、learning 和 capability 分工；新任务必须按上述顺序读取索引和
  相关记录。
- 已建立 `docs/ROBUSTNESS.md`；任何检测能力必须覆盖分场景切片和最差切片，超出能力范围时
  安全拒绝，不能持续输出猜测坐标。

## 已冻结决定

- 唯一正式视觉目录是 `E:\ECHO_Version`。
- MaixCAM Pro 暂定主平台，树莓派 4B 为开发/采集/备用，A/B 测试前不最终冻结。
- MaixCAM Pro 不假设内置陀螺仪；外接 IMU 是后续可选适配器。
- 视觉不控制执行器；MSPM0G3507 是电机、底盘和云台的唯一最终输出者。
- 传统视觉与几何标定优先，跟踪其次，神经网络第三。
- 鲁棒性是正式能力硬门禁；R1 离线结果不能替代 R2 实机台架或 R4 整车赛场演练。
- 模型 `model_262872.mud`、`model_271670.mud` 及标签/训练数据当前缺失。

## 当前禁止事项

- 不修改 `E:\ECHO`、`E:\电赛相关资料`、`E:\电赛开源` 或 `E:\version`。
- 不连接运动输出，不刷 MaixCAM 系统，不操作未知 USB 磁盘。
- 不宣称 MaixCAM、UART 或整机测试通过。

## 下一步：V1 首次设备发现

1. 用户现场将 MaixCAM Pro 通过 USB-C 连接电脑。
2. 运行 `tools/discover_devices.ps1`，由用户确认 USB 网卡/IP 和串口候选。
3. 只读 SSH 查询 hostname、系统/固件、Maix runtime、存储、内存、温度、进程和相机节点。
4. 只读检查 `/root/models/my_model`、`/root/models` 和 `/maixapp`，记录旧模型是否存在。
5. 更新 `docs/HARDWARE.md`、`PROJECT_STATUS.md` 和新的 V1 worklog。
6. 确认实际 API 后才实现 MaixCAM 适配器，禁止根据旧代码猜版本。
7. 建立曝光/增益/白平衡和 nominal/adverse 场景的同步采集流程，为鲁棒性数据集做准备。

在用户尚未连接设备时，可以并行建立第一批离线图片数据集和矩形/圆纯算法，但不得宣称
MaixCAM 已部署。
