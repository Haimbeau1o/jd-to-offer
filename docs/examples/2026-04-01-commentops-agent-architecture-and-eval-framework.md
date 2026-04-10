# CommentOps Agent 架构与评测框架重构

## 目标

这份说明解决两个核心问题：

1. 这个项目到底采用什么 Agent 范式，为什么这样选
2. 应该如何从业务理解出发，抽象问题、定义指标、搭建评测闭环

我把答案组织成一条完整链路：

`业务理解 -> 问题抽象 -> Agent 架构调研 -> node 拆分 -> 指标与方法 -> 闭环优化`

## 1. 业务理解：这不是“评论分类”，而是“评论 case 处理系统”

从 JD 来看，岗位真正要解决的不是“评论是否违规”这么窄的问题，而是：

- 哪些 case 可以安全自动化
- 哪些 case 必须升级人工
- 如何让 policy、reviewer、strategy、model 形成闭环
- 如何用量化指标证明收益和风险边界

因此系统目标至少包含五个维度：

- 平台安全：高风险内容别漏放
- 误杀控制：正常讨论不要被粗暴打掉
- 人工效率：reviewer 不要重复搜证
- 策略一致性：同类 case 不要前后判断漂移
- 申诉友好度：高争议、高影响决策要可复核、可追溯

这意味着审核对象不是一句评论，而是一个 `case`：

- comment_text
- thread_context
- policy_version
- reporter_count
- prior_violation_count
- prior_appeal_overturns
- reviewer_override / appeal_outcome

## 2. 问题抽象：评论审核的优化点到底在哪

如果把问题抽象成二分类，会天然遗漏以下真实成本：

- 上下文敏感：反讽、引用、楼中楼语义常常不能脱离 thread 判断
- 规则约束：审核系统必须回答“依据哪条 policy 判的”
- 多信号合成：举报量、历史违规、申诉翻案历史、新号风险都影响处置
- 人工协同：系统不仅要判，还要决定是否升级、路由到哪类 reviewer queue
- 策略变化：policy version 更新后，系统必须有回归评测能力

所以更合理的抽象不是 classifier，而是 `stateful moderation workflow`：

- 先构造 case
- 再拉上下文和规则证据
- 再聚合风险
- 再做自动化边界决策
- 再把结果交给 reviewer 或下游闭环

## 3. Agent 架构范式调研

### 方案 A：One-shot classifier

优点：

- 实现最简单
- 延迟低

缺点：

- 天然缺 supporting evidence
- 很难表达升级人工和 queue routing
- 很难接 policy version、appeal replay、failure taxonomy

结论：

- 不适合作为这个 JD 的主项目 framing

### 方案 B：顺序工作流

优点：

- 比分类器更接近真实审核链路
- 可解释性明显更好

缺点：

- 如果只有简单顺序调用，仍然缺状态治理和人审打断机制
- 对复杂分支、审计回放和 checkpoint 支持不够自然

结论：

- 适合作为最小原型，但不足以承载“全生命周期管理”的表达

### 方案 C：Bounded single-agent DAG

优点：

- 可以把多步取证、tool use、决策与路由放进统一状态图
- 容易插入 human-in-the-loop 和审计节点
- 每个节点都能独立评测、替换和优化

缺点：

- 设计时要克制，不能把所有事都强行 node 化

结论：

- 这是最符合当前 JD 的主推荐方案

### 方案 D：Supervisor multi-agent

优点：

- 适合多个稳定子域并行协作
- 在大规模复杂组织里有扩展潜力

缺点：

- 调度复杂度高
- 容易弱化一致性和审计清晰度
- 第一版常常收益不如复杂度增长快

结论：

- 适合二阶段以后再拆，例如 policy-agent、appeal-agent、reviewer-assist-agent 真正成熟时再考虑

## 4. 如果用 LangGraph，为什么优先用 Graph API

这里推荐的不是“为了用 LangGraph 而用 LangGraph”，而是因为它的 Graph API 与审核场景的需求高度匹配。

原因有四个：

1. 审核 case 有显式状态  
   `case schema / policy version / risk signals / tool trace / reviewer outcome` 需要保存在统一状态里。

2. 审核场景天然需要 human-in-the-loop  
   reviewer override、appeal replay、high-risk decision 都不能只靠模型自动走到底。

3. 审核系统需要 checkpoint 和可回放  
   一旦发生错判、误杀、申诉翻案，需要回看当时 evidence、route、decision boundary。

4. 审核链路需要细粒度控制流  
   不同 case 会走不同分支：直接 pass、直接 reject、shadow audit、priority queue、context review。

因此，如果后续把当前原型迁到 LangGraph，我会优先选：

- `StateGraph` / `Graph API`
- 显式 state schema
- 可插入 interrupt / human review 的节点
- 每个节点保留 trace 和可评测输入输出

而不是先做自由聊天式 agent。

## 5. 如果用 LangGraph，node 怎么选

node 不按“一个模型一个 node”来拆，而按业务状态边界拆。

拆分标准：

- 是否有独立输入输出契约
- 是否可能被不同工具或模型替换
- 是否值得单独评测
- 是否需要独立 audit

按这个标准，在线链路推荐拆成：

