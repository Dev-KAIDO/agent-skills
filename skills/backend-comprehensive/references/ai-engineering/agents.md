# AI Agents (الوكلاء الذكية)

Patterns for tool-using, goal-driven LLM loops.

## 1. The Loop

```
observe → (plan?) → act via tool → observe → … → final answer
```

Bounded by: max iterations, max tokens, wall-clock timeout, cost ceiling.

**Rule:** every agent needs a hard stop. An unbounded loop is an unbounded bill.

## 2. When an Agent (and When Not To)

Use an agent only when the path is genuinely unknown. Otherwise:

| Shape | Use instead |
|-------|-------------|
| Single known tool call | plain function call |
| Fixed sequence of steps | deterministic workflow / code |
| One-shot Q&A with docs | RAG (`rag.md`) |

**Default to the simplest thing that works** — agents are the least reliable, most expensive option.

## 3. Tool Design for Agents

- Name tools by **intent** (`find_customer`, not `query_db_table_customers`).
- Descriptions state **when NOT to use** the tool too — overlapping tools cause oscillation.
- Return compact, model-sized results (summaries + ids), not raw dumps — the context fills fast.
- Make tools **idempotent** or give them a dry-run mode; the model will retry.

## 4. Planning Modes

| Mode | Use |
|------|-----|
| ReAct (think→act→observe) | short tasks, ≤ ~10 steps |
| Plan-then-execute | multi-step goals; write plan to state, execute, re-plan on failure |
| Sub-agents | fan-out research/decomposition; each has its own context window |

Persist state (plan, findings, artifacts) **outside** the message list so a crash/retry resumes instead of restarting.

## 5. Guardrails

- **Permissions:** tools are typed — read-only by default; write/delete tools require explicit allow-list, and destructive ones require human approval (human-in-the-loop).
- **Budget:** per-run token + dollar + iteration caps; enforced server-side, not in the prompt.
- **Output gate:** validate final answers (schema, citations, no PII) before returning to the user.
- **Prompt injection:** tool results (web, email, files) are untrusted data — re-assert the system prompt after ingesting them.

## 6. Reliability

- Treat tool errors as observations: feed the error back ("order not found — check id format") instead of crashing the run.
- Retry only **transient** failures inside the loop; deterministic failures end the run with a typed error.
- Log the full trajectory (inputs, tool calls, outputs, tokens) — it is your debugging and eval corpus (`evals.md`).

## 7. Evals for Agents

- Trajectory-level checks: did it call the right tools **in order**, with valid args?
- Task-level: final outcome correct + cost/latency within budget.
- Regression suite: replay recorded trajectories against every prompt/model change.
