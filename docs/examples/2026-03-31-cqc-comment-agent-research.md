# CQC 评论审核 Agent 研究与框架映射

## 目标

这份文档把三类信息合并起来：

1. 用户给出的 `大模型审核 Agent 专家（评论方向）-CQC` JD
2. 字节 / TikTok 与其他大厂公开披露的内容治理、审核、Trust & Safety 方法
3. Agent、审核、评测、后训练相关的一手技术资料

目标不是做“信息堆砌”，而是提炼出对项目框架真正有约束力的设计原则。

## 结论先行

这个 JD 更像一个 `评论治理工作流 + 大模型 Agent + 持续优化闭环` 岗，而不是单纯的文本分类岗。

最匹配的项目框架应该具备这些特征：

- 审核不是单一模型判定，而是 `自动检测 + policy grounding + 人工升级`
- 输出不是一个 label，而是 `action + policy evidence + rationale + escalation reason`
- 评测不是单纯 accuracy，而是同时看 `误杀、漏放、升级质量、时延、申诉/复核友好度`
- 训练闭环不是“凭空训练”，而是用 `争议样本、申诉样本、错判样本` 做 SFT / preference / reward
- 组织协作必须显式体现在设计里：Policy、Ops、Data、ML 都要有位置

## 一手信息源与设计含义

### 1. TikTok 官方治理信号：自动化不是终点，透明度和复核链路同样重要

#### 来源 A

