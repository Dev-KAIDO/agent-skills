---
name: agent-workflows
description: Agent workflow methodologies — brainstorming before design, writing plans before code, test-driven development, systematic debugging, code review etiquette, verification before completion, subagent dispatching, git worktrees, and session management. Use when establishing HOW to work on any task, not WHAT to do.
---

# Agent Workflows — Complete Skill

## Overview

**Methodologies for HOW the agent works.** These are process skills, not domain skills. They enforce: think before design, plan before code, test before implementation, debug systematically, verify before claiming done.

Merges `brainstorming`, `writing-plans`, `executing-plans`, `subagent-driven-development`, `dispatching-parallel-agents`, `test-driven-development`, `systematic-debugging`, `verification-before-completion`, `receiving-code-review`, `requesting-code-review`, `finishing-a-development-branch`, `using-git-worktrees`, `writing-skills`, `using-superpowers`, `codex-session-start-router`, `codex-brainstorming-governor`, `plan-creator`, and `project-prechange-backup-guard`.

---

## 1. Session Start (بداية الجلسة)

### 1.1 Boot Sequence
```
1. Load context     → read AGENTS.md, project docs, prior session memory
2. Route the work   → identify task type (design/repair/research/build)
3. Check capability → what tools/skills are available?
4. Backup           → project-prechange-backup-guard before any mutation
5. Acknowledge      → confirm understanding with user
```

### 1.2 Task Classification
| Type | Route To | Key Skill |
|------|----------|-----------|
| New feature | Design → Plan → Build | brainstorming → writing-plans → coding |
| Bug fix | Diagnose → Fix → Verify | systematic-debugging → defect-fixer |
| Review | Analyze → Report | ui-audit, security-gate, code review |
| Research | Gather → Synthesize | web search, codebase-intelligence |
| Refactor | Map → Plan → Execute | change-impact-mapper → regression-guard |

### 1.3 Mandatory Gate Chain (سلسلة البوابات الإلزامية)
```
session-memory → repo-intake-triage → prechange-backup
    → security-gate (if auth/secrets/deps touched)
        → remediation-batch (if confirmed findings)
            → gui-orchestrator (if desktop UI touched)
```
- Each gate produces a durable artifact before the next step
- **Response contract per task type** — analysis tasks return findings, not edits; build tasks return working code + verification
- **CityOfAIAgents disclosure:** state when that system is involved
- **Flexible Skip Rule:** a gate may be skipped ONLY with explicit user approval, recorded with the reason

### 1.4 Capability Routing (توجيه القدرات)
Before invoking a tool, disclose what is actually available:
| State | Meaning | Action |
|-------|---------|--------|
| **Callable** | Tool present and enabled | Use it |
| **Enabled, cache-only** | Configured but not live this session | Disclose; offer fallback |
| **Missing** | Not installed | Request install OR use safe fallback |

- Route to currently-available capabilities first
- Never silently degrade: if a required capability is missing, say so and propose the fallback

### 1.5 Session Memory Placement (مكان ذاكرة الجلسة)
- ✅ Session memory lives in a **sibling folder** beside the project (`../<project>-session-memory/`), never inside the app root
- ✅ Keep `.codex-session-memory` (per-session notes) **separate** from `.codex-project-intel` (durable project state)
- ✅ Write memory contract files (index, summary) so the next session can resume
- ❌ Never write session artifacts into the app root (they pollute the build and get committed)

---

## 2. Brainstorming (العصف الذهني) — Before Any Creative Work

### 2.1 Rule
**No code before design approval.** This is a hard gate.

### 2.2 Process
```
1. Understand intent  → What problem are we solving?
2. Explore options    → Generate 3+ approaches
3. Ask ONE question   → At a time (not a barrage)
4. Classify scope     → light_design | full_design | decompose_first
5. Present design     → Goal, scope, risks, verification, approval
6. Get approval       → Wait for explicit yes
7. THEN start coding
```

### 2.3 Design Output Template
```markdown
## Design: [Feature Name]

**Goal:** What we're building and why
**Scope:** What's in / what's out
**Approach:** Technical approach (1-3 sentences)
**Components:** Files/modules to create or modify
**Risks:** What could go wrong
**Verification:** How we'll know it works
**Alternatives considered:** Why this approach over others
```

### 2.4 Question Strategy
- One question at a time
- Recommended answer included
- Binary when possible (yes/no)
- Converge to decision, don't explore endlessly
- If user says "you decide" → make the call and proceed

---

## 3. Writing Plans (كتابة الخطط)

### 3.1 Plan Template
```markdown
# Implementation Plan: [Feature]

## Context
[What we know, what we don't, constraints]

## Approach
[High-level strategy]

## Steps
1. [ ] Step 1 — exact file, exact change
2. [ ] Step 2 — exact file, exact change
3. [ ] Step 3 — tests
4. [ ] Step 4 — verification

## Verification
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual verification steps
- [ ] No regressions

## Risks & Rollback
- Risk: X → Mitigation: Y
- Rollback: revert commit Z
```

