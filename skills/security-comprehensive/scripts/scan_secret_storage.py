#!/usr/bin/env python3
"""Scan project files for likely secret-storage surfaces and plan migration."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


PATTERNS = {
    "password": re.compile(r"password|passwd|pin_code", re.IGNORECASE),
    "token": re.compile(r"token|api[_-]?key|secret", re.IGNORECASE),
    "cookie": re.compile(r"cookie|session", re.IGNORECASE),
}
TEXT_SUFFIXES = {".py", ".js", ".ts", ".json", ".env", ".ini", ".cfg", ".toml", ".yaml", ".yml", ".sql"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def iter_files(root: Path, max_files: int):
    count = 0
    for path in root.rglob("*"):
        if count >= max_files:
            break
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES and ".venv" not in path.parts:
            count += 1
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan secure secret-storage migration.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    payload = load_json(Path(args.input))
    root = Path(payload.get("project_root", ".")).expanduser().resolve()
    max_files = int(payload.get("max_files", 200))
    findings = []
    for file_path in iter_files(root, max_files):
        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        matches = sorted(name for name, pattern in PATTERNS.items() if pattern.search(file_path.name) or pattern.search(text[:20000]))
        if matches:
            findings.append({"file": str(file_path), "signals": matches})

    write_json(
        Path(args.output),
        {
            "artifact_type": "secure-storage-migration-plan",
            "generated_at": utc_now(),
            "project_root": str(root),
            "finding_count": len(findings),
            "findings": findings,
            "recommended_storage_options": ["Windows Credential Manager", "DPAPI", "keyring", "OS keychain", "encrypted local store"],
            "verification": ["search persisted stores for raw secret values", "test migration from legacy storage", "test missing/corrupt secure-store entry"],
            "implementation_performed": False,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
