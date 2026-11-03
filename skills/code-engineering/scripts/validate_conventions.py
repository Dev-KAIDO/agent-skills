#!/usr/bin/env python3
"""Validate repository naming and structural conventions."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "validate_conventions.py",
  "mode": "validate",
  "summary": "Validate repository naming and structural conventions.",
  "title": "Convention Validation",
  "default_output": "convention_validation.json",
  "required_fields": [
    "project_name"
  ],
  "rules": [
    {
      "keyword": "src",
      "message": "The project structure should describe a source root.",
      "severity": "low"
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
