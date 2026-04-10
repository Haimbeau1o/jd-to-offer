from __future__ import annotations


def project_overview_payload() -> dict:
    return {
        "title": "项目全景",
        "summary": "这一页把项目讲法固定成统一主线：先说明评论治理业务要解决什么，再说明为什么它应该被建模成 bounded moderation agent，最后再落到指标体系、评测闭环、文档与产出物。",
        "hero_chips": [
            "Business-first framing",
            "Bounded single-agent DAG",
            "LangGraph-ready state model",
            "Eval and optimization loop",
            "Docs and artifacts",
        ],
        "storyline": [
            {
                "status": "业务理解",
                "title": "先定义业务目标，不先谈模型",
                "body": "评论审核的核心不是给一条文本打标签，而是在安全、误杀、人工效率、一致性、申诉友好度之间找到稳定边界。",
                "items": [
                    "审核对象是 case，不是单句文本。",
                    "系统目标既包括风险控制，也包括 reviewer 提效和策略一致性。",
                    "真正的难点来自上下文、规则、人工协同和策略变更。",
                ],
            },
            {
                "status": "问题抽象",
                "title": "把问题抽象成 stateful workflow",
                "body": "如果抽象成 classifier，会丢掉 supporting evidence、queue routing、appeal replay 和 reviewer handoff 这些高价值环节，所以更合理的是带状态的 case workflow。",
                "items": [
                    "case intake 先统一输入契约。",
                    "证据获取和决策要明确分层。",
                    "高风险 / 不确定样本要有人工兜底分支。",
                ],
            },
            {
                "status": "架构选择",
                "title": "推荐 bounded single-agent DAG",
                "body": "第一版最合适的不是 one-shot classifier，也不是 supervisor multi-agent，而是可控、可追溯、可评测的 single-agent DAG。",
                "items": [
                    "每个节点对应一个真实业务责任点。",
                    "便于插入 human review 和 checkpoint。",
                    "后续仍可按职责把局部节点扩成独立 agent。",
                ],
            },
            {
                "status": "闭环优化",
                "title": "先评测系统，再优化模型",
                "body": "更符合 JD 的做法是先建立 evidence、decision、routing、reward design 四层优化框架，再让失败样本持续回灌。",
                "items": [
                    "离线回放、shadow audit、人工回灌三层评测。",
                    "failure taxonomy 连接系统表现与训练数据。",
                    "SFT / preference / reward 只处理已经被识别出的高价值失败样本。",
                ],
            },
        ],
        "architecture_options": [
            {
                "name": "One-shot classifier",
                "fit": "最低",
                "why": "适合做最小基线，但不适合作为这个 JD 的主项目叙事。",
                "tradeoffs": [
                    "优点是实现简单、延迟低。",
                    "缺点是缺少 supporting evidence、queue routing、appeal replay 和 reviewer handoff。",
                ],
            },
            {
                "name": "Sequential workflow",
                "fit": "中等",
                "why": "比 classifier 更接近审核链路，但对 state、interrupt、checkpoint 表达还不够充分。",
                "tradeoffs": [
                    "适合做最小原型。",
                    "不足以完整表达全生命周期管理和人审打断。",
                ],
            },
            {
                "name": "Bounded single-agent DAG",
                "fit": "最高",
                "why": "最适合高约束、高审计需求的审核场景，也最符合当前项目的业务表达。",
                "tradeoffs": [
                    "优点是可控、可审计、可替换、可评测。",
                    "需要克制 node 粒度，避免把技术实现过度图化。",
                ],
            },
            {
                "name": "Supervisor multi-agent",
                "fit": "二阶段考虑",
                "why": "只有当 policy、appeal、reviewer-assist 真正成为独立稳定子域后才值得引入。",
                "tradeoffs": [
                    "优点是扩展性强。",
                    "缺点是复杂度、调度成本和一致性治理成本都更高。",
                ],
            },
        ],
        "langgraph_mapping": {
            "why_graph_api": [
                "审核 case 天然需要 state：policy version、risk signals、tool trace、reviewer outcome 都要挂在一个对象上。",
                "审核系统需要 human-in-the-loop：reviewer override、appeal replay、high-risk case 都不能让模型自由到底。",
                "审核系统需要 checkpoint 和可回放，以支持错判复盘和 policy version regression。",
            ],
            "state_fields": [
                "review_case",
                "policy_hits",
                "similar_cases",
                "risk_signals",
                "decision",
                "queue_routing",
                "reviewer_outcome",
                "appeal_outcome",
                "tool_trace",
            ],
            "nodes": [
                "case_intake -> 统一输入契约",
                "context_loader -> 获取上下文证据",
                "policy_retrieval -> 绑定 policy grounding",
                "similar_case_retrieval -> 补一致性参照",
                "risk_synthesis -> 合成多源弱信号",
                "decision_policy -> 定义自动化边界",
                "queue_routing -> 映射 reviewer queue / SLA",
                "reviewer_handoff -> 给人审交付证据和建议",
            ],
            "interrupts": [
                "低置信度但高风险样本强制升级人工",
                "appeal-sensitive 用户命中时强制保留 trace",
                "policy version 变更后对关键类别走 shadow audit",
            ],
        },
        "metric_groups": [
            {
                "title": "在线质量指标",
                "items": [
                    "action_accuracy：最终动作是否与 gold / reviewer outcome 一致",
                    "high_risk_escalation_recall：高风险样本是否被稳定升级人工",
                    "over_enforcement_proxy：正常讨论被误杀的代理指标",
                    "under_enforcement_proxy：高风险内容被漏放的代理指标",
                    "policy_grounding_rate：决策是否能明确回溯到 policy evidence",
                ],
            },
            {
                "title": "运营效率指标",
                "items": [
                    "queue_routing_accuracy：是否进入正确队列和优先级",
                    "human_review_rate：多少样本需要人工介入",
                    "reviewer_throughput：证据准备是否减少 reviewer 整理成本",
                    "priority_queue_sla：高风险样本是否按时进入处理",
                ],
            },
            {
                "title": "治理稳定性指标",
                "items": [
                    "consistency_on_similar_cases：历史相似样本是否前后一致",
                    "appeal_sensitive_error_rate：申诉敏感样本是否更容易误判",
                    "policy_version_regression_rate：规则版本更新后是否出现回归",
                    "reviewer_override_rate：系统决策被人工推翻的比例",
                ],
            },
        ],
        "deliverables": [
            {
                "kind": "核心研究文档",
                "title": "CommentOps Agent 架构与评测框架重构",
                "path": "docs/examples/2026-04-01-commentops-agent-architecture-and-eval-framework.md",
                "purpose": "系统回答为什么选这种 Agent 范式、如何做 LangGraph 映射、如何设计评测闭环。",
            },
            {
                "kind": "研究原始文档",
                "title": "CQC 评论审核 Agent 研究与框架映射",
                "path": "docs/examples/2026-03-31-cqc-comment-agent-research.md",
                "purpose": "保留初轮从 JD、TikTok/Meta/OpenAI 等资料反推框架的调研过程。",
            },
            {
                "kind": "实现计划",
                "title": "Architecture and evals reframe plan",
                "path": "docs/plans/2026-04-01-commentops-architecture-evals-reframe.md",
                "purpose": "记录本轮把研究页重构成业务 -> 架构 -> 指标 -> 闭环结构的实施步骤。",
            },
            {
                "kind": "实现计划",
                "title": "Project overview presentation plan",
                "path": "docs/plans/2026-04-01-commentops-project-overview-presentation.md",
                "purpose": "记录本轮如何把项目整体呈现做得更清晰。",
            },
            {
                "kind": "评测产物",
                "title": "Baseline eval report",
                "path": "examples/commentops/eval/baseline_eval_report.json",
                "purpose": "展示 action、queue、human review 等基础指标的结构化产出。",
            },
            {
                "kind": "训练数据产物",
                "title": "SFT / preference / failure review artifacts",
                "path": "examples/commentops/eval/sft_samples.jsonl | preference_pairs.jsonl | failure_review.json",
                "purpose": "证明这不是只停留在 demo 的项目，而是往训练和优化闭环继续延伸。",
            },
        ],
        "presentation_flow": [
            "先讲业务目标：安全、误杀、效率、一致性、申诉友好度。",
            "再讲问题抽象：为什么是 case workflow，而不是单轮分类。",
            "然后讲架构取舍：为什么 first version 选 bounded single-agent DAG。",
            "接着讲评测框架：在线质量、运营效率、治理稳定性三层指标。",
            "最后讲闭环与产出：failure taxonomy、SFT、preference、reward design 怎么接起来。",
        ],
    }


