#!/usr/bin/env python3
"""Calculate simple coverage progress from status items."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "calculate_coverage.py",
  "mode": "tracking",
  "summary": "Calculate simple coverage progress from status items.",
  "title": "Coverage Snapshot",
  "default_output": "coverage.json",
  "preferred_item_keys": [
    "tests",
    "items"
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
