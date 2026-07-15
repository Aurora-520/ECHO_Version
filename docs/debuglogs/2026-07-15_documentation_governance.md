# 2026-07-15 文档传承门禁补强

## 背景与影响

V0 已有状态、交接和 worklog，但用户要求进一步保证每个阶段的问题、解决过程、学习材料和模块
复用方法都能在重开聊天后继续使用。若只依赖 worklog，新接手者仍可能知道“改了什么”，却不
知道“为什么这样改、怎样避免复发、比赛任务如何安全接入”。

## 现象

- `AGENTS.md` 的开工顺序没有强制读取调试、学习和能力索引。
- 阶段闭环只笼统要求“必要学习文档”，没有独立 debuglog 和 capability 门禁。
- worklog 没有明确说明它不能替代问题复盘和初学者教程。
- 已调模块缺少统一的“什么条件才算可复用”判定。

## 初始假设

仅在现有 worklog 中增加更多章节可能满足记录需求。

## 调查与 A/B 证据

对比现有文档职责后发现，单个 worklog 同时承担当前状态、问题证据、教学和稳定 API 会快速
膨胀，也难以按模块检索。将内容拆成状态、worklog、debuglog、learning 和 capability 五类后，
每类能回答一个稳定问题，并由索引建立连接。

## 根因

原规则重点解决“工作有没有记录”，尚未定义“知识如何被检索、复用和验证”，因此缺少阶段
完成门禁和模块可复用门禁。

## 修复

- 新增 `DOCUMENTATION_SYSTEM.md`，定义五类文档和强制阅读顺序。
- 新增 debuglog、learning 和 capability 目录规则及索引。
- 在 `AGENTS.md`、交接和工作流中加入不可跳过的开工/收工门禁。
- 为 V0 建立实际调试复盘、基础学习材料和运行底座复用说明。

## 验证

- 检查所有新入口都能从 `AGENTS.md`、`CURRENT_HANDOFF.md` 和 README 找到。
- 检查 V0 的问题、学习结论和复用入口分别有独立文档。
- 首次直接运行 `python -m unittest` 时，PowerShell 命中的 `D:\sftoware\Python\python.exe`
  是 Python 3.6.5，无法解析项目使用的 future annotations。
- 改用 Codex bundled Python 3.12.13 后，第一次仍因 src-layout 未安装且没有 `PYTHONPATH`
  出现 `ModuleNotFoundError: echo_vision`。
- 设置 `PYTHONPATH` 为仓库 `src` 并使用 Python 3.12.13 后，14/14 单元测试通过。
- 本次只有文档变更；没有因此重新宣称 OpenCV、MaixCAM、UART 或整机通过。

### 验证环境问题的根因与预防

同一个 `python` 命令会受 PATH 顺序影响，src-layout 项目在未执行 editable install 时也不会自动
找到 `src/echo_vision`。以后运行测试前先记录 `python --version` 和 `(Get-Command python).Source`，
优先使用项目虚拟环境；未安装包时明确设置 `PYTHONPATH=src`。不能把解释器或导入路径错误误判为
业务代码回归。

## 如何避免复发

阶段验收清单固定检查五类记录；新聊天先读索引，再按当前模块读取相关条目。缺少复用门禁的
模块只能标记 `experimental`、`host-validated` 或 `deferred`。

## 对真实视觉任务的影响

比赛任务接入矩形、圆、光斑、黑线或跟踪模块时，可以从能力目录找到稳定入口、配置、故障
行为、回归测试和回退方法，不需要复制代码或新建第二个相机/UART 所有者。

## 可复用结论

工作记录、问题复盘、教学材料和 API 复用说明必须分工，但要通过统一开工顺序和阶段门禁连接。

## 仍未解决

后续每个真实算法和硬件阶段仍需产生自己的记录；V0 文档不能代替 V1/V2 的设备和数据证据。