def agent_evolution_payload() -> dict:
    return {
        "title": "工程进化",
        "summary": "这一页不再回答“项目是什么”，而是回答“这个审核 Agent 如何从原型持续进化成更像工程系统的产品”。重点是成熟度、评测指标、优化抓手、Agent 演化路线和 ROI 排序，而不是堆更多花哨架构。",
        "hero_chips": [
            "Current maturity snapshot",
            "Evidence to ROI",
            "Metric-first iteration",
            "Big-tech-informed roadmap",
            "Avoid complexity theatre",
        ],
        "maturity_snapshot": {
            "stage": "V2.5 / bounded workflow prototype",
            "headline": "当前成熟度：已经超出纯 demo，但还没有走到生产化审核平台",
            "already_built": [
                "有 case schema，不是裸文本分类。",
                "有 policy hit、risk signal、queue routing 和 reviewer notes。",
                "有基础 eval、failure review、SFT / preference 产物。",
                "有 project overview、workflow、research log 三类讲解页。",
            ],
            "known_gaps": [
                "还没有显式 retrieval decision policy。",
                "还没有 tool failure harness 和 safe degrade。",
                "还缺 reviewer override / appeal outcome 的一等数据结构。",
                "还缺 slice eval、baseline 对照和 policy version regression。",
            ],
            "next_priorities": [
                "先补 retrieval sufficiency 与 escalation boundary。",
                "先补 high-risk recall、appeal-sensitive slice、ROI instrumentation。",
                "先补 harness，再考虑更复杂 agentic patterns。",
            ],
        },
        "engineering_layers": [
            {
                "name": "Evidence Layer",
                "problem": "先收集足够证据，再决定是否自动化，而不是看一句评论就拍板。",
                "current": "已有 comment_text、thread_context、policy hit、similar case 和 risk signals 雏形。",
                "next": "增加 retrieval decision policy、evidence sufficiency 判断、appeal / adjudication memory。",
                "metric": "policy_grounding_rate / evidence_sufficiency_rate / unnecessary_retrieval_rate",
            },
            {
                "name": "Decision Boundary Layer",
                "problem": "定义 safe pass、hard reject、human review 三态边界，避免一味全自动。",
                "current": "已有 pass / reject / escalate 三态和置信度逻辑。",
                "next": "增加 high-risk recall、low-confidence no-auto-action、appeal-sensitive guardrail。",
                "metric": "high_risk_recall / over_enforcement_proxy / under_enforcement_proxy",
            },
            {
                "name": "Ops Routing Layer",
                "problem": "审核结果必须进入真实运营流程，而不是停在标签层。",
                "current": "已有 queue routing、priority、SLA 和 shadow audit 雏形。",
                "next": "增加 exposure-aware prioritization、reviewer throughput 观测、evidence-ready handoff。",
                "metric": "queue_routing_accuracy / human_review_rate / evidence_ready_rate / priority_queue_sla",
            },
            {
                "name": "Harness / Safety Layer",
                "problem": "工具失败、证据缺失、规则冲突时要能保守降级，而不是继续假装成功。",
                "current": "已有 tool_trace，但没有完整 recovery harness。",
                "next": "增加 retry / fallback / safe degrade / policy gate / high-risk approval hooks。",
                "metric": "tool_failure_recovery_rate / unsafe_auto_action_rate / guarded_fallback_rate",
            },
            {
                "name": "Learning Flywheel Layer",
                "problem": "把 reviewer、appeal 和错判样本沉淀成下一轮优化燃料。",
                "current": "已有 failure review、SFT、preference 导出骨架。",
                "next": "把 reviewer override、appeal overturn、policy regression 和 slice eval 统一进闭环。",
                "metric": "reviewer_override_rate / appeal_overturn_rate / policy_version_regression_rate / trainable_case_yield",
            },
        ],
        "metric_groups": [
            {
                "title": "在线质量指标",
                "status": "已实现一部分",
                "items": [
                    "action_accuracy：当前已有，衡量最终动作正确率。",
                    "policy_grounding_rate：当前已有，衡量决策是否能回溯到 policy。",
                    "high_risk_recall：下一步重点补齐，比整体 accuracy 更能代表治理价值。",
                    "over_enforcement_proxy / under_enforcement_proxy：下一步补齐，用于平衡误杀和漏放。",
                ],
            },
            {
                "title": "运营效率指标",
                "status": "已有雏形，需扩展",
                "items": [
                    "queue_routing_accuracy：当前已有，衡量是否进入正确队列。",
                    "human_review_rate：当前已有，衡量人工介入占比。",
                    "evidence_ready_rate：下一步新增，衡量 reviewer 接手时证据是否齐全。",
                    "priority_queue_sla：下一步新增，衡量高风险 case 的处理时效。",
                ],
            },
            {
                "title": "治理稳定性指标",
                "status": "主要是下一步",
                "items": [
                    "reviewer_override_rate：人工推翻系统决策的比例。",
                    "appeal_overturn_rate：申诉翻案比例，直接对应误杀风险。",
                    "policy_version_regression_rate：规则版本变更后的回归情况。",
                    "consistency_on_similar_cases：相似 case 的处理一致性。",
                ],
            },
            {
                "title": "经济性 / ROI 指标",
                "status": "需要未来埋点支持",
                "items": [
                    "cost_per_1k_cases：每千条 case 的模型和系统成本。",
                    "manual_review_hours_saved：节省的人工复核时长。",
                    "marginal_quality_gain_per_cost_unit：每单位成本换来的质量收益。",
                    "shadow_audit_hit_rate：guarded auto-pass 是否真的提高 ROI。",
                ],
            },
        ],
        "roadmap_stages": [
            {
                "name": "V0",
                "title": "分类器 / 刚性工作流基线",
                "focus": "先证明任务能不能做。",
                "gate": "有最小 baseline，不追求复杂度。",
                "roi": "低成本、低说服力，适合作为起点，不适合作为终点。",
            },
            {
                "name": "V1",
                "title": "Policy-grounded bounded workflow",
                "focus": "把 case、policy、risk、queue 串成一个可解释链路。",
                "gate": "必须能说明为什么 pass / reject / escalate。",
                "roi": "高 ROI，是从 toy 进入工程化叙事的第一步。",
            },
            {
                "name": "V2",
                "title": "Evidence + routing + shadow audit",
                "focus": "把 evidence 获取、队列路由和 guarded auto-pass 做出来。",
                "gate": "queue_routing_accuracy 和 human_review_rate 可评测。",
                "roi": "高 ROI，直接提升业务可信度和 reviewer 协作感。",
            },
            {
                "name": "V3",
                "title": "Eval platform + regression",
                "focus": "把 baseline、slice、policy regression、failure taxonomy 固定下来。",
                "gate": "每次改 prompt / tool / policy 都能回归。",
                "roi": "极高 ROI，是进入持续优化阶段的前提。",
            },
            {
                "name": "V4",
                "title": "Reviewer / appeal / learning loop",
                "focus": "让 reviewer override 和 appeal overturn 真正回灌系统。",
                "gate": "知道哪些错误该修 policy，哪些才该进训练。",
                "roi": "中高 ROI，决定系统是否具备长期学习能力。",
            },
            {
                "name": "V5",
                "title": "Durable execution + stronger harness",
                "focus": "在有证据时再上更强的 harness、checkpoint 和 selective specialization。",
                "gate": "先证明当前瓶颈真来自架构，而不是 retrieval / eval / data 问题。",
                "roi": "选择性 ROI，必须由证据驱动，不应为了炫技提前做。",
            },
        ],
        "roi_buckets": [
            {
                "title": "现在就该做",
                "why": "高收益、低额外复杂度、直接提升说服力。",
                "items": [
                    "retrieval decision policy",
                    "slice / regression evals",
                    "failure harness",
                    "reviewer / appeal data model",
                ],
            },
            {
                "title": "量上来再做",
                "why": "对规模化治理更重要，但前提是主链路已稳定。",
                "items": [
                    "shadow audit instrumentation",
                    "adjudication memory",
                    "exposure-aware prioritization",
                    "reviewer throughput dashboards",
                ],
            },
            {
                "title": "有证据再做",
                "why": "复杂度高，不应先于基础闭环。",
                "items": [
                    "multi-agent specialization",
                    "heavy multimodal pipeline",
                    "complex reward learning",
                    "planner-critic orchestration everywhere",
                ],
            },
        ],
        "industry_mappings": [
            {
                "source": "TikTok",
                "lesson": "自动审核、additional review、appeal 和透明度是一起出现的，不是只做一个模型判定。",
                "application": "所以我们强调 safe automation boundary、queue routing、appeal loop，而不是单次分类正确率。",
            },
            {
                "source": "Meta",
                "lesson": "AI 适合放大规模和一致性，但高影响决策仍要保留人工关键角色。",
                "application": "所以 reviewer handoff 和 human review 不是失败兜底，而是系统设计的一部分。",
            },
            {
                "source": "YouTube",
                "lesson": "平台真正关心的是伤害暴露和政策一致性，而不是只看单次准确率。",
                "application": "所以我们必须补 exposure-aware prioritization、policy regression 和 consistency metrics。",
            },
            {
                "source": "OpenAI",
                "lesson": "先做 eval，再做 prompt、tool 和训练优化；trace 级评测很关键。",
                "application": "所以这页会把 baseline、slice eval、failure taxonomy 放在演化路线的前半段。",
            },
            {
                "source": "Anthropic",
                "lesson": "先从简单、可控的 workflow 开始，只在有证据时增加 agentic complexity。",
                "application": "所以 multi-agent 被放到后置项，而不是第一页亮点。",
            },
        ],
        "references": [
            {
                "label": "TikTok Transparency Update",
                "url": "https://newsroom.tiktok.com/en-US/bringing-even-more-transparency",
                "why_it_matters": "提供评论治理规模、自动化覆盖率和透明度报告的公开信号。",
            },
            {
                "label": "TikTok Community Guidelines Enforcement",
                "url": "https://www.tiktok.com/community-guidelines/en/enforcement",
                "why_it_matters": "说明 automated review、additional review、notice 和 appeal 必须一起看。",
            },
            {
                "label": "Meta Support and Safety With AI",
                "url": "https://about.fb.com/news/2026/03/boosting-your-support-and-safety-on-metas-apps-with-ai/",
                "why_it_matters": "说明高影响决策仍需 human judgment，支持人审协同设计。",
            },
            {
                "label": "YouTube Policy Development",
                "url": "https://blog.youtube/inside-youtube/policy-development-at-youtube/",
                "why_it_matters": "说明 policy quality、appeals 和一致性校准的重要性。",
            },
            {
                "label": "OpenAI Evaluation Best Practices",
                "url": "https://developers.openai.com/api/docs/guides/evaluation-best-practices",
                "why_it_matters": "支持 eval-first 和 human-calibrated evaluation 的方法。",
            },
            {
                "label": "Anthropic Building Effective Agents",
                "url": "https://www.anthropic.com/research/building-effective-agents/",
                "why_it_matters": "支持先简后繁、避免复杂度表演式升级的架构原则。",
            },
        ],
    }


