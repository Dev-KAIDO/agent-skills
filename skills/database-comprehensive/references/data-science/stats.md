# Statistics (الإحصاء التطبيقية)

## 1. Distributions — Quick Pick

| Data | Distribution |
|------|--------------|
| Counts of rare independent events | Poisson |
| Time between events | Exponential |
| Binary success rate | Binomial → Normal approx if n·p ≥ ~10 |
| Measurement noise, sums of many effects | Normal |
| Wait time until k-th event | Gamma / Negative Binomial |
| Survival / time-to-failure | Weibull / Kaplan-Meier |

Check before modeling: histogram + Q-Q plot. Heavy tails (finance, latencies) → median/IQR and log-transform, not mean/std.

## 2. Summary Stats

- **Normal-ish:** mean ± std.
- **Skewed / outliers:** median + IQR (Q1–Q3), p95/p99 for SLAs and latencies.
- Always report **n**. A mean without sample size is not a result.

## 3. Hypothesis Tests

| Question | Test |
|----------|------|
| One sample vs a value | one-sample t-test (or Wilcoxon if non-normal) |
| Two independent means | Welch's t-test (default; don't assume equal var) |
| Paired (before/after) | paired t / Wilcoxon signed-rank |
| Categorical association | χ² test of independence |
| Distributions differ | KS test |
| Variances differ | Levene's test |

**Rules:**
- State H₀, α (default 0.05), and **n** with every result.
- p < 0.05 ≠ important: report effect size (Cohen's d, odds ratio, % lift) + CI.
- Multiple comparisons (many columns/segments): Bonferroni or FDR correction — otherwise you're mining noise.
- A/B tests: check **sample ratio mismatch and peeking** first; sequential tests need corrected boundaries.

## 4. Confidence Intervals

```
mean ± 1.96 · SE    (n large / normal)
SE = std / sqrt(n)
```

- CI is not "95% probability the mean is in this range" in frequentist terms — but practically: if the CI of the difference excludes 0, the effect is detectable at α=0.05.
- For proportions use Wilson interval, not normal approx, when p near 0/1 or n small.

## 5. Regression Sanity

- Check residuals: constant variance, no autocorrelation (Durbin-Watson), roughly normal.
- VIF > 10 → multicollinearity; drop or combine features.
- Correlation ≠ causation — only an experiment (or a strong causal design) supports "X increases Y".

## 6. Reporting Template

```
question → data (n, period) → method → result (effect size + CI + p)
→ assumptions checked → limitations → recommendation
```
