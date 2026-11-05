# Strix — AI Penetration Testing (فهرس اختبار الاختراق بالذكاء الاصطناعي)

9 workflows from [`usestrix/strix`](https://github.com/usestrix/strix) (Apache-2.0) — autonomous AI pentesting with validated, PoC-backed findings.

## Run modes (same engine)

| Mode | Needs | Choose when |
|------|-------|-------------|
| **OSS CLI (self-hosted)** | Docker + BYO LLM key | local dev loop, air-gapped, free, CI with Docker |
| **Managed cloud** (`strix cloud`) | account, no infra | no Docker/keys, team dashboards, scheduled scans, PDF reports |

## Routing (من يقود المهمة)

| Task | Doc |
|------|-----|
| Run any pentest (code/URL/domain/IP) — **start here** | `penetration-testing-with-strix.md` |
| Managed platform via CLI/REST (asset registration → scans → reports) | `managed-pentesting-with-strix.md` |
| Fix findings, re-scan to verify remediation | `fix-security-vulnerabilities-with-strix.md` |
| Wire diff-scoped PR scanning into CI/CD | `ci-security-scanning-with-strix.md` |
| Whole-product AppSec: pick test per asset, rank results | `application-security-testing.md` |
| Black-box pentest of a live web app / staging URL | `web-app-penetration-testing.md` |
| REST/GraphQL/gRPC API + OWASP API Top 10 (BOLA/IDOR) | `api-security-testing.md` |
| Systematic OWASP Top 10 assessment | `owasp-top-10-testing.md` |
| White-box source review of a repo | `find-security-vulnerabilities-in-code.md` |

## Non-negotiable

- **Authorization only:** scan targets the user owns or is authorized to test
- Always `-n` (headless) for agents; always set `--max-budget`
- A `0` exit ≠ full coverage — verify `run.json` status + cost vs budget before calling a run clean
- CLI docs for LLMs: `https://docs.strix.ai/llms.txt` · Cloud: `https://docs.app.strix.ai/llms.txt`

Install (self-hosted): `curl -sSL https://strix.ai/install | bash` or `pipx install strix-agent` · env: `STRIX_LLM`, `LLM_API_KEY`.
