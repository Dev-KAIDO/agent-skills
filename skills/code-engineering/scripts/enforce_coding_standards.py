#!/usr/bin/env python3
"""Validate that implementation notes align with coding standards."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "enforce_coding_standards.py",
  "mode": "validate",
  "summary": "Validate that implementation notes align with coding standards.",
  "title": "Coding Standards Validation",
  "default_output": "coding_standards_validation.json",
  "required_fields": [
    "language"
  ],
  "rules": [
    {
      "keyword": "tests",
      "message": "Implementation notes should mention tests or quality gates.",
      "severity": "medium"
    },
    {
      "keyword": "lint",
      "message": "Implementation notes should mention linting or formatting expectations.",
      "severity": "medium"
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
