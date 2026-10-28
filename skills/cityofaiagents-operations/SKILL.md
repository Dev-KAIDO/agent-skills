---
name: cityofaiagents-operations
description: CityOfAIAgents operations skill — workspace analysis, workflow governance, QA validation, security hardening, documentation authoring, translation ops, session handoff, firmware gap handling, UI design ops, and read-only state snapshots. Use for CityOfAIAgents-specific workflows and enterprise governance.
---

# CityOfAIAgents Operations — Complete Skill

## Overview

**Single skill for all CityOfAIAgents workflows.** Merges all 12 `cityofaiagents-*` skills: `workspace-analysis`, `workflow-governance`, `qa-validation`, `security-hardening`, `documentation-authoring`, `translation-ops`, `session-handoff-ops`, `firmware-gap-ops`, `desktop-ui-ops`, `ui-design-ops`, `visual-gui-verification-ops`, `readonly-state-snapshot`, and `custom-repro-skill`.

---

## 1. Workspace Analysis (تحليل مساحة العمل)

### 1.1 Discovery Process
```
1. List files          → structure, key modules
2. Read project docs   → README, AGENTS.md, CLAUDE.md
3. Discover commands   → build, test, lint, run
4. Map important files → entrypoints, configs, hotspots
5. Capture assumptions → env vars, dependencies, versions
```

### 1.2 Analysis Output
```markdown
## Workspace Analysis: [Project Name]

**Type:** [Web/Mobile/Desktop/Library]
**Stack:** [Frameworks, languages, versions]
**Entrypoints:** [main files]
**Commands:**
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`

**Important files:**
- [file] — [purpose]
- [file] — [purpose]

**Assumptions:**
- [Environment variables needed]
- [External services]
- [Platform constraints]
```

---

## 2. Workflow Governance (حوكمة سير العمل)

### 2.1 Governance Model
```
Request → Approval → Bundle Planning → Comparison Gate → Dispatch → Run → Record → Monitor → Decision
```

### 2.2 Approval Levels
| Level | Criteria | Approver |
|-------|----------|----------|
| **Auto** | Read-only, no side effects | None |
| **Standard** | Small, reversible changes | User |
| **Elevated** | Large, destructive, or security-sensitive | User + Manager |
| **Blocked** | Requires explicit bypass | Never auto |

### 2.3 Run Record Template
```markdown
## Run Record: [Task]

**Requestor:** [User/Agent]
**Approval:** [Level + timestamp]
**Bundle:** [Files included]
**Verification:** [Commands + expected output]
**Dispatch:** [Assigned agent]
**Result:** [Success/Failure/Blocked]
**Evidence:** [Logs, screenshots, artifacts]
**Decision:** [Approved/Rejected/Needs revision]
```

### 2.4 Comparison Gate
```python
# Before vs After comparison
def comparison_gate(before, after):
    # Compare outputs, not just exit codes
    assert before["output"] == after["output"], "Output changed"
    assert before["side_effects"] == after["side_effects"], "Side effects changed"
    return ComparisonResult(
        equivalent=True,
        confidence=0.95,
        evidence=[before["stdout"], after["stdout"]],
    )
```

---

## 3. QA Validation (التحقق من الجودة)

### 3.1 Evidence Levels
| Level | Evidence Required |
|-------|-------------------|
| **Smoke** | Compile + startup check |
| **Screen-state** | Screenshot + element presence |
| **User-flow** | Step-by-step interaction trace |
| **Business-continuity** | Full workflow + data verification |

### 3.2 Validation Rules
- ✅ Record exact commands and working directory
- ✅ Capture stdout/stderr summary
- ✅ Classify as: passed / failed / inconclusive
- ✅ Don't mark pass with empty screenshots
- ✅ Don't treat missing credentials as success
- ❌ Don't run destructive actions on core workspace (use sandbox)
- ❌ Don't broaden failed validation (fix the failure, don't change the test)

### 3.3 Validation Template
```markdown
## Validation Report

