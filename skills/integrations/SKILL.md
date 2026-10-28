---
name: integrations
description: Complete integrations skill — Linear, Notion, Sentry, GitHub CLI, Slack, skill management (registry, installer, forge), API integrations (Claude, ChatGPT Apps), and third-party service connections. Use for connecting to ANY external service or managing skills.
---

# Integrations — Complete Skill

## Overview

**Single skill for all external service integrations and skill management.** Merges `linear`, all `notion-*` skills, `sentry`, `gh-*` skills, `yeet`, `claude-api`, `chatgpt-apps`, all `skill-*` skills, `slack-gif-creator` (Slack context), and `delivery-sync`.

---

## 1. Linear (إدارة المشاريع)

### 1.1 Core Operations
| Task | Action |
|------|--------|
| Create issue | `linear.createIssue(title, description, priority)` |
| Update status | `linear.updateIssue(id, { state })` |
| Assign | `linear.assignIssue(id, userId)` |
| Comment | `linear.createComment(issueId, body)` |
| List cycles | `linear.listCycles()` |
| Link PR | `linear.linkPullRequest(issueId, prUrl)` |

### 1.2 Sync Pattern (Local → Linear)
```python
# 1. Read local artifacts
backlog = read_json("backlog.json")
sprint_plan = read_sprint_plan()

# 2. Transform to Linear format
issues = []
for item in backlog:
    issues.append({
        "title": item["title"],
        "description": item["description"],
        "priority": item["priority"],     # 0-4
        "estimate": item["points"],
        "cycleId": sprint_plan["cycle_id"],
    })

# 3. Validate (never overwrite human changes)
for issue in issues:
    existing = linear.findIssue(title=issue["title"])
    if existing:
        log.warning(f"Skipped (exists): {issue['title']}")
        continue
    linear.createIssue(**issue)
```

### 1.3 Sync Rules
- ✅ Never overwrite human-created/edited issues
- ✅ Validate before pushing (dry-run first)
- ✅ Preserve existing assignees/labels
- ✅ Use idempotent operations (check before create)
- ❌ Never delete issues (archive instead)
- ❌ Never bulk-modify without confirmation

---

## 2. Notion (قواعد المعرفة)

### 2.1 Four Operations
| Operation | Skill | Action |
|-----------|-------|--------|
| Knowledge capture | `notion-knowledge-capture` | Create structured page |
| Meeting prep | `notion-meeting-intelligence` | Research + agenda |
| Research docs | `notion-research-documentation` | Multi-source synthesis |
| Spec → tasks | `notion-spec-to-implementation` | Convert to plan |

### 2.2 Page Structure
```markdown
# [Page Title]
> Context: why this page exists

## Summary
[2-3 sentences: what this page covers]

## Details
[Main content with headings, lists, tables]

## Related
- [[Related Page 1]]
- [[Related Page 2]]

## Last Updated
[Date]
```

### 2.3 Notion API Patterns
```python
# Create page
notion.pages.create(
    parent={"database_id": db_id},
    properties={"Name": {"title": [{"text": {"content": "New Page"}}]}},
    children=[
        {"object": "block", "type": "heading_1",
         "heading_1": {"rich_text": [{"text": {"content": "Overview"}}]}},
        {"object": "block", "type": "paragraph",
         "paragraph": {"rich_text": [{"text": {"content": "Content here"}}]}},
    ]
)

# Search
results = notion.search(query="meeting notes", filter={"property": "object", "value": "page"})
```

---

## 3. Sentry (مراقبة الأخطاء)

### 3.1 Setup & Auth (إعداد المصادقة)
```bash
curl https://cli.sentry.dev/install -fsS | bash   # install
sentry auth login                                  # authenticate (or set SENTRY_AUTH_TOKEN)
sentry auth status                                 # confirm
sentry schema <resource>                           # discover available endpoints quickly
```
- The CLI **auto-detects org/project** from DSNs in `.env` files, source code, and config files
- If auto-detection fails, pass explicitly: `sentry issue list my-org/my-project`
- ⚠️ Use the **`sentry`** CLI (not the legacy `sentry-cli` command)

