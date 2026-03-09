# 主项目蓝图：DriverOps Agent Lab

- 目标公司：didi
- 目标岗位：agent-algorithm
- 项目摘要：面向司机经营问题的垂域 Agent 与后训练实验平台，覆盖意图识别、ReAct 工具调用、记忆、推荐、SFT 与偏好优化闭环。

## 为什么匹配这个 JD

- 覆盖 `强化学习与奖励设计`：项目中体现 需要展示 reward 设计与失败案例；需要展示偏好数据或可验证奖励数据构造。
- 覆盖 `Agent 系统设计`：项目中体现 需要有端到端 Agent 主链路；需要展示工具调用与记忆模块。
- 覆盖 `后训练与对齐`：项目中体现 需要展示训练数据设计；需要展示 SFT 或偏好优化实验。
- 覆盖 `前沿推理方法`：项目中体现 需要能解释为什么不用过度复杂的多智能体设计；需要体现方法选型依据。
- 覆盖 `网约车供需策略理解`：项目中体现 需要项目场景贴近司机经营与供需问题；需要解释业务指标与模型指标关系。

## 技术栈

- Python + FastAPI 服务层
- PyTorch + TRL 训练实验
- vLLM 或 SGLang 推理服务
- SQLite / PostgreSQL 业务数据
- 向量检索用于政策与规则知识库
- Pydantic 约束工具输入输出 schema

## 核心模块

- Intent Router：将问题分流到 FAQ / 策略建议 / 任务执行 / 解释说明
- Planner / ReAct Loop：多步工具调用与失败恢复
- Tool Layer：司机画像、行程统计、活动中心、规则知识库、推荐引擎
- Memory Layer：短期会话记忆 + 长期司机画像
- Post-training Pipeline：SFT 数据、偏好数据、GRPO/DPO 小实验
- Offline Evaluator：任务完成率、工具调用正确率、解释质量与时延

## 里程碑

- 第 1 周：搭服务骨架、定义工具 schema、准备司机场景模拟数据
- 第 2 周：实现意图识别与 ReAct 主链路，接入 4-5 个核心工具
- 第 3 周：加入记忆层与推荐解释，补异常恢复与 fallback
- 第 4 周：构造多轮 SFT 样本，完成一版小模型或 LoRA 训练
- 第 5 周：加入偏好数据或 grouped reward，完成 DPO/GRPO 小实验
- 第 6 周：固化离线评测、补充架构图、形成简历与面试表达

## 建议评测指标

- Intent accuracy
- Tool call accuracy
- Task success rate
- Explanation coverage
- Response latency
- Driver-side business alignment notes

## Demo 场景

- 收入解释：解释今日收入结构与影响因素
- 活动推荐：结合司机画像与时段推荐活动参与策略
- 热区建议：基于时空模式给出接单建议与风险说明
- 规则答疑：用检索 + tool grounding 解释司机规则和平台政策

## 对应业务问题

- 结合 `滴滴26届春招-算法工程师（供需策略）`，把司机收入解释、活动推荐、热区建议、规则答疑做成统一入口。
- 重点展示模型能力如何影响司机体验、供需平衡和平台效率。
