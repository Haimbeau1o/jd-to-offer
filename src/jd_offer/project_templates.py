from __future__ import annotations

from collections import OrderedDict
from pathlib import Path

import yaml

from jd_offer.schemas import CompetencyMap, JDDocument, ProjectTemplate, ResourceEntry


def load_project_templates(path: Path) -> list[ProjectTemplate]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return [ProjectTemplate.model_validate(item) for item in payload.get("templates", [])]


def load_resource_registry(path: Path) -> list[ResourceEntry]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return [ResourceEntry.model_validate(item) for item in payload.get("resources", [])]


def select_project_template(competencies: CompetencyMap, path: Path) -> ProjectTemplate:
    templates = load_project_templates(path)
    top_names = set(competencies.top_names)

    ranked = []
    for template in templates:
        overlap = len(top_names.intersection(template.use_when))
        ranked.append((overlap, template))

    ranked.sort(key=lambda item: (-item[0], item[1].id))
    return ranked[0][1]


def select_resources(competencies: CompetencyMap, resources: Path | list[ResourceEntry]) -> list[ResourceEntry]:
    resource_list = load_resource_registry(resources) if isinstance(resources, Path) else list(resources)
    desired_tags = set()
    for competency in competencies.items[:5]:
        desired_tags.add(competency.name)
        desired_tags.update(competency.resource_tags)

    picked: list[ResourceEntry] = []
    for resource in resource_list:
        if desired_tags.intersection(resource.tags):
            picked.append(resource)

    seen: set[str] = set()
    unique: list[ResourceEntry] = []
    for resource in sorted(picked, key=lambda item: (item.priority, item.title.lower())):
        if resource.id in seen:
            continue
        seen.add(resource.id)
        unique.append(resource)
    return unique


def build_jd_decomposition(jd: JDDocument, competencies: CompetencyMap) -> str:
    top = competencies.items[:6]
    hidden_expectations = []
    top_names = set(competencies.top_names)
    if "agent_system_design" in top_names:
        hidden_expectations.append("需要展示完整 Agent 链路能力，而不是只做单点问答。")
    if "post_training_alignment" in top_names or "rl_and_reward_design" in top_names:
        hidden_expectations.append("需要把后训练、奖励设计和可量化指标串成闭环。")
    if "ride_hailing_supply_demand" in top_names:
        hidden_expectations.append("需要把模型指标翻译成司机经营与供需策略指标。")
    if "training_inference_stack" in top_names:
        hidden_expectations.append("需要同时理解训练和推理承载层，而不只是算法名词。")

    lines = [
        f"# {jd.title} JD 拆解",
        "",
        "## 结构化概览",
        "",
        f"- 岗位职责数：{len(jd.responsibilities)}",
        f"- 任职要求数：{len(jd.requirements)}",
        f"- 加分项数：{len(jd.bonus_items)}",
        "",
        "## 关键能力优先级",
        "",
    ]

    for index, item in enumerate(top, start=1):
        keywords = "、".join(item.matched_keywords[:6])
        lines.append(f"{index}. `{item.display_name}`（{item.name}）- score={item.score}；命中关键词：{keywords}")

    lines.extend([
        "",
        "## 隐含期待",
        "",
    ])
    for expectation in hidden_expectations or ["需要把研究理解、工程落地、业务价值三者统一表达。"]:
        lines.append(f"- {expectation}")

    lines.extend([
        "",
        "## 原始条目摘要",
        "",
        "### 岗位职责",
        "",
    ])
    lines.extend([f"- {item}" for item in jd.responsibilities])
    lines.extend(["", "### 任职要求", ""])
    lines.extend([f"- {item}" for item in jd.requirements])
    lines.extend(["", "### 加分项", ""])
    lines.extend([f"- {item}" for item in jd.bonus_items])
    return "\n".join(lines).strip() + "\n"


