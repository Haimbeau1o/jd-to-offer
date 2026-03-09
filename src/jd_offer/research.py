from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml

from jd_offer.schemas import CompetencyMap, JDDocument, ResearchOverrideBundle, ResourceEntry


def load_resource_overrides(path: Path) -> list[ResourceEntry]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    bundle = ResearchOverrideBundle.model_validate(payload)
    return bundle.resources


def merge_resources(base: list[ResourceEntry], overrides: list[ResourceEntry]) -> list[ResourceEntry]:
    merged: dict[str, ResourceEntry] = {item.id: item for item in base}
    for item in overrides:
        merged[item.id] = item
    return sorted(merged.values(), key=lambda item: (item.priority, item.title.lower()))


def scaffold_research_template(jd: JDDocument, competencies: CompetencyMap, outpath: Path) -> Path:
    payload = {
        "case_slug": None,
        "verified_on": str(date.today()),
        "notes": f"根据《{jd.title}》生成的联网研究模板。先用 agent 浏览官方文档/一手论文，再把资源填回这里。",
        "top_competencies": competencies.top_names[:6],
        "resources": [],
    }
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return outpath
