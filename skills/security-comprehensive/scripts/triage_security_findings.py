#!/usr/bin/env python3
"""Rank security findings and decide whether the gate passes."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import list_from_payload, load_artifact, write_artifact  # noqa: E402


SEVERITY_SCORE = {"critical": 4, "high": 3, "medium": 2, "low": 1}

BASELINE_CHECKS = {
    "auth": [
        "Verify login/session state cannot be bypassed.",
        "Verify credentials, tokens, and cookies are not logged or stored in clear text.",
    ],
    "authorization": [
        "Verify role and per-user permissions use deny-by-default behavior.",
        "Verify privileged actions require the expected role and audit event.",
    ],
    "database": [
        "Verify untrusted values are parameterized before SQL/database writes.",
        "Verify migrations, restore, import, and delete operations have rollback or dry-run evidence.",
    ],
    "api": [
        "Verify input validation and output encoding for untrusted request data.",
        "Verify error responses do not expose secrets or internal stack traces.",
    ],
    "licensing": [
        "Verify license, trial, transfer, and device-fingerprint checks are not bypassable by local edits alone.",
        "Verify license or transfer operations are auditable and reversible where required.",
    ],
    "secrets": [
        "Verify secrets are not committed, logged, or stored in plain local files.",
        "Verify secret rotation or migration risk is documented when storage changes.",
    ],
    "destructive": [
        "Verify destructive operations are developer/admin gated and require explicit confirmation.",
        "Verify dry-run evidence exists before real deletion or irreversible state changes.",
    ],
}


def normalize_finding(item):
    if not isinstance(item, dict):
        return {"title": str(item), "severity": "medium", "owner": "security-owner", "status": "open"}
    return {
        "title": item.get("title") or item.get("rule") or "Unnamed finding",
        "severity": str(item.get("severity", "medium")).lower(),
        "owner": item.get("owner") or "security-owner",
        "status": str(item.get("status", "open")).lower(),
    }


def build_baseline(payload: dict) -> dict:
    raw_surfaces = payload.get("project_surfaces") or payload.get("surfaces") or []
    if isinstance(raw_surfaces, str):
        raw_surfaces = [raw_surfaces]
    surfaces = [str(item).strip().lower() for item in raw_surfaces if str(item).strip()]
    if not surfaces:
        surfaces = ["auth", "authorization", "database", "api", "secrets"]

    checks = []
    unknown_surfaces = []
    for surface in surfaces:
        mapped = BASELINE_CHECKS.get(surface)
        if not mapped:
            unknown_surfaces.append(surface)
            continue
        checks.extend({"surface": surface, "check": check, "status": "required"} for check in mapped)

    gate_status = "warn" if checks else "fail"
    return {
        "artifact_type": "security-baseline-gate",
        "gate_status": gate_status,
        "mode": "baseline",
        "surfaces": surfaces,
        "required_checks": checks,
        "unknown_surfaces": unknown_surfaces,
        "must_not_weaken": [
            "authorization",
            "encryption_or_signing",
            "license_enforcement",
            "input_validation",
            "audit_logging",
            "backup_or_dry_run_requirements",
        ],
        "recommended_actions": [
            "Run or document each required check before implementation closeout.",
            "Route any confirmed issue to project-remediation-batch-controller with backup and rollback evidence.",
            "Block release or completion if a critical security control is weakened or unverified.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="Triage security findings into a gate decision.")
    parser.add_argument("--input", required=True, help="Path to the findings artifact")
    parser.add_argument("--output", default="security_gate.json", help="Output artifact path")
    args = parser.parse_args()

    payload = load_artifact(args.input)
    if isinstance(payload, dict) and (payload.get("mode") == "baseline" or payload.get("project_surfaces") or payload.get("surfaces")):
        path = write_artifact(build_baseline(payload), args.output, "json")
        print(path)
        return 0

    findings = [normalize_finding(item) for item in list_from_payload(payload, ["findings", "items", "alerts"])]
    findings.sort(key=lambda item: (-SEVERITY_SCORE.get(item["severity"], 0), item["title"]))

    open_findings = [item for item in findings if item["status"] not in {"resolved", "fixed", "closed"}]
    if any(item["severity"] == "critical" for item in open_findings):
        gate_status = "fail"
    elif any(item["severity"] == "high" for item in open_findings):
        gate_status = "warn"
    else:
        gate_status = "pass"

    report = {
        "artifact_type": "security-gate",
        "gate_status": gate_status,
        "open_findings": open_findings,
        "recommended_actions": [
            "Resolve all critical findings before release.",
            "Create owner-tracked remediation tickets for all high findings.",
            "Document accepted risk explicitly for any deferred medium findings.",
        ],
    }

    path = write_artifact(report, args.output, "json")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