### 3.2 Read-Only Queries (استعلامات للقراءة فقط)
```bash
# List issues (always --json when processing programmatically)
sentry issue list \
  --json --fields shortId,title,priority,level,status

# View one issue
sentry issue view ABC-123 --json

# Issue events
sentry issue events ABC-123 --limit 20 --json

# Specific event
sentry event view my-org/my-project/{event_id} --json
```
- **Always `--json`** for programmatic use; add `--fields` to trim payload size
- This skill is **read-only** — never mutate Sentry state (no resolving/deleting)

### 3.3 Issue Triage
```python
def classify_sentry_issue(issue):
    if issue.level == "fatal":
        return "P0 — page immediately"
    if issue.level == "error" and issue.count > 100:
        return "P1 — investigate today"
    if issue.level == "error" and issue.count > 10:
        return "P2 — investigate this week"
    return "P3 — backlog"
```

---

## 4. GitHub CLI (أدوات GitHub)

### 4.1 PR Workflow
```bash
# One-flow PR (stage + commit + push + create PR)
git add -A
git commit -m "feat: description"
git push -u origin feature-branch
gh pr create --fill  # title/body from commit

# Address comments
gh pr checks <pr>                    # view checks
gh pr comment <pr> --body "Fixed"    # reply
gh pr review <pr> --approve          # approve
gh pr merge <pr> --squash            # merge
```

**One-flow ("yeet") specifics:**
- Branch naming: short, descriptive (e.g. `fix/checkout-tax`)
- Draft PR first, then promote: `GH_PROMPT_DISABLED=1 gh pr create --draft` avoids the interactive editor
- Long PR body → write to a temp file: `gh pr create --body-file pr-body.md`
- If auth fails mid-flow: `gh auth login`, then retry the same step (idempotent)

### 4.2 Linear & Notion MCP (إعداد MCP)
```bash
# Add MCP servers (Claude/opencode config equivalent)
codex mcp add linear    # Linear issues/projects
codex mcp add notion    # Notion pages/databases
```
- **Auth:** OAuth flow on first use; complete it once, tokens persist
- **Linear:** list/create issues, update status, manage projects — route backlog work here
- **Notion:** `notion-search` → `notion-fetch` → `create-pages`. Use for wiki, meeting notes, research
- **Notion discipline:** cite sources when researching; link spec → plan → tasks so traceability survives; meeting prep uses templates, not freeform

### 4.2 CI Debugging
```bash
gh run list --limit 5               # recent runs
gh run view <run-id> --log-failed   # failed job logs
gh run rerun <run-id> --failed      # re-run failed
gh run watch <run-id>               # watch live
```

### 4.3 Issue Management
```bash
gh issue list --label bug
gh issue create --title "Bug: ..." --body "..."
gh issue close <n> --comment "Fixed in #123"
```

---

## 5. Claude API (واجهة برمجية كلاود)

### 5.1 Model Lineup (النماذج الحالية)
> ⚠️ Use these exact model ID strings — they are complete identifiers.

| Model | Model ID | Context | Input $/M | Output $/M |
|-------|----------|---------|-----------|------------|
| Claude Fable 5 | `claude-fable-5` | 1M | $10.00 | $50.00 |
| Claude Opus 4.8 | `claude-opus-4-8` | 1M | $5.00 | $25.00 |
| Claude Opus 4.7 | `claude-opus-4-7` | 1M | $5.00 | $25.00 |
| Claude Opus 4.6 | `claude-opus-4-6` | 1M | $5.00 | $25.00 |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 1M | $3.00 | $15.00 |
| Claude Haiku 4.5 | `claude-haiku-4-5` | 200K | $1.00 | $5.00 |

**Default: `claude-opus-4-8`** unless the user explicitly names another model.
- **Fable 5:** thinking always on (omit the `thinking` param); new tokenizer → ~30% more tokens for same content vs older models
- **Thinking:** Opus 4.8/4.7/4.6, Sonnet 4.6 use `thinking: {type: "adaptive"}`
- **Effort parameter:** GA (no beta header) — controls thinking depth/token usage
- For deep reference work, read the original `claude-api` skill before heavy use.

### 5.2 Core Patterns
```python
from anthropic import Anthropic
client = Anthropic()

# Text generation
message = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
)

# Streaming
with client.messages.stream(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user", "content": "..."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# Tool use
tools = [{
    "name": "get_weather",
    "description": "Get current weather",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
    },
}]
```

