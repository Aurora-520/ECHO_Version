# ECHO_Vision 架构边界

## 1. 依赖方向

```text
Mission
  -> Pipeline
    -> Algorithm / Estimation
      -> Core Types

Runtime / Services -> Ports -> Platform Adapters
```

上层可以依赖下层稳定接口，下层不得读取上层 Mission 状态。

## 2. 目录责任

| 目录 | 责任 |
| --- | --- |
| `core` | 时间、坐标、帧、检测、跟踪、结果和健康类型 |
| `ports` | CameraSource、ResultSink 等平台无关接口 |
| `adapters` | 文件、MaixCAM、树莓派、UART/HTTP/SSH 薄适配 |
| `algorithms` | 纯图像和几何算法，不接触设备 |
| `estimation` | 多帧关联、滤波和跟踪状态 |
| `pipelines` | 组合算法并产出 VisionResult |
| `missions` | 赛题模式、转换条件和 Pipeline 选择 |
| `services` | 配置、标定、模型、健康、录像、日志和调试服务 |
| `runtime` | 进程生命周期、线程/任务编排和有界数据流 |
| `protocol` | 视觉-MCU 帧格式、CRC、命令和结果编码 |

## 3. 数据所有权

- CameraSource 单写相机帧；发布后不得继续修改帧内容。
- 高频通道默认容量 1 或小容量有界队列，满时丢旧帧并递增计数。
- Pipeline 消费只读 Frame，产出不可变 VisionResult。
- UART service 是串口唯一读写者；Mission 和算法不得直接调用串口。
- HealthSnapshot 由健康服务单写，其他模块只读。
- 录像和 HTTP 获取帧副本或只读快照，不能反向控制采集循环。

## 4. 时间与坐标

- 采集、处理和结果统一使用单调时间戳；墙钟只用于文件名和人工日志。
- 时间字段名称必须带 `_ns`、`_ms` 或 `_s`。
- 坐标必须携带 CoordinateFrame，禁止仅用裸 `(x, y)`。
- `valid=false`、故障标志和坐标相互独立；合法坐标不得承担错误语义。
