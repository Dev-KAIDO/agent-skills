# Technical SEO (تحسين محركات البحث التقني)

## 1. Crawlability (first — nothing else matters if this fails)

- `robots.txt` allows the pages you want indexed; **never** block CSS/JS needed to render.
- XML sitemap: only canonical, 200-status, indexable URLs; submitted in Search Console.
- Server-render meaningful HTML — content behind client-side fetch alone is a gamble.
- Faceted/nav URLs: `rel="canonical"` on duplicates; parameters that explode the crawl space (`?sort=`, `?page=`) → canonical or `noindex`.

## 2. Per-Page Metadata

```html
<title>Primary keyword — qualifier | Brand</title>   ≤ ~60 chars, unique per page
<meta name="description" content="…">                ≤ ~160 chars, written to earn the click
<link rel="canonical" href="https://…/page">          self-referencing unless consolidating
<meta property="og:title|og:description|og:image">   social + preview quality
```

- One `h1` per page matching the topic; heading hierarchy `h2/h3` meaningful, not size choices.
- Every image: `alt` (descriptive, not "image1") + `width/height` (prevents layout shift).
- Duplicate content: pick one canonical URL (trailing slash, http/https, params) and enforce it with redirects — **one URL per page, always**.

## 3. Structured Data (Schema.org JSON-LD)

```json
{ "@context": "https://schema.org", "@type": "Article",
  "headline": "…", "datePublished": "…", "author": {"@type":"Person","name":"…"} }
```

Mark up what exists on the page: `Article`, `Product` (+`Offer`), `FAQPage`, `BreadcrumbList`, `Organization`.
→ eligibility for rich results (stars, FAQ, breadcrumbs). Validate with Rich Results Test. **No marking-up of invisible/fake content** — manual action risk.

## 4. Core Web Vitals (ranking + UX)

| Metric | Target | Primary lever |
|--------|--------|---------------|
| LCP (largest paint) | ≤ 2.5s | preload hero image, server render, fast TTFB |
| INP (interaction) | ≤ 200ms | break up long JS tasks, lightweight handlers |
| CLS (layout shift) | ≤ 0.1 | fixed image/video dimensions, reserved ad/embed slots |

Measure **field data** (CrUX/Search Console), not just lab Lighthouse — lab numbers are a simulation.

## 5. Internal Linking & URLs

- Human-readable paths (`/guides/react-performance`), stable forever — URL changes cost rankings.
- Descriptive anchor text (never "click here"); every important page reachable in ≤ 3 clicks from home.
- Breadcrumbs visible + marked up.
- 404s → 301 to the closest equivalent; monitor Search Console for broken inbound links.

## 6. International (hreflang)

```html
<link rel="alternate" hreflang="ar" href="…/ar/page" />
<link rel="alternate" hreflang="en" href="…/en/page" />
<link rel="alternate" hreflang="x-default" href="…/en/page" />
```

Reciprocal (each page points back), same URL language across the set, one `x-default`. Don't auto-translate only titles — thin translated pages hurt more than they help.

## 7. Release Checklist

- [ ] Crawlable, canonical, indexable (robots + sitemap agree)
- [ ] Unique title + description + one h1
- [ ] Structured data validated
- [ ] Images: alt + dimensions; CWV in field green
- [ ] Internal links to the page exist
- [ ] `hreflang` correct for localized versions
- [ ] No accidental `noindex` in staging leaked to prod (classic)
