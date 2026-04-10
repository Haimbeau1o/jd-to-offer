# JD to Offer

把一份目标 JD 变成可执行的求职准备方案，并在需要时落到一个可运行的旗舰项目样板上。

这个仓库不是单纯的“JD 解析器”，也不是单纯的“Agent demo”。它把两件事连起来了：

1. 上层 `jd_offer`：把 JD 转成结构化能力图谱、知识体系、资源包、项目蓝图和面试素材。
2. 下层 `driverops_agent_lab`：把蓝图里的旗舰项目落成一个可运行、可评测、可导出训练数据的演示系统。

如果你只想回答“这个岗位到底要我补什么、做什么项目”，用上层就够。
如果你还想回答“这个项目我真的能跑起来、能讲评测闭环吗”，再继续用下层。

## Related Resume Source

- 简历 LaTeX 源码不在本仓库内，在 `/Volumes/passport/简历/latex-resume`
- 供 Codex / agent 使用的对接说明见 `docs/resume_latex_reference.md`

## 你能用它做什么

- 输入一份 JD Markdown，生成一套固定结构的 case bundle
- 把静态资源表和联网核对后的最新资源合并进输出
- 自动给出一个更像“主项目”而不是“零散 demo”的项目蓝图
- 产出可直接用于简历和面试准备的素材
- 在需要时启动 `DriverOps Agent Lab`，演示 Agent、memory、evaluation、training data flywheel

## 仓库到底怎么理解

### 第一层：`jd_offer`

这是一个本地 Python CLI，用来把目标 JD 变成准备方案。

输入：

- 一份 JD Markdown
- 一套能力 taxonomy
- 一份资源注册表
- 可选的联网研究覆盖 YAML

输出：

- `01_jd_decomposition.md`
- `02_knowledge_system.md`
- `03_resource_pack.md`
- `04_project_blueprint.md`
- `05_interview_assets.md`
- `manifest.yaml`

### 第二层：`driverops_agent_lab`

这是仓库内置的旗舰项目样板，面向“司机经营助手”场景，主要用来承接 Agent / LLM / 评测 / 训练闭环这条线。

它当前覆盖：

- 意图识别
- planner / executor 风格的多步执行
- grounded answer
- 短期记忆与轻量长期记忆
- FastAPI 服务与浏览器 demo
- 离线评测导出
- 训练样本导出
- failure review 导出

## 快速开始

### 环境要求

- Python `>=3.11`

下面的示例默认用 `PYTHONPATH=src` 直接运行，不要求先安装包。
如果你习惯 editable install，也可以先执行 `python -m pip install -e .`，之后直接使用 `jd-offer` 和 `driverops-agent-lab` 两个命令。

### 1. 生成一个完整案例包

```bash
PYTHONPATH=src python -m jd_offer.cli generate \
  --input examples/didi_2026_agent_jd.md \
  --company didi \
  --role agent-algorithm \
  --resource-overrides examples/didi_2026_verified_resources.yaml \
  --outdir cases/didi-agent-2026
```

生成后你会在 `cases/didi-agent-2026/` 看到完整 case bundle 和 `manifest.yaml`。

### 2. 先生成研究模板，再由 agent / 人工回填最新资源

```bash
PYTHONPATH=src python -m jd_offer.cli scaffold-research \
  --input examples/didi_2026_agent_jd.md \
  --outpath cases/didi-agent-2026/research_template.yaml
```

这个 YAML 模板用于保存联网核对后的最新一手资源。仓库默认的设计是：

- `configs/resource_registry.yaml` 提供静态基线资源
- `examples/*.yaml` 或 case 内的 research YAML 提供最新覆盖项
- `generate --resource-overrides ...` 把两者合并，保证结果既可复现，也能吸收最新资料

### 3. 验证输出目录是否完整

```bash
python skills/jd-to-offer/scripts/validate_case.py cases/didi-agent-2026
```

### 4. 用 skill 封装脚本运行同一条链路

```bash
python skills/jd-to-offer/scripts/run_case.py generate \
  --input examples/didi_2026_agent_jd.md \
  --company didi \
  --role agent-algorithm \
  --resource-overrides examples/didi_2026_verified_resources.yaml \
  --outdir cases/didi-agent-2026
```

## 推荐工作流

### 场景 A：你只想把 JD 理清楚

按下面顺序就够：

1. `scaffold-research` 生成研究模板
2. 回填最新资源
3. `generate` 生成 case bundle
4. `validate_case.py` 验证输出

### 场景 B：你还想把“旗舰项目”一起讲清楚

除了上面的步骤，再刷新 `DriverOps Agent Lab` 的可复用产物：

```bash
PYTHONPATH=src python -m driverops_agent_lab.cli evaluate \
  --outpath examples/driverops/eval_report.json

PYTHONPATH=src python -m driverops_agent_lab.cli export-training-data \
  --outpath examples/driverops/training_samples.jsonl

PYTHONPATH=src python -m driverops_agent_lab.cli export-failure-review \
  --outpath examples/driverops/failure_review.json
```

这三个文件分别对应：

- 评测快照：`examples/driverops/eval_report.json`
- 训练样本：`examples/driverops/training_samples.jsonl`
- 失败归因：`examples/driverops/failure_review.json`

## DriverOps Agent Lab

### 它适合在 README 里怎么理解

把它看成“项目样板间”最准确。

`jd_offer` 负责回答：

