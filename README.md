# JD to Offer

把目标 JD 转成结构化能力图谱、知识体系、优质资源包、主项目蓝图和面试素材。

## 当前能力

- 解析 Markdown 格式 JD
- 映射到可编辑的能力 taxonomy
- 生成 5 份核心输出和 `manifest.yaml`
- 提供 `jd-to-offer` Codex skill 与两个可执行脚本
- 内置一个滴滴 2026 Agent/供需策略 JD 示例

## 快速开始

```bash
PYTHONPATH=src python -m jd_offer.cli generate \
  --input examples/didi_2026_agent_jd.md \
  --company didi \
  --role agent-algorithm \
  --outdir cases/didi-agent-2026
```

或直接运行 skill 包装脚本：

```bash
python skills/jd-to-offer/scripts/run_case.py generate \
  --input examples/didi_2026_agent_jd.md \
  --company didi \
  --role agent-algorithm \
  --outdir cases/didi-agent-2026
```

验证输出目录：

```bash
python skills/jd-to-offer/scripts/validate_case.py cases/didi-agent-2026
```

## 目录说明

- `src/jd_offer/`：CLI、解析器、taxonomy、内容生成、渲染与校验
- `configs/`：能力 taxonomy、资源注册表、项目模板
- `skills/jd-to-offer/`：Codex skill、本地脚本、参考文档
- `examples/`：输入 JD 样例
- `cases/`：生成出的案例包
- `docs/examples/`：人工撰写的滴滴蓝图示例

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
  --outdir cases/didi-agent-2026
python skills/jd-to-offer/scripts/validate_case.py cases/didi-agent-2026
python /Users/liuche/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/jd-to-offer
```

## 资源策略

- 资源包优先使用官方文档、官方仓库和一手论文
- 如果用户明确要求“最新”或“当前最优”，agent 应联网刷新资源，再覆盖生成结果
- 当前仓库的 `configs/resource_registry.yaml` 提供的是可复用种子资源表
