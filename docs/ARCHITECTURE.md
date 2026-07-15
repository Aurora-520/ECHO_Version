# ECHO_Vision 架构与数据流

## 1. 运行数据流

```text
CameraSource (single owner)
  -> Frame + monotonic timestamp + camera/scene metadata
  -> bounded latest-frame channel
  -> Mission-selected Pipeline
  -> image-quality gate + pure algorithms / estimation
  -> VisionResult immutable snapshot
  -> ResultSink / UART service (single owner)
  -> MSPM0G3507 perception receiver
```

旁路服务订阅快照：

```text
Frame/Result -> recorder / debug HTTP / overlay / failure capture / metrics / logs
```

旁路满载时优先 drop 并计数，不允许拖慢主路径。

## 2. 核心接口

- `CameraSource.start/read/stop/health`：文件、MaixCAM 和树莓派统一入口。
- `Pipeline.process(frame) -> VisionResult`：硬件无关处理入口。
- `ResultSink.send_result/send_health`：UART、JSONL 或调试后端统一出口。
- `Frame`：图像、帧序号、采集单调时间、来源和不可变元数据。
- `VisionResult`：模式、valid、类别、坐标系、坐标、置信度、故障和时效。
- `HealthSnapshot`：FPS、延迟、drop、资源、温度、状态和首要故障。

相机参数、画面亮度/饱和/清晰度等质量信息属于可观测元数据，不由算法直接回写相机。质量门禁
不通过时 Pipeline 发布无效或降级结果，由 MCU 执行安全策略。详细要求见 `docs/ROBUSTNESS.md`。

## 3. 平台适配

- File：无硬件开发、回归和故障样本复现。
- MaixCAM：使用设备确认后的 MaixPy/MaixCDK API；不得在未读取版本时猜 API。
- Raspberry Pi：优先 OpenCV/V4L2 相机后端；系统和相机确定后冻结配置。
- IMU：MaixCAM Pro 已确认板载六轴 IMU，但必须通过独立 `ImuSource` 接入；图像算法不得直接
  打开或校准 IMU。外接 IMU 仍使用相同端口，不把平台细节泄漏到 Pipeline。

## 4. 能力沉淀顺序

1. 光斑、黑线/路径、矩形、圆和轮廓中心。
2. 亚像素/几何精修、相机内参和畸变。
3. 平面单应性和像素到场地坐标。
4. 棋盘占用、泊车区域和运动目标。
5. 多帧跟踪与状态估计。
6. 数据足够后再训练、转换和评估神经网络。
