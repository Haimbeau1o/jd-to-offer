# 滴滴货运岗知识包

## 这份知识包解决什么问题

你不是在准备一个泛算法岗，而是在准备一个 **货运交易 / 供需 / 策略** 方向的算法岗。

所以知识准备必须回答 4 件事：

1. 货运平台到底在优化什么
2. 为什么这不是普通的分类 / 回归题
3. 调度、补贴、流量分发、因果评估之间是什么关系
4. LLM 在这里应该放在哪一层才合理

## 一、业务本质先吃透

### 1. 业务对象

你至少要能熟练说出这些对象：

- 货主 / 发单方
- 订单
- 司机 / 车主
- 车辆类型
- 区域
- 时间窗
- 运价 / 补贴 / 司机收入
- 曝光 / 分发 / 派单结果

### 2. 平台真正要优化的不是单一指标

面试里不要只说“提升完单率”。

更完整的指标板应该是：

- 订单匹配率
- 司机响应 / 接单率
- 履约完成率
- 时效达成率
- 空驶距离或接货距离 proxy
- 补贴消耗
- 补贴 ROI
- 流量曝光集中度
- 区域稳定性

### 3. 业务张力

最值得讲的不是“模型是什么”，而是“目标之间为什么冲突”：

- 提升短期完单率，可能会伤害长期供给健康
- 更多补贴可能提升成交，但不一定带来增量价值
- 局部最优派单，不一定等于全局效率最优
- 把曝光集中给少数高概率司机，可能会伤害平台公平性和长期活跃

你只要把这些张力说清楚，面试官就会觉得你不是在背模型。

## 二、算法层到底怎么拆

### 1. 预测层

先预测，再决策。

最常见的预测任务包括：

- 某区域 / 时段的需求量预测
- 某区域 / 时段的可用供给预测
- 某司机对某类订单的响应概率预测
- 订单履约成功概率预测

这里你可以把 `RingConn` 经验迁移进来，因为底层都属于动态数据建模。

### 2. 调度 / 匹配层

这层解决的是：

- 订单给谁看
- 谁应该优先收到什么单
- 有时间窗、距离、车型约束时怎么分配

你不一定要把它做成复杂运筹求解器，但至少要懂：

- assignment / matching 的基本直觉
- score-based dispatch 和 hard constraints 的区别
- 为什么会有全局最优与局部最优冲突

### 3. 补贴 / 定价 / 干预层

这里面试官最想看的是你是否理解“相关性”和“增量价值”的区别。

正确的思路是：

- 补贴不是给最可能完成的人
- 补贴应该优先给“因为补贴才增加完成概率”的人或区域
- 所以策略上要考虑 uplift / treatment effect

你不一定要把因果推导讲成论文，但至少要会说：

- correlation 不等于 incrementality
- 需要 treatment / control 视角
- 需要离线反事实或准实验思维

### 4. 流量分发层

流量分发不只是“排序”。

它同时包含：

- order exposure
- driver opportunity distribution
- 平台公平性
- 不同目标之间的打分权衡

最值得准备的是：

- 多目标打分
- 曝光集中度
- fairness proxy
- 短期效率和长期供给的关系

## 三、LLM 应该放哪里

这是个很容易讲偏的地方。

这类岗位里，LLM 最合理的位置是：

- 策略解释层
- 运营 / 策略 copilot
- 决策复盘报告生成
- 复杂指标和策略结果的自然语言总结

最不应该讲成的是：

- LLM 直接替代派单核心逻辑
- LLM 直接替代补贴优化
- LLM 直接做关键约束求解

一句话说：

> LLM 负责解释、分析和协同，核心交易决策仍然要由显式特征、规则、模型和优化逻辑承担。

## 四、面试准备顺序

### Must Know

- 供需预测基本思路
- matching / assignment 基本直觉
- uplift / treatment effect 为什么重要
- 离线评估和 KPI 板怎么设计
- 流量分发中的多目标权衡