### 3.2 Plan Quality Checklist
- [ ] Each step names exact files
- [ ] Steps are ordered (dependencies first)
- [ ] Verification is explicit (commands, expected output)
- [ ] Risks identified
- [ ] Scope is clear (what's NOT included)
- [ ] No vague steps ("improve code" ❌ → "extract method X from file Y" ✅)

### 3.3 Interrogation Protocol (بروتوكول الاستجواب)
When requirements are ambiguous, resolve them **before** planning:
- **One question at a time**, each with a recommended answer (so the user can just confirm)
- **Ground in docs:** read the project docs and code before asking — never ask what the repo already answers
- Apply lenses: **KISS**, **YAGNI** (cut speculative features), **tracer bullet** (thin end-to-end slice first)
- Fuzzy terms ("fast", "modern", "scalable") must be replaced with concrete numbers/criteria
- Output: a plan file on disk (not just chat text)

---

## 4. Executing Plans (تنفيذ الخطط)

### 4.1 Rules
- Execute in a **separate session** from planning
- Checkpoint after each step (verify before proceeding)
- Stop and re-plan if reality diverges from plan
- Update plan checkbox as steps complete
- Document deviations from plan

### 4.2 Checkpoint Questions
After each step:
1. Did this step produce expected output?
2. Do tests still pass?
3. Is anything unexpected happening?
4. Should we continue or adjust?

---

## 5. Subagent Development (تطوير الوكلاء الفرعيين)

### 5.1 When to Use
- Task has **independent subtasks** (no shared state)
- Each subtask can be verified in isolation
- Parallel execution saves time

### 5.2 Pattern
```
1. Decompose  → break into independent tasks
2. Dispatch   → assign each to a subagent with full context
3. Monitor    → wait for completion
4. Review     → check each subagent's output
5. Integrate  → combine results
6. Verify     → run full verification
```

### 5.3 Subagent Prompt Template
```
Task: [exact task description]
Context: [relevant files, constraints, prior decisions]
Expected output: [exact deliverable]
Verification: [how to confirm it's correct]
Constraints: [what NOT to do]
```

---

## 6. Parallel Dispatching (التوزيع المتوازي)

### 6.1 Preconditions
- Tasks are **independent** (no shared state)
- No **sequential dependencies**
- Tasks won't **conflict** (different files)
- Resource availability allows parallelism

### 6.2 Dispatch Pattern
```javascript
// Conceptual
const results = await Promise.allSettled([
  taskA(),  // Independent
  taskB(),  // Independent
  taskC(),  // Independent
]);

// Verify each result independently
results.forEach((r, i) => verify(r, criteria[i]));
```

---

## 7. Test-Driven Development (TDD)

### 7.1 Cycle
```
RED      → Write a small failing test
GREEN    → Write minimum code to pass
REFACTOR → Improve code, keep tests green
REPEAT   → Next test
```

### 7.2 Rules
1. Write ONE test at a time
2. Watch it FAIL (verify it fails for the right reason)
3. Write MINIMUM code to make it pass (no extra)
4. REFACTOR while keeping all tests green
5. Never skip the RED phase

### 7.3 Test Quality
- One assertion per test (or one logical assertion)
- Descriptive name: `test_user_cannot_delete_without_permission`
- Independent: tests don't depend on each other
- Fast: unit tests < 100ms each
- Deterministic: same result every time

---

## 8. Systematic Debugging (التصحيح المنهجي)

### 8.1 Process
```
1. REPRODUCE    → exact steps to trigger the bug
2. ISOLATE      → narrow down (binary search: which line?)
3. HYPOTHIZE    → propose root cause (not just symptoms)
4. TEST         → verify hypothesis with evidence
5. FIX          → address root cause (not the symptom)
6. VERIFY       → confirm fix works AND doesn't break others
7. PREVENT      → add test to prevent recurrence
```

### 8.2 Rules
- **Never** fix without understanding root cause first
- **Never** apply multiple fixes simultaneously
- **Always** verify the fix with a test
- **Always** check if same bug exists elsewhere
- **Always** add a regression test

### 8.3 Debugging Tools
| Symptom | Tool |
|---------|------|
| Test failing | Read error, check assertion, trace |
| Runtime error | Stack trace, breakpoints, print debugging |
| Performance | Profiler, timing, memory analysis |
| Build failure | Log analysis, dependency check |
| CI failure | ci-failure-analyzer, build logs |

---

## 9. Verification Before Completion (التحقق قبل الإكمال)

### 9.1 The Golden Rule
**Run actual verification commands. Never claim success without evidence.**

### 9.2 Verification Template
```markdown
## Verification Results

| Check | Command | Expected | Actual | Status |
|-------|---------|----------|--------|--------|
| Build | `npm run build` | exit 0 | exit 0 | ✅ |
| Tests | `npm test` | all pass | 47/47 | ✅ |
| Lint | `npm run lint` | no errors | 0 errors | ✅ |
| Type check | `tsc --noEmit` | no errors | 0 errors | ✅ |

**Status: ALL PASSED**
```

### 9.3 Evidence Requirements
- **Exact command** used
- **Working directory**
- **Exit code** (0 = success)
- **Key output** (stdout/stderr summary)
- **Classification:** passed | failed | inconclusive

### 9.4 Rules
- ✅ Record exact commands and working directory
- ✅ Capture stdout/stderr summary
- ✅ Classify as: passed, failed, or inconclusive
- ❌ Don't broaden failed validation (fix the failure, don't change the test)
- ❌ Don't treat inconclusive as success

