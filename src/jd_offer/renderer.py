from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import yaml

from jd_offer.schemas import Manifest


FILE_MAP = {
    "jd_decomposition": "01_jd_decomposition.md",
    "knowledge_system": "02_knowledge_system.md",
    "resource_pack": "03_resource_pack.md",
    "project_blueprint": "04_project_blueprint.md",
    "interview_assets": "05_interview_assets.md",
}


def render_case_bundle(
    case_slug: str,
    outdir: Path,
    payload: dict[str, str],
    *,
    source_jd: str | None = None,
    company: str | None = None,
    role: str | None = None,
    competencies: list[str] | None = None,
    extra: dict | None = None,
) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    files: dict[str, str] = {}
    for key, filename in FILE_MAP.items():
        content = payload[key]
        target = outdir / filename
        target.write_text(str(content), encoding="utf-8")
        files[key] = filename

    manifest = Manifest(
        case_slug=case_slug,
        generated_at=datetime.now(timezone.utc).isoformat(),
        source_jd=source_jd,
        company=company,
        role=role,
        competencies=competencies or [],
        files=files,
        extra=extra or {},
    )
    (outdir / "manifest.yaml").write_text(
        yaml.safe_dump(manifest.model_dump(mode="json"), allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return outdir
