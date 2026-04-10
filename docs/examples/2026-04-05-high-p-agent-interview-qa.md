# 高 P 面试官追问 Agent 项目时的标准问答稿

## 这份文档怎么用

这不是一份“标准话术大全”，而是一份“高 P 面试官视角的拆题手册”。

每个问题都按五层来写：

1. `面试官真正想考什么`
2. `差回答长什么样`
3. `好回答应该怎么组织`
4. `放到当前评论审核项目里，应该怎么答`
5. `如果继续追问，下一层该怎么接`

目标不是让你背答案，而是让你建立一种稳定的答题框架：

`业务问题 -> 设计取舍 -> 工程边界 -> 指标证明 -> 下一步优化`

如果你能按这个顺序回答，大多数 Agent 面试问题都会显得更稳。

---

## 总原则：先讲问题，再讲设计

高 P 最讨厌的回答方式：

- “我用了 LangGraph / MCP / 多 Agent / 多模态 / mem0”

高 P 更想听的回答方式：

- “我遇到了什么业务问题”
- “为什么原方案不够”
- “所以我这样设计”
- “这样设计的代价是什么”
- “我如何验证它比 baseline 更好”

所以每一道题，你都尽量按下面这个模板答：

1. 先说这道题对应的业务问题
2. 再说你的设计选择
3. 再说 trade-off
4. 再说指标或证据
5. 最后说下一步优化

---

## 1. 你的 Agent 是怎么决定“要不要检索”的？

### 面试官真正想考什么

这题不是在问你“会不会调 RAG”，而是在问：

- 系统有没有真正的决策点
- 是不是写死流程
- 你是否理解“检索也有成本和风险”

### 差回答

`用户提问后我就去查知识库，再把结果拼到 prompt 里。`

这类回答的问题是：

- 默认永远查
- 没有拒绝检索的条件
- 没有检索充分性的判断

### 好回答结构

推荐回答结构：

`我把检索决策拆成三步：先判断需不需要查，再判断查哪个源，最后判断当前证据是否足够，不够才继续补查。如果问题本身已经在当前状态里能回答，就不再额外检索，避免引入噪声和成本。`

然后补一句 trade-off：

`这样做的原因是，检索不是越多越好，查错源、查过量都会让结果变差。`

### 当前评论审核项目怎么答

可以诚实地这样答：

`当前评论审核项目已经把 retrieval 拆成了 policy、similar case 和 context 几类证据来源，但严格说还没有做到完整的 retrieval decision policy。现在更像是一个 bounded workflow：先做 policy hit，再看相似 case 和风险信号。下一步我会把它升级成“什么时候查 policy、什么时候补上下文、什么时候直接升级人工”的显式决策层。`

可以引用本地实现：

