from __future__ import annotations

from pathlib import Path

import yaml

from jd_offer.schemas import CompetencyDefinition, CompetencyMap, CompetencyScore, JDDocument


SECTION_WEIGHTS = {
    "title": 2,
    "responsibilities": 3,
    "requirements": 2,
    "bonus_items": 1,
}


def load_taxonomy(path: Path) -> list[CompetencyDefinition]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return [CompetencyDefinition.model_validate(item) for item in payload.get("competencies", [])]


def map_jd_to_competencies(jd: JDDocument, taxonomy_path: Path) -> CompetencyMap:
    definitions = load_taxonomy(taxonomy_path)
    scored: list[CompetencyScore] = []

    title_text = jd.title.lower()
    resp_text = "\n".join(jd.responsibilities).lower()
    req_text = "\n".join(jd.requirements).lower()
    bonus_text = "\n".join(jd.bonus_items).lower()

    for definition in definitions:
        matched_keywords: list[str] = []
        score = 0
        for keyword in definition.trigger_keywords:
            normalized = keyword.lower()
            if normalized in title_text:
                score += SECTION_WEIGHTS["title"]
                matched_keywords.append(keyword)
            if normalized in resp_text:
                score += SECTION_WEIGHTS["responsibilities"]
                matched_keywords.append(keyword)
            if normalized in req_text:
                score += SECTION_WEIGHTS["requirements"]
                matched_keywords.append(keyword)
            if normalized in bonus_text:
                score += SECTION_WEIGHTS["bonus_items"]
                matched_keywords.append(keyword)

        matched_keywords = sorted(set(matched_keywords), key=matched_keywords.index)
        if score <= 0:
            continue

        scored.append(
            CompetencyScore(
                name=definition.name,
                display_name=definition.display_name,
                score=score,
                matched_keywords=matched_keywords,
                foundational_subtopics=definition.foundational_subtopics,
                project_signals=definition.project_signals,
                interview_signals=definition.interview_signals,
                resource_tags=definition.resource_tags or [definition.name],
            )
        )

    scored.sort(key=lambda item: (-item.score, item.name))
    return CompetencyMap(items=scored)
