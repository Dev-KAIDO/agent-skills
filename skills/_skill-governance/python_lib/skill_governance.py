#!/usr/bin/env python3
"""Shared governance helpers for the skill-forge stack."""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence
from urllib.parse import urlparse

import sys

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

try:
    from authored_skill_tools import authored_skill_dirs, load_openai_yaml  # type: ignore  # noqa: E402
    from sdlc_common import parse_simple_yaml  # type: ignore  # noqa: E402
except ModuleNotFoundError:
    SYSTEM_DIRS = {"sdlc-system", "superpowers", "__pycache__"}

    def parse_scalar(value: str):
        value = value.strip()
        if not value:
            return ""
        if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
            return value[1:-1]
        lowered = value.lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
        if lowered in {"null", "none"}:
            return None
        if re.fullmatch(r"-?\d+", value):
            return int(value)
        if re.fullmatch(r"-?\d+\.\d+", value):
            return float(value)
        return value

    def parse_simple_yaml(text: str):
        root = {}
        stack = [(-1, root)]
        for raw_line in text.splitlines():
            line = raw_line.rstrip()
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            indent = len(line) - len(line.lstrip(" "))
            stripped = line.strip()
            while stack and indent <= stack[-1][0]:
                stack.pop()
            parent = stack[-1][1]
            if ":" not in stripped:
                raise ValueError("Unsupported YAML structure: missing ':' separator")
            key, raw_value = stripped.split(":", 1)
            key = key.strip()
            raw_value = raw_value.strip()
            if raw_value == "":
                node = {}
                if not isinstance(parent, dict):
                    raise ValueError("Unsupported YAML structure: nested mapping under non-mapping")
                parent[key] = node
                stack.append((indent, node))
                continue
            if not isinstance(parent, dict):
                raise ValueError("Unsupported YAML structure: scalar under non-mapping")
            parent[key] = parse_scalar(raw_value)
        return root

    def authored_skill_dirs(root: Path):
        return sorted(
            path
            for path in root.iterdir()
            if path.is_dir() and path.name not in SYSTEM_DIRS and (path / "SKILL.md").exists()
        )

    def load_openai_yaml(skill_dir: Path):
        path = skill_dir / "agents" / "openai.yaml"
        if not path.exists():
            raise FileNotFoundError(f"agents/openai.yaml not found for {skill_dir.name}")
        return parse_simple_yaml(path.read_text(encoding="utf-8-sig")), path


SKILLS_ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE_ROOT = SKILLS_ROOT / "_skill-governance"
REGISTRY_PATH = GOVERNANCE_ROOT / "registry.json"
VERSIONS_PATH = GOVERNANCE_ROOT / "skill_versions.json"
POLICIES_PATH = GOVERNANCE_ROOT / "source_policies.json"
LOG_PATH = GOVERNANCE_ROOT / "operations_log.jsonl"
UPDATE_REQUESTS_DIR = GOVERNANCE_ROOT / "update_requests"


@dataclass
class SkillInfo:
    name: str
    path: Path
    description: str
    display_name: str
    short_description: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def append_jsonl(path: Path, payload) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return path


def log_operation(actor: str, action: str, target: str, status: str, details: Optional[Dict[str, object]] = None) -> None:
    append_jsonl(
        LOG_PATH,
        {
            "timestamp": utc_now(),
            "actor": actor,
            "action": action,
            "target": target,
            "status": status,
            "details": details or {},
        },
    )


def read_skill_frontmatter(skill_dir: Path) -> Dict[str, object]:
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        raise ValueError(f"Missing YAML frontmatter in {skill_md}")
    return parse_simple_yaml(match.group(1))


def read_skill_body(skill_dir: Path) -> str:
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n.*?\n---\n(.*)$", text, re.DOTALL)
    return match.group(1) if match else text


