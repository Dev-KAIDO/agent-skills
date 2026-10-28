#!/usr/bin/env python3
"""Wave 2 enterprise skill runner."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "_skill-governance" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from project_intel import (  # noqa: E402
    append_decision,
    append_operation,
    build_local_dependency_graph,
    collect_repo_files,
    ensure_project_intel,
    finding,
    load_json,
    matching_tests,
    replace_items_for_source,
    reverse_graph,
    safe_read_text,
    update_progress_state,
    write_json,
)
from skill_governance import utc_now  # noqa: E402


SOURCE_SKILL = "security-remediator"


def load_request(args) -> dict:
    if args.input:
        payload = load_json(Path(args.input), {})
        if isinstance(payload, dict):
            return payload
    return {}


def repo_root_from_request(request: dict) -> Path:
    repo_path = str(request.get("repo_path", "")).strip()
    if not repo_path:
        raise SystemExit("repo_path is required.")
    repo_root = Path(repo_path).resolve()
    if not repo_root.exists():
        raise SystemExit(f"Repository path does not exist: {repo_root}")
    return repo_root


def as_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def normalize_rel(path: str) -> str:
    return str(path).replace("\\", "/").strip()


def artifact_items(payload: dict, *keys: str) -> list[dict]:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def select_targets(repo_root: Path, request: dict, paths) -> list[str]:
    targets = [normalize_rel(item) for item in as_list(request.get("target_files")) if str(item).strip()]
    if targets:
        return sorted(set(targets))
    for artifact_path, key in (
        (paths.diagnostic_findings, "findings"),
        (paths.risk_register, "risks"),
        (paths.repair_plan, "repairs"),
    ):
        payload = load_json(artifact_path, {})
        for item in artifact_items(payload, key):
            if item.get("status") in {"closed", "completed", "verified"}:
                continue
            for field in ("affected_files", "affected_area", "target_files"):
                for candidate in as_list(item.get(field)):
                    if str(candidate).strip():
                        targets.append(normalize_rel(candidate))
            if targets:
                return sorted(set(targets))
    files = collect_repo_files(repo_root)
    return [files[0].as_posix()] if files else []


def docs_containing_targets(repo_root: Path, targets: list[str]) -> list[str]:
    docs = []
    tokens = {Path(target).stem.lower() for target in targets if Path(target).stem}
    for rel in collect_repo_files(repo_root):
        if rel.suffix.lower() not in {".md", ".txt", ".rst"}:
            continue
        haystack = (rel.as_posix() + "\n" + safe_read_text(repo_root / rel)).lower()
        if any(token and token in haystack for token in tokens):
            docs.append(rel.as_posix())
    return sorted(set(docs))


def run_change_impact_mapper(repo_root: Path, request: dict, paths, output_path: Path) -> int:
    targets = select_targets(repo_root, request, paths)
    graph = build_local_dependency_graph(repo_root)
    reversed_graph = reverse_graph(graph)
    impacts = []
    for target in targets:
        dependencies = graph.get(target, [])
        dependents = reversed_graph.get(target, [])
        impacted = sorted(set([target] + dependencies + dependents))
        tests = matching_tests(repo_root, impacted)
        docs = docs_containing_targets(repo_root, impacted)
        impacts.append(
            {
                "target": target,
                "dependencies": dependencies,
                "dependents": dependents,
                "impacted_files": impacted,
                "impacted_tests": tests,
                "impacted_docs": docs,
                "verification_strategy": [
                    "Run targeted tests for impacted files." if tests else "Run syntax or startup checks for impacted files.",
                    "Re-run original failing command when this map comes from a diagnostic finding.",
                ],
            }
        )
    payload = {
        "artifact_type": "change-impact-map",
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "source_skill": SOURCE_SKILL,
        "changes": impacts,
    }
    write_json(paths.change_impact_map, payload)
    append_operation(paths, SOURCE_SKILL, "map-change-impact", repo_root.name, "completed", {"targets": len(targets)})
    update_progress_state(paths, {"last_change_impact_map": paths.change_impact_map.as_posix()})
    output = {"artifact_type": "change-impact-mapper-output", "generated_at": utc_now(), "artifacts": {"change_impact_map": str(paths.change_impact_map)}, "target_count": len(targets)}
    write_json(output_path, output)
    print(output_path)
    return 0


def load_log_text(repo_root: Path, request: dict) -> str:
    if request.get("ci_log"):
        return str(request["ci_log"])
    if request.get("ci_log_path"):
        path = Path(str(request["ci_log_path"]))
        if not path.is_absolute():
            path = repo_root / path
        return safe_read_text(path)
    return ""


def classify_ci_failure(log_text: str) -> str:
    lowered = log_text.lower()
    if "timed out" in lowered or "timeout" in lowered or "flaky" in lowered:
        return "flaky-or-timeout"
    if "no such file" in lowered or "environment" in lowered or "permission denied" in lowered:
        return "environment"
    if ".github/workflows" in lowered or "yaml" in lowered and "workflow" in lowered:
        return "configuration"
    if "failed" in lowered or "traceback" in lowered or "assert" in lowered:
        return "test-or-command"
    return "unknown"


def run_ci_failure_analyzer(repo_root: Path, request: dict, paths, output_path: Path) -> int:
    log_text = load_log_text(repo_root, request)
    if not log_text:
        raise SystemExit("ci_log or ci_log_path is required.")
    commands = re.findall(r"(?:Run|running|command:)\s+([^\n\r]+)", log_text, flags=re.IGNORECASE)
    tests = re.findall(r"([\w./\\-]*test[\w./\\-]*(?:::\w+)?)", log_text)
    files = sorted(set(normalize_rel(item) for item in re.findall(r"([\w./\\-]+\.(?:py|js|ts|tsx|yml|yaml))", log_text)))
    failure_type = classify_ci_failure(log_text)
    failure = {
        "id": "ci-failure-001",
        "failure_type": failure_type,
        "status": "open",
        "confidence": 0.86 if files or tests or commands else 0.62,
        "commands": commands[:5],
        "tests": sorted(set(tests))[:20],
        "affected_files": files[:20],
        "suspected_root_cause": "CI log contains failing command or test evidence; reproduce locally before repair.",
        "reproduction_command": commands[0] if commands else None,
        "log_excerpt": "\n".join(log_text.splitlines()[:40]),
        "source_skill": SOURCE_SKILL,
    }
    report = {"artifact_type": "ci-failure-report", "generated_at": utc_now(), "repo_root": str(repo_root), "failures": [failure]}
    write_json(paths.ci_failure_report, report)
    diag = finding(
        "cifailure-001",
        "CI failure requires local reproduction and scoped repair",
        "ci",
        "high" if failure_type in {"test-or-command", "configuration"} else "medium",
        failure["confidence"],
        SOURCE_SKILL,
        [{"type": "ci_log", "failure_type": failure_type, "commands": commands[:3], "tests": failure["tests"][:5]}],
        files[:20],
        "Use the CI failure report to reproduce locally, then route through regression-guard and defect-fixer.",
    )
    replace_items_for_source(paths.diagnostic_findings, "diagnostic-findings", "findings", SOURCE_SKILL, [diag])
    append_operation(paths, SOURCE_SKILL, "analyze-ci-failure", repo_root.name, "completed", {"failure_type": failure_type})
    update_progress_state(paths, {"last_ci_failure_report": paths.ci_failure_report.as_posix()})
    output = {"artifact_type": "ci-failure-analyzer-output", "generated_at": utc_now(), "artifacts": {"ci_failure_report": str(paths.ci_failure_report), "diagnostic_findings": str(paths.diagnostic_findings)}, "failure_type": failure_type}
    write_json(output_path, output)
    print(output_path)
    return 0


def security_candidates(request: dict, paths) -> list[dict]:
    candidates = [item for item in as_list(request.get("security_findings")) if isinstance(item, dict)]
    if candidates:
        return candidates
    risk_payload = load_json(paths.risk_register, {})
    for item in artifact_items(risk_payload, "risks"):
        haystack = f"{item.get('risk_type', '')} {item.get('title', '')}".lower()
        if "security" in haystack or "secret" in haystack or "vulnerab" in haystack:
            candidates.append(item)
    diag_payload = load_json(paths.diagnostic_findings, {})
    for item in artifact_items(diag_payload, "findings"):
        haystack = f"{item.get('type', '')} {item.get('title', '')}".lower()
        if "security" in haystack or "secret" in haystack or "vulnerab" in haystack:
            candidates.append(item)
    return candidates


def security_evidence_profile(item: dict) -> dict:
    text = " ".join(str(value) for value in item.values()).lower()
    return {
        "kev_priority": bool(item.get("kev_listed") or item.get("cisa_kev") or "known exploited" in text or "kev" in text),
        "secure_by_design_relevant": "secure by design" in text or "default" in text,
        "memory_safety_relevant": any(term in text for term in ("buffer overflow", "memory safety", "out-of-bounds", "use-after-free")),
        "asvs_mapping": item.get("asvs_mapping") or item.get("asvs_control_family"),
        "ghsa_advisory": item.get("ghsa") or item.get("github_advisory") or item.get("advisory_url"),
        "nvd_polling_recommended": bool(item.get("cve") or "cve-" in text),
    }


def run_security_remediator(repo_root: Path, request: dict, paths, output_path: Path) -> int:
    candidates = security_candidates(request, paths)
    if not candidates:
        raise SystemExit("A confirmed security finding or risk is required.")
    remediations = []
    repairs = []
    for index, item in enumerate(candidates, 1):
        affected = [normalize_rel(value) for value in as_list(item.get("affected_files") or item.get("affected_area")) if str(value).strip()]
        evidence_profile = security_evidence_profile(item)
        remediations.append(
            {
                "id": f"security-remediation-{index:03d}",
                "source_id": item.get("id", f"security-{index:03d}"),
                "title": item.get("title", "Security remediation candidate"),
                "severity": item.get("severity", "high"),
                "confidence": item.get("confidence", 0.8),
                "status": "planned",
                "affected_files": affected,
                "required_prechecks": ["change-impact-mapper", "regression-guard"],
                "recommended_action": item.get("recommended_action") or item.get("mitigation") or "Apply the smallest verified security fix.",
                "upgrade_policy": "No broad dependency upgrade unless the advisory names a safe target version.",
                "evidence_profile": evidence_profile,
                "verification_mapping": {
                    "asvs": evidence_profile["asvs_mapping"],
                    "secure_by_design": evidence_profile["secure_by_design_relevant"],
                    "memory_safety": evidence_profile["memory_safety_relevant"],
                },
            }
        )
        repairs.append(
            {
                "id": f"security-repair-{index:03d}",
                "finding_id": item.get("id"),
                "title": item.get("title", "Security repair"),
                "target_files": affected,
                "recommended_action": remediations[-1]["recommended_action"],
                "status": "planned",
                "source_skill": SOURCE_SKILL,
            }
        )
    write_json(paths.security_remediation_plan, {"artifact_type": "security-remediation-plan", "generated_at": utc_now(), "repo_root": str(repo_root), "source_skill": SOURCE_SKILL, "remediations": remediations})
    existing_repair = load_json(paths.repair_plan, {"artifact_type": "repair-plan", "repo_root": str(repo_root), "repairs": []})
    existing_repair["repairs"] = [item for item in existing_repair.get("repairs", []) if item.get("source_skill") != SOURCE_SKILL] + repairs
    existing_repair["generated_at"] = utc_now()
    write_json(paths.repair_plan, existing_repair)
    append_operation(paths, SOURCE_SKILL, "prepare-security-remediation", repo_root.name, "completed", {"remediations": len(remediations)})
    update_progress_state(paths, {"last_security_remediation_plan": paths.security_remediation_plan.as_posix()})
    output = {"artifact_type": "security-remediator-output", "generated_at": utc_now(), "artifacts": {"security_remediation_plan": str(paths.security_remediation_plan), "repair_plan": str(paths.repair_plan)}, "remediation_count": len(remediations), "kev_priority_count": len([item for item in remediations if item["evidence_profile"]["kev_priority"]])}
    write_json(output_path, output)
    print(output_path)
    return 0


def incident_text(repo_root: Path, request: dict) -> str:
    parts = []
    if request.get("incident_description"):
        parts.append(str(request["incident_description"]))
    if request.get("logs"):
        parts.append(str(request["logs"]))
    if request.get("log_path"):
        path = Path(str(request["log_path"]))
        if not path.is_absolute():
            path = repo_root / path
        parts.append(safe_read_text(path))
    return "\n".join(parts)


def run_incident_investigator(repo_root: Path, request: dict, paths, output_path: Path) -> int:
    text = incident_text(repo_root, request)
    if not text.strip():
        raise SystemExit("incident_description, logs, or log_path is required.")
    frames = re.findall(r'File "([^"]+)", line (\d+), in ([^\n]+)', text)
    affected = sorted(set(normalize_rel(frame[0]) for frame in frames))
    symptoms = []
    for marker in ("Traceback", "Fatal", "Exception", "Error", "crash", "timeout", "failed"):
        if marker.lower() in text.lower():
            symptoms.append(marker)
    confidence = 0.88 if frames else 0.64
    incident = {
        "id": "incident-001",
        "status": "investigating",
        "symptoms": sorted(set(symptoms)) or ["reported-runtime-symptom"],
        "trigger_signals": request.get("trigger_signals", []),
        "affected_files": affected,
        "suspected_root_cause": request.get("suspected_root_cause", "Requires targeted reproduction before confirmation."),
        "confirmed_root_cause": request.get("confirmed_root_cause"),
        "verification_gap": "Original failing runtime path has not been re-run after remediation.",
        "evidence": [{"type": "incident_text", "excerpt": "\n".join(text.splitlines()[:60])}],
        "confidence": confidence,
        "source_skill": SOURCE_SKILL,
    }
    report = {"artifact_type": "incident-report", "generated_at": utc_now(), "repo_root": str(repo_root), "incidents": [incident]}
    write_json(paths.incident_report, report)
    diag = finding(
        "incidentfailure-001",
        "Runtime incident requires reproduction and root-cause closure",
        "incident",
        "high" if frames else "medium",
        confidence,
        SOURCE_SKILL,
        incident["evidence"],
        affected,
        "Reproduce the incident path, then route the confirmed cause through regression-guard and stability-hardener or defect-fixer.",
    )
    replace_items_for_source(paths.diagnostic_findings, "diagnostic-findings", "findings", SOURCE_SKILL, [diag])
    if request.get("decision_note"):
        append_decision(paths, "Incident investigation note", str(request["decision_note"]))
    append_operation(paths, SOURCE_SKILL, "investigate-incident", repo_root.name, "completed", {"affected_files": len(affected)})
    update_progress_state(paths, {"last_incident_report": paths.incident_report.as_posix()})
    output = {"artifact_type": "incident-investigator-output", "generated_at": utc_now(), "artifacts": {"incident_report": str(paths.incident_report), "diagnostic_findings": str(paths.diagnostic_findings)}, "incident_count": 1}
    write_json(output_path, output)
    print(output_path)
    return 0


def run_stability_hardener(repo_root: Path, request: dict, paths, output_path: Path) -> int:
    incident_payload = load_json(paths.incident_report, {})
    risk_payload = load_json(paths.risk_register, {})
    failure_payload = load_json(paths.failure_catalog, {})
    impact_payload = load_json(paths.change_impact_map, {})
    sources = []
    sources.extend({"source": "incident", **item} for item in artifact_items(incident_payload, "incidents"))
    sources.extend({"source": "risk", **item} for item in artifact_items(risk_payload, "risks") if item.get("status") != "closed")
    sources.extend({"source": "failure", **item} for item in artifact_items(failure_payload, "failures"))
    if not sources:
        raise SystemExit("At least one incident, risk, or failure-catalog entry is required.")
    items = []
    repairs = []
    for index, source in enumerate(sources[:5], 1):
        affected = [normalize_rel(value) for value in as_list(source.get("affected_files") or source.get("affected_area")) if str(value).strip()]
        if not affected and impact_payload.get("changes"):
            affected = list(impact_payload["changes"][0].get("impacted_files", []))[:5]
        title = source.get("title") or source.get("code") or source.get("id") or "Stability hardening target"
        action = "Apply the smallest resilience patch, then verify the original failing or risky path."
        items.append(
            {
                "id": f"hardening-{index:03d}",
                "source_id": source.get("id") or source.get("code"),
                "source_type": source.get("source"),
                "title": title,
                "status": "planned",
                "affected_files": affected,
                "recommended_action": action,
                "verification_required": ["targeted test", "original failing command when available"],
            }
        )
        repairs.append(
            {
                "id": f"hardening-repair-{index:03d}",
                "finding_id": source.get("id") or source.get("code"),
                "title": title,
                "target_files": affected,
                "recommended_action": action,
                "status": "planned",
                "source_skill": SOURCE_SKILL,
            }
        )
    write_json(paths.hardening_plan, {"artifact_type": "hardening-plan", "generated_at": utc_now(), "repo_root": str(repo_root), "source_skill": SOURCE_SKILL, "hardening_items": items})
    existing_repair = load_json(paths.repair_plan, {"artifact_type": "repair-plan", "repo_root": str(repo_root), "repairs": []})
    existing_repair["repairs"] = [item for item in existing_repair.get("repairs", []) if item.get("source_skill") != SOURCE_SKILL] + repairs
    existing_repair["generated_at"] = utc_now()
    write_json(paths.repair_plan, existing_repair)
    append_operation(paths, SOURCE_SKILL, "prepare-hardening-plan", repo_root.name, "completed", {"hardening_items": len(items)})
    update_progress_state(paths, {"last_hardening_plan": paths.hardening_plan.as_posix()})
    output = {"artifact_type": "stability-hardener-output", "generated_at": utc_now(), "artifacts": {"hardening_plan": str(paths.hardening_plan), "repair_plan": str(paths.repair_plan)}, "hardening_item_count": len(items)}
    write_json(output_path, output)
    print(output_path)
    return 0


def summarize_artifact(path: Path, label: str) -> dict:
    payload = load_json(path, {})
    if not payload:
        return {"label": label, "path": str(path), "exists": False, "count": 0}
    count = 0
    for key in ("findings", "risks", "repairs", "checks", "failures", "remediations", "incidents", "hardening_items", "changes"):
        if isinstance(payload.get(key), list):
            count += len(payload[key])
    return {"label": label, "path": str(path), "exists": True, "artifact_type": payload.get("artifact_type"), "count": count, "generated_at": payload.get("generated_at")}


def run_evidence_sync(repo_root: Path, request: dict, paths, output_path: Path) -> int:
    artifacts = [
        summarize_artifact(paths.diagnostic_findings, "diagnostics"),
        summarize_artifact(paths.risk_register, "risks"),
        summarize_artifact(paths.repair_plan, "repair_plan"),
        summarize_artifact(paths.verification_report, "verification"),
        summarize_artifact(paths.ci_failure_report, "ci"),
        summarize_artifact(paths.security_remediation_plan, "security"),
        summarize_artifact(paths.incident_report, "incidents"),
        summarize_artifact(paths.hardening_plan, "stability"),
        summarize_artifact(paths.change_impact_map, "impact"),
    ]
    verification = load_json(paths.verification_report, {})
    repairs = load_json(paths.repair_plan, {})
    risks = load_json(paths.risk_register, {})
    bundle = {
        "artifact_type": "evidence-bundle",
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "source_skill": SOURCE_SKILL,
        "evidence": artifacts,
        "handoffs": {
            "docs_automation": {
                "source_artifacts": [item["path"] for item in artifacts if item["exists"]],
                "update_reason": "Synchronize docs with verified findings, risks, repairs, and incident evidence.",
            },
            "release_manager": {
                "verified_checks": verification.get("checks", []),
                "repair_count": len(repairs.get("repairs", [])) if isinstance(repairs.get("repairs"), list) else 0,
                "release_note_inputs": ["closed repairs", "verified checks", "remaining risks"],
            },
            "delivery_sync": {
                "open_risks": [item for item in risks.get("risks", []) if isinstance(item, dict) and item.get("status") != "closed"],
                "tracker_payload_ready": True,
            },
        },
    }
    write_json(paths.evidence_bundle, bundle)
    append_operation(paths, SOURCE_SKILL, "sync-evidence-bundle", repo_root.name, "completed", {"artifact_count": len([item for item in artifacts if item["exists"]])})
    update_progress_state(paths, {"last_evidence_bundle": paths.evidence_bundle.as_posix()})
    output = {"artifact_type": "evidence-sync-output", "generated_at": utc_now(), "artifacts": {"evidence_bundle": str(paths.evidence_bundle)}, "source_artifact_count": len([item for item in artifacts if item["exists"]])}
    write_json(output_path, output)
    print(output_path)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=f"Run {SOURCE_SKILL}.")
    parser.add_argument("--input", help="JSON input")
    parser.add_argument("--output", default=f"{SOURCE_SKILL.replace('-', '_')}_output.json", help="Summary JSON output")
    args = parser.parse_args()
    request = load_request(args)
    repo_root = repo_root_from_request(request)
    paths = ensure_project_intel(repo_root)
    output_path = Path(args.output)
    if SOURCE_SKILL == "change-impact-mapper":
        return run_change_impact_mapper(repo_root, request, paths, output_path)
    if SOURCE_SKILL == "ci-failure-analyzer":
        return run_ci_failure_analyzer(repo_root, request, paths, output_path)
    if SOURCE_SKILL == "security-remediator":
        return run_security_remediator(repo_root, request, paths, output_path)
    if SOURCE_SKILL == "incident-investigator":
        return run_incident_investigator(repo_root, request, paths, output_path)
    if SOURCE_SKILL == "stability-hardener":
        return run_stability_hardener(repo_root, request, paths, output_path)
    if SOURCE_SKILL == "evidence-sync":
        return run_evidence_sync(repo_root, request, paths, output_path)
    raise SystemExit(f"Unsupported skill: {SOURCE_SKILL}")


if __name__ == "__main__":
    raise SystemExit(main())
