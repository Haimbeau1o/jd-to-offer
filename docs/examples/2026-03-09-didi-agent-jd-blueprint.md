# 滴滴 2026 届算法工程师（供需策略）JD 示例蓝图

## 一句话判断

这个 JD 的核心并不是“只会调包做应用”，而是要你同时证明四件事：

1. 你能设计并落地 LLM Agent 系统
2. 你理解后训练，尤其是 SFT、DPO、PPO、GRPO 这条线
3. 你能把模型能力和真实业务指标绑定起来
4. 你具备工程化与策略业务理解，而不只是论文理解

如果你时间有限，最优策略不是同时做很多小项目，而是做一个“能跑、能讲、能扩展、能对齐 JD 关键词”的主项目，然后围绕它补齐知识图谱、训练流程、评测闭环与业务映射。

## JD 能力拆解

### A. Agent 系统设计与应用

**对应 JD 原文：** 意图识别、复杂任务拆解、多步推理、ReAct 工具调用、长短期记忆、智能推荐。

**你需要会讲的知识点：**

- 用户请求分类：FAQ、任务执行、策略建议、查询解释
- 任务规划：单轮决策、多步规划、失败重试、观察-行动循环
- 工具使用：函数签名设计、工具选择、参数填充、错误恢复
- 记忆设计：短期会话状态、长期用户画像、偏好与历史行为
- 推荐闭环：把规则、画像、上下文、目标函数组合成行动建议
- Agent 评测：工具调用成功率、任务完成率、步骤冗余率、延迟、用户满意度

**面试里常见追问：**

- 为什么不是纯 RAG，而要用 Agent？
- 什么时候需要 planner，什么时候直接 tool router 就够？
- 你怎么避免 Agent 无限循环或错误调用工具？
- 长记忆怎么避免脏数据和过期记忆污染？

### B. 大模型后训练与垂域增强

**对应 JD 原文：** SFT、RL、上下文遵循、ReAct 工具调用、领域问答。

**你需要会讲的知识点：**

- Pre-train / CPT / SFT / Preference Optimization / RL 的边界
- 指令数据构造：单轮、多轮、工具调用、规划链路、拒答样本
- Loss 与目标：next-token、pairwise preference、group relative reward
- 训练前后评测：格式遵循、工具调用正确率、推理链质量、领域问答命中率
- 数据分布：通用数据、垂域数据、合成数据、难例回灌

**面试里常见追问：**

- 为什么先 SFT 再 RL，而不是直接 RL？
- DPO 与 PPO 的主要差异是什么？
- GRPO 适合什么类型的问题？
- 你如何定义“上下文遵循”并可量化地优化它？

### C. 数据反馈、奖励函数与强化学习

**对应 JD 原文：** 高质量训练数据、奖励函数、PPO/GRPO、强化学习迭代路径。

**你需要会讲的知识点：**

- 数据闭环：日志采集、失败归因、样本清洗、样本去重、难例抽样
- 奖励建模：可验证奖励、规则奖励、模型奖励、混合奖励
- PPO 基本结构：policy、reference、advantage、clip objective
- DPO 基本结构：无显式 reward model 的 preference learning
- GRPO 基本结构：组内相对比较、适合可验证或排序型任务
- 离线验证：A/B 前的离线指标、reward hacking 检测、长度偏差控制

**面试里常见追问：**

- 你如何防止 reward hacking？
- 奖励函数里如何平衡工具正确率与回答自然度？
- 如果线上反馈延迟很长，怎么做训练迭代？

### D. 模型训练/推理基础设施

**对应 JD 原文：** PyTorch、Megatron-LM、DeepSpeed、vLLM、SGLang。

**你需要会讲的知识点：**

- PyTorch 训练与推理基础、autograd、mixed precision
- 分布式训练的概念：DP、TP、PP、ZeRO/FSDP
- 推理服务：吞吐、时延、KV Cache、连续批处理、前缀缓存
- 线上部署：OpenAI-compatible API、服务观测、超时与重试、限流
- 训练与服务接口衔接：数据格式、tokenizer、一致性评测

### E. 前沿技术与研究视野

**对应 JD 原文：** 多智能体协作、Long Context、CoT。

**你需要会讲的知识点：**