---

## 10. Code Review (مراجعة الكود)

### 10.1 Requesting Review
**When:** After completing a task, before merging
```markdown
## Review Request: [Feature Name]

**Changes:** [Files changed with brief description]
**What to check:**
- [ ] Logic correctness
- [ ] Error handling
- [ ] Security implications
- [ ] Performance impact
- [ ] Code style consistency

**Verification:** [Commands run and results]
```

### 10.2 Receiving Review
**Principles:**
- **Verify before agreeing** — don't accept feedback blindly
- **Technical rigor** — check if the comment is technically correct
- **No rubber-stamping** — disagree if the suggestion is wrong
- **Especially for vague comments** — ask for specifics

**Response format:**
```markdown
| Comment | Analysis | Action |
|---------|----------|--------|
| "Add error handling" | Valid — line 45 can throw | ✅ Added try/catch |
| "Use async/await" | Valid — cleaner than .then() | ✅ Refactored |
| "Extract to function" | Not applicable — only used once | ❌ Disagree, adds indirection |
```

---

## 11. Git Worktrees (عزل العمل)

### 1.1 When to Use
- Need to work on **new feature** without disturbing current work
- Want to **compare** two branches side by side
- Need to **isolate** experimental work

### 1.2 Setup
```bash
# Create worktree
git worktree add ../project-feature-a feature-a

# List worktrees
git worktree list

# Remove worktree (after merge)
git worktree remove ../project-feature-a
```

### 1.3 Safety Checks
- [ ] Worktree path doesn't conflict with existing directory
- [ ] Branch doesn't already have a worktree
- [ ] Sufficient disk space
- [ ] Current work is committed before switching

---

## 12. Finishing a Branch (إغلاق الفرع)

### 1.1 Pre-merge Checklist
- [ ] All tests pass
- [ ] Code review completed
- [ ] No merge conflicts (or resolved)
- [ ] Documentation updated
- [ ] Changelog updated (if applicable)
- [ ] No TODO/FIXME left unresolved

### 1.2 Options
```
Option A: Merge to main (squash)     → single commit
Option B: Merge to main (merge)      → preserves history  
Option C: Create Pull Request        → for team review
Option D: Keep as branch             → defer decision
Option E: Delete branch              → work was experimental
```

---

## 13. Backup Guard (النسخ الاحتياطي)

### 1.1 Rule
**No file mutation without backup.** This is enforced.

### 1.2 Process
```
1. Identify target files
2. Create backup copy (project-adjacent directory)
3. Write manifest (file list, timestamp, hash)
4. Verify backup integrity
5. ONLY THEN proceed with mutation
6. Keep latest 3 backups only
```

### 1.3 Backup Directory
```
.codex-prechange-backups/
├── 2026-01-01_120000/
│   ├── manifest.json
│   ├── file1.ts
│   ├── file2.ts
│   └── ...
└── (keep latest 3 only)
```

---

## 14. Writing Skills (كتابة المهارات)

### 1.1 Skill Structure
```
skill-name/
├── SKILL.md          # Required: name, description, instructions
├── references/       # Optional: deep docs loaded on demand
├── scripts/          # Optional: deterministic helpers
└── templates/        # Optional: templates for outputs
```

### 1.2 SKILL.md Frontmatter
```yaml
---
name: skill-name
description: One sentence — what it does AND when to trigger it. Front-load keywords.
---
```

### 1.3 Quality Criteria
- [ ] Description includes BOTH what and when
- [ ] Trigger keywords are front-loaded
- [ ] Instructions are step-by-step
- [ ] Verification is explicit
- [ ] No placeholder text remains
- [ ] Examples provided for key scenarios

---

## Workflow Chains (سلاسل العمل)

### Feature Development
```
brainstorming → writing-plans → executing-plans
  → test-driven-development (during coding)
  → verification-before-completion
  → requesting-code-review → receiving-code-review
  → finishing-a-development-branch
```

### Bug Fix
```
systematic-debugging → change-impact-mapper → regression-guard
  → defect-fixer → verification-before-completion
```

### Parallel Work
```
brainstorming → writing-plans → dispatching-parallel-agents
  → (each subagent) test-driven-development → verification
  → integrate → verification-before-completion
```
