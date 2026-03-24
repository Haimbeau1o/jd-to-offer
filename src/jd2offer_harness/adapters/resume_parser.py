from __future__ import annotations

from pathlib import Path

from jd2offer_harness.domain.resume import ResumeDocument


def parse_resume(path: Path) -> ResumeDocument:
    text = path.read_text(encoding="utf-8")
    return ResumeDocument.from_markdown(text)