| Check | Command | Expected | Actual | Status |
|-------|---------|----------|--------|--------|
| Build | `npm run build` | exit 0 | exit 0 | ✅ |
| Tests | `npm test` | all pass | 47/47 | ✅ |
| GUI | Launch + click | Window opens | Screenshot: ✓ | ✅ |

**Classification:** PASSED
**Confidence:** High
**Evidence:** [links to artifacts]
```

---

## 4. Security Hardening (تحصين الأمان)

### 4.1 Least Privilege Rules
- ✅ Read-only by default
- ✅ Write access only when explicitly needed
- ✅ Destructive operations require confirmation
- ✅ Secrets never in logs or commit messages
- ❌ Never weaken security for convenience
- ❌ Never bypass license checks
- ❌ Never disable encryption "temporarily"

### 4.2 Destructive Operation Safeguards
```python
def destructive_operation(target, confirm=True):
    # 1. Backup first
    backup = create_backup(target)

    # 2. Require confirmation
    if confirm:
        user_confirms = ask_user(f"About to modify {target}. Continue?")
        if not user_confirms:
            return OperationCancelled()

    # 3. Execute with rollback
    try:
        result = execute(target)
        verify(result)
        return OperationSuccess(result, backup)
    except Exception as e:
        restore(backup)  # Automatic rollback
        raise
```

---

## 5. Documentation Authoring (تأليف التوثيق)

### 5.1 Artifact Types
| Type | Format | Audience |
|------|--------|----------|
| Run evidence | Markdown | Technical |
| Operator instructions | Markdown | Ops team |
| User summary | Arabic (RTL) | End users |
| Archive notes | Markdown | Historical |
| Traceable docs | Markdown + links | Compliance |

### 5.2 Traceability Rules
```markdown
## Traceable Document

**Source:** [run-id, commit, or task-id]
**Date:** [ISO 8601]
**Author:** [Agent/User]

## Content
[Main content]

## Evidence
- [Link to run output]
- [Link to artifact]
- [Link to commit]
```

### 5.3 Evidence Discipline (انضباط الأدلة)
Core rules for honest, traceable documentation:
- ✅ **Separate confirmed evidence from interpretation** — label what you saw vs what you conclude ("The build failed" vs "The build likely failed due to a race condition")
- ✅ **Note missing evidence instead of inventing it** — "log truncated, root cause unconfirmed" beats a confident guess
- ✅ **Preserve verbatim:** commands, paths, code, IDs, dates, error strings — never paraphrase identifiers
- ✅ Route artifact types to their audience (Arabic user summaries vs English technical evidence)
- ❌ Never fabricate a run result, screenshot, or metric to complete a report

---

## 6. Translation Ops (عمليات الترجمة)

### 6.1 Rules
- ✅ Preserve verbatim: commands, paths, code, IDs, API names
- ✅ Translate prose: descriptions, explanations
- ✅ Internal docs: English (developers)
- ✅ User-facing docs: Arabic (end users)
- ❌ Never translate: code, file paths, CLI commands

### 6.2 Anti-Mojibake Checklist
- [ ] Save as UTF-8
- [ ] Arabic characters render correctly
- [ ] No encoding errors (Ã, Ø, Ù replacements)
- [ ] Code blocks remain in English
- [ ] Mixed content renders properly (Arabic + English)

### 6.3 Arabic PDF Generation
```python
import arabic_reshaper
from bidi.algorithm import get_display
from fpdf import FPDF

def ar(text):
    return get_display(arabic_reshaper.reshape(text))

pdf = FPDF()
pdf.add_font("Arial", "", "C:/Windows/Fonts/arial.ttf")
pdf.add_page()
pdf.set_font("Arial", "", 14)
pdf.multi_cell(0, 10, ar("نص عربي"), align="R")
pdf.output("arabic.pdf")

