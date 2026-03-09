from __future__ import annotations

from pathlib import Path


REQUIRED_CASE_FILES = [
    "01_jd_decomposition.md",
    "02_knowledge_system.md",
    "03_resource_pack.md",
    "04_project_blueprint.md",
    "05_interview_assets.md",
    "manifest.yaml",
]


def validate_case_directory(path: Path) -> list[str]:
    missing = []
    for filename in REQUIRED_CASE_FILES:
        if not (path / filename).exists():
            missing.append(filename)
    return missing
