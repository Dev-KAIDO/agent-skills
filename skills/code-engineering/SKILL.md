---
name: code-engineering
description: Complete code engineering skill — senior development practices, codebase intelligence, architecture analysis, dependency management, performance auditing, refactoring, scaffolding (CLI/Next.js), prototyping, and code quality. Use for ANY code architecture, review, or improvement task.
---

# Code Engineering — Complete Skill

## Overview

**Single skill for all code engineering work.** Merges `engineering-senior-developer`, `engineering-frontend-developer`, `engineering-rapid-prototyper`, `codebase-intelligence`, `architecture-guardian`, `dependency-governor`, `performance-auditor`, `future-risk-forecast`, `project-frontend-architecture-builder`, `project-operations-ledger`, `repo-intake-triage`, `sdlc-dev`, `frontend-builder`, `cli-creator`, `scaffold-cli`, and `scaffold-nextjs`.

---

## 1. Codebase Intelligence (ذكاء قاعدة الكود)

### 1.1 Analysis Process
```
1. Framework detection  → package.json, requirements.txt, go.mod
2. Entrypoint mapping   → main files, routers, index files
3. Dependency tracing   → imports, module boundaries
4. Hotspot discovery    → most-edited, most-imported files
5. Risk surface         → security-sensitive paths, business logic
```

### 1.2 Architecture Rules
- **Dependency direction:** high-level modules don't import low-level details
- **No cycles:** module A → B → C → A is forbidden
- **Hub detection:** files imported by >20 others = review for splitting
- **Boundary leaks:** internal utilities imported across domains

---

## 2. Architecture Guardian (حارس المعمارية)

### 2.1 Import Graph Checks
```bash
# Detect cycles
npx madge --circular src/

# Find circular dependencies
npx dpdm --circular src/index.ts

# Detect unused exports
npx ts-prune
```

### 2.2 Layer Rules
```
routes/     → calls services/ only
services/   → calls repositories/ + external APIs
repositories/ → calls database/ only
domain/     → no framework imports (pure logic)
```

### 2.3 File Size Monitoring
| File Size | Action |
|-----------|--------|
| < 300 lines | OK |
| 300-500 lines | Consider splitting |
| 500-1000 lines | Should split (extract modules) |
| 1000+ lines | Split immediately (hub risk) |

---

## 3. Dependency Management (إدارة الاعتماديات)

### 3.1 Drift Detection
```bash
# npm
npm outdated
npm audit

# Check unused
npx depcheck

# Python
pip list --outdated
pip-audit

# Check lockfile presence
ls package-lock.json yarn.lock pnpm-lock.yaml
```

### 3.2 Risk Heuristics
| Signal | Risk |
|--------|------|
| No lockfile | Unreproducible builds |
| Version drift (package.json vs lock) | Supply chain risk |
| > 6 months since last release | Abandoned dependency |
| Weekly downloads < 1000 | Low maintenance |
| No repository link | Unverifiable |
| > 500 dependencies | Too many attack surfaces |

### 3.3 Upgrade Strategy
```
1. Patch versions   → auto-upgrade (safe)
2. Minor versions   → review changelog, upgrade
3. Major versions   → plan migration, test thoroughly
4. Abandoned deps   → find alternatives
```

---

## 4. Performance Auditor (مدقق الأداء)

### 4.1 Performance Smells
| Pattern | Detection |
|---------|-----------|
| Slow tests | Test suite > 5 minutes |
| Large files | > 500 lines |
| Nested loops | `for` inside `for` inside `for` |
| Loop-scoped I/O | `await`/`fetch` inside loop without batching |
| N+1 queries | Repeated queries in loops |
| Unbounded queries | `SELECT *` without `LIMIT` |

### 4.2 Optimization Priority
```
1. Database queries  → biggest impact (indexing, batching)
2. API calls         → parallelize, cache, batch
3. Frontend bundle   → code split, lazy load
4. Computation       → memoize, worker threads
```

