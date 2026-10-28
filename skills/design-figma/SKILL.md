---
name: design-figma
description: Complete Figma design skill — reading designs, writing designs, building design systems, converting Figma to code and code to Figma, Code Connect, variables/tokens, component libraries, and design system rules. Use when working with Figma in any direction (Figma→Code, Code→Figma, or within Figma itself).
---

# Figma Design — Complete Skill

## Overview

The **single skill for all Figma work**. Covers both directions:
- **Figma → Code:** read and implement designs
- **Code → Figma:** generate designs and libraries
- **Within Figma:** create, edit, manage files and components

Merges `figma`, `figma-use`, `figma-implement-design`, `figma-generate-design`, `figma-generate-library`, `figma-create-new-file`, `figma-code-connect-components`, `figma-create-design-system-rules`, and `ui-asset-design-system-curator`.

---

## ⚠️ Mandatory Prerequisite

**Before ANY `use_figma` call, you MUST load `figma-use` skill.**

This is a hard rule. Skipping it causes:
- Font not loaded errors
- Incorrect color ranges
- Missing node IDs
- Broken auto-layout

---

## 1. Figma → Code (من التصميم للكود)

### 1.1 Workflow
```
1. Get design context   → get_design_context(nodeId)
2. Get metadata (large) → get_metadata(nodeId)
3. Get screenshot       → get_screenshot(nodeId)
4. Download assets      → images, icons, fonts
5. Implement in code    → match 1:1 visual fidelity
6. Verify               → compare screenshot with rendered output
```

### 1.2 Implementation Rules
- **Match exactly:** spacing, typography, colors, shadows, border-radius
- **Extract tokens:** convert Figma variables to CSS custom properties
- **Component mapping:** Figma component → code component (1:1)
- **State handling:** design only shows default; you add hover/focus/disabled
- **Responsive:** Figma shows one breakpoint; you make it responsive
- **Assets:** download all images/icons; optimize (WebP, SVG)
- **Fonts:** check font family, weight, size, line-height, letter-spacing

### 1.3 Common Patterns
| Figma Element | Code Equivalent |
|---------------|-----------------|
| Frame (fixed) | `<div>` with fixed dimensions |
| Frame (fill) | `<div>` with `flex: 1` or `width: 100%` |
| Auto Layout (H) | `display: flex; flex-direction: row` |
| Auto Layout (V) | `display: flex; flex-direction: column` |
| Component | React/Vue component |
| Instance | Component usage with props |
| Text (auto-height) | Text with natural wrapping |
| Text (fixed-width) | Text with `max-width` |
| Rectangle + fill | `<div>` with background color |
| Ellipse | `<div>` with `border-radius: 50%` |
| Boolean (visible) | Conditional rendering |

### 1.4 Extraction Checklist
- [ ] Colors (hex, opacity, gradients)
- [ ] Typography (family, size, weight, line-height, letter-spacing)
- [ ] Spacing (padding, margin, gap)
- [ ] Border radius (all corners or individual)
- [ ] Shadows (x, y, blur, spread, color)
- [ ] Borders (width, style, color)
- [ ] Layout (direction, alignment, distribution)
- [ ] Size (width, height, min/max)
- [ ] Images (download and optimize)
- [ ] Icons (SVG preferred)
- [ ] States (default, hover, focus, disabled, active)
- [ ] Responsive behavior (what changes at breakpoints?)

---

## 2. Code → Figma (من الكود لـFigma)

### 2.1 Screen Generation Workflow
```
1. Understand screen    → read code/description
2. Discover system      → search_design_system (components, variables, styles)
3. Create cover frame   → cover with project info
4. Build sections       → one use_figma call per section
5. Verify               → screenshots after each section
```

### 2.2 Design System Discovery
```javascript
// Before creating anything, search for existing:
search_design_system("components")  // Find reusable components
search_design_system("variables")   // Find color/spacing tokens
search_design_system("styles")      // Find text styles, effect styles
```

### 2.3 Design System Library Build (4 Stages)
```
Stage 0: Discovery & Scope (user approval)
Stage 1: Foundations (variables, color styles, text styles)
Stage 2: File Structure & Pages
Stage 3: Components (one by one with variants)
Stage 4: Integration & QA (Code Connect, accessibility, naming)
```

### 2.4 Variables & Tokens
```javascript
// Color variables
const colorPrimary = figma.variables.createVariable("color/primary", collection, "COLOR");
colorPrimary.setValueByMode(defaultMode, { r: 0, g: 0.47, b: 1 });

// Spacing variables  
const spacingMd = figma.variables.createVariable("spacing/md", collection, "FLOAT");
spacingMd.setValueByMode(defaultMode, 16);

// Typography variables
const fontSize = figma.variables.createVariable("font/size/body", collection, "FLOAT");
fontSize.setValueByMode(defaultMode, 16);
```

