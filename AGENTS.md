# ECHO_Vision 工程协作规则

本文件是 `E:\ECHO_Version` 中所有后续工作的常驻入口。用户当前任务中的最新明确指令优先；
发生冲突时必须先说明，不得静默扩大路径、Git 或硬件操作权限。

## 1. 唯一正式工程与只读来源

- 唯一正式视觉工程：`E:\ECHO_Version`
- 文档中出现的 `E:\ECHO-Vision` 一律视为旧笔误，不得创建或使用该目录。
- 正式电控工程：`E:\ECHO`，只读参考，禁止修改。
- 往年赛题与硬件资料：`E:\电赛相关资料`，只读参考。
- 开源工程：`E:\电赛开源`，只读参考。
- 旧 MaixCAM 代码：`E:\version`，只读参考。

不得向以上只读来源写入、移动、清理、格式化或生成缓存。视觉工程必须独立存在，Python、
OpenCV、模型、数据集和录像不得放入 `E:\ECHO`。

## 2. 新任务与重开聊天的读取顺序

任何修改前依次执行：

1. 读取本文件。
2. 读取 `docs/PROJECT_STATUS.md`。
3. 读取 `docs/CURRENT_HANDOFF.md`。
4. 读取 `docs/DOCUMENTATION_SYSTEM.md`。
5. 读取 `docs/ROBUSTNESS.md`。
6. 读取 `docs/CURRENT_WORKFLOW.md` 和当前 `docs/phases` 文档。
7. 读取 `docs/CAPABILITY_CATALOG.md` 和本任务要使用模块的能力文档。
8. 读取 `docs/debuglogs/README.md` 和当前阶段/模块相关的最近调试日志。
9. 读取 `docs/learning/README.md` 和本任务相关的学习日志。
10. 执行 `git status --short --branch`、`git diff`、`git diff --cached`。
11. 只读取本次任务直接相关的架构、协议、硬件、源码和最近 worklog。

`PROJECT_STATUS.md` 是当前事实的权威摘要；`CURRENT_HANDOFF.md` 是最近工作断点；worklog 记录
一次工作；debuglog 记录问题的证据链；learning 面向初学者解释原理；capability 文档说明模块如何
安全复用。不得依赖聊天记忆替代这些文件。

## 3. 架构边界与所有权

依赖方向固定为：

```text
Mission -> Pipeline -> Algorithm / Estimation -> Core Types
                    -> Service Ports -> Platform Adapters
```

- Mission 只编排赛题状态，不打开相机、不读写 UART、不控制执行器。
- Pipeline 组合算法和状态估计，不拥有硬件。
- Algorithm 只接收图像、参数和必要状态，返回结构化结果。
- CameraSource 是相机的唯一所有者；同一物理相机不得被多个任务打开。
- ResultSink/UART service 是视觉 UART 的唯一所有者。
- MCU 是电机、底盘和云台输出的唯一最终写入者。视觉只发布结果和健康状态。
- 日志、HTTP、录像和 UI 只能订阅有界快照，不得阻塞高频采集与推理。
- 高频路径使用单调时间戳、有界队列、latest-frame 策略、超时和明确 drop 计数。

详细规则见 `docs/ARCHITECTURE_BOUNDARIES.md` 和 `docs/ENGINEERING_RED_LINES.md`。

## 4. 鲁棒性与赛场环境

- 鲁棒性是所有正式视觉能力的硬门禁，不得只在单一光照、单一距离和干净背景下调通后宣称可用。
- 每个算法必须定义正常工作范围、退化范围和拒绝工作范围；超出能力时输出 `valid=false`、低置信度
  或明确故障，不得为了“持续有坐标”而输出猜测值。
- 固定数据集必须覆盖正常、边界、恶劣、负样本和故障恢复场景，至少考虑亮度、色温、阴影、
  逆光、反光、频闪、曝光瞬态、运动模糊、失焦、尺度、旋转、透视、遮挡、背景干扰和相机差异。
- 验收必须分别报告各场景切片和最差切片，不得只用总体平均值掩盖某类赛场条件下的失效。
- 相机曝光、增益、白平衡、分辨率和帧率必须版本化并写入帧/数据集元数据；无测量工具时不得
  凭空填写照度、色温或物理量。
