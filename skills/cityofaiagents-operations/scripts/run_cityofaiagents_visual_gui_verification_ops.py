#!/usr/bin/env python3
"""Build a structured visual GUI verification brief for the mirrored skill."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import flatten_text, load_artifact, write_artifact  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="Build a visual GUI verification brief.")
    parser.add_argument("--input", required=True, help="Input artifact path")
    parser.add_argument("--output", default="visual_gui_verification_plan.json", help="Output artifact path")
    args = parser.parse_args()

    payload = load_artifact(args.input)
    text = flatten_text(payload).lower()

    evidence = ["step trace", "screenshots"]
    if "error" in text or "exception" in text:
        evidence.append("error capture")
    if "timing" in text or "wait" in text:
        evidence.append("timing observations")

    report = {
        "artifact_type": "cityofaiagents-visual-gui-verification-plan",
        "artifact_id": "SKL-0009",
        "revision": 1,
        "supported_tags": [
            "visual-gui-test",
            "desktop-ui",
            "testing",
            "visual-feedback",
        ],
        "required_evidence": evidence,
        "guide_constraints": [
            "Use safe sandbox boundaries",
            "Record failures before proposing root causes",
            "Do not modify product code during visual verification",
        ],
        "input_summary": flatten_text(payload)[:240],
    }

    path = write_artifact(report, args.output, "json")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
