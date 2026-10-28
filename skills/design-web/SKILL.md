---
name: design-web
description: Web design skill covering complete UI/UX for web — layout, typography, color, components, animation, accessibility, responsive design, modern design systems, landing pages, dashboards, forms, navigation, and professional aesthetics. Use when building, reviewing, or redesigning any web interface.
---

# Web Design — Complete Skill

## Overview

This skill covers **every aspect of web design**: from foundations (layout, typography, color) to advanced patterns (design systems, animations, accessibility). It merges the best of `frontend-design`, `frontend-skill`, `ui-audit`, `ux-audit`, `typography-audit`, `ui-animation`, `theme-factory`, `brand-guidelines`, and `web-artifacts-builder`.

---

## 1. Design Foundations (الأساسيات)

### 1.1 Layout System
- **Grid:** CSS Grid for page structure (12-column standard), Flexbox for component alignment
- **Spacing scale:** 4px base unit (4, 8, 12, 16, 24, 32, 48, 64, 96, 128)
- **Breakpoints:** mobile-first (640, 768, 1024, 1280, 1536)
- **Container max-widths:** prose=65ch, content=1200px, full=100%
- **Z-index scale:** base=0, dropdown=10, sticky=20, modal=30, toast=40

### 1.2 Typography
- **Font pairing rules:**
  - Headings: geometric sans (Inter, Poppins, Plus Jakarta Sans, Satoshi)
  - Body: readable sans (Inter, Source Sans, IBM Plex Sans) or serif (Lora, Merriweather)
  - Monospace: JetBrains Mono, Fira Code (for code)
- **Type scale:** 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72
- **Line height:** 1.2 (headings), 1.5-1.7 (body)
- **Letter spacing:** -0.02em (large headings), 0 (body), 0.05em (labels/caps)
- **Font weights:** 400 (body), 500 (medium), 600 (semibold), 700 (bold)
- **OpenType features:** `font-feature-settings: "liga" 1, "kern" 1`

### 1.3 Color System
- **HSL approach:** define hues, then create scales (50-900)
- **Semantic colors:** primary, secondary, success, warning, error, info
- **Neutral scale:** gray-50 to gray-900
- **Dark mode:** use `prefers-color-scheme` + CSS custom properties
- **Contrast ratios:** WCAG AA (4.5:1 body, 3:1 large text), AAA (7:1 body)
- **Color accessibility:** never rely solely on color for meaning — use icons, patterns, labels

### 1.4 Spacing & Sizing
- **Consistent rhythm:** all spacing from the 4px scale
- **Section padding:** 64-120px vertical (desktop), 40-64px (mobile)
- **Component padding:** 8-24px depending on size
- **Gap:** 8-16px between related items, 24-48px between groups

---

## 2. Page Components (مكونات الصفحة)

### 2.1 Header / Navbar
- **Sticky header:** `position: sticky; top: 0` with backdrop blur
- **Logo:** left-aligned, links to home
- **Navigation:** horizontal links, active state indicator
- **Mobile:** hamburger menu with slide-in drawer or full-screen overlay
- **Height:** 56-72px desktop, 56px mobile
- **Search:** optional integrated search bar
- **CTA button:** right-aligned primary action

### 2.2 Hero Section
- **Structure:** headline + subheadline + CTA(s) + visual
- **Headline rules:** max 10 words, benefit-driven, clear value proposition
- **Visual:** illustration, screenshot, or video background
- **Height:** 60-80vh (viewport height)
- **Background:** gradient, image, video, or solid color

### 2.3 Navigation Patterns
- **Primary nav:** main sections (Home, Features, Pricing, About)
- **Secondary nav:** breadcrumbs, pagination, tabs
- **Footer nav:** sitemap, legal, social, newsletter
- **Mega menu:** for complex sites with many categories
- **Skip link:** `Skip to content` for accessibility