def build_knowledge_system(competencies: CompetencyMap) -> str:
    lines = [
        "# 配套知识体系",
        "",
        "## 学习顺序",
        "",
        "1. 先补通用基础：Python / PyTorch / Transformer / 服务化",
        "2. 再补岗位核心：Agent、后训练、奖励设计、评测",
        "3. 最后补业务映射：网约车供需、司机经营、策略指标",
        "",
    ]

    for item in competencies.items:
        lines.append(f"## {item.display_name}")
        lines.append("")
        lines.append(f"- 优先级得分：{item.score}")
        lines.append(f"- 命中关键词：{'、'.join(item.matched_keywords)}")
        lines.append("- 必学子主题：")
        for subtopic in item.foundational_subtopics:
            lines.append(f"  - {subtopic}")
        if item.project_signals:
            lines.append("- 项目要体现：")
            for signal in item.project_signals:
                lines.append(f"  - {signal}")
        if item.interview_signals:
            lines.append("- 面试要会讲：")
            for signal in item.interview_signals:
                lines.append(f"  - {signal}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_resource_pack(competencies: CompetencyMap, resources: list[ResourceEntry]) -> str:
    grouped: OrderedDict[str, list[ResourceEntry]] = OrderedDict()
    for competency in competencies.items[:6]:
        grouped[competency.display_name] = []

    fallback_key = "补充资源"
    grouped[fallback_key] = []

    name_by_tag = {item.name: item.display_name for item in competencies.items}
    for resource in resources:
        placed = False
        for tag in resource.tags:
            if tag in name_by_tag and name_by_tag[tag] in grouped:
                grouped[name_by_tag[tag]].append(resource)
                placed = True
                break
        if not placed:
            grouped[fallback_key].append(resource)

    lines = [
        "# 最新优质资源包",
        "",
        "- 资源原则：优先官方文档、一手论文、官方项目仓库",
        "- 校验方式：以当前可访问的官方入口为主，避免依赖二手博客",
        "",
    ]

    for section, items in grouped.items():
        if not items:
            continue
        lines.append(f"## {section}")
        lines.append("")
        for resource in items:
            detail = f"- [{resource.title}]({resource.url})｜{resource.source_type}｜{resource.why}｜verified {resource.verified_on}"
            if resource.verified_source:
                detail += f"｜source {resource.verified_source}"
            lines.append(detail)
            if resource.evidence:
                lines.append(f"  - evidence: {resource.evidence}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def build_project_blueprint(
    jd: JDDocument,
    competencies: CompetencyMap,
    template: ProjectTemplate,
    company: str,
    role: str,
) -> str:
    lines = [
        f"# 主项目蓝图：{template.name}",
        "",
        f"- 目标公司：{company}",
        f"- 目标岗位：{role}",
        f"- 项目摘要：{template.summary}",
        "",
        "## 为什么匹配这个 JD",
        "",
    ]
    for item in competencies.items[:5]:
        lines.append(f"- 覆盖 `{item.display_name}`：项目中体现 {('；'.join(item.project_signals[:2]) or '相关能力演示')}。")

    lines.extend([
        "",
        "## 技术栈",
        "",
    ])
    lines.extend([f"- {tech}" for tech in template.tech_stack])
    lines.extend([
        "",
        "## 核心模块",
        "",
    ])
    lines.extend([f"- {module}" for module in template.modules])
    lines.extend([
        "",
        "## 里程碑",
        "",
    ])
    lines.extend([f"- {milestone}" for milestone in template.milestones])
    lines.extend([
        "",
        "## 建议评测指标",
        "",
    ])
    lines.extend([f"- {metric}" for metric in template.metrics])
    lines.extend([
        "",
        "## Demo 场景",
        "",
    ])
    lines.extend([f"- {scenario}" for scenario in template.demo_scenarios])
    lines.extend([
        "",
        "## 对应业务问题",
        "",
        f"- 结合 `{jd.title}`，把司机收入解释、活动推荐、热区建议、规则答疑做成统一入口。",
        "- 重点展示模型能力如何影响司机体验、供需平衡和平台效率。",
    ])
    return "\n".join(lines).strip() + "\n"


def build_interview_assets(jd: JDDocument, competencies: CompetencyMap, template: ProjectTemplate) -> str:
    top = competencies.items[:3]
    lines = [
        "# 面试与简历素材",
        "",
        "## 简历 Bullet",
        "",
        f"- 设计并实现 `{template.name}`，围绕司机经营问题构建包含意图识别、ReAct 工具调用、短长期记忆与策略推荐的 Agent 主链路。",
        f"- 基于合成对话、工具轨迹和偏好数据构建后训练样本，围绕 {(' / '.join(item.display_name for item in top))} 完成 SFT + DPO/GRPO 实验与离线评测。",
        "- 建立任务完成率、工具调用正确率、解释覆盖率与时延等指标闭环，将模型优化与业务价值表达打通。",
        "",
        "## 项目讲解顺序",
        "",
        "1. 先讲业务问题：司机经营问题复杂且高频，需要比传统 FAQ 更强的决策链路",
        "2. 再讲系统设计：intent router → planner/ReAct → tools → memory → evaluator",
        "3. 再讲训练闭环：SFT 打底、偏好优化或可验证奖励提升工具调用和解释质量",
        "4. 最后讲结果：离线评测、失败样例、下一步业务价值",
        "",
        "## 高频追问",
        "",
    ]
    for item in competencies.items[:5]:
        for signal in item.interview_signals[:2]:
            lines.append(f"- {signal}")
    lines.extend([
        "",
        "## 自我介绍主线",
        "",
        f"- 我围绕 `{jd.title}` 做的不是单点问答，而是面向司机场景的垂域 Agent 与后训练闭环。",
        "- 我会把技术拆成业务目标、系统设计、数据与训练、离线评测四层来讲。",
    ])
    return "\n".join(lines).strip() + "\n"