- CoT 的收益与风险：性能提升 vs 冗长推理和泄漏风险
- ReAct 相比纯 CoT 的优势：把推理与行动耦合
- Multi-Agent 适用边界：角色分工明确时有效，简单任务会过度设计
- Long Context 的工程代价：显存、延迟、检索替代方案、上下文污染

### F. 业务理解：网约车供需策略

这个岗位虽然写的是 Agent 与 LLM，但落地场景是供需策略，所以你必须会把模型能力翻译成业务问题。

**必须建立的业务视角：**

- 司机侧问题不只是问答，还包括收入解释、活动推荐、热区建议、规则说明、申诉辅助
- 核心业务指标可能包括：完单率、在线时长、接驾时长、司机活跃、补贴效率、供需平衡、订单响应率
- Agent 价值不是“回答更像人”，而是“更快定位问题、减少人工介入、提升司机经营体验和平台效率”

## 建议的知识体系学习顺序

### 第一层：必须先补齐的基础

1. Python 工程能力
2. PyTorch 训练与推理基础
3. Transformer、tokenizer、attention、推理成本
4. Agent 基础工作流：intent → plan → act → observe → memory → evaluate
5. SFT / DPO / PPO / GRPO 的基本差异
6. 模型服务与工具调用闭环

### 第二层：强相关进阶

1. 训练数据构造与样本质检
2. Reward 设计与离线评测
3. vLLM / SGLang 服务能力
4. Long Context 与 memory 的边界
5. 供需策略与司机经营指标

### 第三层：面试加分项

1. Multi-Agent 协作框架
2. 合成数据生成与回灌机制
3. 训练过程可观测性
4. 失败 case 归因与 ablation

## 最新且高质量的学习资源

下面优先给官方文档与原始论文。对这个 JD，二手博客价值不高，面试官更看你是否能回到“原方法、原接口、原约束”。

### 训练与工程基础

