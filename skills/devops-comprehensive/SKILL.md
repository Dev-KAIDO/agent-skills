---
name: devops-comprehensive
description: Complete DevOps skill — infrastructure automation, CI/CD pipelines, CI failure analysis, GitHub CLI workflows, incident response, release management, system diagnostics, observability, and governance. Use for ANY DevOps, CI/CD, or operational task.
---

# DevOps Comprehensive — Complete Skill

## Overview

**Single skill for all DevOps work.** Merges `engineering-devops-automator`, `sdlc-devops`, `sdlc-orchestrator`, `system-diagnostics`, `ci-failure-analyzer`, `gh-fix-ci`, `gh-address-comments`, `incident-investigator`, `release-manager`, and `project-release-update-governance`.

---

## 1. CI/CD Pipeline Design (تصميم خط الأنابيب)

### 1.1 Pipeline Stages
```
Stage 1: Lint       → fast fail on style issues (~30s)
Stage 2: Build      → compile/bundle (~1-2min)
Stage 3: Unit       → fast tests (~1-2min)
Stage 4: Integration→ API/DB tests (~3-5min)
Stage 5: Security   → SAST + dependency scan (~2min)
Stage 6: E2E        → browser tests (~5-10min)
Stage 7: Deploy     → staging/production
Stage 8: Verify     → smoke tests post-deploy
```

### 1.2 Pipeline Principles
- Fail fast (lint before tests before deploy)
- Parallelize independent stages
- Cache dependencies (node_modules, pip, docker layers)
- Artifacts between stages (build once, deploy many)
- Block deploy on failing tests
- E2E on PRs optional (run on merge to main)

### 1.3 GitHub Actions Template
```yaml
name: CI
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - run: npm run lint

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - run: npm test -- --coverage

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - run: ./deploy.sh
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

---

## 2. CI Failure Analysis (تحليل فشل CI)

### 2.1 Classification Framework
| Type | Signature | Action |
|------|-----------|--------|
| **Test bug** | Assertion failure, bad expectation | Fix test |
| **Code bug** | Real failure, logic error | Fix code |
| **Flaky** | Intermittent, passes on retry | Stabilize test |
| **Environment** | Works locally, fails in CI | Fix config |
| **Dependency** | Package install failure | Fix version/registry |
| **Timeout** | Slow test, exceeded limit | Optimize or increase timeout |
| **Infrastructure** | Runner failure, network | Re-run or escalate |

### 2.2 Analysis Process
```
1. Read the failing job log (exact step + error)
2. Classify using table above
3. Reproduce locally (same command, same env if possible)
4. Fix root cause
5. Re-run CI (verify fix)
6. Document in PR (what failed, why, how fixed)
```

### 2.3 GitHub CLI for CI
```bash
# List checks on PR
gh pr checks <pr-number>

# View failed job logs
gh run view <run-id> --log-failed

# Re-run failed jobs
gh run rerun <run-id> --failed

# Watch a run
gh run watch <run-id>
```

---

## 3. GitHub Workflows (سير عمل GitHub)

### 3.1 PR Comment Responses
```bash
# View PR comments
gh api repos/{owner}/{repo}/pulls/{pr}/comments

# Reply to a review comment
gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment-id}/replies \
  -f body="Fixed in abc123 — moved validation to service layer"
```

### 3.2 Response Etiquette
- Address every comment (even if disagreeing)
- Reference the commit that fixes it
- Ask for clarification on vague comments
- Explain why when disagreeing (technically)

### 3.3 One-Flow PR (yeet pattern)
```bash
# Stage + commit + push + create PR in one flow
gh pr create \
  --title "feat: add user authentication" \
  --body "## Changes
- Added auth middleware
- JWT token generation
- Login/logout endpoints

## Verification
- npm test: 47/47 pass
- Manual: login flow works end-to-end" \
  --base main
```

---

## 4. System Diagnostics (تشخيص النظام)

### 4.1 Diagnostic Process
```
1. Build check    → does it compile? (exact error)
2. Import check   → broken imports? (trace paths)
3. Config check   → env vars present? (validate all)
4. Runtime check  → does it start? (watch for errors)
5. Test check     → do tests pass? (classify failures)
```

### 4.2 Common Diagnostics
```bash
# Node.js
npm run build 2>&1 | grep -E "error|Error"
node --trace-warnings index.js

# Python
python -c "import myapp"  # check imports
python -m pytest -x --tb=short

# Check environment
env | grep -E "DATABASE_URL|API_KEY|SECRET"

# Port check
netstat -ano | findstr :3000
```

### 4.3 Evidence Collection
```markdown
## Diagnostic Evidence

**Command:** `npm run build`
**Working directory:** `C:/project`
**Exit code:** 1
**Error output:**
```
src/app.ts:15:3 - error TS2304: Cannot find name 'user'
```
**Classification:** Build failure — type error
**Affected files:** src/app.ts
```

---

## 5. Release Management (إدارة الإصدارات)

### 5.1 Release Types
| Type | Trigger | Process |
|------|---------|---------|
| **Patch** | Bug fix | CI + deploy |
| **Minor** | New feature | CI + staging + canary + full |
| **Major** | Breaking change | Full checklist + advance notice |
| **Hotfix** | Production P0 | Expedited, skip staging, verify immediately |

### 5.2 Release Checklist
- [ ] All tests green on main
- [ ] Security scan passed
- [ ] CHANGELOG updated
- [ ] Version bumped (semver)
- [ ] Database migration tested (if applicable)
- [ ] Rollback plan documented
- [ ] Monitoring/alerts configured
- [ ] Team notified
- [ ] Backup taken (if stateful)

### 5.3 Rollback Strategy
```bash
# Quick rollback options:
# 1. Previous deploy (fastest)
vercel rollback