# ⚠️ Avoid mixing Arabic+English in one multi_cell > 80 chars
# Use safe_multi_cell wrapper for mixed content
```

---

## 7. Session Handoff (التسليم بين الجلسات)

### 7.1 Split-Credit Ownership
```markdown
## Session Handoff Record

**From session:** [session-id]
**To session:** [session-id]
**Timestamp:** [ISO 8601]

## State Transferred
- Current task: [description]
- Completed steps: [list]
- Remaining steps: [list]
- Blocking issues: [list]

## Ledger Items
| Item | Owner (From) | Owner (To) | Status |
|------|--------------|------------|--------|
| [task] | [agent-A] | [agent-B] | In progress |

## Timer Continuity
- Started: [timestamp]
- Elapsed: [duration]
- Remaining estimate: [duration]
- Timer preserved: Yes/No
```

### 7.2 Rules
- ✅ Explicit ownership transfer (no ambiguity)
- ✅ Ledger updated with both agents
- ✅ Timer continuity documented
- ✅ State captured before handoff
- ❌ Never leave items ownerless
- ❌ Never lose timer context

---

## 8. Firmware Gap Ops (معالجة الفجوات)

### 8.1 Gap Handling
```python
# When hardware/firmware capability is unsupported:
def handle_firmware_gap(capability, evidence):
    # 1. Preserve the gap as evidence
    gap_record = {
        "capability": capability,
        "status": "unsupported",
        "evidence": evidence,
        "detected_at": now(),
    }
    save_to_registry(gap_record)

    # 2. DON'T invent support
    # 3. DON'T claim it works
    # 4. DO document the limitation
    # 5. DO suggest alternatives (if any)

    return GapDocumented(gap_record)
```

### 8.2 Rules
- ✅ Preserve gaps as evidence
- ✅ Document limitations clearly
- ✅ Suggest workarounds (if available)
- ❌ Never invent support for unsupported hardware
- ❌ Never claim "it should work" without testing
- ❌ Never skip validation because "it's probably fine"

---

## 9. Desktop UI Ops (عمليات واجهة سطح المكتب)

### 9.1 Scope Rules
- ✅ UI-only changes (layout, styling, dialogs, polish)
- ✅ Visual bug fixes (alignment, spacing, colors)
- ✅ UX improvements (navigation, feedback)
- ❌ Never modify business logic during UI ops
- ❌ Never touch database during UI ops
- ❌ Never change licensing/security during UI ops

### 9.2 UI Brief Template
```markdown
## Desktop UI Brief