- 参数可以通过版本化配置切换，但禁止比赛现场无记录地同时修改曝光、ROI、阈值和控制参数。
- 模块未完成 `docs/ROBUSTNESS.md` 对应层级的验证时，不得标记为 `reusable` 或比赛就绪。

## 5. 硬件与烧录安全

- 当前设备包括 MaixCAM Pro、树莓派 4B、独立相机和 MSPM0G3507 主控。
- MaixCAM Pro 不假设存在内置陀螺仪；外接 IMU 只能通过可选适配器接入。
- USB-TTL 必须为 3.3 V TTL 并可靠共地，禁止向 UART 接入 5 V。
- 普通视觉开发只部署应用、模型和配置，不等于授权刷系统镜像。
- 未经用户明确批准，不得刷系统、全盘写镜像、全片擦除或修改启动/配置分区。
- 刷 MaixCAM Pro 系统前必须备份 `/root`、`/maixapp` 和重要配置，核对
  `maixcam-pro_os` 镜像来源与 SHA-256，并由用户现场确认目标 USB 磁盘。
- 按 USER 键上电、切换启动模式、重新接线和确认目标磁盘由用户现场完成。
- 涉及电机、云台或整车动作时，必须由 MCU 保持唯一输出控制，并取得用户现场许可。

## 6. Git 安全

- 不自动 push，不自动创建远端。
- 禁止 `git add .`、`git add -A` 和 `git commit -am`。
- 只显式暂存本任务文件，并检查 `git diff --cached --name-only`。
- 提交前执行 `git diff --cached --check`。
- 禁止自动删除 stash、备份、分支、标签、worktree、数据集或录像。
- 禁止 `git reset --hard`、`git checkout -- <file>` 等破坏用户改动的操作。
- 阶段 commit 和 annotated tag 只能在该阶段全部门禁通过后创建。
- 大型数据集、视频、模型权重和原始日志默认不进入 Git；只提交索引、版本和哈希。

## 7. 验证层级

报告必须明确区分：

```text
资料审查完成
-> 代码实现完成
-> 静态检查/单元测试通过
-> 本机离线回放通过
-> MaixCAM 部署通过
-> UART 实测通过
-> 整机联调通过
```

不得用低层级结果替代高层级结果。FPS、p50/p95 延迟、丢帧、误检、漏检、结果年龄、
CPU、内存、温度和通信错误必须来自保存的日志或快照；没有证据时写“未执行”或 `deferred`。

## 8. 文档与交接

- 工程文档、阶段报告、worklog 和用户沟通默认使用中文。
- 代码标识符、协议字段、命令、路径和工具原始输出保留英文。
- 有实质修改的会话结束时必须：
  1. 更新 `docs/PROJECT_STATUS.md`。
  2. 更新 `docs/CURRENT_HANDOFF.md`，确保下一次工作可直接继续。
  3. 在 `docs/worklogs` 新建结构化摘要。
  4. 有调试、失败或重要风险时更新 `docs/debuglogs`；每个阶段结束前必须有阶段调试总结。
  5. 把新增原理和排障方法写入 `docs/learning`，使用没有视觉基础的队员能理解的语言。
  6. 已调模块必须更新 `docs/CAPABILITY_CATALOG.md` 和对应 `docs/capabilities` 复用说明。
  7. 必要时更新当前 Phase、架构、协议或硬件文档。
- 阶段缺少状态、交接、worklog、debuglog、学习材料、能力说明或真实验证证据时，不得标记完成，
  不得创建阶段 tag。
- 模块缺少稳定接口、所有权、配置、故障行为、示例、回归测试、性能证据、限制和版本/哈希时，
  不得标记为 `reusable` 或“比赛可直接使用”。
- 旧 worklog 不随新状态重写；发现错误时追加带日期的勘误。

完整规则见 `docs/DOCUMENTATION_SYSTEM.md`。

## 9. 当前阶段原则

当前目标是 V0“稳定调试基线”，不是一次实现全部赛题。传统视觉和几何标定优先，跟踪
其次，神经网络模型第三。不得为看起来完整而提前堆入未验证的具体 Mission。