def get_skill_info(skill_dir: Path) -> SkillInfo:
    frontmatter = read_skill_frontmatter(skill_dir)
    openai_data, _ = load_openai_yaml(skill_dir)
    interface = openai_data.get("interface", {})
    return SkillInfo(
        name=str(frontmatter.get("name", skill_dir.name)),
        path=skill_dir,
        description=str(frontmatter.get("description", "")).strip(),
        display_name=str(interface.get("display_name", skill_dir.name)).strip(),
        short_description=str(interface.get("short_description", "")).strip(),
    )


def all_skill_dirs(root: Path = SKILLS_ROOT) -> List[Path]:
    return authored_skill_dirs(root)


def find_skill_dir(skill_name: str, root: Path = SKILLS_ROOT) -> Optional[Path]:
    for path in all_skill_dirs(root):
        if path.name == skill_name:
            return path
    return None


def count_files(path: Path, pattern: str) -> int:
    if not path.exists():
        return 0
    return len(list(path.glob(pattern)))


def quality_report(skill_dir: Path) -> Dict[str, object]:
    info = get_skill_info(skill_dir)
    body = read_skill_body(skill_dir)
    scripts_dir = skill_dir / "scripts"
    refs_dir = skill_dir / "references"
    assets_dir = skill_dir / "assets"
    inputs_dir = assets_dir / "inputs"
    outputs_dir = assets_dir / "outputs"

    frontmatter = read_skill_frontmatter(skill_dir)
    openai_data, _ = load_openai_yaml(skill_dir)
    interface = openai_data.get("interface", {})

    issues: List[Dict[str, str]] = []
    scores = {
        "trigger_quality": 0,
        "instruction_clarity": 0,
        "resource_design": 0,
        "determinism": 0,
        "validation_strength": 0,
        "update_safety": 0,
    }

    description = info.description
    if "Use when" in description or "Use when" in body:
        scores["trigger_quality"] += 3
    if len(description) >= 120:
        scores["trigger_quality"] += 2
    else:
        issues.append({"code": "trigger_too_thin", "message": "Frontmatter description lacks enough trigger detail."})

    if "## Workflow" in body:
        scores["instruction_clarity"] += 2
    else:
        issues.append({"code": "workflow_missing", "message": "SKILL.md is missing a dedicated workflow section."})
    if "## Failure Modes" in body:
        scores["instruction_clarity"] += 1
        scores["update_safety"] += 2
    else:
        issues.append({"code": "failure_modes_missing", "message": "SKILL.md is missing a Failure Modes section."})
    if "## References" in body:
        scores["instruction_clarity"] += 1
    if "Use these scripts:" in body or "Run:" in body:
        scores["determinism"] += 2

    if scripts_dir.exists() and any(scripts_dir.glob("*.py")):
        scores["resource_design"] += 2
        scores["determinism"] += 1
    else:
        issues.append({"code": "scripts_missing", "message": "No Python scripts are present for deterministic execution."})
    if refs_dir.exists() and any(refs_dir.iterdir()):
        scores["resource_design"] += 1
    else:
        issues.append({"code": "references_missing", "message": "No references were provided for progressive disclosure."})
    if outputs_dir.exists() and any(outputs_dir.rglob("*")):
        scores["validation_strength"] += 2
    else:
        issues.append({"code": "sample_outputs_missing", "message": "No sample outputs are present under assets/outputs."})
    if inputs_dir.exists() and any(inputs_dir.rglob("*")):
        scores["validation_strength"] += 2
    else:
        issues.append({"code": "sample_inputs_missing", "message": "No sample inputs are present under assets/inputs."})

    default_prompt = str(interface.get("default_prompt", ""))
    if f"${info.name}" in default_prompt:
        scores["trigger_quality"] += 1
    else:
        issues.append({"code": "default_prompt_missing_skill_name", "message": "default_prompt does not mention the explicit skill token."})
    if str(interface.get("display_name", "")).strip():
        scores["instruction_clarity"] += 1
    if str(interface.get("short_description", "")).strip():
        scores["instruction_clarity"] += 1

    if any(term in description.lower() for term in ("update", "security", "govern", "policy")):
        scores["update_safety"] += 1

    total = sum(scores.values())
    quality_grade = "excellent" if total >= 18 else "good" if total >= 13 else "fair" if total >= 8 else "weak"
    return {
        "artifact_type": "skill-quality-report",
        "generated_at": utc_now(),
        "skill": info.name,
        "display_name": info.display_name,
        "scores": scores,
        "total_score": total,
        "quality_grade": quality_grade,
        "issues": issues,
        "inventory": {
            "scripts": count_files(scripts_dir, "*.py"),
            "references": len(list(refs_dir.iterdir())) if refs_dir.exists() else 0,
            "asset_inputs": len(list(inputs_dir.rglob("*"))) if inputs_dir.exists() else 0,
            "asset_outputs": len(list(outputs_dir.rglob("*"))) if outputs_dir.exists() else 0,
        },
        "metadata": {
            "description_length": len(description),
            "default_prompt": default_prompt,
            "frontmatter_keys": sorted(frontmatter.keys()),
        },
    }


