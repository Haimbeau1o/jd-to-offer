from __future__ import annotations

from pathlib import Path
import json

import yaml

from commentops_agent_lab.schemas import PolicyClause, ReviewCase


REPO_ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = REPO_ROOT / "examples" / "commentops" / "policies" / "comment_policy_v1.yaml"
CASE_PATH = REPO_ROOT / "examples" / "commentops" / "cases" / "sample_review_cases.jsonl"


def load_policy_clauses(path: Path | None = None) -> list[PolicyClause]:
    payload = yaml.safe_load((path or POLICY_PATH).read_text(encoding="utf-8"))
    return [PolicyClause.model_validate(item) for item in payload.get("clauses", [])]


def load_sample_review_cases(path: Path | None = None) -> list[ReviewCase]:
    records: list[ReviewCase] = []
    for line in (path or CASE_PATH).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        records.append(ReviewCase.model_validate(json.loads(line)))
    return records


def load_review_case_map(path: Path | None = None) -> dict[str, ReviewCase]:
    return {item.case_id: item for item in load_sample_review_cases(path)}