| Node | 作用 | 为什么值得单独成为 node |
|---|---|---|
| `case_intake` | 把评论、上下文、风险字段收束成 case | 输入契约清晰，是后续一切证据与决策的起点 |
| `context_loader` | 获取 thread / parent / conversation context | 上下文质量直接影响误杀与漏放 |
| `policy_retrieval` | 拉取规则条款与 reviewer guidance | 审核系统必须 policy-grounded |
| `similar_case_retrieval` | 拉历史 adjudication 作为参考 | 处理争议样本和一致性问题 |
| `risk_synthesis` | 合成举报、历史违规、申诉敏感等信号 | 风险不只是文本风险 |
| `decision_policy` | 决定 pass / reject / escalate | 自动化边界的核心 |
| `queue_routing` | 路由 queue、priority、SLA | 审核不是只有判定，还有处置流程 |
| `reviewer_handoff` | 交付 notes / evidence / actions | 减少 reviewer 的二次搜证成本 |

离线链路继续拆成：

- `eval_snapshot`
- `failure_review`
- `sft_export`
- `preference_export`

这样做的意义是：每个节点都可以独立替换、独立评测、独立复盘。

## 6. 评测指标：不只看 action accuracy

### 6.1 在线质量指标

- `action_accuracy`
- `queue_routing_accuracy`
- `high_risk_escalation_recall`
- `over_enforcement_proxy`
- `under_enforcement_proxy`
- `policy_grounding_rate`
- `consistency_on_similar_cases`

### 6.2 运营效率指标

- `human_review_rate`
- `shadow_audit_hit_rate`
- `priority_queue_sla`
- `reviewer_throughput`
- `evidence_ready_rate`

### 6.3 治理稳定性指标

- `appeal_sensitive_error_rate`
- `policy_version_regression_rate`
- `reviewer_override_rate`
- `low_confidence_auto_action_rate`

## 7. 评测方法：要分层，不要只跑一次 demo

### 7.1 离线回放评测

数据集至少应覆盖：

- 明确违规样本
- 明确安全样本
- 上下文敏感样本
- 争议样本
- 申诉翻案样本
- policy version 变更回归样本

### 7.2 Shadow mode / 审计抽检

在不直接放权的情况下观察：

- 自动化边界是否保守
- 哪类样本最容易误杀
- queue routing 是否合理

### 7.3 人工复核回灌

用 reviewer override、appeal outcome 反推：

- 决策边界是否过激
- 哪类 supporting evidence 缺失
- 哪条 policy guidance 最容易引发漂移

## 8. 评测闭环：失败样本如何变成优化资产

推荐闭环：

1. 收集 case、在线结果、queue、reviewer override、appeal outcome
2. 生成 offline eval snapshot
3. 归纳 failure taxonomy
4. 导出高价值 SFT / preference / reward 数据
5. 反向优化 evidence、decision、routing、reward design

这里的关键不是“做了后训练”，而是知道失败应当在什么层面被修：

- policy retrieval 差：补知识检索
- context 理解差：补 conversation context 和 evidence extraction
- 误杀高：调 decision boundary
- 升级过多：调 queue routing 和阈值策略
- 争议样本集中：进入 preference / reward 数据

## 9. 对当前项目的落地建议

项目展示上，应该优先强调：

- 这是一个 `bounded moderation agent`，不是聊天机器人
- 架构上更接近 `single-agent DAG / StateGraph`
- node 是按业务状态边界拆的
- 评测不只测最终 action，还测 route、grounding、误杀/漏放、人工效率
- failure review 直接连接后训练与策略优化

## 参考资料

- [TikTok Community Guidelines Enforcement](https://www.tiktok.com/community-guidelines/en/enforcement)
- [TikTok transparency update (December 18, 2024)](https://newsroom.tiktok.com/en-US/bringing-even-more-transparency)
- [TikTok DSA transparency report in Europe](https://newsroom.tiktok.com/en-eu/digital-services-act-our-sixth-transparency-report-on-content-moderation-in-europe)
- [TikTok Safety Product role on LLM-powered content moderation](https://lifeattiktok.com/search/7554140353420380424)
- [TikTok Safety Product role on Model Policy Lead](https://lifeattiktok.com/search/7554140353688807688)
- [Meta AI support and safety post (March 20, 2026)](https://about.fb.com/news/2026/03/boosting-your-support-and-safety-on-metas-apps-with-ai/)
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph Workflows and agents](https://docs.langchain.com/oss/javascript/langgraph/workflows-agents)
- [Choosing a LangGraph API](https://docs.langchain.com/oss/python/langgraph/choosing-apis)
- [Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)
- [Anthropic: Building Effective AI Agents](https://www.anthropic.com/learn/building-effective-agents)
- [Anthropic: Safe and trustworthy agents framework](https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents)
- [Perspective API codelab](https://developers.google.com/codelabs/setup-perspective-api)
- [OpenAI Evals Guide](https://developers.openai.com/api/docs/guides/evals)
- [OpenAI Moderation Guide](https://developers.openai.com/api/docs/guides/moderation)
- [Hugging Face TRL GRPO Trainer](https://huggingface.co/docs/trl/en/grpo_trainer)