- 这个 JD 重视哪些能力？
- 我应该学什么？
- 我该做一个什么项目来证明匹配度？

`driverops_agent_lab` 负责回答：

- 这个项目如果真的做出来，系统长什么样？
- 工具调用、memory、evaluation、training data 怎么串起来？
- 面试里我能展示哪些可运行证据？

### 新增中的 `commentops_agent_lab`

面向评论审核与内容治理场景的新框架骨架已经开始补进仓库，目标是承接类似抖音 / TikTok CQC、Trust & Safety、内容审核 Agent 方向的 JD。

当前阶段已经具备：

- 评论审核 policy schema、风险信号与历史 case
- `pass / reject / escalate` 三态审核 workflow
- reviewer queue routing 与 guarded auto-pass
- 相似 case 检索、运营建议与业务影响摘要
- 离线评测、SFT / preference / failure review 数据导出
- FastAPI + CLI + review workbench demo

快速试跑：

```bash
PYTHONPATH=src python -m commentops_agent_lab.cli evaluate \
  --outpath examples/commentops/eval/baseline_eval_report.json

PYTHONPATH=src python -m commentops_agent_lab.cli export-sft \
  --outpath examples/commentops/eval/sft_samples.jsonl

PYTHONPATH=src python -m commentops_agent_lab.cli export-preferences \
  --outpath examples/commentops/eval/preference_pairs.jsonl

PYTHONPATH=src python -m commentops_agent_lab.cli export-failure-review \
  --outpath examples/commentops/eval/failure_review.json
```

### 启动服务

```bash
PYTHONPATH=src python -m driverops_agent_lab.cli serve
```

兼容旧入口：

```bash
PYTHONPATH=src python -m driverops_agent_lab.app
```

启动后访问：

- Demo 页面：`http://127.0.0.1:8001/demo`
- Chat API：`http://127.0.0.1:8001/chat`

### 调用示例

```bash
curl -X POST http://127.0.0.1:8001/chat \
  -H 'Content-Type: application/json' \
  -d '{"driver_id":"driver-001","city":"beijing","query":"今天有什么活动适合我"}'
```

### 当前能展示的能力

- 收入解释
- 活动推荐
- 热区建议
- 规则问答
- grounded answer 与 evidence items
- planner step trace 与 observations
- 短期记忆与轻量长期记忆
- fallback 与 failure review

## 目录结构

```text
src/jd_offer/                 JD -> case bundle 的本地生成链路
src/driverops_agent_lab/      旗舰项目样板、服务、评测、训练数据导出
configs/                      taxonomy、资源注册表、项目模板
examples/                     JD 输入、资源覆盖样例、DriverOps 产物
cases/                        生成出来的案例包
skills/jd-to-offer/           Codex skill、包装脚本、参考文档
docs/examples/                人工整理的项目蓝图、项目说明和面试素材
docs/plans/                   设计与实现计划
tests/                        CLI、生成链路、DriverOps 能力测试
```

## 关键入口

### `jd_offer`

- `src/jd_offer/cli.py`：CLI 入口
- `src/jd_offer/parser.py`：JD Markdown 解析
- `src/jd_offer/taxonomy.py`：能力映射
- `src/jd_offer/research.py`：研究模板与资源覆盖合并
- `src/jd_offer/renderer.py`：渲染 case bundle

### `driverops_agent_lab`

- `src/driverops_agent_lab/agent.py`：核心 Agent 流程
- `src/driverops_agent_lab/tools.py`：工具层
- `src/driverops_agent_lab/memory.py`：记忆层
- `src/driverops_agent_lab/app.py`：FastAPI 服务和 demo
- `src/driverops_agent_lab/eval.py`：离线评测
- `src/driverops_agent_lab/training_data.py`：训练样本与 failure review 导出

## 已有样例

- JD 输入：`examples/didi_2026_agent_jd.md`
- 联网资源覆盖：`examples/didi_2026_verified_resources.yaml`
- 生成后的案例包：`cases/didi-agent-2026/`
- 项目说明：`docs/examples/2026-03-09-driverops-agent-lab.md`
- JD 蓝图说明：`docs/examples/2026-03-09-didi-agent-jd-blueprint.md`

## 验证命令

```bash
PYTHONPATH=src pytest -v

PYTHONPATH=src python -m jd_offer.cli generate \
  --input examples/didi_2026_agent_jd.md \
  --company didi \
  --role agent-algorithm \
  --resource-overrides examples/didi_2026_verified_resources.yaml \
  --outdir /tmp/didi-agent-2026

PYTHONPATH=src python -m jd_offer.cli scaffold-research \
  --input examples/didi_2026_agent_jd.md \
  --outpath /tmp/didi_research_template.yaml

PYTHONPATH=src python -m driverops_agent_lab.cli evaluate \
  --outpath /tmp/driverops_eval_report.json

PYTHONPATH=src python -m driverops_agent_lab.cli export-training-data \
  --outpath /tmp/driverops_training_samples.jsonl

PYTHONPATH=src python -m driverops_agent_lab.cli export-failure-review \
  --outpath /tmp/driverops_failure_review.json

python skills/jd-to-offer/scripts/validate_case.py cases/didi-agent-2026
```

## 一句话总结

如果你把这个仓库当成“从 JD 出发，反推学习路径、项目设计、面试表达，并在必要时给出可运行项目证据”的工具链，它的结构就会很清楚：

- `jd_offer` 负责规划和产出
- `driverops_agent_lab` 负责把规划落成可演示项目
