---
name: documentation-comprehensive
description: Complete documentation skill — Word (docx), PDF, PowerPoint (pptx), Excel (xlsx), technical writing, co-authoring, Notion, knowledge bases, Arabic/English bilingual docs, and internal communications. Use for ANY document creation, editing, or management task.
---

# Documentation Comprehensive — Complete Skill

## Overview

**Single skill for all documentation work.** Merges `doc-coauthoring`, `doc`, `docx`, `pdf`, `pptx`, `xlsx`, `internal-comms`, `docs-automation`, `cityofaiagents-documentation-authoring`, `cityofaiagents-translation-ops`, and all `notion-*` skills.

---

## 1. Document Co-Authoring (التأليف التعاوني)

### 1.1 Three-Stage Process
```
Stage 1: Context Gathering
  → User dumps all context
  → Ask clarifying questions (ONE at a time)
  → Identify audience and purpose

Stage 2: Refinement & Structure (per section)
  → Clarify the section goal
  → Brainstorm key points
  → Curate the best content
  → Gap check (what's missing?)
  → Draft the section
  → Refine the language

Stage 3: Reader Testing
  → Give to a fresh reader (new Claude session)
  → Ask 5-10 realistic questions
  → Fix confusion points
  → Final polish
```

### 1.2 Document Structure Template
```markdown
# [Document Title]

## Executive Summary (for leadership)
[2-3 sentences: what, why, impact]

## Problem / Context
[What situation led to this document?]

## Proposed Solution / Content
[The main body - organized logically]

## Implementation / Next Steps
[Action items with owners and dates]

## Risks & Mitigations
[What could go wrong + how to prevent]

## Appendix
[Supporting data, references]
```

---

## 2. Word Documents (.docx)

### 2.1 Creation (docx-js)
```javascript
const docx = require("docx");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, 
        AlignmentType, Table, TableRow, TableCell, WidthType } = docx;

const doc = new Document({
  sections: [{
    properties: {
      page: {
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }, // 1" in DXA
        size: { width: 12240, height: 15840 }, // US Letter
      }
    },
    children: [
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun({ text: "Title", bold: true, size: 32 })],
      }),
      new Paragraph({
        children: [new TextRun({ text: "Body text", size: 24 })],
        alignment: AlignmentType.JUSTIFIED,
      }),
    ]
  }]
});
```

### 2.2 Critical Rules
- ✅ Set page size explicitly (US Letter: 12240×15840 DXA)
- ✅ Tables: use `WidthType.DXA` with dual widths
- ✅ Bullets: use `LevelFormat.BULLET` (never unicode bullets)
- ✅ Validate after creation: `scripts/office/validate.py`
- ✅ Visual check: render DOCX → PDF → PNG and inspect

### 2.3 Editing Workflow
```
1. Unpack: python scripts/office/unpack.py doc.docx
2. Edit XML files directly
3. Pack: python scripts/office/pack.py doc.docx
4. Validate: python scripts/office/validate.py doc.docx
5. Visual check: render and inspect
```

### 2.4 python-docx Route (المسار البديل الأبسط)
For simple documents where docx-js/XML precision isn't needed:
```bash
pip install python-docx
```
```python
from docx import Document
from docx.shared import Pt, Inches

doc = Document()
doc.add_heading("Title", level=1)
p = doc.add_paragraph("Body text")
p.runs[0].font.size = Pt(12)
doc.add_page_break()
doc.save("out.docx")
```
- **Use python-docx for:** quick docs, programmatic generation, reading/modifying existing files
- **Use docx-js + XML unpack for:** precise formatting (TOC, letterhead, tracked changes, comments)
- Visual check: `scripts/render_docx.py` → soffice → pdftoppm → inspect at 100%
- **Reading:** `pandoc doc.docx -t markdown` (or python-docx paragraph iteration); `.doc` → convert to `.docx` first
- **Features:** TOC, headers/footers, tracked changes, comments, images, letterhead templates

---

## 3. PDF Documents

### 3.1 Creation
```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

c = canvas.Canvas("output.pdf", pagesize=A4)
width, height = A4

# Title
c.setFont("Helvetica-Bold", 24)
c.drawString(50, height - 50, "Document Title")

# Content
c.setFont("Helvetica", 12)
c.drawString(50, height - 80, "Body text here")

c.save()
```

### 3.2 Arabic PDF (RTL)
```python
import arabic_reshaper
from bidi.algorithm import get_display
from fpdf import FPDF

def ar(text):
    return get_display(arabic_reshaper.reshape(text))

pdf = FPDF()
pdf.add_font("Arial", "", "C:/Windows/Fonts/arial.ttf")
pdf.add_page()
pdf.set_font("Arial", "", 14)
pdf.multi_cell(0, 10, ar("نص عربي"), align="R")
pdf.output("arabic.pdf")
```

