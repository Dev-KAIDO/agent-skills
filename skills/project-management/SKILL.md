---
name: project-management
description: Complete project management skill — SDLC coordination, requirements discovery, business analysis, product management, sprint planning, backlog management, meeting-to-tasks, delivery sync, risk management, and release governance. Use for ANY project planning, tracking, or coordination work.
---

# Project Management — Complete Skill

## Overview

**Single skill for all project management.** Merges all `sdlc-*` skills, `plan-creator`, `meeting-to-backlog`, `delivery-sync`, `evidence-sync`, `change-impact-mapper`, all `project-*` skills, `linear`, and `sentry`.

---

## 1. SDLC Orchestration (تنسيق دورة الحياة)

### 1.1 Pipeline
```
Requirements → Analysis → Architecture → Development → QA → DevOps → Delivery
     ↑              ↑           ↑              ↑          ↑         ↑
sdlc-requirements sdlc-ba   sdlc-arch      sdlc-dev   sdlc-qa  sdlc-devops
     ↑
sdlc-pm-product (product strategy)
     ↑
sdlc-pm-project (execution tracking)
     ↑
sdlc-orchestrator (overall coordination)
```

### 1.2 Phase Gates
| Gate | Criteria | Approver |
|------|----------|----------|
| **G0: Idea** | Clear problem statement, target users | Product owner |
| **G1: Requirements** | Complete PRD, acceptance criteria | Product + Engineering |
| **G2: Design** | Architecture approved, UI mockups | Engineering lead |
| **G3: Ready to build** | Plan approved, estimates complete | Tech lead |
| **G4: Code complete** | All features, tests, review approved | Engineering lead |
| **G5: QA passed** | All tests pass, no P0/P1 bugs | QA lead |
| **G6: Release ready** | Deploy plan, rollback plan, monitoring | Release manager |

---

## 2. Requirements Discovery (اكتشاف المتطلبات)

### 2.0 Pre-Requirements Research (بحث ما قبل المتطلبات)
For a brand-new project, do source-backed research **before** writing requirements:
```
1. Research similar products / established patterns (web search, cited sources)
2. Classify competitors (direct / indirect / alternative approaches)
3. Produce a project-adjacent research pack (opportunities, risks, positioning)
4. Ask the user: which target platforms & OS versions must be supported?
5. THEN begin requirements discovery
```
- ✅ Cite real sources; label anything unverified
- ✅ Never invent market facts — mark gaps as "unknown, needs validation"
- This produces a research pack on disk, not just chat prose

### 2.1 Discovery Questions
```
1. What problem are we solving?
2. Who are the users? (personas)
3. What are the success metrics?
4. What are the constraints? (time, budget, tech)
5. What are the non-functional requirements? (performance, security, scale)
6. What's in scope? What's explicitly OUT of scope?
7. What are the risks?
8. What dependencies exist?
```

### 2.1b Readiness & Ambiguity Check (فحص الجاهزية)
Before planning, score the requirements:
- **Ambiguity detection:** flag vague terms ("fast", "user-friendly", "scalable") → convert to measurable criteria
- **Domain question bank:** for each unclear domain term, ask a targeted question with a recommended answer
- **Readiness gate:** requirements are ready when every ambiguity is resolved or explicitly deferred with an owner

### 2.2 Requirements Document
```markdown
# PRD: [Feature Name]

## Problem Statement
[What's broken or missing?]

## Goals (SMART)
- Specific: ...
- Measurable: ...
- Achievable: ...
- Relevant: ...
- Time-bound: ...

## User Stories
As a [persona], I want [goal] so that [benefit].

### Acceptance Criteria
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]

## Non-Functional Requirements
- Performance: p95 < 200ms
- Security: OWASP Top 10 compliant
- Availability: 99.9%
- Accessibility: WCAG 2.1 AA

## Out of Scope
- [Explicitly what's NOT included]

## Risks
| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
```

---

## 3. Business Analysis (تحليل الأعمال)

### 3.1 User Story Format
```
As a [persona]
I want [action/feature]
So that [benefit/value]

Acceptance Criteria:
Given [precondition]
When [action]
Then [expected result]
```

### 3.2 Story Estimation
| Points | Description | Time (approx) |
|--------|-------------|---------------|
| 1 | Trivial | < 2 hours |
| 2 | Small | 2-4 hours |
| 3 | Medium | 4-8 hours |
| 5 | Large | 1-2 days |
| 8 | Extra large | 3-5 days |
| 13 | Epic (split!) | 1+ weeks |

### 3.3 Priority Framework
```
MoSCoW:
Must have    → ship or don't ship
Should have  → important but not critical
Could have   → nice to have
Won't have   → explicitly not this release
```

