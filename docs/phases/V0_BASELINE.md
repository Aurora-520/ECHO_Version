# V0：工具链与可运行基线

状态：纯软件验收通过；OpenCV 和硬件相关门禁不属于 V0，保持未执行

## 目标

在没有相机和模型的情况下，建立可安装、可测试、可回放、可交接的正式工程底座。

## 范围

- 工程规则、状态、交接、架构、协议、硬件和 worklog。
- 核心结构化类型和平台端口。
- JSON 配置加载、文件图像源和无操作 Pipeline。
- 离线回放 JSONL 输出和性能摘要。
- CRC 协议参考实现与单元测试。
- MaixCAM/树莓派适配边界、设备发现和部署工具占位。

## 非目标

- 不实现具体赛题 Mission。
- 不训练或伪造模型。
- 不连接 MaixCAM、树莓派相机、UART 或整车。
- 不刷系统镜像。
- 不宣称 OpenCV、设备或整机通过。

## 验收标准

- Python 3.11+ 包可导入。
- 标准库单元测试通过。
- Pillow 文件图像源可以读取临时图片并完成回放。
- 输出结果包含结构化 valid、坐标系、时间、sequence、置信度和故障字段。
- 协议坏 CRC 能被拒绝，合法帧可往返编码。
- `PROJECT_STATUS.md` 和 `CURRENT_HANDOFF.md` 与真实状态一致。
- 大型模型、数据集和录像默认被 Git 忽略。

## 进入 V1 的门槛

- V0 验收全部通过并保存证据。
- 用户连接 MaixCAM Pro 或提供明确的系统/接口信息。
- 确认相机型号、接口和基础供电。
- 只读设备发现流程得到系统、网络、存储和相机节点信息。

## 2026-07-15 实际结果

- 建立正式 Git 仓库、AGENTS、权威状态、当前交接、阶段和 worklog 机制。
- 实现 Frame、Detection、Track、VisionResult、HealthSnapshot 和显式坐标/故障枚举。
- 实现 JSON 配置、Pillow/NumPy 文件源、容量一 latest-value 槽、no-op Pipeline 和 JSONL 回放。
- 实现协议 v1 帧、CRC-16/CCITT-FALSE、增量流重同步和 RESULT payload。
- 建立 MaixCAM deferred 适配边界、树莓派 OpenCV 延迟导入适配器和设备工具占位。
- Python 3.12.13 下标准库单元测试 14/14 通过。
- 5 个 JSON/schema 通过解析，26 个包模块通过导入。
- 两张往年赛题截图完成 CLI 回放：2 帧、0 failure。
- 当前环境没有 OpenCV/pytest/pyserial；MaixCAM、树莓派相机、UART 和整机均未测试。

V0 的 no-op Pipeline 不做目标检测，输出 `valid=false` 是设计行为，不是算法能力证明。
