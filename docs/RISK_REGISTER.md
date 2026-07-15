# ECHO_Vision 风险清单

| 风险 | 影响 | 当前控制措施 | 状态 |
| --- | --- | --- | --- |
| 正式路径混淆 | 写入错误工程 | AGENTS 明确只允许 `E:\ECHO_Version` | controlled |
| 旧模型和标签缺失 | AI 结果无法复现 | 记录缺失，设备连接后只读查找 | open |
| 相机型号/接口未知 | 适配器 API 无法冻结 | V0 只定义端口，V1 实机发现后实现 | open |
| MaixCAM 固件未知 | 猜错 MaixPy API | 禁止在读取版本前宣称设备实现可用 | open |
| 树莓派系统未知 | 环境和性能不可预测 | V1 记录镜像、内核、Python/OpenCV | open |
| UART 协议未实测 | 坏帧或失联导致错误控制 | CRC、序号、valid、age 和 MCU 安全策略 | open |
| 文本日志混入控制 | 延迟和解析歧义 | 控制协议二进制，日志独立通道 | controlled |
| 网络/录像阻塞采集 | FPS/时延退化 | 有界旁路、latest-frame、drop 计数 | design |
| 相机曝光与光照变化 | 阈值、颜色和中心估计失效 | 鲁棒性切片、相机元数据、质量门禁、失败帧和安全拒绝 | open |
| 只看总体平均指标 | 特定逆光/遮挡场景完全失效却被掩盖 | 强制分切片报告和最差切片门禁 | design |
| 自动曝光/白平衡瞬态 | 短时坐标跳变或连续误检 | 记录参数、收敛时间、原子配置和恢复测试 | open |
| 现场同时修改多类参数 | 无法定位问题且无法回退 | 版本化 profile、单变量 A/B、配置哈希 | controlled |
| USB-TTL 电平错误 | 损坏设备 | 强制 3.3 V TTL、共地、禁止 5 V | gate |
| 系统镜像写错磁盘 | 数据永久丢失 | 用户现场确认目标盘，未经批准不烧录 | gate |
| 视觉越权控制执行器 | 失控或碰撞 | MCU 唯一执行器写入者 | controlled |
| 新聊天丢失上下文 | 重复或越权操作 | PROJECT_STATUS + CURRENT_HANDOFF + worklog | controlled |