### 2.4 Content Sections
- **Cards:** consistent padding, border/shadow, hover effects
- **Grids:** responsive (1-4 columns based on breakpoint)
- **Lists:** clean, with icons or bullets
- **Tables:** sortable, filterable, responsive (horizontal scroll on mobile)
- **Media:** images with lazy loading, responsive srcset, alt text

### 2.5 Forms
- **Input fields:** label above (not placeholder-only), clear focus state
- **Validation:** inline errors (below field), success checkmarks
- **Buttons:** primary (filled), secondary (outline), ghost (text), danger (red)
- **States:** default, hover, focus-visible, disabled, loading, error, success
- **Layout:** single column on mobile, max 2 columns on desktop
- **Accessibility:** `aria-label`, `aria-describedby`, `required`, `autocomplete`

### 2.6 Footer
- **Structure:** logo + nav columns + newsletter + social + legal
- **Dark/light:** often inverse of header
- **Responsive:** stack columns on mobile

---

## 3. Modern Design Styles (التصاميم العصرية)

### 3.1 Aesthetic Anchors (pick one)
1. **Swiss/International:** grid, clean, Helvetica-like type, black/white + one accent
2. **Brutalist:** raw, bold, high contrast, unconventional, exposed structure
3. **Glassmorphism:** frosted glass, transparency, blur, layered depth
4. **Neumorphism:** soft shadows, subtle 3D, light background
5. **Minimalism:** whitespace-driven, single accent, extreme simplicity
6. **Dark Mode:** deep backgrounds, vibrant accents, high contrast
7. **Retro-Futuristic:** nostalgia + modern tech, bold gradients, geometric
8. **Organic/Natural:** soft shapes, earthy colors, flowing layouts
9. **Aurora/Gradient:** luminous gradients, ethereal glow, animated backgrounds
10. **Lo-Fi/Handcrafted:** imperfect, textured, warm, personal

### 3.2 2025-2026 Trends
- **Bento grids:** asymmetric grid layouts (Apple-style)
- **Oversized typography:** 100px+ headlines
- **Scroll animations:** elements reveal on scroll
- **Micro-interactions:** hover effects, loading states, transitions
- **AI-generated visuals:** unique illustrations
- **3D elements:** subtle 3D with CSS/WebGL
- **Variable fonts:** responsive typography with one file
- **Color trends:** warm neutrals, sage green, terracotta, electric blue
- **Motion:** smooth easing (cubic-bezier), spring physics
- **No more:** cookie-cutter AI look, generic stock photos, cookie banners as afterthought

---

## 4. Component Design (تصميم المكونات)

### 4.1 Button System
```
Primary:    filled, brand color, white text
Secondary:  outline, border, brand text
Ghost:      transparent, brand text
Danger:     red, white text
Link:       underlined on hover, no fill
```
- Sizes: sm (32px), md (40px), lg (48px)
- Icon buttons: 32/40/48px square with icon centered
- Loading state: spinner replaces text/icon

### 4.2 Card Patterns
- **Elevated:** shadow, hover lift
- **Outlined:** border only, hover border-color change
- **Filled:** background color, no border
- **Interactive:** entire card clickable, cursor pointer
- **Media card:** image on top, content below
- **Horizontal card:** image left, content right

### 4.3 Modal / Dialog
- **Trigger:** button click
- **Backdrop:** semi-transparent overlay with blur
- **Content:** title, body, actions (cancel + confirm)
- **Focus trap:** Tab cycles within modal
- **Escape:** closes modal
- **Animation:** fade in + slide up (200ms)

### 4.4 Toast / Notification
- **Position:** top-right (desktop), bottom (mobile)
- **Types:** success (green), error (red), warning (yellow), info (blue)
- **Auto-dismiss:** 3-5 seconds for success, persistent for errors
- **Animation:** slide in from right + fade

