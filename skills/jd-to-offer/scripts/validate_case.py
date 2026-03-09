#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = REPO_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from jd_offer.validators import validate_case_directory  # noqa: E402


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_case.py <case_dir>")
        return 2

    case_dir = Path(sys.argv[1])
    missing = validate_case_directory(case_dir)
    if missing:
        print("Missing files:")
        for item in missing:
            print(f"- {item}")
        return 1

    print(f"Case bundle OK: {case_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