def patch_plan(skill_dir: Path, report: Dict[str, object], intent: str = "improve existing skill quality") -> Dict[str, object]:
    touched_files = [str(skill_dir / "SKILL.md"), str(skill_dir / "agents" / "openai.yaml")]
    report_issues = report.get("issues", [])
    actions = []
    for issue in report_issues:
        code = issue["code"]
        if code in {"workflow_missing", "failure_modes_missing", "trigger_too_thin"}:
            actions.append("Refine SKILL.md instructions, triggers, and failure boundaries.")
        elif code in {"scripts_missing"}:
            actions.append("Add or improve deterministic scripts for the skill's core workflow.")
            touched_files.append(str(skill_dir / "scripts"))
        elif code in {"references_missing"}:
            actions.append("Add concise references for progressive disclosure.")
            touched_files.append(str(skill_dir / "references"))
        elif code in {"sample_inputs_missing", "sample_outputs_missing"}:
            actions.append("Add smoke-test inputs and outputs under assets.")
            touched_files.append(str(skill_dir / "assets"))
        elif code == "default_prompt_missing_skill_name":
            actions.append("Regenerate or fix agents/openai.yaml default_prompt to include the explicit skill token.")
    if not actions:
        actions.append("No urgent changes required; preserve the skill and only refresh metadata if needed.")

    return {
        "artifact_type": "skill-patch-plan",
        "generated_at": utc_now(),
        "skill": skill_dir.name,
        "intent": intent,
        "scoped_files": sorted(set(touched_files)),
        "actions": dedupe(actions),
        "non_goals": [
            "Do not refactor unrelated skills.",
            "Do not widen tool dependencies unless the skill's core workflow requires it.",
            "Do not rewrite unrelated governance files during a skill-local update.",
        ],
    }


def impact_report(skill_name: str, authored_root: Path = SKILLS_ROOT) -> Dict[str, object]:
    target_dir = find_skill_dir(skill_name, authored_root)
    if not target_dir:
        raise FileNotFoundError(f"Skill not found: {skill_name}")

    direct_refs = []
    transitive_hints = []
    target_token = f"${skill_name}"
    for skill_dir in all_skill_dirs(authored_root):
        if skill_dir.name == skill_name:
            continue
        content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        hits = []
        if skill_name in content:
            hits.append("skill_name_mention")
        if target_token in content:
            hits.append("explicit_skill_token")
        if hits:
            direct_refs.append({"skill": skill_dir.name, "hits": hits})
        if any(keyword in content.lower() for keyword in ("governance", "update request", "registry", "policy")):
            transitive_hints.append(skill_dir.name)

    governance_files = [
        str(POLICIES_PATH),
        str(REGISTRY_PATH),
        str(VERSIONS_PATH),
    ]
    return {
        "artifact_type": "skill-change-impact-report",
        "generated_at": utc_now(),
        "skill": skill_name,
        "direct_skill_references": direct_refs,
        "governance_files_to_check": governance_files,
        "transitive_governance_hints": sorted(set(transitive_hints)),
        "summary": {
            "direct_reference_count": len(direct_refs),
            "requires_governance_review": bool(direct_refs or transitive_hints),
        },
    }


