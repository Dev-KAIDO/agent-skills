---
name: repair-stability
description: Complete repair and stability skill â€” defect fixing, regression prevention, stability hardening, remediation batching, risk evidence packaging, and incident recovery. Use when fixing bugs, stabilizing systems, or planning remediation work.
---

# Repair & Stability â€” Complete Skill

## Overview

**Single skill for fixing and stabilizing systems.** Merges `defect-fixer`, `regression-guard`, `stability-hardener`, `project-remediation-batch-controller`, `project-risk-evidence-packager`, `change-impact-mapper`, and `incident-investigator`.

---

## 1. Defect Fixing (Ø¥ØµÙ„Ø§Ø­ Ø§Ù„Ø¹ÙŠÙˆØ¨)

### 1.1 Repair Workflow
```
1. Diagnose     â†’ root cause (not symptoms)
2. Map impact   â†’ what else is affected?
3. Plan fix     â†’ narrow scope, explicit verification
4. Apply fix    â†’ minimal changes
5. Verify       â†’ fix works + no regressions
6. Document     â†’ before/after, evidence
```

### 1.2 Fix Plan Template
```markdown
## Repair Plan: [Bug Title]

**Symptom:** What the user sees
**Root cause:** Why it happens (file:line)
**Blast radius:** Files/tests affected by the fix
**Fix approach:** Exact change planned
**Verification commands:**
- `npm test -- --grep "specific test"`
- Manual steps: [exact clicks/inputs]
**Rollback:** How to undo if fix causes issues
```

### 1.3 Fix Quality Rules
- âœ… Fix the root cause, not the symptom
- âœ… Narrowest possible scope
- âœ… Add a regression test for the bug
- âœ… Verify related paths still work
- âŒ Don't fix multiple bugs in one commit
- âŒ Don't weaken tests to make them pass
- âŒ Don't add workarounds without TODO + issue link

---

## 2. Change Impact Mapping (خريطة تأثير التغيير)

Read-only pre-repair analysis that runs **BEFORE** regression-guard and defect-fixer.

### 2.1 What It Produces
```
Target file(s) + findings
  → Dependency-graph expansion (direct + transitive importers)
    → Test-matching expansion (which tests touch these files)
      → Excluded paths: vendor/, node_modules/, generated/, build/
        → change_impact_map.json
```

### 2.2 Rules
- ✅ **Read-only** — never edits code; it only maps
- ✅ Expand from findings, not from guesses
- ✅ Exclude vendor/generated/build paths (false blast radius)
- ✅ Sequencing: impact map → regression scope → repair plan → fix
- ❌ Never skip straight to fixing without knowing what breaks

### 2.3 Artifact Contract
```json
// change_impact_map.json
{
  "targets": ["src/billing/invoice.ts"],
  "direct_importers": ["src/api/orders.ts"],
  "transitive_importers": ["src/api/index.ts"],
  "affected_tests": ["tests/billing.test.ts"],
  "excluded": ["node_modules/", "dist/"],
  "confidence": "high"
}
```

---

## 3. Regression Guard (Ø­Ø§Ø±Ø³ Ø§Ù„Ø§Ù†Ø­Ø¯Ø§Ø±)

### 3.1 Blast Radius Mapping
```
Target file
  â†’ Direct importers (files that import it)
    â†’ Transitive importers (their importers)
      â†’ Tests covering these files
        â†’ API contracts exposed
          â†’ Deploy artifacts affected
```

### 3.2 Verification Scope
```markdown
## Verification Scope

**Must pass (blocking):**
- Unit tests for modified file
- Integration tests for modified module
- E2E tests for affected user flows

**Should pass (non-blocking):**
- Full unit test suite
- Lint + type check
- Build succeeds

**Monitoring (post-deploy):**
- Error rate for affected endpoint
- Performance metrics for modified path
```

---

## 4. Stability Hardening (ØªØ­ØµÙŠÙ† Ø§Ù„Ø§Ø³ØªÙ‚Ø±Ø§Ø±)

### 4.1 Hardening Targets
| Area | Hardening Action |
|------|-----------------|
| **Startup** | Timeout guards, config validation, graceful failure |
| **Teardown** | Cleanup listeners, close connections, clear timers |
| **Retries** | Exponential backoff, max attempts, circuit breaker |
| **Timers** | Always clear intervals/timeouts on unmount |
| **Config** | Validate on load, fallback defaults |
| **Null safety** | Guard optional chains, default values |
| **External calls** | Timeout + fallback for every external dependency |

### 4.2 Resilience Patterns
```python
# Retry with backoff
def with_retry(fn, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(base_delay * (2 ** attempt))

# Circuit breaker
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_time=60):
        self.failures = 0
        self.state = "closed"  # closed = working, open = blocked

    def call(self, fn):
        if self.state == "open":
            raise CircuitOpenError()
        try:
            result = fn()
            self.failures = 0
            return result
        except Exception:
            self.failures += 1
            if self.failures >= self.failure_threshold:
                self.state = "open"
            raise
```

### 4.3 Graceful Degradation
```
Primary service fails
  â†’ Fall back to cache (stale data OK)
    â†’ Fall back to secondary service
      â†’ Return meaningful error to user
        â†’ Log for investigation
```

---

