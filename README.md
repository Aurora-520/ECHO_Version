# ECHO_Vision

全国大学生电子设计竞赛视觉方向正式工程。唯一正式位置为 `E:\ECHO_Version`。

GitHub：`https://github.com/Aurora-520/ECHO_Version`

本工程提供可替换平台、可替换赛题和可离线回放的视觉底座。MaixCAM Pro 暂定为比赛主视觉，
树莓派 4B 用于开发、采集、回放和备用；最终平台需经过同场景 A/B 测试后确定。视觉只向
MSPM0G3507 发布结构化结果，电机、底盘和云台的最终输出始终由 MCU 控制。

正式能力必须通过 `docs/ROBUSTNESS.md` 的分场景验证：不仅在正常光照下正确，还要在逆光、
阴影、反光、模糊、遮挡、背景干扰和曝光瞬态中可观测地退化；不能可靠判断时必须安全拒绝。

## 当前状态

- 当前阶段：V0 工具链与可运行基线已完成纯软件验收。
- 已完成：只读资料调查、工程规则、核心数据类型、文件源、配置、离线回放、协议参考实现、
  平台适配边界和设备工具占位。
- 未执行：MaixCAM 部署、树莓派相机测试、UART 实测和整机联调。

权威状态见 `docs/PROJECT_STATUS.md`。重开任务必须从 `AGENTS.md`、
`docs/CURRENT_HANDOFF.md` 和 `docs/DOCUMENTATION_SYSTEM.md` 开始，并读取相关调试、学习和
能力记录。

## 快速开始

项目支持 Python 3.11 及以上。宿主机最小依赖为 NumPy 和 Pillow，OpenCV 为传统视觉与
树莓派相机适配的可选依赖。

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,opencv,device]"
python -m unittest discover -s tests -v
python tools\replay.py --input <image-or-directory>
```

当前 Codex bundled Python 没有 OpenCV 和 pytest，因此本机验证会使用标准库 `unittest`
并如实记录未执行的 OpenCV 路径。

## 目录

```text
src/echo_vision/  正式 Python 包
configs/          版本化默认配置和本机配置示例
calibrations/     相机/平面/云台标定参数与哈希
protocol/         视觉-MCU 协议说明、schema 与测试向量
tools/            回放、设备发现、部署和抓取工具
tests/            单元测试与离线测试入口
docs/             状态、交接、架构、阶段、调试、学习、能力复用和 worklog
models/           模型元数据；权重默认忽略
datasets/         数据集索引；原始数据默认忽略
recordings/       录像索引；视频默认忽略
```

## 安全边界

`E:\ECHO`、`E:\电赛相关资料`、`E:\电赛开源` 和 `E:\version` 只读。系统镜像烧录与普通
应用部署严格分离，未经明确批准不得写镜像或操作未知 USB 磁盘。

已经调好的模块从 `docs/CAPABILITY_CATALOG.md` 进入；未满足接口、所有权、回归、性能和限制
门禁的模块，不得标记为比赛可直接复用。