---

## 5. Senior Development Practices (ممارسات تطوير متقدمة)

### 5.1 Code Review Checklist
- [ ] Logic correct (edge cases covered)
- [ ] Error handling comprehensive
- [ ] No security vulnerabilities
- [ ] Performance impact acceptable
- [ ] Code style consistent
- [ ] Tests included
- [ ] Documentation updated
- [ ] No dead code left behind

### 5.2 Refactoring Rules
```
1. Never refactor without tests
2. One step at a time (small commits)
3. Run tests after each change
4. No behavior changes (pure refactor)
5. Update all callers
```

### 5.3 Rapid Prototyping (MVP)
```markdown
## Prototype Scope
- Core feature only (no edge cases)
- Hard-coded data (no real backend)
- Single platform (usually web)
- 2-4 hours max

## Quality Bar
- Works end-to-end (click through)
- Shows the idea (not pixel-perfect)
- Throws away after validation
```

**Hypothesis template (hour 0):**
> "We believe [user] will [action] because [reason], measured by [metric]."

If you cannot write this sentence, you are not ready to build.

**Hard caps (scope rules — from `engineering-rapid-prototyper`):**
| Cap | Limit | If exceeded |
|-----|-------|-------------|
| Database tables | ≤ 5 | cut scope or simplify the data model |
| Features | 3-5 | rank by hypothesis impact, cut the bottom ones |
| Pages/routes | ≤ 8 | combine views or cut features |
| Custom UI components | 0 | use shadcn/ui, Radix, or similar; simplify design to fit |
| Backend logic | CRUD + 1 business rule | mock complex processing with a fake-data endpoint |
| Optimization | none | caching, CDN, indexes, code splitting are production concerns |

**Instant stack:**
- Auth: Clerk or NextAuth — never build custom auth for a prototype; skip entirely if the hypothesis doesn't need accounts
- Database: Prisma + Supabase (JSON file / localStorage if < 100 records)
- Deploy: Vercel — first deploy must happen within 2 hours of project start
- UI: shadcn/ui + react-hook-form + Zod; State: Zustand only if client state is needed (prefer server components + server actions)

**Kill criteria (stop immediately):**
- Setup (init → first deploy) > 3 hours → the stack is too complex; switch
- After 2 days the core hypothesis is untestable → redesign the prototype, not the hypothesis
- A single feature > 1 day → too complex; simplify or fake it with static data
- Writing tests → you left prototype mode (prototypes are disposable)
- Never iterate on a prototype > 1 week → rebuild for production or archive it

**Workflow timeline:**
```
Hour 0-2:   hypothesis + scaffold + shadcn/ui + deploy empty shell to Vercel
Hour 2-8:   core flow end-to-end (entry → action → result); deploy on day 1
Hour 8-20:  2-4 supporting features, deploy after each; add feedback mechanism
Hour 20-24: share with 5-10 users, measure metric, decide: build / pivot / kill
```

References: `references/stack-setup.md`, `references/code-examples.md`, `references/full-stack-integration.md`, `references/ui-patterns.md`; scaffold helper: `scripts/scaffold.sh`.

### 5.4 Coding Standards, SOLID & Unit Tests (sdlc-dev)

**SOLID principles:**
| Principle | Rule |
|-----------|------|
| Single Responsibility | One reason to change per class/module |
| Open/Closed | Extend by adding code, not modifying existing code |
| Liskov Substitution | Subtypes must be substitutable for their base types |
| Interface Segregation | Small, specific interfaces over fat ones |
| Dependency Inversion | Depend on abstractions, not concrete implementations |

**Design patterns rule:** compare at least two options before choosing a default pattern; document why the chosen pattern fits the stated constraints; call out operational and quality tradeoffs, not only design benefits.

**Unit-test generation:** generate unit-test cases from user stories or function lists — `scripts/generate_unit_tests.py`.

