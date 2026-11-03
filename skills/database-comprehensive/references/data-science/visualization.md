# Data Visualization (التvisualisation)

## 1. Pick by Question

| Question | Chart |
|----------|-------|
| Comparison between categories | horizontal bar (sorted) |
| Trend over time | line |
| Distribution | histogram / KDE / box / violin |
| Relationship of 2 numerics | scatter (+ trend line) |
| Composition (parts of whole) | stacked bar; pie only for ≤ 3 slices with big differences |
| Correlation matrix | heatmap |
| Ranking with many items | lollipop or bar; never pie |
| Geography | choropleth / symbol map |

**Anti-defaults:** no 3D, no dual y-axes (split into two charts), no truncated bar baseline for comparisons (line charts may truncate).

## 2. Grammar of Graphics (altair/plotly express)

```
data → mark (bar/line/point/area) → encoding (x, y, color, size, tooltip)
```

- One message per chart; facet (`column=`) instead of overplotting series.
- Sort bars by value unless category order is meaningful.

## 3. Library Choice

| Library | Use when |
|---------|----------|
| **matplotlib** | precise control, publication figures, anything stat-model produced |
| **plotly** | interactive dashboards, hover, zoom; exports to HTML |
| **altair/vega-lite** | declarative statistical charts, small–medium data (< ~10k rows) |
| seaborn | quick statistical plots on dataframes (built on matplotlib) |
| ggplot (plotnine) | ggplot2 muscle memory in Python |

## 4. Design Rules

- Label axes with **units**; title states the takeaway ("Revenue +12% QoQ"), not the variable name.
- Direct-label lines instead of legends when ≤ 5 series.
- Color: colorblind-safe palettes (viridis, Okabe-Ito); reserve red/green for real semantic polarity.
- Annotate the one point that matters — the chart exists to make a claim obvious in 3 seconds.
- Consistent time axis: equal spacing, sensible ticks (`%Y-%m`, weekly/monthly).
- Log scale for orders-of-magnitude data — and say so in the axis label.

## 5. Hygiene

- Plot the **distribution before** any model; most "model failures" are skewed/leaky data.
- Show uncertainty (CI bands, error bars) for estimates — a naked mean line overstates certainty.
- For big data: sample or hexbin/density — overplotting hides everything.