### 2.5 Component with Variants
```javascript
// Create component set with variants
const button = figma.createComponent();
button.name = "Button";

// Add variant properties
button.addComponentProperty("variant", "VARIANT", "primary");
button.addComponentProperty("size", "VARIANT", "md");
button.addComponentProperty("state", "VARIANT", "default");

// Create each combination as separate component
// primary/md/default, primary/md/hover, secondary/md/default, etc.
```

---

## 3. Within Figma (داخل Figma)

### 3.1 File Operations
- **Create new file:** `figma-create-new-file` (design or FigJam)
- **Read file:** get_metadata for structure
- **Read node:** get_design_context for specific element
- **Screenshot:** get_screenshot for visual reference

### 3.2 Plugin API Essentials (figma-use)
```javascript
// MANDATORY: load font before creating text
await figma.loadFontAsync({ family: "Inter", style: "Regular" });

// Create text
const text = figma.createText();
text.characters = "Hello";
text.fontSize = 16;

// Create frame with auto-layout
const frame = figma.createFrame();
frame.layoutMode = "HORIZONTAL";
frame.primaryAxisAlignItems = "CENTER";
frame.counterAxisAlignItems = "CENTER";
frame.itemSpacing = 8;
frame.paddingLeft = frame.paddingRight = 16;
frame.paddingTop = frame.paddingBottom = 8;

// Append child
parent.appendChild(child);

// Set fill
node.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }];

// Set stroke
node.strokes = [{ type: "SOLID", color: { r: 0.9, g: 0.9, b: 0.9 } }];
node.strokeWeight = 1;

// Return node IDs (required!)
return { textId: text.id, frameId: frame.id };
```

### 3.3 Rules
- ✅ Use `return` to output (never `closePlugin`/`notify`)
- ✅ Load fonts before creating/editing text
- ✅ Use `setCurrentPageAsync` for page switches (synchronous `setCurrentPage` is unreliable)
- ✅ Return all node IDs
- ✅ Set `FILL`/`HUG` after `appendChild` (sizing modes reset on reparent)
- ✅ Color values: 0–1 (not 0–255)
- ✅ One `use_figma` call per section/screen

**Additional critical rules:**
- ✅ **Atomic error recovery:** if a script fails mid-way, roll back partial nodes before retrying — never leave orphans
- ✅ **Position nodes away from 0,0** — new nodes at origin overlap existing content and are hard to find
- ✅ **Page must be loaded** before querying nodes on it; wait for the page to finish loading (`setCurrentPageAsync` + await)
- ✅ **Plugin data exceptions:** `setPluginData` has size limits; store large state on disk, not in plugin data
- ✅ Pass `skillNames` when the tool supports it so the platform can attribute the operation
- ✅ **20–100 calls per library build** — split large builds across many calls; each call is a checkpoint
- ✅ Verify after each stage (screenshot or re-query node counts) before proceeding