**Coverage analysis:** calculate simple coverage progress from status items — `scripts/calculate_coverage.py`.

**Coding-standards enforcement:** validate implementation notes align with coding standards — `scripts/enforce_coding_standards.py`; language standards in `references/coding_standards/{javascript,python,shell,sql}.md`. Additional helpers: `scripts/run_code_review.py` (structured review checklist), `scripts/generate_code_structure.py`, `scripts/generate_api_docs.py`, `scripts/validate_conventions.py`.

**Handoff contract:** inputs `architecture_review.json` + `user_stories.json` → outputs `implementation_plan.json`, `unit_test_plan.json`, `api_docs_outline.md`. Stop and request clarification when a required upstream artifact is missing or contradictory; never hand off vague artifacts — record open issues inside the output itself. References: `references/solid_principles.md`, `references/design_patterns.md`, `references/clean_code.md`, `references/testing_best_practices.md`, `references/api_design_guidelines.md`.

---

## 6. Scaffolding (إنشاء المشاريع)

### 6.1 CLI Project (TypeScript)
```bash
# Structure
my-cli/
├── src/
│   ├── index.ts        # entrypoint
│   ├── commands/       # one file per command
│   ├── lib/            # shared utilities
│   └── types.ts        # shared types
├── tests/
├── package.json
├── tsconfig.json
└── README.md

# Key decisions
- ESM (import/export) not CommonJS
- commander.js for CLI parsing
- tsdown/esbuild for bundling
- vitest for testing
- oxlint for linting
```

**Composable command design (cli-creator):**
- Design first-pass commands in order: **Discover** containers (accounts, projects, repos) → **Resolve** names/URLs/slugs to stable IDs → **Read** exact objects → **Context** around an anchor.
- Write commands do one named action each (create, update, delete, upload, retry) and accept the narrowest stable resource ID; support `--dry-run`/`draft`/`preview` first. Never hide writes inside broad `fix`, `debug`, or `auto` commands.
- Every CLI needs: `--help` listing all capabilities, `--json doctor` (verifies config, auth, version, endpoint reachability), and a raw escape hatch (`request get ...`, reads first).
- Install convention: personal tools live under `~/code/clis/<tool-name>`; check `command -v <tool-name>` before scaffolding; install on PATH and smoke test **from another directory**, not only via `cargo run` or package-manager wrappers.

**Runtime selection:** Rust (durable default — one fast binary: clap/reqwest/serde) · TypeScript/Node (when the official SDK or auth helper is the reason) · Python (data/SQLite/notebook-heavy sources). State the choice in one sentence, with reason, before scaffolding.

**Auth precedence:** 1) env var (`GITHUB_TOKEN`), 2) `~/.<tool-name>/config.toml`, 3) token flag only for one-off tests (flags leak into shell history/process listings). Never print full tokens; `doctor --json` reports the auth source category (`flag`/`env`/`config`/missing) and the missing setup step.

**JSON output contract:** JSON to stdout only; progress/diagnostics to stderr; documented success AND error shapes; machine-readable errors with no credentials; exit 0 on success (including empty result), nonzero on auth/network/parse/API failure. Return `next_cursor`/`offset` for paginated lists with bounded `--limit`.

**Production scaffold (scaffold-cli):** ESM only (`"type": "module"`), Node 22+, dual tsdown build (CLI with shebang + library with dts — kept separate), changesets for versioning, GitHub Actions (`ci.yml` + `npm-publish.yml`), `AGENTS.md` + `skills/<bin>/SKILL.md` agent skill definition (symlink `CLAUDE.md` → `AGENTS.md`). After scaffolding: run the full post-scaffold command sequence (install, lint, typecheck, tests) and validate every checklist item — use `ultracite check`/`ultracite fix`, never call oxlint/oxfmt directly; lefthook hooks are set up automatically. No CommonJS, no chalk/ora (use `node:util` styleText + `@clack/prompts`), no test files in the scaffold. References: `references/agent-cli-patterns.md`, `references/scaffold-configs.md`, `references/scaffold-source.md`, `references/post-scaffold.md`.

