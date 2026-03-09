# 最新优质资源包

- 资源原则：优先官方文档、一手论文、官方项目仓库
- 校验方式：以当前可访问的官方入口为主，避免依赖二手博客

## 强化学习与奖励设计

- [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)｜primary_paper｜PPO 是理解 RLHF/RLAIF 训练路径的基础算法论文。｜verified 2026-03-09

## Agent 系统设计

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)｜primary_paper｜ReAct 是工具调用型 Agent 的核心一手论文，和 JD 高度贴合。｜verified 2026-03-09

## 后训练与对齐

- [TRL Documentation](https://huggingface.co/docs/trl/en/index)｜official_docs｜当前官方文档已同时列出 SFTTrainer、DPOTrainer、GRPOTrainer 和 PPOTrainer，适合岗位中的后训练主线。｜verified 2026-03-09｜source huggingface.co/docs/trl/en/index
  - evidence: 首页离线方法含 SFTTrainer 与 DPOTrainer，在线方法含 GRPOTrainer 与 PPOTrainer。
- [DeepSeekMath](https://arxiv.org/abs/2402.03300)｜primary_paper｜开源社区常用它来理解 GRPO 的实践路线与可验证奖励训练思路。｜verified 2026-03-09
- [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290)｜primary_paper｜DPO 是当前面试里高频被问的偏好优化方法，需要直接读原论文。｜verified 2026-03-09

## 前沿推理方法

- [AgentChat — AutoGen](https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/index.html)｜official_docs｜官方多智能体入口，覆盖 AgentChat、Swarm、GraphFlow、Memory 等模式，适合补岗位中的多智能体协作与记忆设计。｜verified 2026-03-09｜source microsoft.github.io/autogen/dev
  - evidence: 页面列出了 AgentChat、Swarm、GraphFlow 和 Memory 等模块。
- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)｜primary_paper｜CoT 是岗位里多步推理与 reasoning 方法的经典基线论文。｜verified 2026-03-09

## 网约车供需策略理解

- [Large-Scale Order Dispatch in On-Demand Ride-Sharing Platforms: A Learning and Planning Approach](https://www.kdd.org/kdd2018/accepted-papers/view/large-scale-order-dispatch-in-on-demand-ride-sharing-platforms-a-learning-a)｜primary_paper｜滴滴业务背景下的经典派单论文，有助于把 Agent 能力翻译回供需策略与业务价值。｜verified 2026-03-09
- [Supply-Demand-aware Deep Reinforcement Learning for Dynamic Fleet Management](https://dl.acm.org/doi/10.1145/3467979)｜primary_paper｜供需感知的 RL 论文，适合补齐司机/运力调度场景与强化学习的连接。｜verified 2026-03-09
