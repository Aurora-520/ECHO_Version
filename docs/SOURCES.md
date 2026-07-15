# ECHO_Vision 资料来源

调查日期：2026-07-15。以下外部路径全部只读。

## 1. 正式电控工程方法参考

来源：`E:\ECHO`

- `AGENTS.md`
- `docs/PROJECT_STATUS.md`
- `docs/CURRENT_WORKFLOW.md`
- `docs/ARCHITECTURE_BOUNDARIES.md`
- `docs/ENGINEERING_RED_LINES.md`
- `docs/phases/PHASE1F_OPERABILITY_DIAGNOSTICS.md`
- `docs/worklogs/README.md`

采用的方法：权威状态、分阶段验收、架构边界、单写者、非阻塞高频路径、健康快照、Git
安全、证据分级和结构化 worklog。未复制电控源码。

## 2. 往年赛题截图

来源：`E:\电赛相关资料\赛题`

- 2025 简易自行瞄准装置：黑线循迹、靶面光斑和云台瞄准。
- 具有自动泊车功能的电动车：道路边界、车位区域和泊车状态。
- 运动目标控制与自动追踪系统：红/绿光斑、矩形轨迹、旋转靶面和双目标跟踪。
- 自动行驶小车：黑色半圆路径、端点与线路连续性。
- 三子棋游戏装置：棋盘定位、格点映射、棋子颜色/占用和变化检测。

当前目录只有 6 张截图，没有完整 PDF/Word 题目文件。

## 3. 旧 MaixCAM 代码

来源：`E:\version`，共 8 个 Python 文件：

- `pattern recognition.py`
- `SMC.py`
- `version 1.0.0.py`
- `version 3.0.0.py`
- `version 4.0.0(1).py`
- `version 4.1.0.py`
- `version 4.3.0.py`
- `version 4.4.0(1).py`

详细结论见 `docs/LEGACY_CODE_AUDIT.md`。

## 4. 开源工程

来源：`E:\电赛开源`

- `basic_framework-master`：电控分层、pub/sub、daemon 和调试方法参考。
- `diansai_yuntai_mc02-yuntai_karman`：2025 E 题云台 MCU 工程；包含视觉 UART、CRC 协议、
  离线判断、频率门槛、卡尔曼和搜索/跟踪状态，但不包含相机识别程序。
- `MSPM0G3507_Library-master`：TSL1401/GS08RA 采集、阈值标定和逐飞助手传图示例。
- `SeekFree_MSPM0G3507_Opensource_Library`：外设与上位机通信库。

这些工程只用于方法审查，不复制整份源码。

## 5. 模型和训练资料状态

旧代码引用：

```text
/root/models/my_model/model_262872.mud
/root/models/my_model/model_271670.mud
```

在 `E:\version`、`E:\电赛相关资料` 和 `E:\电赛开源` 中未找到上述模型、其他 `.mud`
权重、对应标签、训练集或训练说明。状态：缺失。设备连接后只读检查 MaixCAM 的 `/root/models`
和 `/maixapp`，未找到前不得补写类别映射。
