#!/usr/bin/env python3
"""Generate a language-specific project structure plan or scaffold."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "generate_code_structure.py",
  "mode": "scaffold",
  "summary": "Generate a language-specific project structure plan or scaffold.",
  "title": "Code Structure",
  "default_output": "code_structure.json",
  "default_language": "python",
  "trees": {
    "python": [
      "src/",
      "src/app/",
      "tests/",
      "tests/unit/",
      "pyproject.toml"
    ],
    "javascript": [
      "src/",
      "src/components/",
      "tests/",
      "package.json"
    ],
    "sql": [
      "ddl/",
      "dml/",
      "tests/",
      "README.sql"
    ],
    "default": [
      "src/",
      "tests/"
    ]
  }
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
