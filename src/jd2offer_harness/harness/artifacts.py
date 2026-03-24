from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterable, Sequence

import yaml

from jd2offer_harness.adapters.jd_parser import parse_jd
from jd2offer_harness.adapters.resume_parser import parse_resume

DEFAULT_STAGE_NAMES = [
    "intake",
    "competency-analysis",
    "gap-mapping",
    "project-design",
    "visual-story",
    "interview-assets",
    "bundle-render",
    "evaluation",
]


@dataclass
class StageRecord:
    slug: str
    name: str
    status: str = "pending"


@dataclass
class CaseManifest:
    case_slug: str
    company: str
    role: str
    source_resume: str
    source_jd: str
    stages: list[StageRecord] = field(default_factory=list)


@dataclass
class CaseWorkspace:
    root: Path


def _ensure_dirs(outdir: Path) -> None:
    for sub in ("raw", "normalized", "stages", "outputs"):
        (outdir / sub).mkdir(parents=True, exist_ok=True)


def _write_stage_dirs(outdir: Path) -> list[StageRecord]:
    stage_dir = outdir / "stages"
    records: list[StageRecord] = []
    for index, slug in enumerate(DEFAULT_STAGE_NAMES, start=1):
        dir_name = f"{index:02d}-{slug}"
        (stage_dir / dir_name).mkdir(exist_ok=True)
        records.append(StageRecord(slug=slug, name=dir_name))
    return records


def _write_normalized(outdir: Path, resume_doc, target_jd) -> None:
    normalized_dir = outdir / "normalized"
    (normalized_dir / "resume_document.yaml").write_text(
        yaml.safe_dump(resume_doc.to_dict(), allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    (normalized_dir / "target_jd.yaml").write_text(
        yaml.safe_dump(target_jd.to_dict(), allow_unicode=True, sort_keys=False), encoding="utf-8"
    )


def _write_raw(outdir: Path, resume_path: Path, jd_path: Path) -> None:
    raw_dir = outdir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_dir / "resume.md"
    (raw_dir / "resume.md").write_text(resume_path.read_text(encoding="utf-8"), encoding="utf-8")
    (raw_dir / "jd.md").write_text(jd_path.read_text(encoding="utf-8"), encoding="utf-8")


def _write_manifest(outdir: Path, company: str, role: str, case_slug: str, manifest: CaseManifest) -> Path:
    manifest_path = outdir / "manifest.yaml"
    manifest_data = asdict(manifest)
    manifest_path.write_text(
        yaml.safe_dump(manifest_data, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    return manifest_path


def initialize_case_workspace(
    resume_path: Path,
    jd_path: Path,
    outdir: Path,
    company: str,
    role: str,
) -> CaseWorkspace:
    outdir.mkdir(parents=True, exist_ok=True)
    _ensure_dirs(outdir)
    resume_doc = parse_resume(resume_path)
    target_jd = parse_jd(jd_path)
    _write_raw(outdir, resume_path, jd_path)
    _write_normalized(outdir, resume_doc, target_jd)
    stages = _write_stage_dirs(outdir)
    case_slug = outdir.name
    manifest = CaseManifest(
        case_slug=case_slug,
        company=company,
        role=role,
        source_resume=str(resume_path),
        source_jd=str(jd_path),
        stages=stages,
    )
    _write_manifest(outdir, company, role, case_slug, manifest)
    return CaseWorkspace(root=outdir)


def load_case_manifest(path: Path) -> CaseManifest:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    stages_data = data.get("stages", [])
    stages = [StageRecord(**stage) for stage in stages_data]
    return CaseManifest(
        case_slug=data.get("case_slug", ""),
        company=data.get("company", ""),
        role=data.get("role", ""),
        source_resume=data.get("source_resume", ""),
        source_jd=data.get("source_jd", ""),
        stages=stages,
    )


def save_case_manifest(path: Path, manifest: CaseManifest) -> Path:
    path.write_text(
        yaml.safe_dump(asdict(manifest), allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return path
