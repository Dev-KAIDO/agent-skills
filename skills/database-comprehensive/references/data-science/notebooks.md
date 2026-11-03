# Notebooks (دفاتر Jupyter)

## 1. Structure

```
1. Title + one-paragraph purpose
2. Setup (imports, config, data paths)
3. Load + first look (shape, dtypes, head, NaNs)
4. Clean (documented decisions)
5. Analyze (each cell: question → code → finding)
6. Visualize
7. Conclusions (numbered findings + next steps)
```

**Rule:** every notebook must be runnable top-to-bottom on a clean machine. `Restart & Run All` is the acceptance test — no hidden state.

## 2. Reproducibility

- Pin the environment: `requirements.txt`/`uv.lock` committed next to the notebook; record library versions in a setup cell.
- Fix seeds: `random.seed(42)`, `np.random.seed(42)`.
- Read data by **relative path** from the repo root; never `C:\Users\...` or `/home/...`.
- No wall-clock in logic (use a fixed `REF_DATE = pd.Timestamp("2026-01-01")`).
- Clear outputs before commit **or** commit them deliberately — pick one policy for the team.

## 3. Hygiene

- Extract repeated logic into `src/` functions; notebooks for exploration, **production code lives in modules**.
- Notebook size: if > ~200 cells or the `.ipynb` > ~10 MB, split or move heavy work out.
- Use `%load_ext autoreload` + `%autoreload 2` during development.
- Parameterize (papermill/jupyter parameters) for scheduled/report runs.

## 4. Review Checklist

- [ ] Restart & Run All passes
- [ ] No secrets/paths/PII printed in outputs
- [ ] Data version/date recorded
- [ ] Findings summarized at the bottom (a notebook nobody scrolls to the end of is a log, not an analysis)
- [ ] Heavy cells cached or moved to scripts