### Should Know

- OR-Tools 如何表达 assignment / routing
- `econml` / `causalml` 解决什么问题
- score-based policy 和 optimization-based policy 的边界
- counterfactual evaluation 为什么难
- fairness / concentration 为什么和长期供给有关

### Stretch

- offline RL / contextual bandit 在补贴 / 分发中的适用边界
- 多智能体或分层决策在调度中的新论文
- LLM agent 在策略分析台中的落地方式

## 五、你要会说的 6 个高频句子

### 1. 为什么这是货运策略岗，不是普通 ML 岗

因为它的核心不是单点预测准确率，而是把预测、派单、补贴、流量分发和业务指标放进一个交易市场闭环里做联合优化。

### 2. 为什么补贴问题要讲因果

因为平台要的不是“高相关的完成用户”，而是“因为补贴才额外完成的增量订单”，所以相关性不够，必须考虑增量效果。

### 3. 为什么调度不是简单排序

因为调度会同时受到距离、时间窗、车型、区域压力和全局资源约束影响，所以单个 pair 的最优不等于市场整体最优。

### 4. 为什么流量分发不能只追短期成交

因为过度集中曝光会影响长期供给健康和公平性，短期效率和长期生态之间要做权衡。

### 5. 为什么 `RingConn` 能迁移一部分能力

因为两边底层都涉及动态、多噪声、个体差异明显的数据决策问题，但业务核心不是同一个领域，所以只能迁移技术底座，不能等价替换业务经验。

### 6. 为什么 LLM 不是核心策略引擎

因为货运交易决策需要显式约束、可控优化和稳定评估，LLM 更适合做解释、分析和协作，不适合直接替代核心调度和补贴逻辑。

## 六、推荐一手资料

- [Didi Global 2023 20-F](https://www.sec.gov/Archives/edgar/data/1764757/000110465924053916/tm2329116-7_20f.htm)
说明：用于理解平台业务 framing 和货运平台在公司业务体系中的位置。

- [交通运输行业发展统计公报（2024）](https://www.gov.cn/lianbo/bumen/202506/content_7028627.htm)
说明：用于建立“公路货运是大规模真实市场”的业务背景。

- [Google OR-Tools: Assignment](https://developers.google.com/optimization/assignment/assignment_example)
说明：补齐 assignment / matching 的实现直觉。

- [Google OR-Tools: Vehicle Routing Problem](https://developers.google.com/optimization/routing/vrp)
说明：补齐 routing / time-window 这类约束优化的工程入口。

- [`econml`](https://github.com/py-why/econml)
说明：看 heterogeneous treatment effect / CATE 这条线的主流工具入口。

- [`causalml`](https://github.com/uber/causalml)
说明：看 uplift / causal inference 在工业场景里的工程化工具。

- [Didi KDD 2018 dispatch paper](https://www.kdd.org/kdd2018/accepted-papers/view/large-scale-order-dispatch-in-on-demand-ride-sharing-platforms-a-learning-a)
说明：虽然是网约车，但对平台派单思路非常有帮助。

- [Large-Scale Order Dispatch in On-Demand Ride-Hailing Platforms: A Learning and Planning Approach](https://arxiv.org/abs/2202.05118)
说明：适合你补“学习 + 规划”结合的 dispatch 思路。

- [Uber: Causal Inference in Marketplace Machine Learning](https://www.uber.com/en-GB/blog/causal-inference-at-uber/)
说明：适合建立“平台增量价值”而不是“相关性预测”的思维。

## 七、一个重要 caveat

公开可获得的 **滴滴货运** 算法细节非常有限。

所以你后续做准备时，应该把资料分成两层：

- 货运业务 framing：尽量用官方或行业材料
- 调度 / 补贴 / 因果 / 分发方法：大量借鉴同类 marketplace、网约车和物流优化的一手论文与官方文档

这不是偷换概念，而是公开资料条件下最合理的准备方式。
