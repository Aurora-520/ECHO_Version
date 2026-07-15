# 2026-07-15 鲁棒性门禁与 GitHub 首次上传

## 目标与范围

把赛场光照等环境变化提升为全工程硬门禁，建立可执行的扰动、数据、指标、降级和验证规则，
并把正式仓库上传到用户提供的 GitHub 仓库。

## 开始状态

- 工作区干净，HEAD 为 `8fa298a`，没有远端。
- V0 数据流和文档门禁已完成；没有正式检测算法和鲁棒性数据集。
- MaixCAM、树莓派相机、UART 和整机仍未测试。

## 调查与修改

- 新增 `docs/ROBUSTNESS.md` 和 R0-R4 验证等级。
- 把鲁棒性接入 AGENTS、架构、红线、阶段流程、能力、指标、风险和数据集索引。
- 新增鲁棒性 debuglog 和面向初学者的 learning 文档。
- GitHub 目标为 `https://github.com/Aurora-520/ECHO_Version.git`。

## 硬件状态

本次不连接、不部署、不刷写硬件。所有 R2-R4 实机/整车鲁棒性验证均为 `deferred`。

## 验证

- `git diff --check` 在暂存前通过。
- Python 3.12.13 且 `PYTHONPATH=src`：14/14 单元测试通过。
- 扩展后的数据集 CSV 索引：16 列、1 行，标准库解析通过。
- `git diff --cached --check` 通过，第一笔鲁棒性提交为 `bf88704`。
- 已配置 `origin`，`git push -u origin main --follow-tags` 成功。
- GitHub 已创建 `main` 分支和 `vision-v0-baseline` annotated tag，本地 `main` 跟踪
  `origin/main`。
- 目标识别鲁棒性没有数据，明确为未执行。

## 问题与判断

鲁棒性不能只靠自适应阈值。工程需要同时保存相机元数据、分场景数据、质量门禁、失败样本、
安全拒绝和恢复证据。

## 风险与下一步

- 真实照明范围、相机参数 API 和数值验收阈值仍需 V1/V2 数据决定。
- 首批矩形/圆数据必须同时采集正常、恶劣、负样本和恢复场景。

## 结束状态

鲁棒性门禁、学习材料和数据集元数据已完成本机验证并上传 GitHub。没有执行 MaixCAM、树莓派
相机、UART、目标识别鲁棒性或整车测试。
