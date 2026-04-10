# CommentOps 项目讲述脚本

## 1. 用一句话开场

我做的不是一个评论分类 demo，而是一个面向内容治理场景的评论审核 Agent 样板间。它把业务理解、证据获取、自动化边界、人审协同、评测闭环和后训练数据回灌串成了一套完整系统。

## 2. 先讲业务，不先讲模型

这个项目首先解决的是业务问题，不是技术问题。评论审核在真实场景里同时要满足：

- 平台安全
- 误杀控制
- reviewer 提效
- 策略一致性
- 申诉友好度

所以审核对象不是一句评论，而是一个 case。case 里不只有 comment_text，还包括 thread_context、policy_version、举报量、历史违规、申诉翻案历史等字段。

## 3. 再讲问题抽象

如果把这个问题抽象成二分类，很多最关键的治理能力都会丢掉，比如：

- policy grounding
- queue routing
- reviewer handoff
- appeal replay

因此我把它抽象成一个 stateful moderation workflow，而不是一轮 prompt 分类。

## 4. 再讲架构取舍

我调研后把方案分成四类：

- one-shot classifier
- sequential workflow
- bounded single-agent DAG
- supervisor multi-agent

第一版我选择的是 `bounded single-agent DAG`。原因不是它最炫，而是它最符合审核业务的高约束、高审计、高一致性需求。

如果后续迁到 LangGraph，我会优先使用 `Graph API / StateGraph`，因为这个场景天然需要：

- state
- checkpointing
- human-in-the-loop
- traceable control flow

## 5. 再讲 node 怎么拆

我不是按“一个模型一个 node”拆，而是按业务状态边界拆：

- case_intake
- context_loader
- policy_retrieval
- similar_case_retrieval
- risk_synthesis
- decision_policy
- queue_routing
- reviewer_handoff

离线继续拆：

- eval_snapshot
- failure_review
- sft_export
- preference_export

这样每个节点都可以独立替换、独立评测、独立复盘。

## 6. 再讲评测指标

我不会只讲 accuracy，而会把指标分三层：

### 在线质量指标

- action_accuracy
- high_risk_escalation_recall
- over_enforcement_proxy
- under_enforcement_proxy
- policy_grounding_rate

### 运营效率指标

- queue_routing_accuracy
- human_review_rate
- reviewer_throughput
- priority_queue_sla

### 治理稳定性指标

- consistency_on_similar_cases
- appeal_sensitive_error_rate
- policy_version_regression_rate
- reviewer_override_rate

## 7. 最后讲闭环

真正符合 JD 的亮点不在于“我做了一个 Agent”，而在于：

1. 我知道哪个问题属于 evidence layer
2. 哪个问题属于 decision boundary
3. 哪个问题属于 routing strategy
4. 哪个问题应该进 SFT / preference / reward

完整闭环是：

`在线 case -> offline eval -> failure taxonomy -> reviewer / appeal 回灌 -> SFT / preference / reward -> 反向优化系统`

## 8. 该展示哪些产出物

展示项目时，最能证明深度的不是前端，而是这些产出：

- `docs/examples/2026-04-01-commentops-agent-architecture-and-eval-framework.md`
- `docs/examples/2026-03-31-cqc-comment-agent-research.md`
- `examples/commentops/eval/baseline_eval_report.json`
- `examples/commentops/eval/sft_samples.jsonl`
- `examples/commentops/eval/preference_pairs.jsonl`
- `examples/commentops/eval/failure_review.json`

## 9. 最后一句收束

如果面试里只说“我做了个审核 Agent”，很容易显得泛；但如果说“我把评论治理业务抽象成一个 bounded moderation agent，并设计了 evidence、decision、routing、training 四层闭环”，项目的层次会明显更高。
