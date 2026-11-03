# LLM Evals (تقييمات النماذج اللغوية)

How to know a change made things **better**, not just different.

## 1. The Ladder

```
vibes  →  golden set  →  LLM-as-judge  →  online A/B
(never)   (always)      (scale)           (truth)
```

Start with a golden set of **20–50 real cases** with expected outputs. It catches ~80% of regressions on day one.

## 2. Golden Set Design

- Sample from **production traffic**, including failures — not hand-written fantasies.
- Label expected behavior precisely: exact answer, required facts, or rubric.
- Split: fast (run every change, ~30) + full (nightly, grows to 200+).
- Version it in git next to the prompts; a prompt change without a set update is unreviewable.

## 3. Metrics by Task

| Task | Metric |
|------|--------|
| Classification / extraction | accuracy, F1, exact JSON match |
| RAG answer | citation correctness, faithfulness (no unsupported claims) |
| Summarization | rubric scores (coverage, no-hallucination) via judge |
| Tool use | task success rate, invalid-arg rate, steps-to-success |
| Free chat | pairwise preference (A vs B), toxicity/PII rate |

## 4. LLM-as-Judge

- Judge with a **fixed rubric + explicit output schema**; never "is this good?".
- Prefer pairwise (which of A/B is better) over absolute scores — more stable.
- Use a **different, stronger model** than the one under test.
- Calibrate: human-score 30 cases; if judge agreement < ~80%, fix the rubric before trusting it.
- Blind the judge to which system produced which answer.

## 5. Regression Gate (CI)

```bash
python tools/run_evals.py --set fast --fail-below 0.92
```

- Block merge when score drops > 2 points vs baseline **or** any PII/toxicity case fails.
- Track cost + latency per run alongside quality — a "better" prompt that triples cost is a decision, not a win.
- Store every run (score, model, prompt hash) for trend charts.

## 6. Common Pitfalls

- **Overfitting the set:** rotate 20% of cases out periodically; hold out a private slice.
- **One aggregate number hides everything:** report per-category scores; +5 overall can mean −20 on your hardest category.
- **Judging style, not substance:** rubric must reward correctness first, formatting second.
- **Ignoring production:** weekly review of real failures → append to the set (that's the loop).