def workflow_graph_payload() -> dict:
    return {
        "lanes": ["online_review", "offline_optimization"],
        "references": [
            {
                "title": "TikTok Community Guidelines Enforcement",
                "url": "https://www.tiktok.com/community-guidelines/en/enforcement",
                "note": "业务链路参考：自动化审核、补充复核、申诉机制必须进工作流设计。",
            },
            {
                "title": "TikTok Transparency Update (December 18, 2024)",
                "url": "https://newsroom.tiktok.com/en-US/bringing-even-more-transparency",
                "note": "治理产品参考：透明度和规模化治理能力需要通过可解释链路来体现。",
            },
            {
                "title": "TikTok LLM-Powered Content Moderation Role",
                "url": "https://lifeattiktok.com/search/7554140353420380424",
                "note": "岗位信号参考：agentic workflows、supporting evidence、policy logic 和 human review 的组合是目标能力。",
            },
            {
                "title": "LangGraph Workflows and agents",
                "url": "https://docs.langchain.com/oss/javascript/langgraph/workflows-agents",
                "note": "Agent 模式参考：prompt chaining、routing、orchestrator-worker、evaluator-optimizer 的官方拆法。",
            },
            {
                "title": "Choosing a LangGraph API",
                "url": "https://docs.langchain.com/oss/python/langgraph/choosing-apis",
                "note": "架构选型参考：Graph API 更适合 checkpointing、human-in-the-loop、memory 和细粒度控制流。",
            },
            {
                "title": "Anthropic: Building Effective AI Agents",
                "url": "https://www.anthropic.com/learn/building-effective-agents",
                "note": "架构原则参考：先从简单、可控的 workflow 开始，再逐步引入更复杂 agent loops。",
            },
            {
                "title": "OpenAI Evals Guide",
                "url": "https://developers.openai.com/api/docs/guides/evals",
                "note": "评测闭环参考：不能只看单次 demo，要评测整个审核工作流。",
            },
            {
                "title": "Hugging Face TRL GRPO Trainer",
                "url": "https://huggingface.co/docs/trl/en/grpo_trainer",
                "note": "后训练参考：争议 case 和 failure taxonomy 可以进一步进入 reward 设计。",
            },
        ],
        "nodes": [
            {
                "id": "case_intake",
                "lane": "online_review",
                "title": "Case Intake",
                "subtitle": "评论、上下文、举报量、历史风险进入同一 case",
                "summary": "评论审核不是只看一句文本，平台需要把 thread context、reporter_count、prior_violation_count、appeal 历史一起纳入当前案例。",
                "inputs": ["comment_text", "thread_context", "reporter_count", "prior_violation_count", "prior_appeal_overturns"],
                "outputs": ["normalized_review_case"],
                "why_agentic": "Agent 的第一步不是回答，而是把松散输入整理成结构化 case，决定后续要拉哪些证据。",
                "current_impl": "当前用 ReviewCase 承载输入，并在页面上允许手动编辑这些风险字段。",
                "optimize_next": ["接入更完整的账号画像", "区分楼中楼与主评论上下文", "把举报原因标签化"],
                "position": {"x": 70, "y": 96},
            },
            {
                "id": "context_loader",
                "lane": "online_review",
                "title": "Context Loader",
                "subtitle": "拿上下文，不让模型只盯一句话",
                "summary": "许多评论审核问题依赖上下文，尤其是反讽、阴阳怪气、指代不明的表达。",
                "inputs": ["review_case"],
                "outputs": ["context_items", "thread_direction"],
                "why_agentic": "这一步体现了先取证再决策，而不是直接文本分类。",
                "current_impl": "当前用输入的 thread_context 作为最小可用上下文源。",
                "optimize_next": ["接 conversation tree", "补父评论和楼层摘要", "支持上下文缺失告警"],
                "position": {"x": 320, "y": 96},
            },
            {
                "id": "policy_retrieval",
                "lane": "online_review",
                "title": "Policy Retrieval",
                "subtitle": "从规则里找依据，而不是裸给标签",
                "summary": "审核系统必须能回答：你为什么这么判。policy grounding 是评论审核 Agent 的核心，不是附属功能。",
                "inputs": ["comment_text", "policy_version"],
                "outputs": ["matched_policy_hits", "reviewer_guidance"],
                "why_agentic": "这是 tool use 的核心，模型需要围绕规则证据做决策。",
                "current_impl": "当前使用 policy fixture 做关键词命中和 guidance 返回。",
                "optimize_next": ["做 BM25 / hybrid retrieval", "支持 policy version regression", "支持条款层级冲突消解"],
                "position": {"x": 570, "y": 96},
            },
            {
                "id": "similar_case_retrieval",
                "lane": "online_review",
                "title": "Similar Case Retrieval",
                "subtitle": "给 reviewer 和模型一个历史参照物",
                "summary": "对上下文敏感 case，只靠规则不够，还要看历史 adjudication。",
                "inputs": ["matched_policy_hits", "review_case"],
                "outputs": ["similar_cases"],
                "why_agentic": "Agent 不只看规则，还要决定是否需要调用历史案例工具。",
                "current_impl": "当前从样例 case 中按 category 取最相似的历史案例。",
                "optimize_next": ["做 embedding 检索", "引入 reviewer override 历史", "支持申诉翻案样本优先展示"],
                "position": {"x": 820, "y": 96},
            },
            {
                "id": "risk_synthesis",
                "lane": "online_review",
                "title": "Risk Synthesis",
                "subtitle": "文本风险和用户风险一起看",
                "summary": "平台风险往往不是单点文本风险。举报密度、历史违规、申诉翻案历史、新账号等都要合成进来。",
                "inputs": ["matched_policy_hits", "reporter_count", "prior_violation_count", "prior_appeal_overturns"],
                "outputs": ["risk_signals"],
                "why_agentic": "Agent 的价值就在于把多个来源的弱信号聚合成下一步决策依据。",
                "current_impl": "当前生成 repeat_offender、appeal_sensitive_user、crowd_reports、new_account 等信号。",
                "optimize_next": ["做 calibrated risk score", "引入用户图谱信号", "区分恶意举报与真实举报"],
                "position": {"x": 180, "y": 280},
            },
            {
                "id": "decision_policy",
                "lane": "online_review",
                "title": "Decision Policy",
                "subtitle": "不是 yes/no，而是自动化边界策略",
                "summary": "这一步决定 pass / reject / escalate，并且显式保留 shadow audit 这样的 guarded auto-pass 边界。",
                "inputs": ["matched_policy_hits", "risk_signals", "context_items"],
                "outputs": ["action", "confidence", "rationale", "evidence_spans"],
                "why_agentic": "这里不是普通分类器逻辑，而是多步证据后的策略决策。",
                "current_impl": "当前优先按最高 severity 条款决策；上下文敏感表达稳定升级人工。",
                "optimize_next": ["引入 model + tool mixed policy", "做阈值学习", "把误杀成本纳入 reward"],
                "position": {"x": 430, "y": 280},
            },
            {
                "id": "queue_routing",
                "lane": "online_review",
                "title": "Queue Routing",
                "subtitle": "把不同 case 派去不同 reviewer 流程",
                "summary": "真正的审核系统不是只给 action，还要给 reviewer queue、priority、SLA。",
                "inputs": ["action", "risk_signals", "category"],
                "outputs": ["queue_name", "priority", "sla_minutes", "recommended_actions"],
                "why_agentic": "这里体现 workflow 设计能力，而不是单点模型能力。",
                "current_impl": "当前支持 priority_threat_queue、context_review_queue、shadow_audit_queue、auto_pass_archive。",
                "optimize_next": ["和真实 reviewer SLA 联动", "按业务时段动态调优", "支持队列负载感知路由"],
                "position": {"x": 680, "y": 280},
            },
            {
                "id": "reviewer_handoff",
                "lane": "online_review",
                "title": "Reviewer Handoff",
                "subtitle": "把决策、依据和建议一起交给人",
                "summary": "人审不应该重新做一遍搜索。系统应该交付 policy hit、risk signals、similar cases、recommended actions。",
                "inputs": ["queue_routing", "decision", "similar_cases"],
                "outputs": ["review_notes", "operator_actions"],
                "why_agentic": "Agent 不是取代 reviewer，而是减少 reviewer 的信息整合负担。",
                "current_impl": "当前工作台右侧已展示 reviewer notes、trace、similar cases 和 recommended actions。",
                "optimize_next": ["支持 reviewer override 写回", "支持 appeal replay", "支持批量审核台"],
                "position": {"x": 930, "y": 280},
            },
            {
                "id": "eval_snapshot",
                "lane": "offline_optimization",
                "title": "Eval Snapshot",
                "subtitle": "把审核系统变成可量化系统",
                "summary": "只看 demo 没法说明你理解审核业务。必须有 action accuracy、queue routing accuracy、human review rate 这类指标。",
                "inputs": ["review_cases", "agent_outputs"],
                "outputs": ["baseline_eval_report"],
                "why_agentic": "Agent 系统需要被评测整个工作流，而不是只测单个分类结果。",
                "current_impl": "当前 dashboard summary 和 baseline_eval_report 已导出。",
                "optimize_next": ["拆分类别维度指标", "加入 over-enforcement proxy", "加入 latency 和 reviewer throughput"],
                "position": {"x": 180, "y": 470},
            },
            {
                "id": "failure_review",
                "lane": "offline_optimization",
                "title": "Failure Review",
                "subtitle": "把失败样本变成结构化复盘对象",
                "summary": "误杀风险、人工压力、shadow audit 边界都需要进入 taxonomy，而不是只存在口头经验里。",
                "inputs": ["eval_report", "queue_outcomes"],
                "outputs": ["failure_review_report"],
                "why_agentic": "工作流优化来自 case-level 失败复盘，而不是只调 prompt。",
                "current_impl": "当前导出 manual_review_pressure、appeal_sensitive、shadow_audit_candidate 等 taxonomy。",
                "optimize_next": ["补 reviewer override taxonomy", "补 policy drift taxonomy", "加入 false positive / false negative 对账"],
                "position": {"x": 430, "y": 470},
            },
            {
                "id": "sft_export",
                "lane": "offline_optimization",
                "title": "SFT Export",
                "subtitle": "把好链路沉淀成监督样本",
                "summary": "成功的 policy-grounded trace 可以沉淀成 SFT 数据，不一定一上来就做大规模训练。",
                "inputs": ["successful_cases", "review_traces"],
                "outputs": ["sft_samples"],
                "why_agentic": "多步审核轨迹比单标签更适合作为后续模型学习对象。",
                "current_impl": "当前导出 decision、queue_routing、risk_signals、similar_cases 和 business tags。",
                "optimize_next": ["区分 gold trace 与 silver trace", "加入 reviewer correction", "支持多轮解释样本"],
                "position": {"x": 680, "y": 470},
            },
            {
                "id": "preference_export",
                "lane": "offline_optimization",
                "title": "Preference / Reward Loop",
                "subtitle": "争议 case 是后训练价值最高的资产",
                "summary": "申诉翻案、人工 override、shadow audit case 最适合进入 preference 或 reward 设计。",
                "inputs": ["appeal_cases", "reviewer_disagreements", "failure_taxonomy"],
                "outputs": ["preference_pairs", "reward_design_candidates"],
                "why_agentic": "这一步把在线审核边界和后训练策略连起来，符合 JD 对持续优化的期待。",
                "current_impl": "当前已有 preference_pairs 和 failure_review 报告，但还没接真实训练器。",
                "optimize_next": ["接 TRL DPO/GRPO", "做 queue-aware reward", "用人工纠偏构造高价值 preference 数据"],
                "position": {"x": 930, "y": 470},
            },
        ],
        "edges": [
            {"from": "case_intake", "to": "context_loader"},
            {"from": "context_loader", "to": "policy_retrieval"},
            {"from": "policy_retrieval", "to": "similar_case_retrieval"},
            {"from": "similar_case_retrieval", "to": "risk_synthesis"},
            {"from": "risk_synthesis", "to": "decision_policy"},
            {"from": "decision_policy", "to": "queue_routing"},
            {"from": "queue_routing", "to": "reviewer_handoff"},
            {"from": "reviewer_handoff", "to": "eval_snapshot"},
            {"from": "eval_snapshot", "to": "failure_review"},
            {"from": "failure_review", "to": "sft_export"},
            {"from": "failure_review", "to": "preference_export"},
            {"from": "preference_export", "to": "decision_policy"},
        ],
    }