**Scope:** [UI changes only]
**Files affected:** [UI files only]
**Visual behavior:** [What changes visually]
**Risks:** [UI regression risks]
**Verification:**
- Launch app → Window opens
- Navigate → Panels switch
- Interact → Buttons respond
- Screenshot → Compare with expected
```

### 9.3 Design-Spec First (المواصفة قبل التنفيذ)
For larger UI work, produce a research-backed design spec **before** coding:
```
1. Information architecture  → screens/panels and how they nest
2. Navigation strategy       → sidebar / tabs / menus; primary vs secondary
3. Spacing grid              → base unit, margins, gutters, density
4. Components                → platform controls; native vs custom
5. Theme tokens              → bg / surface / text / accent / border / radius
6. Accessibility             → contrast, focus order, keyboard map
7. RTL / LTR                 → mirroring rules and exceptions
```
- ✅ Ground choices in cited sources: **Apple HIG**, **Fluent 2**, **Material 3**, **Nielsen heuristics**
- ✅ Destructive controls (delete / move / restore / license) are **visually isolated** and require explicit confirmation
- ✅ Preserve Windows and legacy-OS compatibility as a stated constraint
- ✅ Spec is presentation-only — never change behavior, permissions, or licensing in design work

---

## 10. Visual GUI Verification (التحقق البصري)

### 10.1 Test Levels
| Level | What to Verify |
|-------|----------------|
| **Smoke** | App launches, window appears |
| **Screen-state** | Expected elements visible |
| **User-flow** | Step-by-step interaction works |
| **Business-continuity** | Full workflow produces correct data |

### 10.2 Evidence Rules
- ✅ Screenshots for every visible claim
- ✅ Element presence verified (not just "looks right")
- ✅ Controlled environment (no other windows)
- ✅ Step traces with timestamps
- ❌ Don't mark pass with empty screenshots
- ❌ Don't treat "app launched" as full validation
- ❌ Don't run destructive actions on production workspace

### 10.3 Runner & Gate Rules (قواعد التشغيل والبوابة)
- **Runner:** `pywinauto` (Windows) drives the real app — launch, click, read element text, capture screenshots; `scripts/run_cityofaiagents_visual_gui_verification_ops.py` if present
- **Test guide language:** write GUI test guides in **English** (stable selectors and element names); user-facing summaries may be Arabic
- **Preflight:** verify **credentials and infrastructure exist** before running — missing credentials is NOT a pass, it's a blocked run
- **Stop-queue rule:** on a **confirmed** GUI failure, STOP the queue — do not continue downstream steps on a broken foundation
- **Sandbox:** run destructive flows against a sandbox workspace, never the core workspace
- **Don't mark pass** with uncontrolled windows or empty screenshots

---

## 11. Read-Only State Snapshot (لقطة الحالة)

### 11.1 Safe Inspection
```python
# Read-only operations (no side effects)
def inspect_state():
    queue_status = read_registry("queue.json")
    workspace_status = read_registry("workspace.json")
    review_status = read_registry("review.json")
    automation_status = read_registry("automation.json")

    return StateSnapshot(
        queue=queue_status,
        workspace=workspace_status,
        review=review_status,
        automation=automation_status,
        timestamp=now(),
    )

# ⚠️ Never write to audit logs, queues, monitor artifacts, or workflow state
```

### 11.2 Snapshot Template
```markdown
## State Snapshot

**Timestamp:** [ISO 8601]
**Read-only:** Yes

**Queue:** [N items, next: ...]
**Workspace:** [status]
**Review:** [pending items]
**Automation:** [running/paused]
```

---

## 12. Custom Repro Skill (إعادة الإنتاج المخصصة)

### 12.1 Reproduction Guide Template
```markdown
## Reproduction Guide: [Defect Title]

**Environment:**
- OS: [Windows/macOS/Linux + version]
- App version: [version]
- Hardware: [relevant specs]

**Setup:**
1. [Prerequisite 1]
2. [Prerequisite 2]

**Steps:**
1. [Exact step 1]
2. [Exact step 2]
3. [Exact step 3]

**Expected:** [What should happen]
**Actual:** [What actually happens]

**Evidence:**
- Screenshot: [link]
- Log: [link]
- Video: [link]

**Minimal boundary:**
- This repro requires: [minimum setup]
- This repro does NOT require: [excluded features]
```

---

## Verification Checklist (قائمة التحقق)

- [ ] Workspace analysis completed (structure, commands, assumptions)
- [ ] Workflow governance followed (approval, gate, record)
- [ ] QA evidence collected (screenshots, traces, logs)
- [ ] Security hardened (least privilege, destructive safeguards)
- [ ] Documentation traceable (source, evidence, links)
- [ ] Translation accurate (prose translated, code preserved)
- [ ] Session handoff complete (ownership, ledger, timer)
- [ ] Firmware gaps documented (not invented)
- [ ] UI ops scoped (UI-only, no logic changes)
- [ ] Visual verification evidence-based (not assumed)
- [ ] State snapshots read-only (no side effects)
- [ ] Reproduction guides minimal (clear boundary)

---

## Related Skills

- `$testing-comprehensive` — for QA validation evidence
- `$security-comprehensive` — for security hardening details
- `$documentation-comprehensive` — for artifact authoring
- `$project-management` — for workflow governance
- `$design-desktop` — for desktop UI operations
- `$repair-stability` — for incident and defect workflows