### 5.3 Cost Controls (ضوابط التكلفة)
- **Prompt caching:** mark stable prefix blocks with `cache_control` — cache reads are far cheaper than re-sending
- **Token counting:** use the count_tokens endpoint before sending very long prompts
- **Model routing:** Haiku 4.5 for high-volume/simple classification; Opus for hard reasoning only
- **Batches API:** for non-real-time bulk work (`/v1/messages/batches`) — lower cost, async results
- ❌ Never send a 1M-context prompt when the task fits in 20K

---

## 6. ChatGPT Apps (تطبيقات شات جي بي تي)

### 6.1 Architecture
```
MCP Server (tools + resources)
    ↓
Widget UI (HTML/JS in iframe)
    ↓
ChatGPT (host application)
```

### 6.2 Key Metadata
```json
{
  "openapps": {
    "name": "my-app",
    "description": "App description",
    "version": "1.0.0",
    "csp": {
      "connect": ["https://api.example.com"],
      "script": ["'self'"],
    }
  }
}
```

---

## 7. Skill Management (إدارة المهارات)

### 7.1 Skill Lifecycle
```
Authored (local) → Reviewed → Published (registry) → Installed (global)
```

### 7.2 Registry Operations
```bash
# List available skills
skill-registry list

# Validate metadata
skill-registry validate skill-name

# Sync from source
skill-registry sync

# Install skill globally
skill-installer install skill-name
```

### 7.3 Skill Authoring (Forge)
```bash
# Design new skill
skill-forge design --name new-skill --description "..."

# Improve existing
skill-forge improve existing-skill

# Quality audit
skill-forge audit existing-skill
```

### 7.4 Skill Update Governance
```
1. Review update request (scope check)
2. Analyze downstream impact
3. Verify verification requirements
4. Approve / Reject / Request changes
5. Apply changes (with backup)
6. Validate after changes
```

### 7.5 Artifact Cleanup (تنظيف المخرجات) — safety protocol
Generated artifacts (`__pycache__/`, `*.pyc`, caches) can be cleaned, but only with evidence:
- ✅ **Backup manifest first** — a verified full-project backup manifest must exist before any deletion
- ✅ **Dry-run is the default** — plan the deletion and report; never delete on first pass
- ✅ Require explicit confirmation flag (`--confirm DELETE_GENERATED_ARTIFACTS`) to execute
- ✅ Keep only the latest N owned backup operations (default 3)
- ❌ Block deletion entirely if backup evidence is missing

### 7.6 Knowledge Refresh (تحديث المعرفة)
Pull fresh, authoritative knowledge into a skill **without editing the skill directly**:
- ✅ **Source allowlist** — only official docs/advisories/guidance; never blogs or guesses
- ✅ **Classify the signal** — breaking change / deprecation / new feature / correction
- ✅ Produce a **scoped update request** (what changes, why, evidence, verification) — a human approves before the skill is edited
- ❌ Never silently rewrite a skill from unverified news

### 7.7 Quality Audit (تدقيق الجودة)
Score skills on: trigger quality, instruction clarity, resource design, determinism, validation strength, update safety. Weak triggers ("useful for X") → strong triggers ("use when [concrete condition]"). Never edit a shared/sensitive skill without an impact analysis (what references it, what breaks).

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
Local artifacts
    → Transform to tracker format
    → Validate (dry-run)
    → Push (idempotent)
    → Verify (read-back)
```

### 8.3 Sync Rules
- ✅ Never overwrite human changes
- ✅ Preserve existing metadata
- ✅ Validate before pushing
- ✅ Log every sync operation
- ❌ Never delete remote items
- ❌ Never bulk-modify without confirmation

---

## Verification Checklist (قائمة التحقق)

- [ ] API credentials configured (env vars, not hardcoded)
- [ ] Sync operations idempotent (safe to re-run)
- [ ] Human changes preserved (no overwrites)
- [ ] Dry-run completed before push
- [ ] Read-back verification done
- [ ] Errors handled gracefully (retry, fallback)
- [ ] Rate limits respected
- [ ] Costs estimated before API calls
- [ ] Local artifacts backed up before sync
- [ ] Sync operations logged

---

## Related Skills

- `$backend-comprehensive` — for building integration APIs
- `$security-comprehensive` — for API security and secrets
- `$documentation-comprehensive` — for Notion page content
- `$project-management` — for Linear/GitHub sync workflow
- `$devops-comprehensive` — for Sentry and CI integrations
