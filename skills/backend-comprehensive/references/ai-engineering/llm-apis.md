# LLM API Patterns (أنماط واجهات برمجية للنماذج اللغوية)

Provider-agnostic patterns. Providers: Anthropic (Claude), OpenAI, Google, and any OpenAI-compatible endpoint.

## 1. Request Anatomy

```
messages[]      → conversation history (system / user / assistant / tool)
max_tokens      → hard cap on output
temperature     → 0 for extraction/agents, 0.7–1.0 for creative
tools           → JSON schema the model may call
stream          → SSE deltas instead of one blob
```

**Rules:**
- Always set `system` separately — never mix instructions into the first user turn.
- Cap `max_tokens`; an uncapped call is an unbounded bill.
- Keep the full message list, but trim oldest turns once past context limit (summary beats truncation for long sessions).

## 2. Streaming

```python
# OpenAI-compatible
for chunk in client.chat.completions.create(model=m, messages=msgs, stream=True):
    delta = chunk.choices[0].delta.content or ""
    send_sse(delta)
```

- Stream by default for chat UIs: **TTFT matters more than total time**.
- Send a final event with token usage for billing/logging.
- Handle mid-stream errors: client should be able to retry from the last complete sentence, not restart.

## 3. Tool Use (Function Calling)

```json
{ "type": "function", "function": {
    "name": "get_order",
    "description": "Fetch one order by id. Use for status questions.",
    "parameters": { "type": "object",
      "properties": { "order_id": { "type": "string" } },
      "required": ["order_id"] } } }
```

**Rules:**
- Write `description` as instructions to the model ("Use when…"), not as documentation for humans.
- Validate arguments server-side against the JSON Schema **before executing** — models hallucinate enum values and dates.
- One tool result per turn; loop until the model stops emitting tool calls (bounded: max ~10 iterations, then force a text answer).
- Prefer **few, well-named tools** over many overlapping ones — tool choice accuracy drops with >~20 tools.

## 4. Structured Output

For extraction/classification, force JSON:

```python
resp = client.chat.completions.create(
    model=m, messages=msgs,
    response_format={"type": "json_object"}   # or json_schema on newer APIs
)
data = json.loads(resp.choices[0].message.content)
```

- Use **JSON Schema with `strict: true`** when the API supports it — eliminates most parse failures.
- Otherwise: instruct + `json.loads` with one repair retry (strip ``` fences, fix trailing commas).
- Never regex-parse JSON out of prose.

## 5. Cost & Latency Budget

| Lever | Effect |
|-------|--------|
| Smaller model for easy turns (router) | 5–10× cost cut, big wins on classification/routing |
| Prompt caching (system + tools) | ~90% discount on cached input tokens |
| `max_tokens` + early-stop | bounds worst case |
| Batch API (24h) | ~50% off for offline jobs |
| Keep context small | input tokens dominate cost; history grows quadratically with naive retry |

**Latency math:** `total ≈ TTFT + (output_tokens / tokens_per_s)`. Reduce output tokens (ask for terse answers) before reaching for a faster model.

## 6. Errors & Retries

| Error | Action |
|-------|--------|
| 429 rate limit | Exponential backoff + jitter; respect `Retry-After` |
| 5xx / timeout | Retry idempotent calls 2–3×; a partial stream must be discarded |
| Context length exceeded | Trim history or summarize — never silently drop the user's question |
| Content filter refusal | Surface a typed error; do not retry the identical request |

## 7. Observability

Log per call: model, latency, input/output tokens, cost, tool calls, finish reason. Correlate with a `trace_id` shared with your app logs — this is what makes evals (`evals.md`) and cost attribution possible.

## 8. Ties

- MCP servers exposing your tools → see section 12 of the main skill.
- Retrieval feeding context → `rag.md`.
- Measuring quality → `evals.md`.
