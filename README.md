# JD to Offer

把目标 JD 转成结构化能力图谱、知识体系、优质资源包、主项目蓝图和面试素材；同时内置一个可运行的旗舰项目脚手架 `DriverOps Agent Lab`。

## 当前能力

- 解析 Markdown 格式 JD
- 映射到可编辑的能力 taxonomy
- 生成 5 份核心输出和 `manifest.yaml`
- 支持把 agent 联网核对后的研究结果通过 `resource_overrides` 注入生成链路
- 提供 `jd-to-offer` Codex skill 与本地可执行脚本
- 内置一个滴滴 2026 Agent/供需策略 JD 示例
- 提供 `DriverOps Agent Lab` 作为旗舰项目：planner/ReAct、grounded answer、长短期记忆、评测与训练导出

## 这个项目到底包含什么

这个仓库其实是 **两层结构**：

- `jd_offer`：把一个 JD 变成可复用的准备方案，产出知识体系、资源包、主项目蓝图和面试素材
- `driverops_agent_lab`：把蓝图里的“主项目”真正落成一个可运行、可评测、可导出训练数据的旗舰 demo

可以把它理解成：

- **上层是求职/项目规划引擎**：负责“这个 JD 需要哪些能力、该学什么、该做什么项目”
- **下层是项目样板间**：负责“如果真的做这个项目，系统怎么搭、怎么评测、怎么沉淀训练数据”

所以这个仓库既能回答“我要学什么”，也能回答“我要做成什么样”。

## 快速开始

### 1) 直接生成案例包

```bash
PYTHONPATH=src python -m jd_offer.cli generate \
  --input examples/didi_2026_agent_jd.md \
  --company didi \
  --role agent-algorithm \
  --resource-overrides examples/didi_2026_verified_resources.yaml \
  --outdir cases/didi-agent-2026
```

### 2) 先生成联网研究模板，再让 agent 回填

```bash
PYTHONPATH=src python -m jd_offer.cli scaffold-research \
  --input examples/didi_2026_agent_jd.md \
  --outpath cases/didi-agent-2026/research_template.yaml
```

这个模板的用途是：先由 agent 联网搜索最新的一手资源，把结果写成 YAML，再通过 `--resource-overrides` 覆盖静态资源表。

### 3) 使用 skill 包装脚本

```bash
python skills/jd-to-offer/scripts/run_case.py generate \
  --input examples/didi_2026_agent_jd.md \
  --company didi \
  --role agent-algorithm \
  --resource-overrides examples/didi_2026_verified_resources.yaml \
  --outdir cases/didi-agent-2026
```

### 4) 验证输出目录

```bash
python skills/jd-to-offer/scripts/validate_case.py cases/didi-agent-2026
```

## `DriverOps Agent Lab`

旗舰项目骨架位于 `src/driverops_agent_lab/`，它现在不只是一个 API demo，而是一个**可讲技能、可跑流程、可导出数据**的项目样板。

### 它主要负责什么

- 把 JD 里关于 Agent / LLM / RL 相关的关键能力，落成一个能演示的司机经营助手
- 让你在面试里不仅能讲“架构图”，还能讲 planner、memory、evaluation、training data flywheel
- 给后续 SFT / preference / reward 方向预留出数据沉淀接口

### 它体现哪些技能

- **Agent 设计**：intent router、planner → executor、grounded answer、fallback
- **工具使用**：画像、经营统计、活动查询、规则检索、策略生成
- **记忆设计**：短期 query history + 轻量长期偏好记忆
- **评测能力**：intent / tool coverage + planner-aware metrics
- **训练闭环**：trace-rich training samples + failure review taxonomy
- **工程化能力**：FastAPI、Typer CLI、pytest、可复现样例产物

### 当前模块分层

- **在线链路**：`/chat` + planner/executor agent
- **记忆层**：recent queries、preferred peak windows、preferred campaigns、recent recommended zones
- **评测层**：`eval_report.json`，覆盖 `plan_validity`、`step_execution_success_rate`、`evidence_coverage`、`fallback_rate`
- **训练层**：`training_samples.jsonl` + `failure_review.json`

### 当前已经提供

- 收入解释
- 活动推荐
- 热区建议
- 规则问答
- grounded answer
- 短期记忆 + 轻量长期记忆
- FastAPI 服务化
- planner-aware 离线评测
- trace-rich 训练样例导出
- failure review / taxonomy 导出
- 浏览器 demo 页面

### 启动服务

```bash
PYTHONPATH=src python -m driverops_agent_lab.cli serve
```

或兼容旧入口：

```bash
PYTHONPATH=src python -m driverops_agent_lab.app
```

### 打开 demo

启动后访问：`http://127.0.0.1:8001/demo`

### 调接口

```bash
curl -X POST http://127.0.0.1:8001/chat \
  -H 'Content-Type: application/json' \
  -d '{"driver_id":"driver-001","city":"beijing","query":"今天有什么活动适合我"}'
```

### 跑离线评测

```bash
PYTHONPATH=src python -m driverops_agent_lab.cli evaluate \
  --outpath examples/driverops/eval_report.json
```

### 导出训练样例

```bash
PYTHONPATH=src python -m driverops_agent_lab.cli export-training-data \
  --outpath examples/driverops/training_samples.jsonl
```

### 示例产物

- 评测结果：`examples/driverops/eval_report.json`
- 训练样例：`examples/driverops/training_samples.jsonl`
- 失败归因：`examples/driverops/failure_review.json`
- 设计说明：`docs/examples/2026-03-09-driverops-agent-lab.md`

## 目录说明

- `src/jd_offer/`：CLI、解析器、taxonomy、研究覆盖、内容生成、渲染与校验
- `src/driverops_agent_lab/`：旗舰项目骨架、评测与训练样例导出
- `configs/`：能力 taxonomy、资源注册表、项目模板
- `skills/jd-to-offer/`：Codex skill、本地脚本、参考文档
- `examples/`：输入 JD、联网研究覆盖样例、DriverOps 示例产物
- `cases/`：生成出的案例包
- `docs/examples/`：人工撰写的滴滴蓝图与 DriverOps 项目说明

## 输出约定

每个 case 目录固定包含：

- `01_jd_decomposition.md`
- `02_knowledge_system.md`
- `03_resource_pack.md`
- `04_project_blueprint.md`
- `05_interview_assets.md`
- `manifest.yaml`

## 验证命令

```bash
PYTHONPATH=src pytest -v
PYTHONPATH=src python -m jd_offer.cli generate \
  --input examples/didi_2026_agent_jd.md \
  --company didi \
  --role agent-algorithm \
  --resource-overrides examples/didi_2026_verified_resources.yaml \
  --outdir cases/didi-agent-2026
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
python /Users/liuche/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/jd-to-offer
```

## 资源策略

- 静态资源表在 `configs/resource_registry.yaml`
- 联网核对后的最新资源通过 `examples/*.yaml` 或 case 内的 research YAML 注入
- 优先官方文档、官方仓库和一手论文
- 如果用户明确要求“最新”或“当前最优”，agent 应先联网核对再回填 YAML
