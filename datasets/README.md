# Datasets

原始图片、标注和视频默认保存在 Git 外。本目录只提交索引示例和说明。每个数据集应记录来源、
采集设备、相机参数、场景、照明、标注格式、拆分、许可证、文件数、总大小和清单 SHA-256。

失败帧进入数据集前保留原始文件，不覆盖、不二次压缩冒充原图。

正式能力的数据集必须按 `docs/ROBUSTNESS.md` 标记 nominal、boundary、adverse、negative 和
recovery 场景，并分离 train/dev/test/field。至少记录相机/镜头 ID、分辨率、帧率、曝光、增益、
白平衡、光照/阴影/反光/模糊/遮挡标签。没有可靠测量时写 `unknown`，不得编造 lux 或色温。