### 3.3 PDF Extraction (استخراج المحتوى)
When you must READ an existing PDF (tables, text, forms) rather than create one:
```bash
pip install pdfplumber pypdf
# Poppler for rendering (pdftoppm) — install: apt/poppler-utils or Windows bundle
```
```python
import pdfplumber

with pdfplumber.open("input.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()          # plain text
        tables = page.extract_tables()      # list of row-lists
        words = page.extract_words()        # with coordinates
```
- **Choose by need:** `pypdf` → merge/split/metadata; `pdfplumber` → text + tables + layout; `pdftoppm` → visual rendering
- Extraction is **lossy** for complex layouts — verify against a rendered page
- For form-filled PDFs, read field values with `pypdf` (`get_fields()`)

### 3.4 PDF Review
- Render every page: `pdftoppm -png input.pdf output`
- Inspect at 100% zoom
- Check: text readability, alignment, colors, images, page numbers

---

## 4. Presentations (.pptx)

### 4.1 Structure
```
Slide 1: Title (title + subtitle + presenter)
Slide 2: Agenda/Overview
Slides 3-N: Content (one key idea per slide)
Final: Summary + Q&A + Contact
```

### 4.2 Design Rules
- **One idea per slide** (not paragraphs)
- **Large text:** titles 36-44pt, body 24-28pt
- **Consistent layout:** use placeholders/master slides
- **Visual hierarchy:** title → subtitle → content
- **Images > text:** use visuals when possible
- **Color consistency:** 2-3 colors maximum
- **White space:** don't fill every pixel

### 4.3 Workflow
```
Read: markitdown or thumbnail → understand content
Edit: unpack → manipulate XML → pack
Create: pptxgenjs (JavaScript) → programmatic creation
QA: render slides as images → visual inspection
```

---

## 5. Spreadsheets (.xlsx)

### 5.1 Operations
- Read data (openpyxl, pandas)
- Add columns/rows
- Formulas (SUM, VLOOKUP, INDEX/MATCH)
- Formatting (conditional, number formats, charts)
- Data cleaning (deduplicate, normalize, fill missing)
- Pivot tables
- Export to CSV/TSV

### 5.2 Best Practices
- Header row with clear labels
- Consistent data types per column
- Formulas over hard-coded values (when possible)
- Conditional formatting for data visualization
- Freeze header row
- Named ranges for complex references

### 5.3 Financial Modeling Standards (معايير النمذجة المالية)
**Cell color coding** — the universal convention that makes models auditable:
| Color | Meaning |
|-------|---------|
| **Blue** font | Hard-coded inputs (constants you typed) |
| **Black** font | Formulas (calculated) |
| **Green** font | Links to other sheets in the same workbook |
| **Red** font | Links to external workbooks |
| **Yellow** fill | Key assumptions to highlight for reviewers |

**Number formats:**
- Years as text (`"2026"`) to avoid date coercion
- Zero values shown as a dash (`-`)
- Negatives in parentheses `(1,250)`
- Multiples as `0.0x` (e.g. `2.5x`)
- Percentages with consistent decimals

**Rules:**
- ✅ **Zero formula errors** — no `#REF!`, `#DIV/0!`, `#N/A` shipped, ever
- ✅ Professional font (Arial/Calibri), consistent size, aligned columns
- ✅ Preserve the template's existing structure/format when editing
- ✅ Separate inputs, calculations, and outputs into visually distinct areas

---

## 6. Internal Communications (الاتصالات الداخلية)

### 6.1 Document Types
| Type | Structure |
|------|-----------|
| **Status report** | What shipped, what's blocked, what's next |
| **Incident report** | Timeline, impact, root cause, actions |
| **Decision doc** | Context, options, decision, rationale |
| **RFC** | Problem, proposal, alternatives, impact |
| **Launch plan** | Features, timeline, risks, rollback |
| **Retro** | What went well, what didn't, actions |

### 6.2 Status Report Template
```markdown
# Status Report — [Date]

## 🟢 Shipped
- Feature A (link to PR)
- Bug fix B (link to issue)

## 🟡 In Progress
- Feature C — 70% complete, on track for Friday
- Feature D — blocked on API from team X

## 🔴 Blocked
- Feature E — waiting on security review (ETA: next week)

## 📊 Metrics
- Test coverage: 85% (+2%)
- Open bugs: 12 (-3)
- Deployments this week: 4

## 🎯 Next Week
- Complete Feature C
- Start Feature F
- Address code review feedback on Feature D
```

### 6.3 The 3P Update Format (تنسيق التحديث الثلاثي)
For quick recurring updates (standups, weekly leadership notes):
```
## Progress  — what shipped / moved since last update (facts + links)
## Plans     — what's next, with owners and dates
## Problems  — blockers + what's needed to unblock (ask explicitly)
```
- **Leadership updates:** lead with impact and numbers, not activity
- **Newsletters / FAQ:** plain language, scannable headings, no jargon
- Route by audience: operational (runbooks) ≠ stakeholder (status) ≠ developer (how-to)
- When in doubt, follow the project's `examples/` or guideline file for house style