## 5. Incident Investigation (ØªØ­Ù‚ÙŠÙ‚ Ø§Ù„Ø­ÙˆØ§Ø¯Ø«)

### 5.1 Separation of Concerns
```markdown
## Symptom vs Trigger vs Root Cause

**Symptom:** What users see (500 errors on login)
**Trigger:** What started it (deploy of v2.3.1)
**Root cause:** Why it was possible (missing validation in PR #123)
**Contributing factors:** What made it worse (no canary, no alert)
```

### 5.2 Timeline Template
```markdown
## Incident Timeline

| Time | Event | Evidence |
|------|-------|----------|
| 14:00 | v2.3.1 deployed | deploy log |
| 14:05 | Error rate spikes | monitoring dashboard |
| 14:07 | Alert fires | alert notification |
| 14:10 | Team acknowledged | incident channel |
| 14:25 | Rollback initiated | deploy command |
| 14:30 | Errors stop | monitoring dashboard |
| 15:00 | Post-mortem scheduled | calendar |
```

### 5.3 Root Cause Analysis
```
5 Whys (stop when reaching process/systemic level):

1. Why did login fail? â†’ Missing env var in production
2. Why was env var missing? â†’ Deploy script didn't copy it
3. Why didn't script copy it? â†’ Script not updated when var added
4. Why wasn't script updated? â†’ No checklist for new env vars
5. Why no checklist? â†’ Process gap (FIX THIS)
```

---

## 6. Remediation Batches (Ø¯ÙØ¹Ø§Øª Ø§Ù„Ø¥ØµÙ„Ø§Ø­)

### 6.1 Batch Structure
```markdown
## Remediation Batch: [Theme]

**Scope:** What's included / excluded
**Risk level:** Low / Medium / High
**Approval required:** Yes / No

### Batch 1 (Low Risk â€” Can Apply)
- [ ] Fix null check in utils/format.ts
- [ ] Add retry to API client
- [ ] Update dependency X to patch version

### Batch 2 (Medium Risk â€” Needs Review)
- [ ] Refactor auth middleware
- [ ] Change database query pattern

### Batch 3 (High Risk â€” Needs Approval + Tests)
- [ ] Replace payment provider SDK
- [ ] Migrate session storage

**Verification for each batch:**
- Command to run
- Expected output
- Rollback step
```

### 6.2 Batching Principles
- Small batches (1-5 changes each)
- Group by risk level
- Low risk first (quick wins build momentum)
- High risk isolated (one change per review)
- Every batch has explicit verification

---

## 7. Risk Evidence (Ø­Ø²Ù… Ø§Ù„Ø£Ø¯Ù„Ø©)

### 7.1 Evidence Package
```markdown
# Risk Evidence: [Finding Title]

**Confidence:** High / Medium / Low
**Verification status:** Verified / Unverified / Partially verified

## Finding
[What's wrong, where, why it matters]

## Evidence
- File:line references
- Command output
- Screenshot (if UI)
- Log excerpt

## Impact if Unfixed
- [Quantified: users affected, data at risk, money lost]

## Recommended Action
- [Specific fix, effort estimate, risk of fix itself]
```

### 7.2 Evidence Dedup & Classification (إزالة التكرار والتصنيف)
When packaging evidence from multiple sources:
- **Dedup by** file + title + evidence excerpt — the same finding from two agents is ONE finding
- **Classify every item:**
  | Class | Meaning | Use |
  |-------|---------|-----|
  | confirmed | Verified in repo/logs this session | Act on it |
  | memory-derived | From prior session notes | Mark provenance; re-verify before acting |
  | unverified | Reported but not seen | Never promote to confirmed |
- ✅ **Never promote unverified memory to confirmed** — re-verify or label it
- ✅ Group findings by category (security / stability / perf / docs)
- ❌ No secrets or tokens in evidence snippets — redact before writing

### 7.3 Artifact Contracts (عقود المخرجات)
| Artifact | Producer | Purpose |
|----------|----------|---------|
| `change_impact_map.json` | change-impact-mapper | Blast radius before repair |
| `diagnostic_findings.json` | system-diagnostics | Classified faults with evidence |
| `repair_plan.json` | defect-fixer | Scoped fix + verification commands |
| `verification_report.json` | regression-guard | What was run + results |
| `evidence_bundle.json` | risk-evidence-packager | Deduped, classified findings |

---

## Verification Checklist (قائمة التحقق)Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„ØªØ­Ù‚Ù‚)

- [ ] Root cause identified (not just symptom)
- [ ] Blast radius mapped (files, tests, APIs)
- [ ] Fix plan written with verification commands
- [ ] Regression test added for the bug
- [ ] Fix is narrow scope (no unrelated changes)
- [ ] All verification commands run and passed
- [ ] No new failures introduced
- [ ] Rollback plan exists
- [ ] Evidence documented (before/after)
- [ ] Related paths checked for same bug pattern
- [ ] Hardening applied for fragile areas
- [ ] Incident lessons captured (if applicable)

---

## Related Skills

- `$code-engineering` â€” for code quality and architecture
- `$testing-comprehensive` â€” for writing regression tests
- `$security-comprehensive` â€” for fixing security vulnerabilities
- `$devops-comprehensive` â€” for incident response and CI/CD
- `$agent-workflows` â€” for systematic debugging methodology
- `$database-comprehensive` â€” for database-related issues