# 2. Git revert (permanent fix)
git revert <bad-commit>
git push origin main  # triggers redeploy

# 3. Feature flag (instant, no deploy)
# Toggle off the feature in config/dashboard
```

---

## 6. Observability (المراقبة)

### 6.1 Three Pillars
| Pillar | Tool Examples | What It Answers |
|--------|---------------|-----------------|
| **Logs** | pino, ELK, Loki | What happened? |
| **Metrics** | Prometheus, Datadog | How often? How slow? |
| **Traces** | Jaeger, Zipkin | Where in the chain? |

### 6.2 Alert Rules
```yaml
# Alert severity levels
P0 (Page immediately):
  - Error rate > 5% for 5 minutes
  - Service down (health check fail)
  - Data loss detected

P1 (Page during work hours):
  - Error rate > 1% for 15 minutes
  - Latency p95 > 2s for 10 minutes

P2 (Create ticket):
  - Error rate > 0.1% for 1 hour
  - Disk usage > 80%
  - Certificate expiring in 14 days
```

---

## 7. Release Governance (حوكمة الإصدار)

### 7.1 Update Types
| Type | Forced? | User Action | Use Case |
|------|---------|-------------|----------|
| **Forced** | Yes | Auto-applied | Security patches |
| **Optional** | No | User prompted | New features |
| **Silent** | Yes | None | Background fixes |

### 7.2 No-Data-Loss Rules
- ✅ DB migrations backward-compatible (expand → migrate → contract)
- ✅ Feature flags for risky changes (disable without deploy)
- ✅ Canary deploys (1% → 10% → 100%)
- ✅ Automated rollback on error spike
- ❌ Never rollback DB schema (add, don't remove)
- ❌ Never deploy on Friday afternoon (without on-call)

---

## 8. Infrastructure as Code (البنية كالأكواد)

### 8.1 Terraform
```hcl
# Remote state (never local in teams)
terraform {
  backend "s3" {
    bucket         = "tfstate-prod"
    key            = "envs/prod/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "tf-locks"      # state locking
    encrypt        = true
  }
}
# Workspaces for environments
# terraform workspace new prod / select prod
```
**Rules:**
- ✅ Remote state + locking (S3+DynamoDB or Terraform Cloud)
- ✅ One workspace per environment (dev/staging/prod)
- ✅ Plan output reviewed before apply
- ❌ Never commit `.tfstate` to git

### 8.2 Container Security
```dockerfile
# Multi-stage → distroless final
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM gcr.io/distroless/nodejs20-debian12   # no shell, no package manager
WORKDIR /app
COPY --from=build /app/dist ./dist
USER nonroot
CMD ["dist/server.js"]
```
- **Gate:** run Trivy on the image before deploy — critical CVEs block
- Reference: `references/docker.md`, `scripts/validate_dockerfile.sh`

### 8.3 Secrets & Resilience
- **Vault** (or cloud secret manager) for dynamic secrets — never static keys in env files
- **PodDisruptionBudget** in Kubernetes: `minAvailable: 2` for critical deployments
- **DR runbook per service** — restore tested, not just documented (`references/infrastructure.md`)
- **Deployment risk:** `scripts/analyze_deployment_risk.py` before high-risk releases

---

## 9. Golden Signals & Runbooks (الإشارات الذهبية)

| Signal | Definition | Alert |
|--------|-----------|-------|
| **Latency** | p95/p99 response time | p95 > 1s for 10 min |
| **Traffic** | Requests per second | Sudden drop to ~0 |
| **Errors** | % non-2xx | > 1% for 15 min |
| **Saturation** | CPU/memory/queue fullness | > 85% sustained |

- ✅ **One runbook per alert** — an alert without a runbook is noise (`references/observability.md`)
- ✅ Alert on symptoms (golden signals), not causes
- ✅ Correlation IDs propagated across services for trace → log → metric chain

---

## 10. CI Evidence & Safety Gates (أدلة CI وبوابات السلامة)

### 10.1 Durable Artifacts
```json
// ci/ci_failure_report.json (produced by scripts/run_ci_failure_analyzer.py)
{
  "run_id": "...",
  "failed_step": "npm test",
  "classification": "test_bug | code_bug | flaky | environment | infra",
  "evidence_log_excerpt": "...",
  "recommended_action": "..."
}
```
- `diagnostic_findings.json` taxonomy: `references/finding_taxonomy.md`
- GH Actions specifics: debug flags, step-summary groups, reusable-workflow boundaries — `references/github_actions_evidence.md`

### 10.2 Safety Gates
- ✅ **gh-fix-ci: implement only after explicit user approval** — inspect first, never auto-fix CI
- ✅ External providers (Buildkite, CircleCI) → report the check URL only, out of scope for fixes
- ✅ Auth-scope precheck (`gh auth status`) before any gh operation
- ✅ System diagnostics are **read-only** — never mutate state while investigating

---

## Verification Checklist (قائمة التحقق)

- [ ] Pipeline stages ordered (fail fast)
- [ ] Dependencies cached in CI
- [ ] Tests block deploy on failure
- [ ] CI failures classified correctly
- [ ] Release checklist completed
- [ ] Rollback plan documented and tested
- [ ] Monitoring alerts configured
- [ ] Logs include correlation IDs
- [ ] Canary deploy used for major releases
- [ ] Post-deploy verification run
- [ ] CHANGELOG and version updated

---

## Related Skills

- `$deployment-comprehensive` — for platform-specific deploys
- `$testing-comprehensive` — for test automation in CI
- `$security-comprehensive` — for security scanning
- `$repair-stability` — for incident recovery
- `$database-comprehensive` — for migration safety
- `$project-management` — for release governance process
