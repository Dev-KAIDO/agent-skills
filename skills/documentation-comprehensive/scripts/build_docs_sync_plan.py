#!/usr/bin/env python3
"""Build a documentation synchronization plan from project artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import flatten_text, load_artifact, write_artifact  # noqa: E402


RULES = [
    ("README.md", {"feature", "setup", "install", "usage"}, "developer-owner"),
    ("docs/spec.md", {"scope", "requirement", "story", "contract"}, "product-owner"),
    ("docs/runbook.md", {"deploy", "incident", "rollback", "support"}, "operations-owner"),
    ("docs/status.md", {"milestone", "risk", "progress", "blocked"}, "project-owner"),
    ("CHANGELOG.md", {"release", "version", "fix", "feature"}, "release-owner"),
]


def main():
    parser = argparse.ArgumentParser(description="Build a documentation sync plan.")
    parser.add_argument("--input", required=True, help="Artifact that describes recent project changes")
    parser.add_argument("--output", default="docs_sync_plan.json", help="Output artifact path")
    args = parser.parse_args()

    payload = load_artifact(args.input)
    words = {token.lower() for token in flatten_text(payload).replace("/", " ").split()}

    updates = []
    for target, triggers, owner in RULES:
        if words.intersection(triggers):
            updates.append(
                {
                    "target": target,
                    "owner": owner,
                    "reason": f"Detected triggers: {', '.join(sorted(words.intersection(triggers)))}",
                }
            )

    report = {
        "artifact_type": "docs-sync-plan",
        "update_backlog": updates,
        "gating_rules": [
            "Update operational docs before or with release notes.",
            "Update status artifacts whenever scope, risk, or progress changes.",
            "Do not mark docs complete until the code or release artifact is linked.",
        ],
    }

    path = write_artifact(report, args.output, "json")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