### 6.2 Next.js Project (App Router)
```bash
# Structure
my-app/
├── app/                    # App Router
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Homepage
│   ├── (auth)/             # Route group
│   └── api/                # API routes
├── components/             # Shared components
├── lib/                    # Utilities
├── public/                 # Static assets
├── tailwind.config.ts
└── next.config.js

# Key decisions
- Server Components by default
- "use client" only when needed (state, effects, browser APIs)
- Server Actions for mutations (not API routes when possible)
- Tailwind CSS v4
- shadcn/ui for components
```

**Data & state stack (frontend-builder):**
| Concern | Choice |
|---------|--------|
| Server state | TanStack Query (client) / Server Components + Server Actions (server); `revalidatePath` for cache |
| Client state | Context API (theme, auth), Zustand (complex state) — avoid Context for frequently changing values |
| Forms | React Hook Form + Zod schema validation, or Server Actions + `useActionState` + `useOptimistic` |
| Errors | Error boundaries per route (`error.tsx`) wrapping feature sections, not individual components |
| Streaming | Suspense for streaming; `React.lazy()` / `next/dynamic` for code splitting |
| Styling | Tailwind CSS v4 CSS-first `@theme` config (no `tailwind.config.js`), shadcn/ui, OKLCH colors |

**Common mistakes to reject in review:**
| Mistake | Correct pattern |
|---------|-----------------|
| `'use client'` on every component | Server Components by default; client only at interactive leaf nodes |
| `useEffect` to compute derived data | `useMemo` for derived values; `useEffect` only for side effects |
| All state lifted to the tree top | Keep state as close to where it's consumed as possible |
| API routes for simple mutations | Server Actions with `'use server'` |
| Non-serializable props across the server/client boundary | Props must be serializable (no functions, classes) |
| Fetching in Client Components when Server Components suffice | Fetch in Server Components; TanStack Query only for client-side caching |

Deep references: `references/component-architecture.md`, `references/server-components.md`, `references/state-management.md`, `references/data-fetching.md`, `references/forms.md`, `references/styling.md`, `references/performance-and-errors.md`.

**Next.js scaffold (scaffold-nextjs):** turborepo with `apps/web/`, Blode UI components from the `ui.blode.co` registry, `blode-icons-react` for icons (never `lucide-react`), Ultracite/Oxlint/Oxfmt (no ESLint), `knip.json`, `reactCompiler: true`. 8-phase workflow: 1 gather info → 2 `create-next-app` → 3 Blode UI registry → 4 Agentation → 5 Ultracite → 6 convert to turborepo → 7 GitHub + Vercel → 8 pre-launch (favicon, OG images). App dependencies go in `apps/web/package.json`; the root keeps only devDependencies (turbo, ultracite). References: `references/app-setup.md`, `references/turbo-configs.md`, `references/deploy-and-launch.md`.

---

## 7. Future Risk Forecast (التنبؤ بالمخاطر)

### 7.1 Risk Signals
```python
# Predict future fragility
risk_signals = {
    "test_coverage": "Low coverage + high churn = future bugs",
    "file_churn": "Files edited often = need tests + review",
    "ownerless_paths": "No one owns a module = unmaintained",
    "todo_density": "High TODO/FIXME count = tech debt",
    "dependency_count": "Many deps = attack surface + upgrade burden",
}
```

### 7.2 Risk Response
| Signal | Response |
|--------|----------|
| High churn + no tests | Write tests first |
| Ownerless module | Assign owner or archive |
| TODO pile | Schedule tech debt sprint |
| Large files | Split incrementally |

---

## 8. Frontend Architecture (معمارية الواجهات)