### 4.5 Tooltip
- **Trigger:** hover or focus
- **Position:** top (default), can be bottom/left/right
- **Delay:** 200-500ms before showing
- **Content:** short text, max 200px width
- **Dark background:** high contrast

---

## 5. Animation & Motion (الحركة)

### 5.1 Principles
- **Duration:** fast=150ms, normal=200-300ms, slow=500ms
- **Easing:** `ease-out` for entering, `ease-in` for exiting, `ease-in-out` for moving
- **Spring:** `cubic-bezier(0.34, 1.56, 0.64, 1)` for playful bounce
- **Never animate:** `width`, `height`, `top`, `left` (use transform)
- **Always animate:** `transform`, `opacity` (GPU-accelerated)

### 5.2 Common Patterns
- **Hover:** scale(1.02), shadow increase, color change (150ms)
- **Page transition:** fade + slide (200-300ms)
- **Scroll reveal:** elements fade in + slide up when entering viewport
- **Loading:** skeleton screens (preferred) or spinners
- **Stagger:** children animate with 50-100ms delay between them
- **Parallax:** background moves slower than foreground on scroll

### 5.3 Accessibility
- `prefers-reduced-motion: reduce` → disable all non-essential animations
- Focus visible: `outline: 2px solid; outline-offset: 2px`
- Transitions must not block interaction

---

## 6. Responsive Design (التصميم المتجاوب)

### 6.1 Mobile-First Approach
1. Design for mobile (375px)
2. Enhance at sm (640px)
3. Enhance at md (768px) — tablet
4. Enhance at lg (1024px) — desktop
5. Enhance at xl (1280px) — large desktop

### 6.2 Breakpoint Behaviors
- **Mobile (< 640px):** single column, hamburger menu, stacked cards
- **Tablet (640-1024px):** 2 columns, simplified nav
- **Desktop (1024+):** full layout, horizontal nav, multi-column grids

### 6.3 Common Patterns
- **Navigation:** hamburger → horizontal links
- **Grids:** 1 → 2 → 3 → 4 columns
- **Tables:** stack → horizontal scroll → full table
- **Typography:** scale down by ~10% per breakpoint
- **Images:** fluid with `object-fit: cover`

---

## 7. Accessibility (إمكانية الوصول)

### 7.1 WCAG 2.1 Checklist
- [ ] All images have meaningful `alt` text
- [ ] Color contrast ≥ 4.5:1 (body) / 3:1 (large)
- [ ] All interactive elements keyboard-accessible
- [ ] Focus visible on every focusable element
- [ ] Forms have labels (not just placeholders)
- [ ] Page has proper heading hierarchy (h1 → h2 → h3)
- [ ] Skip navigation link present
- [ ] Language attribute set (`<html lang="ar">` or `lang="en"`)
- [ ] No content flashes more than 3 times per second
- [ ] Video has captions; audio has transcripts

### 7.2 ARIA Best Practices
- Use native HTML elements first (button, link, input)
- `aria-label` for icon-only buttons
- `aria-describedby` for additional descriptions
- `aria-live` for dynamic content updates
- `role` only when no semantic element exists

### 7.3 Keyboard Navigation
- Tab: forward through focusable elements
- Shift+Tab: backward
- Enter/Space: activate buttons and links
- Escape: close modals/menus
- Arrow keys: within composite widgets (dropdowns, tabs)

---

## 8. Performance (الأداء)

### 8.1 Core Web Vitals
- **LCP (Largest Contentful Paint):** < 2.5s — optimize hero image, font loading
- **FID (First Input Delay):** < 100ms — minimize JavaScript
- **CLS (Cumulative Layout Shift):** < 0.1 — set image dimensions, avoid dynamic content insertion

### 8.2 Optimization Checklist
- [ ] Images: WebP/AVIF format, responsive `srcset`, lazy loading
- [ ] Fonts: `font-display: swap`, preload critical fonts, subset
- [ ] CSS: critical CSS inline, defer non-critical
- [ ] JS: code splitting, tree shaking, defer non-essential
- [ ] Caching: proper `Cache-Control` headers
- [ ] CDN: serve static assets from CDN

