# 视觉-MCU 协议草案 v1

状态：V0 草案和 Python 参考实现已定义；UART、电控端解析和故障策略尚未实测，不得视为冻结。

## 1. 原则

- 控制协议使用二进制帧，文本日志不承担控制功能。
- 帧包含版本、类型、长度、序号、单调时间戳、模式、状态标志和 CRC。
- `valid`、类别、坐标、坐标系、置信度、结果年龄和故障相互独立。
- 合法坐标值不得表示无目标、待机或故障。
- MCU 按 sequence、CRC、模式、置信度、结果年龄和通信超时决定是否接受结果。
- MCU 是执行器唯一写入者，视觉协议只发布观测和状态。

## 2. 帧格式

全部小端，最大 payload 初始为 512 字节。

| 字段 | 大小 | 说明 |
| --- | ---: | --- |
| SOF | 2 | 固定 `0xA5 0x5A` |
| version | 1 | 协议版本，v1 为 1 |
| message_type | 1 | 命令或响应类型 |
| payload_len | 2 | payload 字节数 |
| sequence | 4 | 发送方递增序号，允许 uint32 回绕 |
| timestamp_ms | 4 | 发送方启动后的单调毫秒，允许回绕 |
| mode | 1 | VisionMode |
| header_flags | 2 | ACK/错误/能力等帧级标志 |
| payload | N | 消息数据 |
| crc16 | 2 | CRC-16/CCITT-FALSE，覆盖 version 到 payload |

Python 参考实现：`src/echo_vision/protocol/framing.py`。MCU 实现必须用相同 golden vector 验证。

## 3. 消息类型

### MCU -> Vision

| 类型 | ID | 说明 |
| --- | ---: | --- |
| SET_MODE | `0x01` | 请求模式切换，必须 ACK |
| START | `0x02` | 启动当前模式，必须 ACK |
| STOP | `0x03` | 停止并发布 invalid 结果，必须 ACK |
| SET_PARAM | `0x04` | 设置已登记参数，必须校验并 ACK |
| PING | `0x05` | 链路和时延探测 |

### Vision -> MCU

| 类型 | ID | 说明 |
| --- | ---: | --- |
| RESULT_SNAPSHOT | `0x81` | 最新视觉结果 |
| HEALTH | `0x82` | 低频健康快照 |
| ACK | `0x83` | 命令结果和错误码 |
| PONG | `0x84` | 回显 PING nonce 和视觉时间 |

## 4. RESULT_SNAPSHOT payload

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| valid | u8 | 0/1；无目标或不可用时为 0 |
| target_class | u8 | 稳定 TargetClass ID |
| coordinate_frame | u8 | IMAGE_PX/IMAGE_NORM/ERROR_PX/CAMERA_RAY/PLANE_MM |
| reserved | u8 | 必须为 0 |
| x | f32 | 坐标 1；valid=false 时忽略 |
| y | f32 | 坐标 2；valid=false 时忽略 |
| confidence | f32 | 0..1 |
| result_age_ms | u16 | 发送时相对采集帧的年龄，饱和到 65535 |
| fault_flags | u32 | 相机、过期、低置信度、Pipeline 等状态 |

类别和坐标枚举以 `core/types.py` 为当前草案来源。正式冻结后 MCU 与视觉各保存独立常量表，
不能依赖 Python 枚举的自动顺序。

## 5. HEALTH 最低语义

健康消息至少包含 schema、overall state、uptime、camera state、Pipeline state、FPS、p50/p95、
采集/处理/录像 drop、最近结果年龄、内存、温度、活动故障、sticky 首故障和配置/模型哈希。
V0 尚未冻结二进制 health payload，V1 先依据设备能力确定字段和更新频率。

## 6. MCU 接收安全策略

默认建议：

- CRC 错误、未知版本/类型、sequence 异常：丢弃并计数，不更新控制观测。
- `valid=false`：当前 Mission 进入零输出或停止策略。
- 置信度低于模式阈值：视为无效，不使用坐标。
- `result_age_ms` 或 MCU 本地计算年龄超限：视为过期。
- 视觉链路超时、相机故障或模式不匹配：零输出/禁能并记录 sticky 故障。
- “保持最后结果”只能由 MCU 在明确 Mission 中限时启用，默认关闭，且必须有最大保持时间。
- 恢复通信后先完成 PING/模式确认和新鲜 valid 结果，再允许重新进入运行状态。

具体时限必须通过 V3 台架测试确定，当前不得凭空填写。

## 7. 参数和模式切换

SET_PARAM 使用已登记的 `param_id/type/length/value`，视觉先校验为 pending，在帧边界原子应用，
ACK 返回 transaction/sequence 和结果。模式切换建议：

```text
RUN_OLD -> STOP_REQUESTED -> INVALID_PUBLISHED
-> RESET_PIPELINE_STATE -> SET_MODE_ACK -> START_NEW
```

禁止在运行中的半帧或半份配置上直接切换算法。