---

## 7. Documentation Automation (أتمتة التوثيق)

### 7.1 Drift Detection
```bash
# Compare docs with code
1. Check if API docs match actual endpoints
2. Check if README commands still work
3. Check if architecture diagrams match code structure
4. Check if CHANGELOG includes latest changes
```

### 7.2 Doc Update Checklist
- [ ] README accurate (setup, commands, features)
- [ ] API documentation current (OpenAPI)
- [ ] Architecture docs reflect current design
- [ ] CHANGELOG updated for releases
- [ ] Inline code comments meaningful
- [ ] Examples run without errors
- [ ] Screenshots match current UI
- [ ] Links not broken

### 7.3 Docs Sync Plan (خطة المزامنة)
Build a durable, prioritized docs-backlog instead of ad-hoc edits:
```bash
python scripts/build_docs_sync_plan.py   # → docs_sync_plan.md
```
**Core reference files to maintain:**
| File | Purpose |
|------|---------|
| `source_of_truth.md` | Which artifact is authoritative for each topic (code vs doc vs ticket) |
| `runbook_patterns.md` | Recurring ops procedures captured as reusable patterns |
| `update_triggers.md` | What change forces which doc update (endpoint changed → update API doc) |
| **ownership map** | Who owns which doc — no orphaned docs |

**Doc-type separation** (never mix audiences): operational (runbooks) · stakeholder (status/briefs) · developer (how-to/reference).

**Failure modes:** docs updated without a source of truth → drift returns; docs edited without an owner → decay; triggers not defined → updates missed after every change.

---

## 8. Notion Integration

### 8.1 Operations
| Task | Skill | Action |
|------|-------|--------|
| Capture decision | `notion-knowledge-capture` | Create page with structure |
| Prepare meeting | `notion-meeting-intelligence` | Research + agenda |
| Research docs | `notion-research-documentation` | Multi-source synthesis |
| Spec → tasks | `notion-spec-to-implementation` | Convert to plan + tasks |

### 8.2 Notion Page Structure
```markdown
# [Page Title]
> Context: why this page exists

## Summary
[2-3 sentences]

## Details
[Main content with headings, lists, tables]

## Related
- [[Related Page 1]]
- [[Related Page 2]]

## Last Updated
[Date]
```

---

## 9. Bilingual Documentation (توثيق ثنائي اللغة)

### 9.1 Rules
- **Preserve verbatim:** commands, paths, code, IDs, technical terms
- **Translate prose:** descriptions, explanations, instructions
- **Internal docs:** English (for developers)
- **User-facing docs:** Arabic (for users)
- **Never translate:** code, file paths, API names, CLI commands

### 9.2 Anti-Mojibake Checklist
- [ ] Save as UTF-8
- [ ] Arabic characters render correctly
- [ ] No encoding errors (Ã, Ø, Ù replacements)
- [ ] Code blocks remain in English
- [ ] Mixed content renders properly (Arabic + English in same line)

---

## Bundled Tools (الأدوات المرفقة)

| Task | Tool |
|------|------|
| DOCX create (precise) | docx-js + `scripts/office/{unpack,pack,validate,soffice}.py` |
| DOCX quick route | `scripts/render_docx.py`, `python-docx` |
| Tracked changes / comments | `scripts/accept_changes.py`, `scripts/comment.py` |
| DOCX templates | `scripts/templates/` (comments, people XML) |
| PDF creation | reportlab; **extraction:** pdfplumber, pypdf; **render:** `pdftoppm` |
| PPTX | `scripts/office/soffice.py`, thumbnail + add_slide helpers |
| Comms examples | `examples/3p-updates.md`, `company-newsletter.md`, `faq-answers.md`, `general-comms.md` |
| Docs-sync references | `references/source_of_truth.md`, `runbook_patterns.md`, `update_triggers.md` |

**Rules:** validate every generated Office file; render → PNG and inspect at 100% before delivery.

---

## Verification Checklist (قائمة التحقق)

### For all documents:
- [ ] Content accurate (facts, numbers, links)
- [ ] Structure logical (headings, sections)
- [ ] Language clear (no jargon without explanation)
- [ ] Formatting consistent (fonts, spacing, colors)
- [ ] Visual check (render and inspect at 100%)
- [ ] No broken links or references
- [ ] Spelling and grammar checked
- [ ] Appropriate for target audience
- [ ] Version control (if applicable)
- [ ] Accessible (alt text, heading hierarchy)

### For Word/PDF:
- [ ] Page numbers correct
- [ ] Table of contents updated
- [ ] Headers/footers present
- [ ] Margins consistent
- [ ] Images not pixelated
- [ ] RTL rendering correct (Arabic docs)

### For presentations:
- [ ] One idea per slide
- [ ] Readable from back of room
- [ ] Consistent design throughout
- [ ] Animations purposeful (if any)
- [ ] No text overflow