def load_source_policies() -> Dict[str, object]:
    return load_json(POLICIES_PATH, {})


def allowed_domains_for_category(category: str, policies: Optional[Dict[str, object]] = None) -> List[str]:
    policies = policies or load_source_policies()
    categories = policies.get("categories", {})
    category_data = categories.get(category, {})
    return list(category_data.get("allowed_domains", []))


def is_url_allowed(url: str, category: str, policies: Optional[Dict[str, object]] = None) -> bool:
    parsed = urlparse(url)
    host = (parsed.netloc or "").lower()
    if not host:
        return False
    for allowed in allowed_domains_for_category(category, policies):
        allowed = allowed.lower()
        if host == allowed or host.endswith("." + allowed):
            return True
    return False


def default_urls_for_category(category: str, policies: Optional[Dict[str, object]] = None) -> List[str]:
    policies = policies or load_source_policies()
    categories = policies.get("categories", {})
    category_data = categories.get(category, {})
    return list(category_data.get("default_urls", []))


def classify_update_signal(url: str, text: str, category: str) -> str:
    lowered = text.lower()
    host = (urlparse(url).netloc or "").lower()
    if category == "security" or any(term in host for term in ("cisa", "nvd", "advisory")):
        return "security-driven update"
    if any(term in lowered for term in ("breaking", "deprecat", "migration", "removed")):
        return "breaking change"
    if any(term in lowered for term in ("best practice", "recommended", "guidance", "should")):
        return "recommended improvement"
    if any(term in lowered for term in ("new feature", "new support", "new capability")):
        return "new best practice"
    return "noise / irrelevant"


def normalize_skill_category(value: str) -> str:
    lowered = value.strip().lower()
    if lowered in {"openai", "codex", "openai-codex"}:
        return "openai-codex"
    if lowered in {"security", "vulnerability", "vuln"}:
        return "security"
    if lowered in {"framework", "frameworks", "language", "infra", "infrastructure"}:
        return "frameworks-languages-infra"
    return lowered or "frameworks-languages-infra"


def infer_category_from_skill(skill_name: str) -> str:
    if any(token in skill_name for token in ("security", "vuln", "threat")):
        return "security"
    if any(token in skill_name for token in ("openai", "codex", "chatgpt")):
        return "openai-codex"
    return "frameworks-languages-infra"


def write_registry_entry(skill_name: str, payload: Dict[str, object]) -> None:
    registry = load_json(REGISTRY_PATH, {"governance_version": "1.0.0", "skills": {}, "updated_at": utc_now()})
    skills = registry.setdefault("skills", {})
    skills[skill_name] = payload
    registry["updated_at"] = utc_now()
    write_json(REGISTRY_PATH, registry)


def write_version_entry(skill_name: str, version: str, reason: str) -> None:
    versions = load_json(VERSIONS_PATH, {"skills": {}, "updated_at": utc_now()})
    skills = versions.setdefault("skills", {})
    history = skills.setdefault(skill_name, [])
    history.append({"version": version, "reason": reason, "updated_at": utc_now()})
    versions["updated_at"] = utc_now()
    write_json(VERSIONS_PATH, versions)


def dedupe(values: Sequence[str]) -> List[str]:
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result


def summarize_skill_inventory(root: Path = SKILLS_ROOT) -> Dict[str, object]:
    skills = []
    categories = Counter()
    for skill_dir in all_skill_dirs(root):
        info = get_skill_info(skill_dir)
        category = infer_category_from_skill(info.name)
        categories[category] += 1
        skills.append(
            {
                "name": info.name,
                "display_name": info.display_name,
                "category": category,
                "path": str(skill_dir),
            }
        )
    return {
        "generated_at": utc_now(),
        "skill_count": len(skills),
        "categories": dict(categories),
        "skills": skills,
    }
