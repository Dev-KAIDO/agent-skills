#!/usr/bin/env python3
"""Generate an API documentation outline from interfaces or stories."""

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import execute_configured_script


CONFIG = {
  "file": "generate_api_docs.py",
  "mode": "document",
  "summary": "Generate an API documentation outline from interfaces or stories.",
  "title": "API Documentation Outline",
  "default_output": "api_docs_outline.md",
  "sections": [
    {
      "title": "Overview",
      "fields": [
        "overview",
        "goals"
      ],
      "fallback": "Describe the API audience and purpose."
    },
    {
      "title": "Endpoints",
      "fields": [
        "endpoints"
      ],
      "fallback": "List endpoints or operations with request and response contracts."
    },
    {
      "title": "Errors",
      "fields": [
        "errors"
      ],
      "fallback": "Describe standard error handling and validation responses."
    }
  ]
}


if __name__ == "__main__":
    raise SystemExit(execute_configured_script(CONFIG))
