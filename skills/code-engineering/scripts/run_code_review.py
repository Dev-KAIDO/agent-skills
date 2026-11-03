#!/usr/bin/env python3
"""Apply a structured code-review checklist to code snippets or review notes."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "run_code_review.py",
  "mode": "code-review",
  "summary": "Apply a structured code-review checklist to code snippets or review notes.",
  "title": "Code Review Findings",
  "default_output": "code_review_findings.json",
  "checklist": [
    {
      "keyword": "test",
      "message": "No evidence of test updates was found.",
      "severity": "medium"
    },
    {
      "keyword": "error",
      "message": "Error handling is not obvious from the provided code or notes.",
      "severity": "medium"
    },
    {
      "keyword": "doc",
      "message": "Public API changes should carry documentation updates.",
      "severity": "low"
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
