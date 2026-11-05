# Web Analytics (قياس وتحليل البيانات)

## 1. Event Taxonomy (design before installing any tool)

Naming convention, fixed once: `object_action` in `snake_case`, lowercase, past/no-noise:

```
page_view   cta_click   signup_complete   checkout_purchase
search_performed   video_played   error_shown
```

Rules:
- **Properties carry context** (`{cta_id, page_section, plan}`), not new event names — event count must stay bounded.
- One canonical definition of a conversion per product (agreed with the business), referenced everywhere.
- Track the **funnel** (`signup_started → signup_complete → activation`), not just the final success — diagnosis needs the drop-offs.

## 2. Tool Choice

| Tool | When |
|------|------|
| **GA4** | needs funnels/audiences/Ads integration, enterprise reporting |
| **Plausible / Umami** | privacy-friendly, cookieless, one script, EU hosting |
| **Matomo** | self-hosted, full data ownership, GA-like features |
| **PostHog** | product analytics (events, funnels, session replay) for app teams |
| Server-side (first-party) | ad-blocker resilience, accurate counts, more work |

Privacy floor: cookieless where possible, anonymize IPs, no PII in event properties (emails/usernames in events = GDPR problem), consent gate before non-essential tracking.

## 3. Implementation

```js
// fire once per distinct action; guard against double-fire (React StrictMode!)
track("checkout_purchase", { value_cents: 4900, currency: "USD", item_count: 2 });
```

- Fire events from **one shared module** — scattered snippets drift and double-count.
- Test with a debug view before release: every event fires **once**, with correct properties.
- SPA rule: `page_view` on route change (not just initial load) — otherwise SPA traffic looks like one page.
- Set explicit user id after login (or anonymous id before), consistently across sessions.

## 4. Dashboards That Get Used

- Fewer metrics, each with a **question it answers**: activation rate → "is onboarding working?"
- Segment by source/device/new-vs-return — aggregates hide the truth.
- Compare to a baseline (prev period / cohort), not absolute values alone.
- Weekly review ritual; a dashboard nobody opens is decoration.

## 5. Common Failure Modes

| Symptom | Cause |
|---------|-------|
| Conversion doubled overnight | double-firing event (duplicate snippet / React effect) |
| 40% of traffic "missing" | ad-blockers on client-only tracking → move critical events server-side |
| Bounce rate 0% | `page_view` sent twice or engagement misconfigured |
| Funnel shows 0 at a step | event renamed without alias — taxonomy changes break history |
| Numbers disagree between tools | different session definitions/consent — pick one source of truth |

## 6. Measurement Review (quarterly)

Prune events nobody queries (every event costs attention); re-check tracking against current UI (buttons die, events linger); verify consent banner blocks correctly per region; re-validate the conversion definition still matches the business.