### 3.4 Architecture Decision Records (سجلات القرارات)
When a design choice is made, record it — decisions outlive the people who made them:
```markdown
# ADR-NNN: [Decision Title]

## Status        [Proposed | Accepted | Superseded by ADR-MMM | Deprecated]
## Context       [Forces at play, constraints, NFRs involved]
## Decision      [The choice made — one sentence]
## Alternatives Considered
  - Option A — pros/cons
  - Option B — pros/cons
## Consequences  [What becomes easier/harder, follow-up work]
## NFR Mapping   [Which non-functional requirements this satisfies]
```
- Tradeoffs calculated against NFRs (latency, cost, security, maintainability) — not vibes
- Use a **tech radar** (adopt / trial / assess / hold) to track tooling choices
- One decision = one ADR; supersede, never silently edit

### 3.5 Process Mapping & Traceability (التتبع)
- **BPMN-style flowcharts** for business processes: events (start/end), tasks, gateways (decisions), lanes (actors)
- **Traceability matrix:** requirement → story → test → release. Every requirement maps to at least one test
- **Gap analysis:** current state vs desired state → list the gaps as backlog items
- **Business rules:** documented as discrete, testable statements ("orders > $500 need approval"), not buried in prose

### 3.6 Product Planning (تخطيط المنتج)
- **OKRs:** Objective (qualitative, inspiring) + 3-5 Key Results (quantitative, measurable). Grade 0.0-1.0; 0.7 = good
- **MVP cut-line scoring:** score features on (value × confidence) / effort; draw the cut-line where capacity ends
- **Market analysis:** target user, competitor alternatives, differentiation, pricing model

---

## 4. Sprint Planning (تخطيط السبرنت)

### 4.1 Sprint Structure
```
Duration: 1-2 weeks
Capacity: team_velocity × 0.8 (20% buffer)

Backlog → Select stories → Task breakdown → Sprint commitment
```

### 4.2 Sprint Board
```
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│ Backlog  │ To Do    │ In Prog  │ Review   │ Done     │
├──────────┼──────────┼──────────┼──────────┼──────────┤
│ Story 1  │ Story 4  │ Story 7  │ Story 9  │ Story 11 │
│ Story 2  │ Story 5  │ Story 8  │ Story 10 │ Story 12 │
│ Story 3  │ Story 6  │          │          │          │
└──────────┴──────────┴──────────┴──────────┴──────────┘
```

### 4.3 Daily Standup Template
```
Yesterday: [what I completed]
Today: [what I'm working on]
Blockers: [what's blocking me, or "none"]
```

---

## 5. Meeting to Backlog (اجتماع → مهام)

### 5.1 Extraction Template
```markdown
## From: [Meeting Name] — [Date]

### Decisions Made
1. [Decision] → affects [area]

### Action Items
| Action | Owner | Due | Priority |
|--------|-------|-----|----------|
| [task] | @name | date | P0/P1/P2 |

### Risks Identified
- [Risk] → [mitigation]

### Open Questions
- [Question] → [who to ask]
```

### 5.2 Decision Log & Facilitation Rules (سجل القرارات)
**Decision-log schema** (one record per decision — durable, searchable):
```json
{
  "id": "dec-014",
  "decision": "Use PostgreSQL for the orders store",
  "rationale": "relational integrity + existing team skill",
  "alternatives": ["MongoDB", "DynamoDB"],
  "decided_by": "attendees",
  "date": "2026-01-14",
  "affects": ["billing", "reporting"]
}
```
**Failure modes to avoid:**
- ❌ **Never invent owners** — if no owner was named in the meeting, mark owner as `UNASSIGNED` and list it as an open question
- ❌ Never attribute a decision to someone who didn't say it
- ✅ Facilitation signals: watch for dominant speakers, silent participants, and decisions made without the decider present (flag them)
- ✅ Separate facts (what was said) from interpretation (what you think it means)

---

## 6. Risk Management (إدارة المخاطر)

### 6.1 Risk Register
```markdown
| ID | Risk | Impact | Probability | Score | Owner | Mitigation | Status |
|----|------|--------|-------------|-------|-------|------------|--------|
| R1 | Key person leaves | High | Medium | 12 | PM | Cross-training | Active |
| R2 | API delay | Medium | High | 12 | Tech | Mock implementation | Active |
| R3 | Performance issues | High | Low | 6 | Eng | Load testing | Monitoring |
```

### 6.2 Risk Scoring
```
Score = Impact (1-4) × Probability (1-4)
1-4:   Low risk (monitor)
5-8:   Medium risk (mitigation plan)
9-12:  High risk (active mitigation)
13-16: Critical risk (escalate)
```

---

## 7. Release Governance (حوكمة الإصدار)

