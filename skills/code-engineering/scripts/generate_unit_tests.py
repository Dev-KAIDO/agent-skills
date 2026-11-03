#!/usr/bin/env python3
"""Generate unit-test cases from user stories or function lists."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "generate_unit_tests.py",
  "mode": "tests",
  "summary": "Generate unit-test cases from user stories or function lists.",
  "title": "Unit Test Plan",
  "default_output": "unit_tests.json",
  "preferred_item_keys": [
    "stories",
    "functions"
  ],
  "fallback_items": [
    "happy path",
    "validation failure",
    "boundary case"
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