### 3.4 Library Build Discipline (انضباط بناء المكتبة)
```
Stage 0: Discovery & scope  → user approves what to build (no code yet)
Stage 1: Foundations        → variables, styles, themes (light/dark modes as separate variable collections)
Stage 2: File structure     → pages + naming conventions
Stage 3: Components         → one at a time, with variants
Stage 4: Integration        → Code Connect, a11y, naming audit
```
- **State Ledger:** track what's created (IDs, names, stage) on disk so an interrupted build can resume
- **Theming:** light/dark via variable modes on the SAME collection — not duplicated components
- Helper scripts (if present in this skill's `scripts/`): createVariableCollection, createComponentWithVariants, validateCreation, cleanupOrphans, rehydrateState

---

## 4. Code Connect (ربط الكود بالمكونات)

### 4.1 Workflow
```
1. Get suggestions  → get_code_connect_suggestions
2. Inspect code      → find matching components
3. Confirm           → ask user which to map
4. Send mappings     → send_code_connect_mappings (selected only)
```

### 4.2 Mapping Structure
```typescript
// Figma component → Code component
import { Button } from "./components/Button";

// Each prop maps a Figma variant to a code prop
figma.connect(Button, "figma://button", {
  props: {
    variant: figma.enum("variant", {
      primary: "primary",
      secondary: "secondary",
      danger: "danger",
    }),
    size: figma.enum("size", {
      sm: "small",
      md: "medium",
      lg: "large",
    }),
    disabled: figma.boolean("disabled"),
    children: figma.children("label"),
  },
});
```

### 4.3 Constraints (قيود)
- ✅ **Published library required** — components must come from a published library, not local drafts
- ✅ **Node ID required** — mappings reference the component's node ID (it changes if the component is recreated)
- ✅ **Org/Enterprise plan required** — Code Connect publishing is not available on free plans
- ✅ Confirm each mapping with the user before publishing (`send_code_connect_mappings` for chosen ones only)
- ❌ Never bulk-publish unverified suggestions

### 4.4 URL Parsing (تحليل روابط Figma)
```bash
# From: https://www.figma.com/design/<fileKey>/<name>?node-id=123-456
fileKey = "abc123XYZ"          # the segment after /design/ or /file/
nodeId  = "123-456"            # from ?node-id= (convert - to : for API use → "123:456")
```
- `fileKey` and `nodeId` drive every downstream call (`get_design_context`, `get_screenshot`, `use_figma`)
- Missing `node-id` → fetch metadata first to locate the target node

---

## 5. Design System Rules (قواعد نظام التصميم)

Generate rules for `CLAUDE.md`, `AGENTS.md`, or Cursor:

### 5.1 Rules File Structure
```markdown
# Design System Rules

## Components
- Button: use `Button` component, variants: primary/secondary/ghost
- Input: use `Input` component with `label` and `error` props
- Card: use `Card` component, no custom shadows

## Styling
- Use Tailwind CSS, no inline styles
- Colors from `--color-*` custom properties
- Spacing from 4px scale: `space-xs` to `space-2xl`

## Assets
- Icons from Lucide (not custom SVGs)
- Images: WebP format, lazy loaded
- Fonts: Inter (variable)

## Tokens
- Primary: #0078D4
- Radius: 8px (standard), 16px (large)
- Shadow: --shadow-md
```

### 5.2 Generation Flow
```
1. create_design_system_rules → get template
2. Analyze code → components, styling, architecture
3. Generate rules → tailored to project
4. Save to right agent file → AGENTS.md / CLAUDE.md
5. Re-verify periodically → keep rules current
```

---

## 6. Asset Curation (إدارة الأصول)

### 6.1 Safe Icon Sourcing
| Source | License | Use |
|--------|---------|-----|
| **Lucide** | MIT | UI icons ✅ |
| **Phosphor** | MIT | UI icons ✅ |
| **Heroicons** | MIT | UI icons ✅ |
| **Feather** | MIT | UI icons ✅ |
| **Material Icons** | Apache 2.0 | ✅ |
| **Brand logos** | Check license | ⚠️ verify |

### 6.2 Rules
- ✅ Use open icon libraries (MIT, Apache)
- ⚠️ Verify brand icon licenses before use
- ✅ Preserve RTL/LTR accessibility
- ✅ Include license attribution
- ❌ Never copy random icons from websites
- ❌ Never use protected brand icons without license

---

## 7. Common Commands (الأوامر الشائعة)

| Action | Command |
|--------|---------|
| Read design | `figma-implement-design` + URL |
| Create screen | `figma-generate-design` + description |
| Build library | `figma-generate-library` + codebase |
| New file | `figma-create-new-file` + type |
| Connect components | `figma-code-connect-components` |
| Edit in Figma | `figma-use` + plugin script |
| Design rules | `figma-create-design-system-rules` |
| Curate assets | `ui-asset-design-system-curator` |

---

## 8. Verification Checklist (قائمة التحقق)

### Figma → Code
- [ ] All colors match Figma exactly
- [ ] Typography matches (family, size, weight, spacing)
- [ ] All spacing matches (padding, margin, gap)
- [ ] Border radius matches
- [ ] Shadows match (x, y, blur, spread, color)
- [ ] Images downloaded and optimized
- [ ] Icons are SVG
- [ ] Responsive behavior implemented
- [ ] Interactive states added (hover, focus, disabled)
- [ ] Accessibility: alt text, contrast, keyboard nav
- [ ] Screenshot comparison passes

### Code → Figma
- [ ] Uses existing design system tokens
- [ ] Variables are properly defined
- [ ] Components have correct variants
- [ ] Auto-layout is correct (not manual positioning)
- [ ] Naming conventions followed
- [ ] Screens verified with screenshots

---

## Related Skills

- `$design-web` — for web implementation of Figma designs
- `$design-mobile` — for mobile implementation
- `$design-desktop` — for desktop implementation
- `$code-engineering` — for component architecture