- TikTok Newsroom, December 18, 2024:
  [Bringing even more transparency to how we protect our platform](https://newsroom.tiktok.com/en-US/bringing-even-more-transparency)

#### 关键信号

- TikTok 在 2024 年 7-9 月移除了超过 1.47 亿条违规视频，并且同期还移除了超过 13 亿条评论。
- 文中还提到自动化已经承担了超过 80% 的移除工作，同时 2024 年在 trust & safety 上投入超过 20 亿美元。
- 它们按季度发布 Community Guidelines Enforcement Report，并持续扩展指标维度和 machine-readable 数据。

#### 对项目框架的约束

- 我们的项目必须内置 `automation coverage` 相关指标，而不只是分类准确率。
- 评论是独立治理对象，不能把“视频治理思路”直接平移，评论需要自己的 case schema 和指标。
- 既然真实平台强调透明报告和多维指标，我们的框架也要有 `eval report + failure review` 产物。

### 2. TikTok 官方规则页：先自动检测，再人工追加审核，再给申诉入口

#### 来源 B

- TikTok Community Guidelines Enforcement:
  [Community Guidelines Enforcement](https://www.tiktok.com/community-guidelines/en/enforcement)

#### 关键信号

- 官方页面明确写到内容先经过 automated review。
- 对潜在违规内容，系统会自动移除，或者标记给 moderator 做 additional review。
- 如果内容变热、被举报，平台会追加 review。
- 平台还明确给出 notice 和 appeals 机制，并在 Safety Center 里展示申诉状态。

#### 对项目框架的约束

- 我们的 workflow 不能是“模型直接拍板”。
- 必须有 `pass / reject / escalate` 三态，而不是二分类。
- 必须记录 `为什么升级人工`，因为真实审核链路天然包含 additional review。
- 必须预留 `appeal replay` 或 `case review` 位置，因为申诉/复核是审核系统的真实组成部分。

### 3. TikTok 公开岗位：LLM 审核不是只做模型，而是做 evidence、policy logic 和 human review

#### 来源 C

- TikTok Safety Product 公开岗位：
  [Senior Product Manager (LLM-Powered Content Moderation)](https://lifeattiktok.com/search/7554140353420380424)

#### 关键信号

- 职责里明确写了 success metrics 要反映 `platform integrity outcomes`。
- 岗位要求用 AI-driven detection models 和 ML-powered moderation systems 去减少 misinformation、leakage、over-enforcement。
- 更关键的是，它明确写了要设计 `agentic workflows that retrieve supporting evidence`，并把 `model reasoning + policy logic + human review` 结合起来。

#### 对项目框架的约束

- 这直接说明我们的主项目不能只做 prompt 分类器。
- `policy retrieval` 和 `supporting evidence` 不是锦上添花，而是核心链路。
- `over-enforcement` 必须成为框架里的显式风险指标，也就是中文语境里常说的误杀。

### 4. Meta 公开方法：AI 扩规模，但最高风险决策仍由人兜底

#### 来源 D

- Meta, updated March 20, 2026:
  [Boosting Your Support and Safety on Meta's Apps With AI](https://about.fb.com/news/2026/03/boosting-your-support-and-safety-on-metas-apps-with-ai/)

#### 关键信号

- Meta 明确说 AI 不替代 human judgment，而是帮助在人海量内容上更一致地应用 judgment。
- 最高风险、最高影响的决策，比如 appeals 和 law enforcement 相关事项，仍由人承担关键角色。
- 同时它强调持续 testing、bias protection、consistency 和 accuracy。

#### 对项目框架的约束

- 我们的项目 framing 必须是 `safe automation boundaries`，不是“全自动审查”。
- `appeal`、`high-risk category`、`low confidence` 都应该触发人工升级。
- 评测必须包含 `一致性` 和 `风险边界`，而不是只看最终 action 是否相同。

### 5. Google / Jigsaw 方法：审核辅助工具不是人审替代品

#### 来源 E

- Google for Developers:
  [Get started with Perspective API](https://developers.google.com/codelabs/setup-perspective-api)

#### 关键信号

- 文档直接说明 Perspective API 的目标是让 moderation easier，而不是 completely replace human decision-makers。
- API 支持属性级分数，如 toxicity，并支持 `doNotStore` 这样的数据处理控制项。

#### 对项目框架的约束

- 我们可以把通用 moderation score 看成一个辅助信号层，而不是最终决策层。
- 框架设计上应支持 `base score -> policy grounding -> decision policy` 的分层，而不是单阈值粗暴处理。
- 数据处理和存储策略也要在后续版本里考虑。

### 6. OpenAI 官方文档：moderation score 要校准，eval 要多维

#### 来源 F

- OpenAI Moderation Guide:
  [Moderation](https://developers.openai.com/api/docs/guides/moderation)
- OpenAI Evals Guide:
  [Working with evals](https://developers.openai.com/api/docs/guides/evals)

#### 关键信号

- Moderation guide 明确说明 `category_scores` 依赖的自定义策略可能需要随着模型升级不断 recalibration。
- Evals guide 强调 robust evals 需要更多 criteria、不同 prompts 和不同 data sets，而不是只在一个小例子上通过。

#### 对项目框架的约束

- 审核 Agent 的阈值不能写死成永远不变的神秘常数。
- 必须有独立的 `offline eval` 层，而不是把判断质量埋在 demo 里。
- 评测数据集要有分层：明确违规、明确安全、上下文敏感、争议样本。

### 7. TRL / GRPO 官方文档：后训练更适合放在第二阶段，围绕争议样本和奖励设计展开

#### 来源 G

- Hugging Face TRL:
  [GRPO Trainer](https://huggingface.co/docs/trl/grpo_trainer)

#### 关键信号

- 文档把 GRPO 描述成 online learning：模型用自身生成的数据迭代改进。
- 奖励可以来自 reward model 或 reward function，而且优势是按同题多答案的相对比较来构建。

#### 对项目框架的约束

- 对评论审核来说，更自然的第二阶段不是盲目上 PPO，而是先把 `争议 case / 申诉 overturn case / reviewer disagreement case` 整理成 preference 或 group reward 数据。
- 框架必须提前把 `decision trace`、`policy evidence`、`reviewer override` 记录下来，否则后续没有训练闭环。

### 8. ReAct 论文：Agent 应该把 reasoning 和 action 绑定到证据获取上

#### 来源 H

- ReAct:
  [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)

#### 对项目框架的约束

- 在审核场景里，Agent 的价值不是长篇思维链，而是 `根据问题去拉证据 -> 对照规则 -> 做保守决策`。
- 所以第一版不需要复杂 multi-agent，更适合单 Agent + tool retrieval + escalation policy。

## 由研究反推的框架原则

### 原则 1：先做 workflow，不先做 end-to-end 大模型替代

第一版要先把真实审核链路表达清楚：

- comment input
- thread context
- policy retrieval
- evidence extraction
- decision policy
- human escalation
- audit trace

### 原则 2：先做审核边界，再做自动化率

最强的面试表达不是“自动化率很高”，而是：

- 高风险不乱放
- 低风险不乱杀
- 不确定时稳定升级人工
- 所有关键决策可复核、可申诉、可迭代

### 原则 3：先做评测产物，再做 fancy demo

比一个漂亮前端更重要的是这些文件：

- `baseline_eval_report.json`
- `sft_samples.jsonl`
- `preference_pairs.jsonl`
- 后续可加 `failure_review.json`

### 原则 4：训练闭环应该长在审核 case 上，而不是凭空造任务

真正能支撑这个 JD 的训练数据应来自：

- reviewer disagreement
- appeal overturn
- low-confidence escalation
- policy version change regression

## 已落地到当前代码框架的部分

当前仓库已新增 `commentops_agent_lab` 骨架，先完成了这些模块：

- `schemas.py`：评论审核 case、policy、decision、trace 的结构化契约
- `agent.py`：最小版单 Agent 工作流
- `eval.py`：action accuracy、policy grounding rate、escalation precision
- `training_data.py`：SFT / preference 样本导出
- `app.py` / `cli.py`：API 与 CLI 入口
- `examples/commentops/`：示例 policy 和审核 case

## 下一步最值得做的三件事

1. 从规则匹配升级到 `policy retrieval + similar case retrieval`
2. 加入 `reviewer override / appeal outcome / policy version` 数据结构
3. 补齐 `failure_review.json` 和更像真实业务的评测集

## 不建议现在就做的事

- 不建议一开始就做多智能体
- 不建议一开始就追求复杂 UI
- 不建议一开始就做大规模训练
- 不建议一开始就把系统定位成“全自动审查”

最稳的路线仍然是：

`可解释的审核 workflow -> 可复核的 eval -> 可回灌的数据闭环 -> 再往 SFT / preference / reward 走`