---

## 9. Page Types (أنواع الصفحات)

### 9.1 Landing Page
- Hero with clear CTA
- Social proof (logos, testimonials)
- Feature highlights (3-6 sections)
- Pricing table
- FAQ
- Final CTA
- Footer

### 9.2 Dashboard
- Sidebar navigation (collapsible)
- Top bar with search, notifications, profile
- Stats cards (KPIs)
- Charts (line, bar, pie)
- Data tables with pagination
- Activity feed

### 9.3 E-commerce
- Product grid with filters
- Product detail page
- Shopping cart (slide-in panel)
- Checkout flow (multi-step)
- Order confirmation

### 9.4 Blog
- Article list with cards
- Article page (max-width prose, 65ch)
- Author bio
- Related articles
- Table of contents (sticky sidebar)

---

## 10. Design Tokens (رموز التصميم)

```css
:root {
  /* Colors */
  --color-primary: hsl(220 70% 50%);
  --color-primary-hover: hsl(220 70% 45%);
  --color-success: hsl(140 70% 45%);
  --color-error: hsl(0 70% 50%);
  --color-warning: hsl(38 90% 50%);
  
  /* Neutrals */
  --gray-50: hsl(0 0% 98%);
  --gray-100: hsl(0 0% 96%);
  --gray-900: hsl(0 0% 10%);
  
  /* Typography */
  --font-heading: 'Inter', sans-serif;
  --font-body: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  
  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 48px;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px hsl(0 0% 0% / 0.05);
  --shadow-md: 0 4px 6px hsl(0 0% 0% / 0.1);
  --shadow-lg: 0 10px 15px hsl(0 0% 0% / 0.1);
  
  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --radius-full: 9999px;
  
  /* Animation */
  --duration-fast: 150ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

## 11. Brand Guidelines (إرشادات الهوية البصرية)

### 11.1 Anthropic Brand Palette
| Role | Hex | Use |
|------|-----|-----|
| Ink (primary) | `#141413` | Headings, body text, dark surfaces |
| Cream (canvas) | `#faf9f5` | Page background — never pure white |
| Terracotta (accent 1) | `#d97757` | Primary accent, CTAs, highlights |
| Sky (accent 2) | `#6a9bcc` | Secondary accent, links, data viz |
| Sage (accent 3) | `#788c5d` | Tertiary accent, success states |

**Accent rotation:** pick ONE dominant accent per screen; the other two appear only as small supporting marks. Never mix all three at equal weight.

### 11.2 Typography & Applying Brand to Any Artifact
- Headings: **Poppins**; Body: **Lora** (fallbacks: system serif)
- Apply the same palette to slides, docs, PDFs, and web — not just pages
- Cream `#faf9f5` + Ink `#141413` is the default pairing; accent color carries emphasis
- Reserve pure `#ffffff` for cards/panels sitting ON the cream canvas

### 11.3 Theme Factory (10 ثيمات جاهزة)
A library of preset themes exists under `themes/` — each defines a full token set (bg, surface, text, accent, border, radius, fonts). Preview them with `theme-showcase.pdf`.
| Use case | Theme family |
|----------|-------------|
| Calm / editorial | Ocean Depths, Sage Garden |
| Bold / marketing | Sunset Boulevard, Neon Dusk |
| Technical / dark | Midnight Galaxy, Carbon |
| Playful | Citrus, Bubblegum |
| Corporate | Slate Pro, Paper |
- **Custom themes:** generate a new token set (bg/surface/text/accent/border/radius/font) then apply — never hardcode colors per component.

---

## 12. Aesthetic Anchors (المرساة الجمالية)

Pick **ONE** anchor per project and lock its CSS tokens. Mixing anchors produces the generic "AI look".