def research_log_payload() -> dict:
    return {
        "title": "调研记录",
        "summary": "这份记录不只解释“为什么这是 Agent”，更要回答四个问题：先怎么理解评论治理业务；怎么把问题抽象成可优化链路；为什么选这种 Agent 范式与 node 拆法；最后如何用评测闭环把系统持续做深。",
        "sections": [
            {
                "title": "业务理解与优化目标",
                "body": [
                    "这个 JD 的核心不是做一个会打标签的大模型，而是把评论审核业务拆成可落地、可量化、可持续优化的系统。业务目标至少同时包括平台安全、误杀控制、人工效率、策略一致性和申诉友好度。",
                    "所以项目目标不能是“判断这条评论违规吗”，而应该是“如何把一个评论 case 在正确的自动化边界内处理掉，并把高风险、不确定、争议样本稳定交给人审与后续优化链路”。",
                ],
            },
            {
                "title": "问题抽象",
                "body": [
                    "评论审核的真正难点不在于“识别脏话”本身，而在于上下文敏感、规则约束、多信号合成、人工协同、策略变更和复核申诉这些真实业务条件。",
                    "如果把问题抽象成分类任务，系统会天然忽略 supporting evidence、human review boundary、queue routing 和 appeal replay；但这四件事恰恰是审核业务里最贵也最关键的部分。",
                    "因此这个问题更适合抽象成一个带状态的 case workflow，而不是一个单轮文本判断器。",
                ],
            },
            {
                "title": "为什么这是 Agent",
                "body": [
                    "这里的 Agent 不是通用型万能助手，而是一个 bounded moderation agent。它会依次取上下文、取规则、取相似 case、合成风险、做决策、路由队列，并给 reviewer 交付可复核证据。",
                    "如果系统只是输入一句评论，输出一个 label，那更像分类器。现在这套链路之所以更接近 Agent，是因为它在做多步证据获取、tool use 和工作流控制。",
                    "现阶段它是一个 deterministic-first 的 Agent scaffold，后续可以逐步把 decision policy、policy retrieval、similar case retrieval 替换成更强的模型与工具调用。",
                ],
            },
            {
                "title": "Agent 架构范式调研",
                "body": [
                    "调研后我把候选方案分成四类：one-shot classifier、顺序工作流、bounded single-agent graph、supervisor multi-agent。Anthropic 和 LangGraph 的官方资料都更推荐先从简单、可控、可审计的工作流开始，再视复杂度增加 agent loops。",
                    "内容审核属于高约束、高一致性、高审计需求场景。这里最不缺的是“会回答的模型”，最缺的是“有边界、能追责、能和人审协同的系统”。所以我推荐 deterministic-first 的 bounded single-agent DAG，而不是一开始上 supervisor multi-agent。",
                    "多智能体不是不能做，而是应该等到 policy retrieval、appeal analysis、reviewer assist 明确成为独立子域后，再按职责切出去；第一版直接上多智能体，收益很可能不如复杂度增长快。",
                ],
            },
            {
                "title": "如果用 LangGraph，为什么选 Graph API",
                "body": [
                    "LangGraph 官方明确把 Graph API 放在需要 checkpointing、human-in-the-loop、memory 和更细粒度 control flow 的场景下。评论审核恰好同时命中这四个条件：case 要有状态、需要 reviewer override、策略会变、trace 要可追溯。",
                    "所以如果后续把这套原型迁到 LangGraph，我不会先把它做成自由聊天式 agent，而会优先用 StateGraph/Graph API，把 case schema、policy version、risk signals、tool trace、appeal outcome 放在同一个 state 上。",
                    "这个选择的本质不是‘LangGraph 更酷’，而是 Graph API 更贴合审核业务里的状态转移和审计要求。",
                ],
            },
            {
                "title": "如果用 LangGraph，node 怎么选",
                "body": [
                    "node 不是按“一个模型一个 node”来拆，而是按业务状态边界来拆。拆分标准是：这个步骤是否需要独立输入输出契约、是否可能被不同工具替换、是否值得单独评测、是否需要独立 audit。",
                    "所以在线链路更合理的 node 是：case intake、context loader、policy retrieval、similar case retrieval、risk synthesis、decision policy、queue routing、reviewer handoff。它们每个都对应一个真实业务责任点，而不是任意技术切块。",
                    "离线链路也应继续拆 eval snapshot、failure review、SFT export、preference / reward loop，因为 JD 关心的不是单次上线，而是全生命周期优化。",
                ],
            },
            {
                "title": "评测指标与方法",
                "body": [
                    "评测不能只看 action accuracy。更关键的维度包括：over-enforcement proxy、under-enforcement proxy、high-risk escalation recall、queue routing accuracy、policy grounding rate、consistency across similar cases、reviewer throughput 和 appeal-sensitive error rate。",
                    "方法上至少要分三层：离线回放评测、shadow mode / audit 抽检、人工复核与申诉结果回灌。OpenAI 的 eval 指南强调持续运行 eval、使用多标准 graders 和更广的数据分布，这一点非常适合审核系统。",
                    "数据集也不能只是一堆普通脏话样本，而应覆盖明确违规、明确安全、上下文敏感、争议样本、申诉翻案样本、策略版本变更回归样本。",
                ],
            },
            {
                "title": "评测闭环与优化思路",
                "body": [
                    "评测闭环不是锦上添花，而是内容治理系统可信度的基础。更合理的路径是：在线 case -> offline eval snapshot -> failure taxonomy -> reviewer override / appeal replay -> SFT / preference / reward 数据 -> 反推 policy retrieval、decision policy、queue routing 和阈值策略。",
                    "这意味着优化点不只在 prompt，而在四层：证据层、决策层、路由层、后训练层。比如 policy retrieval 命中差，应该补知识检索；误杀高，应该调 decision boundary；升级太多，应该优化 queue routing；争议样本集聚，则应该进入 preference / reward 数据。",
                    "真正符合 JD 的表达不是‘我会做 Agent’，而是‘我知道哪个业务问题该在哪个层面被优化，并且能用评测闭环把它持续做对’。",
                ],
            },
        ],
        "summary_panels": [
            {
                "status": "业务理解与优化目标",
                "title": "先定义业务目标，再谈 Agent",
                "items": [
                    "目标函数至少同时覆盖安全、误杀、人工效率、一致性、申诉友好度。",
                    "评论审核是 case workflow，不是单轮分类。",
                    "优化边界比盲目追求自动化率更重要。",
                ],
            },
            {
                "status": "推荐 Agent 范式",
                "title": "Bounded Single-Agent DAG / LangGraph Graph API",
                "items": [
                    "先用可控、可审计的 DAG，再决定是否拆成多智能体。",
                    "Graph API 更适合 checkpointing、human-in-the-loop、memory、stateful trace。",
                    "node 按业务状态边界拆，不按模型数量拆。",
                ],
            },
            {
                "status": "评测指标",
                "title": "先评测系统，再优化模型",
                "items": [
                    "质量：action、queue、误杀、漏放、高风险升级召回。",
                    "运营：human review rate、priority queue SLA、reviewer throughput。",
                    "治理：policy grounding、policy version regression、appeal-sensitive error。",
                ],
            },
            {
                "status": "评测闭环",
                "title": "失败样本是后训练和策略优化资产",
                "items": [
                    "failure taxonomy 连接在线表现与后训练数据。",
                    "reviewer override / appeal replay 是高价值监督信号。",
                    "优化层次包括 evidence、decision、routing、reward design。",
                ],
            },
        ],
        "sources": [
            {
                "label": "TikTok Community Guidelines Enforcement",
                "url": "https://www.tiktok.com/community-guidelines/en/enforcement",
                "why_it_matters": "确认 automated review、additional review、appeal 这些真实审核链路元素必须进系统设计。",
            },
            {
                "label": "TikTok transparency update (December 18, 2024)",
                "url": "https://newsroom.tiktok.com/en-US/bringing-even-more-transparency",
                "why_it_matters": "强化了透明度、规模化自动化和评论治理独立性，对 dashboard 和 eval artifact 很有指导意义。",
            },
            {
                "label": "TikTok DSA transparency report in Europe",
                "url": "https://newsroom.tiktok.com/en-eu/digital-services-act-our-sixth-transparency-report-on-content-moderation-in-europe",
                "why_it_matters": "提供自动化执行比例与确认准确性的公开信号，能帮助定义 automation coverage 与 precision 类指标。",
            },
            {
                "label": "TikTok Safety Product role on LLM-powered content moderation",
                "url": "https://lifeattiktok.com/search/7554140353420380424",
                "why_it_matters": "直接点明 agentic workflows、supporting evidence、policy logic 和 human review 的组合价值。",
            },
            {
                "label": "TikTok Safety Product role on Model Policy Lead",
                "url": "https://lifeattiktok.com/search/7554140353688807688",
                "why_it_matters": "补充说明审核系统还要支持 policy calibration、audit、feedback loop 和跨团队对齐。",
            },
            {
                "label": "Meta AI support and safety post (March 20, 2026)",
                "url": "https://about.fb.com/news/2026/03/boosting-your-support-and-safety-on-metas-apps-with-ai/",
                "why_it_matters": "强化了 safe automation boundary 和 high-impact decision 仍需 human judgment 的原则。",
            },
            {
                "label": "LangGraph overview",
                "url": "https://docs.langchain.com/oss/python/langgraph/overview",
                "why_it_matters": "官方明确把 low-level orchestration、human-in-the-loop、persistence 放在 LangGraph 的核心能力里。",
            },
            {
                "label": "LangGraph Workflows and agents",
                "url": "https://docs.langchain.com/oss/javascript/langgraph/workflows-agents",
                "why_it_matters": "官方把 prompt chaining、routing、parallelization、orchestrator-worker、evaluator-optimizer 定义成可组合架构模式。",
            },
            {
                "label": "Choosing a LangGraph API",
                "url": "https://docs.langchain.com/oss/python/langgraph/choosing-apis",
                "why_it_matters": "解释了为什么 Graph API 更适合需要 checkpointing、human-in-the-loop、memory 和细粒度控制流的系统。",
            },
            {
                "label": "Thinking in LangGraph",
                "url": "https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph",
                "why_it_matters": "提供了围绕 state、errors、interrupts 和 node 边界来思考图结构的官方方法。",
            },
            {
                "label": "Anthropic: Building Effective AI Agents",
                "url": "https://www.anthropic.com/learn/building-effective-agents",
                "why_it_matters": "提供从简单 workflow 到更复杂 agentic patterns 的官方建议，支持先简后繁的架构取舍。",
            },
            {
                "label": "Anthropic: Safe and trustworthy agents framework",
                "url": "https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents",
                "why_it_matters": "强调 agent 需要透明边界、人工控制、权限管理和高影响决策保护。",
            },
            {
                "label": "Perspective API codelab",
                "url": "https://developers.google.com/codelabs/setup-perspective-api",
                "why_it_matters": "说明审核模型更适合作为辅助信号，而不是直接替代人类判断。",
            },
            {
                "label": "OpenAI Evals Guide",
                "url": "https://developers.openai.com/api/docs/guides/evals",
                "why_it_matters": "提醒我们不要只看 demo，而要把系统拆成多维评测标准。",
            },
            {
                "label": "OpenAI Moderation Guide",
                "url": "https://developers.openai.com/api/docs/guides/moderation",
                "why_it_matters": "强调 moderation thresholds 和 category scores 需要随策略持续校准。",
            },
            {
                "label": "Hugging Face TRL GRPO Trainer",
                "url": "https://huggingface.co/docs/trl/en/grpo_trainer",
                "why_it_matters": "解释了为什么争议 case、group reward 和在线优化能自然接到这个审核项目后续版本里。",
            },
            {
                "label": "ReAct paper",
                "url": "https://arxiv.org/abs/2210.03629",
                "why_it_matters": "提供了先取证再行动的 Agent 范式基础。",
            },
        ],
        "evaluation_loop": [
            "收集评论 case、在线审核结果、queue routing、reviewer override、appeal outcome",
            "生成 offline eval snapshot，观察 action、queue、误杀、漏放、policy grounding、一致性",
            "把人工压力、申诉敏感样本、shadow audit、policy drift 转成 failure taxonomy",
            "把高价值失败样本导出成 SFT / preference / reward 候选数据",
            "反向优化 policy retrieval、decision boundary、queue routing、阈值策略和 reward design",
        ],
    }