- [PyTorch Documentation](https://docs.pytorch.org/docs/stable/index.html)：补齐训练、自动求导、AMP、分布式概念
- [Megatron-LM](https://github.com/NVIDIA/Megatron-LM)：看大模型训练并行化与训练实践
- [DeepSpeed](https://www.deepspeed.ai/)：重点看 ZeRO 和大模型训练工程实践
- [TRL Documentation](https://huggingface.co/docs/trl/index)：看 `SFTTrainer`、`DPOTrainer`、`GRPOTrainer` 等训练入口

### Agent 与推理方法

- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)：多智能体的官方框架文档，可作为前沿扩展阅读

### 对齐与强化学习

- [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)
- [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290)
- [DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models](https://arxiv.org/abs/2402.03300)

### 推理服务与工具调用承载层

- [vLLM Documentation](https://docs.vllm.ai/en/latest/)
- [SGLang Documentation](https://docs.sglang.ai/)

### 业务与策略建模

- [Large-Scale Order Dispatch in On-Demand Ride-Hailing Platforms: A Learning and Planning Approach](https://arxiv.org/abs/2202.05118)

> 说明：`GRPO`、`RLVR` 这条实践路线，我这里主要依据 `DeepSeekMath` 与当前开源 trainer 的支持情况做归纳。严格说，`RLVR` 更像一类实践范式而不是单篇论文名词，所以这里是结合一手论文与训练框架文档后的推断。

## 最优主项目建议

### 项目名称

`DriverOps Agent Lab`：面向司机经营问题的智能助手与后训练实验平台

### 为什么它最匹配这个 JD

这个项目能一口气覆盖 JD 的绝大多数关键词：

- Agent 设计：意图识别、任务拆解、ReAct、工具调用、记忆、推荐
- 后训练：SFT + DPO/GRPO 小规模实验
- 数据反馈：失败样本回灌、奖励函数、离线评测
- 工程化：FastAPI + 推理服务 + 评测脚本 + 日志闭环
- 业务理解：司机场景、供需策略、收入解释、活动推荐

### MVP 功能范围

第一版不要贪大，做四个真实可演示能力：

1. **司机问题意图识别**
   - 收入解释
   - 活动查询
   - 热区建议
   - 规则答疑

2. **ReAct 工具调用链**
   - `get_driver_profile`
   - `get_trip_stats`
   - `search_policy_kb`
   - `get_campaigns`
   - `recommend_strategy`

3. **短期/长期记忆**
   - 短期：当前对话、最近查询、当前城市与时段
   - 长期：司机等级、偏好、历史完单、活动参与习惯

4. **智能推荐输出**
   - 给出行为建议
   - 解释建议依据
   - 说明收益与风险

### 技术栈建议

- `Python` + `FastAPI`：服务层
- `PyTorch`：训练和实验
- `vLLM` 或 `SGLang`：本地/远程模型服务
- `SQLite` 或 `PostgreSQL`：结构化业务数据
- `Qdrant` 或轻量向量库：政策/规则知识检索
- `TRL`：SFT / DPO / GRPO 实验
- `Pydantic`：工具 schema 和输出约束
- `Streamlit` 或简单前端：演示页面

### 推荐系统架构

```text
User Query
  ↓
Intent Router
  ↓
Planner / ReAct Loop
  ├─ Tool: Driver Profile
  ├─ Tool: Trip Stats
  ├─ Tool: Policy KB
  ├─ Tool: Campaign Center
  └─ Tool: Recommendation Engine
  ↓
Memory Writer
  ↓
Structured Final Answer
  ↓
Offline Evaluator + Data Flywheel
```

### 训练与数据闭环

你不需要真的从零训一个超大模型，但要把“后训练路径”做完整并可讲清楚：

1. 先用模板和规则生成一批司机场景多轮对话
2. 加入正确工具调用轨迹与错误轨迹
3. 做一版 `SFT`，目标是学会格式、上下文遵循、工具调用框架
4. 做一版 `DPO` 或 `GRPO` 小实验，目标是优化：
   - 工具调用正确率
   - 任务完成率
   - 推荐解释质量
5. 用离线数据评测：
   - `intent accuracy`
   - `tool call accuracy`
   - `task success rate`
   - `citation / evidence coverage`
   - `response latency`

### 你需要准备的可讲结果

- 1 个端到端 demo
- 1 套系统架构图
- 1 套数据生成与训练流程图
- 1 组离线评测结果表
- 3 个失败案例与优化过程
- 3 条简历 bullet

## 6 周执行路线

### 第 1 周：基础与脚手架

- 搭服务骨架
- 定义工具 schema
- 准备司机场景模拟数据
- 跑通单轮问答与知识检索

### 第 2 周：Agent 主链路

- 实现意图识别
- 实现 ReAct 循环
- 接入 4 到 5 个工具
- 打通 structured output

### 第 3 周：记忆与推荐

- 加短期记忆
- 加长期画像
- 做推荐策略解释
- 增加异常恢复与 fallback

### 第 4 周：SFT 数据与训练

- 产出多轮样本
- 训练小模型或 LoRA 版本
- 对比训练前后工具调用表现

### 第 5 周：DPO / GRPO 小实验

- 构造 preference 或 grouped reward 数据
- 跑通一版对齐训练
- 记录 reward 设计与失败案例

### 第 6 周：评测与表达

- 固化评测脚本
- 补架构图与项目说明
- 抽取简历 bullet
- 准备 10 个高频面试问答

## 简历与面试表达方向

### 简历 bullet 示例

- 设计并实现面向司机经营问题的 `LLM Agent`，覆盖意图识别、ReAct 工具调用、长短期记忆与策略推荐，完成端到端可演示闭环
- 基于合成多轮数据与业务规则构建后训练样本，完成 `SFT + DPO/GRPO` 小规模实验，提升工具调用正确率与任务完成率
- 建立离线评测体系，围绕意图识别、工具调用、推荐解释质量与延迟等指标形成数据回灌闭环

### 面试最关键的一句话

“我不是只做了一个聊天机器人，而是做了一个围绕司机经营问题的垂域 Agent 系统，并把数据构造、后训练、评测与业务目标串成了闭环。”

## 对你当前行动的建议

如果你的目标是“尽快投递并能讲得像样”，推荐优先级如下：

1. 先做这个主项目的可运行 MVP
2. 同时补齐 `SFT / DPO / PPO / GRPO` 的知识骨架
3. 再补 vLLM / SGLang 与分布式训练的工程理解
4. 最后把多智能体、长上下文作为加分项，不要一开始就陷进去

换句话说，你现在最缺的不是“更多概念”，而是一个能把概念、工程、业务和结果串起来的主线项目。
