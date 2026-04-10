# Didi Freight Skill Dry Run

## Run Goal

Use `jd-resume-latex` on a Didi freight strategy role and check whether the chain is complete enough to:

1. understand the role
2. choose the right proof carrier
3. package one internship professionally
4. output LaTeX-ready resume edits without overclaiming

## Inputs Used

### JD input

- [examples/didi_2026_freight_algo_jd.md](/Volumes/passport/简历/滴滴/examples/didi_2026_freight_algo_jd.md)

### Local source pack

- [docs/examples/2026-04-10-didi-freight-knowledge-pack.md](/Volumes/passport/简历/滴滴/docs/examples/2026-04-10-didi-freight-knowledge-pack.md)
- [docs/examples/2026-04-10-ringconn-internship-packaging.md](/Volumes/passport/简历/滴滴/docs/examples/2026-04-10-ringconn-internship-packaging.md)
- [docs/examples/2026-04-10-ringconn-to-didi-freight-final-packaging.md](/Volumes/passport/简历/滴滴/docs/examples/2026-04-10-ringconn-to-didi-freight-final-packaging.md)
- [docs/resume_latex_reference.md](/Volumes/passport/简历/滴滴/docs/resume_latex_reference.md)

### External grounding

- [RingConn App Features](https://ringconn.com/pages/app-features)
- [Google OR-Tools](https://developers.google.com/optimization)
- [Microsoft EconML](https://www.pywhy.org/EconML/index.html)

## Step 1: JD Proof Map

### Must Prove

- 能处理动态、强约束的数据决策问题，而不是只会做静态表格分析
- 能把预测、分层、策略迭代和离线评估串成闭环
- 能理解策略指标和业务指标之间的映射关系
- 具备把技术能力迁移到货运交易市场问题的表达能力

### Can Bridge

- 智能指环里的多源时序建模，可桥接到货运场景的供需、响应和履约行为建模
- 用户分层与个性化分析，可桥接到司机 / 订单 / 区域分层策略
- 离线评估与版本对比，可桥接到补贴、曝光和策略方案对比

### Must Not Fake

- 已经做过货运交易核心策略
- 已经做过派单优化、补贴策略、因果推断或运筹优化
- 已经对货运业务有完整 owner 级经验

## Step 2: Chosen Proof Carrier

Chosen experience:

- `RingConn`

Reason:

- 它最适合证明动态数据建模、分层分析、版本对比和产品落地
- 它不能证明货运业务本身，所以必须被定位成“技术底座”，不是“货运主证据”
- 货运业务理解应由知识包、项目蓝图和后续 `FreightStrategyLab` 承接

## Step 3: Packaged Experience Output

### Dominant storyline

智能可穿戴场景中的多源时序数据建模、分层分析与离线评估闭环。

### One-sentence summary

面向智能指环产生的多源连续时序数据，参与状态识别、特征挖掘、用户分层与离线评估，形成“动态数据建模 -> 策略迭代 -> 产品落地”的实践闭环，并将这套能力迁移到货运场景中的供需预测、流量分发和策略评估问题。

### Final three bullets

- 围绕智能指环产生的多源连续时序数据，参与用户状态识别与特征建模，完成数据清洗、样本构造、特征提取与离线评估，积累对高噪声、个体差异显著场景的动态数据建模经验。
- 基于用户历史行为、设备指标与上下文特征进行分层分析与个性化策略迭代，支持结果排序、触发逻辑或能力输出优化，形成面向不同人群的分发式决策实践。
- 参与方案版本对比与核心指标分析，围绕准确性、覆盖率、一致性等指标评估不同策略效果，形成“预测 / 分层 -> 策略 -> 评估”的闭环意识，并推动数据能力向产品功能落地。

### Interview bridge sentence

这段经历给我的不是货运业务经验本身，而是动态数据建模、分层分析、策略迭代和离线评估的技术底座；我后面做的货运策略 demo，是把这套技术能力迁移到交易市场场景里。

### Forbidden claims

- 做过货运业务
- 做过货运调度
- 做过补贴策略
- 做过因果推断
- 做过运筹优化

## Step 4: LaTeX Sync Plan

Target source of truth:

- `/Volumes/passport/简历/latex-resume/content.tex`

Recommended sync point:

- Replace the current Shenzhen RingConn internship bullets under `\InternshipSection` with the freight-aligned three-bullet version above.

Leave unchanged for now:

- photo and header identity fields
- education and publication sections
- overall AltaCV layout and theme

Optional next sync:

- If the full freight storyline is confirmed, add one dedicated freight-oriented highlight block or thin entry file instead of forking all resume content.

## Chain Check

### What already closes

- JD input exists
- proof map exists
- source-backed packaging exists
- LaTeX source-of-truth path is explicit
- actual sync target file is explicit

### What is still manual

- final human confirmation before overwriting the current live resume content
- freight flagship project implementation, which should carry domain-specific proof

## Verdict

The chain is complete enough for a first usable skill:

- it can start from a JD
- it can decide what to prove
- it can package one internship with explicit truth boundaries
- it can tell exactly where the final LaTeX edits belong

The main remaining gap is not workflow logic. The remaining gap is richer role coverage and more source packs for other internships and target roles.
