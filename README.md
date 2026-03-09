# JD to Offer

把目标 JD 转成结构化能力图谱、知识体系、优质资源包、主项目蓝图和面试素材；同时内置一个可运行的旗舰项目脚手架 `DriverOps Agent Lab`。

## 当前能力

- 解析 Markdown 格式 JD
- 映射到可编辑的能力 taxonomy
- 生成 5 份核心输出和 `manifest.yaml`
- 支持把 agent 联网核对后的研究结果通过 `resource_overrides` 注入生成链路
- 提供 `jd-to-offer` Codex skill 与本地可执行脚本
- 内置一个滴滴 2026 Agent/供需策略 JD 示例
- 提供 `DriverOps Agent Lab` 的可运行 FastAPI 项目骨架

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

旗舰项目骨架位于 `src/driverops_agent_lab/`，当前已经提供：

- 收入解释
- 活动推荐
- 热区建议
- 规则问答
- 短期记忆
- FastAPI 服务化

运行方式：

```bash
PYTHONPATH=src python -m driverops_agent_lab.app
```

然后调用：

```bash
curl -X POST http://127.0.0.1:8001/chat \
  -H 'Content-Type: application/json' \
  -d '{"driver_id":"driver-001","city":"beijing","query":"今天有什么活动适合我"}'
```

详细说明见 `docs/examples/2026-03-09-driverops-agent-lab.md`。

## 目录说明

- `src/jd_offer/`：CLI、解析器、taxonomy、研究覆盖、内容生成、渲染与校验
- `src/driverops_agent_lab/`：旗舰项目骨架
- `configs/`：能力 taxonomy、资源注册表、项目模板
- `skills/jd-to-offer/`：Codex skill、本地脚本、参考文档
- `examples/`：输入 JD 与联网研究覆盖样例
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
python skills/jd-to-offer/scripts/validate_case.py cases/didi-agent-2026
python /Users/liuche/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/jd-to-offer
```

## 资源策略

- 静态资源表在 `configs/resource_registry.yaml`
- 联网核对后的最新资源通过 `examples/*.yaml` 或 case 内的 research YAML 注入
- 优先官方文档、官方仓库和一手论文
- 如果用户明确要求“最新”或“当前最优”，agent 应先联网核对再回填 YAML
