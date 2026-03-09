#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = REPO_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from jd_offer.cli import app  # noqa: E402
from typer.main import get_command  # noqa: E402


if __name__ == "__main__":
    command = get_command(app)
    raise SystemExit(command())