From `project-frontend-architecture-builder`. Inspect existing routes, components, state, API clients, theme tokens, tests, and conventions **before** proposing structure. Keep UI architecture aligned with product flows, API contracts, authorization, accessibility, and localization. Avoid broad rewrites unless the current structure blocks the requested change.

### 8.1 Architecture Checklist
- Framework and rendering model
- Route and layout strategy
- Component ownership and reuse boundaries
- State source of truth
- Form and validation pattern
- API client and error handling
- Auth and role visibility
- Accessibility and keyboard behavior
- i18n/RTL behavior
- Test layers and verification commands

### 8.2 Decision Rules
| Decision | Rule |
|----------|------|
| Framework | Don't assume React/Vue/Angular/Svelte/Flutter/native UI before inspecting the project |
| State management | No state manager or UI library without evidence it is needed (Context/Zustand/Redux each have a cost) |
| Routing | Route groups and layouts mirror product flows; keep one source of truth for navigation |
| Forms | One schema-based validation pattern shared by client and server |
| i18n / RTL | Translation keys separated from display logic; layout must survive `dir="rtl"` |
| API client | Centralized client layer: auth headers, error normalization, typed responses, retry/timeout policy |
| Authorization | Never hide backend authorization gaps behind frontend-only checks |
| Accessibility | Never sacrifice accessibility for visual polish |

### 8.3 Frontend Test Planning
Plan tests at the right level, per feature:
```
unit (pure logic) → component (Testing Library) → integration (API contract)
  → visual (Playwright screenshots) → a11y (axe) → e2e (Playwright flows)
```
Reference: `references/frontend-architecture-guide.md` (framework + testing/quality doc links).

---

## 9. Project Operations Ledger (سجل عمليات المشروع)

Durable memory/status layer for a target repository under `.codex-project-intel/` at the repository root (from `project-operations-ledger`). Resolve the target repository path explicitly, initialize the folder if missing, and return the exact artifact paths downstream skills should read.

| File | Contract | When to create/update |
|------|----------|----------------------|
| `project_memory.md` | Human-readable durable notes | When durable project facts change (architecture, conventions, verified commands) |
| `project_intelligence.json` | Machine-readable repository summary | Refresh when language mix or manifests change |
| `operations_log.jsonl` | Append-only operations events | Append before/after every diagnostics or remediation run |
| `progress_state.json` | Current snapshot of completed and pending work | At each phase transition |
| `decision_log.md` | Readable, chronological decisions | When a real decision is made — never retroactively |

Rules:
- Downstream skills may replace only their own artifact slices, not the entire project-intel tree.
- Don't invent findings or risks here — this layer establishes memory, state, and logging only.
- Never overwrite downstream diagnostics blindly; append events and merge state carefully.
- Don't point the ledger at a non-repository path by accident; the target root must be explicit.

Script: `scripts/run_project_operations_ledger.py`; reference: `references/project_intel_contract.md`.

---

## Verification Checklist (قائمة التحقق)

- [ ] Architecture rules documented (layers, boundaries)
- [ ] No circular dependencies (madge check)
- [ ] All dependencies have lockfiles
- [ ] No critical vulnerabilities (npm audit)
- [ ] No unused dependencies (depcheck)
- [ ] File sizes within limits (< 500 lines)
- [ ] No nested loops > 2 levels
- [ ] No N+1 database queries
- [ ] Tests cover critical paths
- [ ] Code review checklist applied
- [ ] Performance hotspots identified
- [ ] Refactoring done in small steps
- [ ] Scaffolding follows project conventions

---

## Related Skills

- `$backend-comprehensive` — for server-side implementation
- `$testing-comprehensive` — for test strategy
- `$database-comprehensive` — for data layer design
- `$repair-stability` — for fixing bugs
- `$devops-comprehensive` — for CI/CD integration
- `$agent-workflows` — for development methodology