- [agent.py](/Volumes/passport/简历/滴滴/src/commentops_agent_lab/agent.py#L59)

### 如果继续追问

常见追问：

- 你怎么定义“证据足够”？
- 什么时候不查比查更好？

可以这样接：

`在审核场景里，证据足够通常不是“信息越多越好”，而是看是否已经满足 policy grounding 和动作边界。如果还缺 thread context、policy clause 或历史 adjudication，我更愿意升级人工，而不是继续无边界补证。`

---

## 2. 你的系统有真记忆吗？记什么？什么时候存？

### 面试官真正想考什么

这题在考：

- 你有没有把 memory 和上下文拼接区分开
- 你是否理解长期记忆和短期状态的差别
- 你有没有召回策略和过期策略

### 差回答

`我用了向量库 / mem0，所以系统有记忆。`

这类回答一听就很虚，因为没有回答：

- 存什么
- 为什么存
- 怎么召回
- 召回错了怎么办

### 好回答结构

`我把记忆分成三层：短期会话状态、长期用户或任务记忆、以及摘要压缩。不是所有内容都进长期记忆，只有会影响后续决策的稳定偏好、关键历史事件和高价值结论才会写入。召回时也不是全量拼接，而是按任务类型和时间新鲜度筛选。`

### 当前评论审核项目怎么答

`当前评论审核项目还没有真正做长期记忆系统，但已经把几类关键历史信号显式纳入 case，比如 prior_violation_count、prior_appeal_overturns、author_tenure_days。也就是说，它已经有“风险历史记忆”的 schema，但还没有做 memory write / recall / freshness 管理。下一步如果要升级，我会优先做 adjudication memory 和 appeal-sensitive memory，而不是通用聊天式 memory。`

引用：

- [agent.py](/Volumes/passport/简历/滴滴/src/commentops_agent_lab/agent.py#L34)

### 如果继续追问

常见追问：

- 审核系统最值得长期记住什么？

可以这样答：

`审核场景里最值得长期保留的不是普通用户偏好，而是违规历史、申诉翻案历史、相似 case 的最终裁决，以及 policy version 对应的旧判断。因为这些信息直接影响一致性和误杀控制。`

---

## 3. 你怎么证明这个方案比 baseline 更好？

### 面试官真正想考什么

这题考的是：

- 你是否真的做过评测
- 你是否有比较对象
- 你是否知道自己优化了什么

### 差回答

`我感觉效果更好了，回答更稳定了。`

这类回答几乎等于承认没有评测。

### 好回答结构

`我会先明确 baseline，再看我这次引入的能力主要改善了什么指标。比如相对于 one-shot baseline，我更关注 high-risk recall、policy grounding rate、queue routing accuracy 以及 human review rate，而不是只看 overall accuracy。`

### 当前评论审核项目怎么答

`当前项目已经有第一版离线评测，覆盖 action_accuracy、policy_grounding_rate、escalation_precision、human_review_rate 和 queue_routing_accuracy。但如果按更严格标准说，它还没有完成 baseline 对照，也缺少 high-risk recall、appeal-sensitive slice 和 regression set。所以我现在会把它定义成“评测骨架已建立，但正式 baseline 体系还在补齐”。`

引用：

- [eval.py](/Volumes/passport/简历/滴滴/src/commentops_agent_lab/eval.py#L28)

### 如果继续追问

你可以主动补一句：

`我下一步会把 baseline 明确拆成 rule-based、one-shot LLM 和当前 bounded workflow 三档，这样提升点会更有说服力。`

---

## 4. 你为什么不用多 Agent？或者为什么要用多 Agent？

### 面试官真正想考什么

这题不是在比谁架构更花，而是在看：

- 你会不会为了“显得高级”而过度设计
- 你是否理解复杂度和收益的关系

### 差回答

`因为现在都流行多 Agent，所以我也做了 Planner、Executor、Critic。`

### 好回答结构

`我先看业务本身需不需要多角色协作。如果任务高约束、高审计、主链路比较稳定，我优先做 bounded single-agent workflow，把状态、证据、决策和 routing 做清楚。只有当 eval 证明单 Agent 在某些子问题上确实不够，才会拆多 Agent。`

### 当前评论审核项目怎么答

`评论审核这个场景我刻意没有一开始就做多 Agent。因为它最核心的是 evidence、decision boundary、queue routing 和 human review，这些都要求高一致性、可审计、可回放。当前我更倾向 bounded single-agent workflow。等后续如果 policy retrieval、appeal replay、reviewer assist 真出现稳定的子域边界，再考虑拆成 specialized agents。`

引用：

- [2026-04-01-commentops-project-storyboard.md](/Volumes/passport/简历/滴滴/docs/examples/2026-04-01-commentops-project-storyboard.md#L27)

### 如果继续追问

可以这样接：

`我不把“只有一个 Agent”当缺点，真正的问题是“是不是一个大 prompt 包打天下”。如果内部已经按 case intake、policy retrieval、risk synthesis、decision、routing 拆清楚，单 Agent 也可以非常工程化。`

---

## 5. 你的 Agent 会因为中间结果不对而改计划吗？

### 面试官真正想考什么

这题在考：

- 有没有 adaptive control
- 有没有中间状态驱动分支

### 差回答

`我有 plan，执行就是按 plan 走。`

这说明链路可能是写死的。

### 好回答结构

`我不追求无限制重规划，而是让系统在关键中间条件变化时切换到正确分支。比如证据不足、工具失败、风险提升、结果冲突，都会触发不同路径。`

### 当前评论审核项目怎么答

`当前评论审核项目已经有一些有限分支，而不是完全写死。比如命中上下文敏感表达会走 escalate；文本本身低风险，但举报和历史风险高，会走 shadow audit；如果缺上下文又命中模糊表达，置信度会下降并更倾向人工复核。严格说，这还不是 planner-based replanning，但已经有 bounded branching。`

引用：

- [agent.py](/Volumes/passport/简历/滴滴/src/commentops_agent_lab/agent.py#L276)
- [agent.py](/Volumes/passport/简历/滴滴/src/commentops_agent_lab/agent.py#L335)

### 如果继续追问

可以补：

`在审核业务里，我不会追求开放式重规划，因为那会牺牲一致性。更重要的是把关键分支条件定义清楚。`

---

## 6. 工具失败过吗？失败后系统怎么恢复？

### 面试官真正想考什么

这题几乎就是在考：

- 你有没有 harness
- 你是不是只会改 prompt 重跑

### 差回答

`我们现在工具比较稳定，还没怎么失败。`

这类回答通常非常危险，因为面试官会默认你没认真处理 failure mode。

### 好回答结构

`我会把工具失败视为系统设计的一部分，而不是偶发异常。高风险工具失败时不能继续假装成功，必须显式降级、重试或升级人工。更重要的是，失败后要沉淀成规则、校验或约束，而不是只改 prompt。`

### 当前评论审核项目怎么答

`当前 commentops 原型已经有 tool_trace，但还没有做完整 harness，这是我会明确承认的短板。现在能看到 load_context、policy retrieval、similar case retrieval、risk synthesis 和 route_review_queue 的 trace，但还没有 retry、fallback 或 safe degrade 机制。下一步我会优先补的是：context load fail 直接升级人工、policy retrieval fail 回退到保守规则、routing fail 落入默认安全队列。`

引用：

- [agent.py](/Volumes/passport/简历/滴滴/src/commentops_agent_lab/agent.py#L51)

### 如果继续追问

可以直接说：

`我现在不想把它包装成已经有完整 harness，我更愿意把这部分当成从原型走向工程化的明确升级项。`

---

## 7. 你为什么选这种检索策略，而不是别的？

### 面试官真正想考什么

这题在考：

- 你有没有做 trade-off
- 设计是不是你自己想明白的

### 差回答

`因为 GraphRAG / 向量库 / 动态路由比较先进。`

### 好回答结构

`我先按业务对象拆检索源，再决定检索方式。比如审核系统里的 policy retrieval、thread context retrieval、similar case retrieval 本质不是一类问题，所以我不会默认一个检索器打天下。`

### 当前评论审核项目怎么答

`评论审核场景里，我更看重“检索对象分层”而不是先上某种 fancy 检索框架。政策条款、上下文线程、历史相似裁决其实是三类完全不同的 evidence source。当前项目只是先用规则和样例池把接口雏形搭出来，后续才会把 policy retrieval 和 similar case retrieval 独立升级。`

### 如果继续追问

可以补：

`高约束场景里，我更担心 retrieval 混淆和不可审计，而不是先追求一个统一 fancy 检索框架。`

---

## 8. 你接了 MCP / 工具之后，安全治理怎么做？

### 面试官真正想考什么

这题在考：

- 你有没有生产风险意识
- 你是否理解 tools 是行为边界，不只是能力增强

### 差回答

`我把 MCP server 接上了，Agent 就可以直接用了。`

### 好回答结构

`我会把工具安全治理拆成最小权限、参数校验、调用审计、高危操作禁止或审批、以及失败回滚。真正的工程化分界线不在于“能不能接工具”，而在于“接上后是否可控”。`

### 当前评论审核项目怎么答

`当前评论审核原型的工具还在内置流程阶段，没有真正接外部 MCP server，所以我不会虚构这一层。但如果往工程化做，我会先定义高风险动作，比如删除、封禁、对外发送处罚结论，然后给它们加 policy gate、审批和审计。审核场景比一般 Agent 更需要最小权限和调用留痕。`

### 如果继续追问

你可以接：

`评论审核的高风险点不是“有没有工具”，而是“系统会不会在证据不足时直接执行高影响动作”。`

---

## 9. 你的评论审核 Agent 为什么不是一个 toy 分类器？

### 面试官真正想考什么

这题是在让你自证：

- 你有没有业务抽象能力
- 你是不是把审核理解成系统，而不是标签预测

### 差回答

`因为我用了 Agent 框架、RAG 和多步推理。`

### 好回答结构

`因为我把审核对象建成了 case，不是裸文本；输出也不是单一 label，而是 pass / reject / escalate，并且决策前后都围绕 policy grounding、risk signals、queue routing、reviewer handoff 和 failure review 组织。换句话说，我做的是 case processing system，而不是 prompt classification demo。`

### 当前评论审核项目怎么答

`当前项目最核心的区别是，它不是一句评论进来直接做分类，而是先组织 case，再做 policy hit、similar case、risk synthesis，最后决定是 pass、reject 还是 escalate，并输出 queue_routing、review_notes、recommended_actions。这些东西让它更接近内容治理 workflow，而不是文本分类器。`

引用：

- [agent.py](/Volumes/passport/简历/滴滴/src/commentops_agent_lab/agent.py#L40)
- [schemas.py](/Volumes/passport/简历/滴滴/src/commentops_agent_lab/schemas.py#L80)

### 如果继续追问

可以再上一个层次：

`真正让我把它和 toy 区分开的，不是多步调用本身，而是我开始把 reviewer、appeal、routing、eval、failure taxonomy 一起建模。`

---

## 10. 你这个审核项目最容易误杀的 case 是什么？你怎么控？

### 面试官真正想考什么

这题考的是：

- 你是否理解业务风险
- 你有没有误杀意识

### 差回答

`我们现在整体准确率还不错。`

### 好回答结构

`我最担心的是上下文敏感、反讽、引用、历史纠纷和申诉敏感样本。对这类 case，我宁可保守升级人工，也不会强行自动拒绝。控制手段包括 context requirement、low-confidence no-auto-action、appeal-sensitive routing 和 similar-case consistency checks。`

### 当前评论审核项目怎么答

`当前项目里最容易误杀的是 contextual abuse 这类模糊表达，比如“你可真行啊”。我现在的处理策略是命中这类条款后优先 escalate，而不是直接 reject；如果上下文本身不足，还会进一步降低自动化信心。这部分对应代码里 contextual-001 的 decision 是 escalate，不建议在上下文不足时自动拒绝。`

引用：

- [comment_policy_v1.yaml](/Volumes/passport/简历/滴滴/examples/commentops/policies/comment_policy_v1.yaml#L36)
- [agent.py](/Volumes/passport/简历/滴滴/src/commentops_agent_lab/agent.py#L276)

### 如果继续追问

你可以再补：

`我之后会把这类 case 单独做 appeal-sensitive eval slice，因为它们更接近真实误杀风险。`

---

## 11. reviewer override 和 appeal overturn 你怎么接进闭环？

### 面试官真正想考什么

这题考的是：

- 你是不是只会在线跑通
- 你有没有 offline optimization 意识

### 差回答

`目前先不考虑申诉，先把主流程跑起来。`

### 好回答结构

`reviewer override 和 appeal overturn 是最高价值的反馈源，因为它们直接暴露边界错、证据缺、规则歧义和一致性问题。我的做法是把它们沉淀到 failure taxonomy，再决定进入 policy tuning、threshold tuning、SFT、preference 或 regression set。`

### 当前评论审核项目怎么答

`当前项目已经在 schema 和风险信号里纳入了 prior_appeal_overturns，也有 failure review 和 preference data 的骨架，但 reviewer override、appeal outcome 还没有真正成为一等数据实体。这正是下一步最值得补的闭环能力。`

引用：

- [agent.py](/Volumes/passport/简历/滴滴/src/commentops_agent_lab/agent.py#L36)
- [training_data.py](/Volumes/passport/简历/滴滴/src/commentops_agent_lab/training_data.py#L133)

### 如果继续追问

你可以这样接：

`我不会把所有 overturn case 都直接丢去训练，先做 failure taxonomy，判断是 evidence、policy、threshold 还是 routing 问题，再决定流向。`

---

## 12. 如果现在让你把这个项目从原型升到更像工程项目，前三件事做什么？

### 面试官真正想考什么

这题在考：

- 你是否有升级路线
- 你是不是知道当前项目真实短板

### 差回答

`我会再接更多模型、更多工具、更多 Agent。`

### 好回答结构

`我会先补最短板、最接近真实风险的三件事，而不是先堆复杂度。第一，补 retrieval decision 和 evidence sufficiency。第二，补 baseline + slice eval + regression。第三，补 harness 和 reviewer / appeal loop。`

### 当前评论审核项目怎么答

推荐直接这样答：

`如果现在升级 commentops，我优先做三件事。第一，把 policy retrieval、context retrieval 和 similar-case retrieval 从“会查”升级成“知道什么时候查、什么时候够、什么时候该停”。第二，把 eval 从单一离线指标升级成 baseline 对照、high-risk recall、appeal-sensitive slice 和 policy version regression。第三，补 failure harness 和 reviewer / appeal 回流，让工具失败、证据不足和翻案样本都能进入下一轮优化。`

### 如果继续追问

可以补一句：

`我不会先追求 multi-agent，因为当前瓶颈还不在架构炫技，而在 retrieval、eval 和闭环。`

---

## 13. 快速自检：你现在的回答属于哪一档

### C 档：明显 toy

- 主要在讲框架名、模型名、API 名
- 很少讲 trade-off
- 说不出 baseline
- 说不出失败场景
- 说不出哪些该自动，哪些该升级人工

### B 档：有原型意识

- 能讲出 workflow
- 能讲出几个关键指标
- 能承认短板
- 但 baseline、memory、harness、闭环还不完整

### A 档：工程化候选

- 每个设计都能讲“为什么这样做”
- 说得出 baseline 和指标
- 有失败恢复和 guardrails
- 有 reviewer / appeal / regression 闭环
- 知道哪些复杂度暂时不该上

---

## 14. 最后给你一版面试收口句

如果面试官问到最后，让你总结“你这个 Agent 项目最值钱的地方是什么”，你可以用这句：

`我不把这个项目定义成“我接了几个模型和工具做了个 Agent”，而是把它定义成一个有状态、有证据、有边界、有评测、可持续迭代的业务系统。对评论审核场景来说，最重要的不是它敢不敢自动判，而是它知不知道什么时候该自动、什么时候该升级人工，以及错了以后怎样进入下一轮优化。`

---

## 建议搭配阅读

- [2026-04-05-agent-toy-symptoms-reanalysis.md](/Volumes/passport/简历/滴滴/docs/examples/2026-04-05-agent-toy-symptoms-reanalysis.md#L1)
- [2026-04-05-agent-engineering-vs-demo-and-commentops.md](/Volumes/passport/简历/滴滴/docs/examples/2026-04-05-agent-engineering-vs-demo-and-commentops.md#L1)
- [2026-04-05-commentops-agent-learning-handbook.md](/Volumes/passport/简历/滴滴/docs/examples/2026-04-05-commentops-agent-learning-handbook.md#L1)
- [2026-04-01-commentops-project-storyboard.md](/Volumes/passport/简历/滴滴/docs/examples/2026-04-01-commentops-project-storyboard.md#L1)

## △ Caveats

- 这份问答稿刻意偏“诚实可落地”的回答，不追求把项目包装得比实际更成熟。
- 如果面试官深挖具体线上数值，不要虚构指标，改用“当前已有评测骨架 + 下一步会如何补齐”的表达更稳。