| Anchor | Character | Locked tokens (example) |
|--------|-----------|------------------------|
| **Swiss** | Grid, Helvetica, red/black/white, objective photography | `--accent:#e63312; --radius:0; --font:'Helvetica Neue'` |
| **Brutalist** | Raw HTML look, system fonts, thick borders, underlines | `--radius:0; --border:3px solid #000; --shadow:none` |
| **Chaotic** | Overlapping layers, rotated type, clashing color, dense | `--accent:#ff2e63; rotation on headings; mixed fonts` |
| **Industrial** | Steel grays, monospace, exposed structure, sharp panels | `--font:'JetBrains Mono'; --surface:#2b2f33` |
| **Retro-Futuristic** | CRT glow, scanlines, neon on dark, bitmap type | `--bg:#0a0a12; --glow:0 0 24px currentColor` |
| **Organic** | Soft curves, earthy palette, grain texture, asymmetric | `--radius:24px; --accent:#7d8c61; grain overlay` |
| **Aurora** | Gradient meshes, translucent glass, deep dark base | `--glass:rgba(255,255,255,.08); backdrop-filter:blur` |
| **Lo-Fi** | Nostalgic, low-fi imagery, muted colors, imperfect | `--accent:#c9a227; slight rotations; paper texture` |

### 12.1 The Differentiator Discipline
- Non-obvious anchors (Brutalist, Chaotic, Industrial, Lo-Fi) pair with exactly ONE differentiator (e.g. Brutalist + soft motion)
- Obvious anchors (Swiss, Aurora) stay pure
- **Anchor tokens must match exactly** — the anchor IS the design system

### 12.2 Content Is Not Design (قواعد مضادة)
- ❌ No fabricated data ("Lorem", fake stats, invented testimonials)
- ❌ No filler labels ("Coming Soon", "Feature 1", "Lorem ipsum")
- ❌ No unicode glyphs used as icons (▲ ■ ◆) — use a real icon set
- ❌ No purple-gradient-on-dark centered hero with two buttons (the "AI slop" default)
- ✅ Real strings that name real information; real images or generated art; real empty/loading/error states

---

## 13. Art Direction (توجيه فني مستوى جوائز)

### 13.1 Three Theses (الثلاثية التوجيهية)
Before building, write:
1. **Visual thesis** — one sentence: what the page should FEEL like (e.g. "a printed financial broadsheet that happens to scroll")
2. **Content plan** — the real information architecture: what sections, what REAL copy/data each holds
3. **Interaction thesis** — how the page responds: what moves, what reacts, and why

### 13.2 Composition Rules
- **Poster-first viewport:** the first screen must work as a standalone poster — readable and striking without scrolling
- **Cardless layouts:** prefer whitespace, rules, and typography over boxes-in-boxes
- **Two typefaces maximum** (one display + one text), **one accent color**
- **Generous whitespace** is the cheapest quality signal
- **Hierarchy via scale, not color** — size and weight do the work; color punctuates

### 13.3 Build Order
```
Hero (poster) → Supporting sections → Detail pass (spacing, type, states) → CTA → 2-3 deliberate animations
```
Motion is the LAST step, never the first. Two or three well-chosen animations beat twenty.

---

## 14. Animation Deep Dive (عمق الحركة)

### 14.1 Springs Over Easings
```jsx
// Springs feel physical; avoid duration-based easing for direct manipulation
import { useSpring, useTransform, motionValue } from 'framer-motion';
const x = useSpring(0, { stiffness: 400, damping: 30 });
const scale = useTransform(x, [-300, 0, 300], [0.8, 1, 0.8]);
```

### 14.2 Gestures & Drag
```jsx
<motion.div drag dragConstraints={{ left: 0, right: 300 }} whileDrag={{ scale: 1.05 }} />
```
- Use `dragElastic` for resistance; `onDragEnd` to snap to nearest grid slot