### 7.1 Release Types
| Type | When | Risk Level |
|------|------|------------|
| **Major** | New features, breaking changes | High |
| **Minor** | New features, backward compatible | Medium |
| **Patch** | Bug fixes only | Low |
| **Hotfix** | Critical production issue | High (urgent) |
| **Rollback** | Release caused issues | Critical |

### 7.2 Release Checklist
- [ ] All tests pass (unit, integration, e2e)
- [ ] Security scan passed
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version number bumped (semver)
- [ ] Database migration tested
- [ ] Rollback plan documented and tested
- [ ] Monitoring alerts configured
- [ ] Stakeholders notified
- [ ] Backup created
- [ ] Staged rollout planned (canary → full)

### 7.3 Semantic Versioning
```
MAJOR.MINOR.PATCH

1.0.0 → 1.0.1 (patch: bug fix)
1.0.0 → 1.1.0 (minor: new feature, backward compatible)
1.0.0 → 2.0.0 (major: breaking change)
```

---

## 8. Delivery Sync (مزامنة التسليم)

### 8.1 Sync Targets
| System | What to Sync |
|--------|-------------|
| **Linear** | Issues, projects, cycles |
| **GitHub Projects** | Issues, PRs, milestones |
| **Notion** | Docs, specs, meeting notes |

### 8.2 Sync Strategy
```
Local artifacts → Transform to tracker format → Validate → Push
                                       ↓
                              Never overwrite human changes
```

---

## 9. Evidence Sync (مزامنة الأدلة)

### 9.1 Evidence Bundle
```markdown
# Evidence: [Feature/Task Name]

## Verification Results
| Check | Command | Result |
|-------|---------|--------|
| Build | `npm run build` | ✅ exit 0 |
| Tests | `npm test` | ✅ 47/47 pass |
| Lint | `npm run lint` | ✅ 0 errors |

## Artifacts
- [ ] Screenshots
- [ ] Test reports
- [ ] Performance metrics
- [ ] Security scan results

## Classification
Status: PASSED | FAILED | INCONCLUSIVE
Confidence: High | Medium | Low
```

### 9.2 Bundle Contract & Multi-Wave Ingestion (عقد الحزمة)
```json
// evidence_bundle.json — machine-readable handoff payload
{
  "feature": "checkout-v2",
  "waves": [
    { "source": "ci",        "produced_by": "devops",     "results": [...] },
    { "source": "security",  "produced_by": "security-gate", "results": [...] },
    { "source": "qa",        "produced_by": "testing",    "results": [...] }
  ],
  "classification": "PASSED",
  "confidence": "high",
  "open_gaps": ["perf test not yet run"]
}
```
- **Multi-wave ingestion:** different roles contribute evidence at different times — merge waves, don't overwrite
- Dedup by (check, command) before aggregating
- Record **open gaps** explicitly rather than reporting a clean pass with missing evidence

---

## 10. Change Impact (تأثير التغيير)

### 10.1 Impact Mapping
```
Target file → Direct imports → Transitive imports → Tests → Deploy artifacts
     ↓
Blast radius = all files/tests/docs affected
```

### 10.2 Impact Analysis
```markdown
## Change Impact: [Change Description]

### Directly Affected
- File A (modified)
- File B (import of A)

### Indirectly Affected
- Test A1 (tests File A)
- Test B1 (tests File B)
- Component C (uses File A indirectly)

### Verification Required
- [ ] Run test suite
- [ ] Check integration points
- [ ] Verify API contracts
- [ ] Test critical user flows
```

---

## 11. Observability (المراقبة)

### 11.1 Three Pillars
| Pillar | Tool | What |
|--------|------|------|
| **Logs** | ELK, Loki, pino | Events, errors, audit trail |
| **Metrics** | Prometheus, Datadog | Rates, latencies, resources |
| **Traces** | Jaeger, Zipkin | Request flow across services |

### 11.2 Alerting Rules
```
P0 (Page):  Error rate > 5% for 5 min, Latency p99 > 5s
P1 (Ticket): Error rate > 1% for 15 min, Latency p95 > 1s
P2 (Log):   Error rate > 0.1% for 1 hour
```

---

## Verification Checklist (قائمة التحقق)

- [ ] Requirements documented and approved
- [ ] User stories have acceptance criteria
- [ ] Sprint capacity planned (with buffer)
- [ ] Risks identified and mitigated
- [ ] Release checklist completed
- [ ] Evidence collected and classified
- [ ] Stakeholders informed of status
- [ ] Backlog groomed and prioritized
- [ ] Dependencies identified and managed
- [ ] Change impacts analyzed before modifications
- [ ] Monitoring configured for new features
- [ ] Post-release verification completed