### 14.3 Clip-Path Reveals & @starting-style
```css
@starting-style { .panel { opacity: 0; transform: translateY(24px); } }
.panel { transition: opacity .5s, transform .5s; }
::view-transition-new(root) { animation: slide-in .4s; }
```

### 14.4 Motion Rules
- ❌ Never `transition: all` — name properties
- ❌ Never animate layout properties (top/left/width/height) — use transform/opacity
- ✅ Correct `transform-origin` (drawer from the edge, not center)
- ✅ No infinite off-screen loops (battery + jank)
- ✅ Review format: **Before → After → Why** (what changed, and the reasoning)

---

## 15. Audit Methodology (منهجية التدقيق)

### 15.1 UI Audit (5 steps)
1. Read changed files (diff-aware when a PR is present)
2. Run the rule set — each finding carries a **prefix** (`a11y-`, `interaction-`, `forms-`, `typography-`, `perf-`, `motion-`, `microcopy-`)
3. Order findings **CRITICAL → HIGH → MEDIUM**; a11y, interaction, forms must pass first
4. Emit `file:line` findings with concrete fixes; clean files get `✓ pass`
5. Fix or report — never silently skip a critical rule

### 15.2 UX Audit (3-tier verdict)
Feature-level review of what tools like Lighthouse/axe miss:
| Tier | Meaning |
|------|---------|
| **release-blocker** | Data loss, broken flow, inaccessible core task |
| **fix-this-sprint** | Missing loading/empty/error state, lost form data, broken focus management |
| **backlog** | Vague microcopy, skeleton-induced layout shift, minor polish |

**Playbook coverage per feature:** loading ✓ empty ✓ error ✓ optimistic-with-rollback ✓ focus management ✓ data preservation on validation ✓
**React 19 fix APIs:** `useActionState`, `useFormStatus`, `useOptimistic`, `useTransition`, Suspense boundaries.

### 15.3 Typography Audit (10 categories / 89 rules)
Punctuation · font selection · size · line-height · letter-spacing · OpenType features (`liga`, `kern`) · hierarchy · pairings · brand · responsive scaling.
- Findings are `file:line` with the violated rule id
- Read-only: audit, never redesign

---

## 16. Web Artifacts Builder (أدوات الويب المجمّعة)

Build complex multi-component tools (React + Tailwind + shadcn/ui) **bundled into a single shareable HTML file**.

```bash
bash scripts/init-artifact.sh my-tool      # scaffold Vite + React + Tailwind
bash scripts/bundle-artifact.sh            # produce bundle.html (40+ shadcn components available)
```
- **Stack:** React + Vite + Tailwind + shadcn/ui; state via hooks/context; client-side routing only if needed
- **Output:** one self-contained `bundle.html` — no build step for the consumer
- **Anti-slop:** no purple-gradient hero, no centered generic layout, no fake data
- Reference: the bundled `scripts/` in this skill folder

---

## 17. Verification Checklist (قائمة التحقق)

Before delivering any web design:

- [ ] Responsive at all breakpoints (375, 640, 768, 1024, 1280)
- [ ] Color contrast passes WCAG AA
- [ ] All interactive elements keyboard-accessible
- [ ] Focus states visible
- [ ] Images have alt text
- [ ] Forms have labels and validation
- [ ] Animation respects `prefers-reduced-motion`
- [ ] Loading states for async operations
- [ ] Error states for all failure cases
- [ ] Empty states for all lists/tables
- [ ] Dark mode works (if applicable)
- [ ] No layout shift on load
- [ ] Lighthouse score > 90 (performance, accessibility, SEO)

---

## Related Skills

- `$design-figma` — for Figma-specific design work
- `$design-mobile` — for mobile app design
- `$design-desktop` — for desktop application design
- `$security-comprehensive` — for security review of web apps
- `$testing-web` — for testing web applications
