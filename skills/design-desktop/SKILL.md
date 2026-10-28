---
name: design-desktop
description: Desktop application design skill — PyQt/PySide, WinUI 3, Electron, Flet, Windows/macOS/Linux native UI patterns, window management, dialogs, menus, themes, glassmorphism, animations, and professional desktop UX. Use when building or reviewing any desktop application interface.
---

# Desktop Design — Complete Skill

## Overview

Covers **desktop application design** across platforms: Windows (WinUI, PyQt, Electron), macOS (HIG), Linux (GNOME/KDE). Merges `desktop-ui-designer`, `winui-app`, `cityofaiagents-ui-design-ops`, `cityofaiagents-desktop-ui-ops`, `flet-runtime-smoke-verifier`, `pyqt-test-engine`, and `desktop-e2e-automation`.

---

## 1. Platform Guidelines (إرشادات المنصة)

### 1.1 Windows (WinUI 3 / Fluent Design)
- **Typography:** Segoe UI Variable (dynamic sizing)
- **Colors:** Fluent theme (light/dark/high-contrast), Mica material
- **Spacing:** 4px base, standard margins 16px
- **Controls:** Button, TextBox, ComboBox, ListView, TreeView, TabView
- **Navigation:** NavigationView (left pane), breadcrumbs
- **Title bar:** custom title bar with integrated content
- **Acrylic/Mica:** frosted glass backgrounds for depth
- **Focus:** visible focus rectangle, keyboard navigation

### 1.2 macOS (Human Interface Guidelines)
- **Typography:** SF Pro (system), Monaco (code)
- **Controls:** NSButton, NSTextField, NSPopUpButton, NSTableView
- **Navigation:** toolbar, sidebar, tab bar (or split view)
- **Traffic lights:** close/minimize/maximize (top-left)
- **Menu bar:** application menu at top of screen
- **Corner radius:** 6-10px standard
- **Vibrancy:** translucency for sidebars and toolbars

### 1.3 Cross-Platform (Electron, Qt, Flet)
- **Electron:** Chromium + Node.js, HTML/CSS/JS rendering
- **Qt (PyQt/PySide):** native widgets, cross-platform
- **Flet:** Python-based, Flutter rendering
- **Custom title bar:** often needed for cross-platform consistency

---

## 2. Window Design (تصميم النافذة)

### 2.1 Window Types
| Type | Description | When to Use |
|------|-------------|-------------|
| **Main Window** | Primary application window | Main workspace |
| **Dialog** | Modal, focused task | Confirmations, settings |
| **Palette** | Small, always on top | Quick commands (VS Code) |
| **Utility** | Floating panels | Toolbars, inspectors |
| **Preferences** | Settings window | Application configuration |
| **About** | Information | Version, credits |

### 2.2 Window Layout
```
┌─────────────────────────────────────────┐
│ Title Bar (custom)          [─][□][×]   │
├──────┬──────────────────────────────────┤
│      │ Toolbar / Action Bar             │
│ Side ├───┬────┬────┬────┬───────────────┤
│ bar  │ Tab│ Tab│ Tab│    │              │
│      │    │    │    │    │  Main        │
│ Nav  ├───┴────┴────┴────┴──────────────┤
│      │ Status Bar                       │
└──────┴──────────────────────────────────┘
```

### 2.3 Window Behaviors
- **Resize:** min/max dimensions, aspect ratio lock (optional)
- **Position:** remember last position, center on first launch
- **Multi-window:** support for multiple instances
- **Always on top:** optional (utility panels)
- **Fullscreen:** F11 toggle or maximize

---

## 3. Navigation Patterns (أنماط التنقل)

### 3.1 Sidebar Navigation
- **Collapsed:** icon-only (48-64px)
- **Expanded:** icon + label (200-260px)
- **Sections:** grouped with headers
- **Active state:** highlight + left accent bar
- **Collapsible:** toggle button

### 3.2 Menu Bar
- **File:** New, Open, Save, Save As, Export, Print, Exit
- **Edit:** Undo, Redo, Cut, Copy, Paste, Find
- **View:** Zoom, Fullscreen, Themes, Panels
- **Help:** Documentation, About, Check for Updates

### 3.3 Tab System
- **Tabs:** file/project switching
- **Context menu:** close, close others, close all, pin
- **Drag:** reorder tabs
- **Dirty indicator:** dot for unsaved changes
- **Overflow:** dropdown for many tabs

### 3.4 Toolbar
- **Icons:** with tooltips (24×24px standard)
- **Groups:** related actions separated by dividers
- **Overflow:** "More" menu for secondary actions
- **Context-sensitive:** changes based on selected item
- **Customizable:** allow user to add/remove tools

### 3.5 Command Palette (Modern Pattern)
- **Shortcut:** Ctrl+K / Cmd+K
- **Search:** fuzzy match across all commands
- **Categories:** navigation, actions, settings
- **Recent:** show recently used commands first
- **Examples:** VS Code, Slack, Raycast

---

## 4. Component Design (تصميم المكونات)

### 4.1 Buttons
| Type | Visual | Use |
|------|--------|-----|
| Primary | Filled, brand color | Main action |
| Secondary | Outline/border | Alternative action |
| Ghost | Transparent | Low-priority actions |
| Danger | Red | Destructive actions |
| Icon | Square with icon | Toolbar actions |

### 4.2 Forms
- **Layout:** label left or top, input right or below
- **Group boxes:** section headers with borders
- **Advanced:** collapsible sections
- **Validation:** inline error icons + tooltip
- **Keyboard:** Tab order follows visual order, Enter submits

### 4.3 Data Display
- **Tables:** sortable columns, resizable, row selection
- **Tree views:** hierarchical data (files, categories)
- **Lists:** virtual scrolling for large datasets
- **Cards:** for visual content (galleries, dashboards)
- **Charts:** line, bar, pie for data visualization

### 4.4 Dialogs
- **Confirmation:** title + message + [Cancel] [Confirm]
- **Input:** title + label + input + [Cancel] [OK]
- **Settings:** tabbed or sidebar sections
- **Progress:** determinate (progress bar) or indeterminate (spinner)
- **Modal:** block interaction with parent window

### 4.5 Status Bar
- **Left:** current state (ready, processing)
- **Center:** contextual info (cursor position, selection count)
- **Right:** system info (zoom, connection, version)

---

## 5. Visual Design (التصميم البصري)

### 5.1 Themes
| Theme | Description |
|-------|-------------|
| **Light** | White/gray backgrounds, dark text |
| **Dark** | Dark backgrounds (#1E1E1E, #121212), light text |
| **High Contrast** | Maximum contrast for accessibility |
| **System** | Follow OS preference |

### 5.2 Modern Visual Effects
- **Glassmorphism:** frosted glass, backdrop blur, transparency
  - `backdrop-filter: blur(12px)`
  - Semi-transparent background: `rgba(255,255,255,0.7)`
  - Subtle border: `1px solid rgba(255,255,255,0.2)`
- **Mica (Windows):** system-tinted translucency
- **Acrylic (Windows):** blurred + noise texture
- **Neumorphism:** soft shadows, subtle 3D
  - `box-shadow: 5px 5px 10px #d9d9d9, -5px -5px 10px #ffffff`
- **Flat:** no shadows, solid colors, clean borders

### 5.3 Color System
```css
/* Light theme */
--bg-primary: #FFFFFF;
--bg-secondary: #F5F5F5;
--bg-tertiary: #E8E8E8;
--text-primary: #1A1A1A;
--text-secondary: #666666;
--border: #D0D0D0;
--accent: #0078D4;     /* Windows blue */
--accent-hover: #106EBE;
--success: #107C10;
--warning: #FFB900;
--error: #D13438;

/* Dark theme */
--bg-primary: #1E1E1E;
--bg-secondary: #252526;
--bg-tertiary: #2D2D30;
--text-primary: #FFFFFF;
--text-secondary: #9D9D9D;
--border: #404040;
--accent: #0078D4;
```

### 5.4 Icons
- **Style:** line icons (modern) or filled icons (classic)
- **Size:** 16px (inline), 24px (standard), 32px (large)
- **Color:** inherit from text, or accent for actions
- **Set:** Segoe Fluent Icons, Material Icons, Phosphor, Lucide

### 5.5 Shadows & Depth
- **Elevation levels:**
  - Level 0: no shadow (flat elements)
  - Level 1: `0 1px 3px rgba(0,0,0,0.1)` (cards)
  - Level 2: `0 4px 8px rgba(0,0,0,0.12)` (menus)
  - Level 3: `0 8px 16px rgba(0,0,0,0.14)` (modals)

---

## 6. Animation & Motion (الحركة)

### 6.1 Principles
- **Purpose:** guide attention, confirm action, show state change
- **Duration:** 150-300ms (standard), 50-100ms (micro)
- **Easing:** ease-out (entering), ease-in (exiting), ease-in-out (moving)
- **Consistent:** same animation for same type of action

### 6.2 Common Patterns
| Animation | Duration | Use |
|-----------|----------|-----|
| Window open | 200ms | Fade + scale up |
| Window close | 150ms | Fade + scale down |
| Dropdown | 150ms | Slide down + fade |
| Tooltip | 100ms | Fade in |
| Tab switch | 200ms | Slide + fade |
| Panel expand | 200ms | Height animation |
| Button press | 50ms | Scale down (0.98) |
| Loading | 1s loop | Spinner / skeleton |
| Notification | 200ms | Slide from right |

### 6.3 Performance
- Use GPU-accelerated properties: `transform`, `opacity`
- Avoid animating: `width`, `height`, `top`, `left`
- Limit concurrent animations (60 FPS budget)
- Respect `prefers-reduced-motion`

---

## 7. Responsive Desktop (المرونة)

### 7.1 Window Sizes
| Size | Dimensions | Layout |
|------|-----------|--------|
| Compact | 640-800px | Single column, sidebar hidden |
| Medium | 800-1200px | Two columns, sidebar collapsed |
| Expanded | 1200px+ | Full layout, sidebar expanded |

### 7.2 Layout Patterns
- **Resizable panels:** drag to resize sidebar, editor, inspector
- **Split views:** side-by-side or top-bottom
- **Zoom:** Ctrl+/- to scale UI (10%, 25%, 50%, 75%, 100%, 150%, 200%)
- **DPI awareness:** support high-DPI (200%, 300%)

### 7.3 Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| Ctrl/Cmd + S | Save |
| Ctrl/Cmd + Z | Undo |
| Ctrl/Cmd + Shift + Z | Redo |
| Ctrl/Cmd + K | Command palette |
| Ctrl/Cmd + P | Quick open |
| Ctrl/Cmd + / | Toggle sidebar |
| Ctrl/Cmd + Shift + P | Commands |
| F11 | Fullscreen |
| Ctrl/Cmd + Tab | Switch tabs |
| Escape | Close modal/cancel |

---

## 8. Desktop UX Patterns (أنماط تجربة المستخدم)

### 8.1 Auto-Save
- **Debounced:** save after 1-2s of inactivity
- **Indicator:** subtle "Saved" notification
- **Recovery:** crash recovery (auto-save to temp file)
- **Version history:** optional file history

### 8.2 Drag & Drop
- **Visual feedback:** ghost/drop target highlight
- **Accepted types:** show which items can be dropped
- **Invalid:** show "no drop" cursor
- **Multi-select:** Ctrl/Cmd + click, Shift + click for ranges

### 8.3 Context Menus
- **Right-click:** contextual actions
- **Sub-menus:** for related grouped actions
- **Shortcuts:** show keyboard shortcut next to action
- **Separator:** between action groups
- **Danger zone:** destructive actions at bottom with red color

### 8.4 Undo/Redo
- **Stack:** unlimited undo history
- **Grouping:** related actions grouped as one undo
- **Keyboard:** Ctrl+Z / Ctrl+Shift+Z
- **Menu:** Edit > Undo / Redo with action description

### 8.5 Search
- **Find:** Ctrl+F (within content)
- **Find & Replace:** Ctrl+H
- **Quick Open:** Ctrl+P (files)
- **Command Palette:** Ctrl+K (commands)
- **Incremental:** results update as you type

---

## 9. Windows-Specific (مخصص ويندوز)

### 9.1 WinUI 3 Development
- **Setup:** `winget configure -f config.yaml` → `dotnet new winui -o <name>`
- **Controls:** from Windows App SDK + CommunityToolkit
- **Themes:** XAML resource dictionaries
- **Navigation:** NavigationView with pane
- **Title bar:** `ExtendsContentIntoTitleBar`
- **Mica:** `SystemBackdrop` → `MicaBackdrop`

### 9.2 PyQt/PySide Development
- **Style:** QSS (Qt Style Sheets) or native
- **Custom title bar:** frameless window + custom controls
- **Threading:** QThread for background operations
- **Signal/slot:** event system
- **Testing:** pytest-qt with qtbot

### 9.3 OS Capability Detection & Legacy Fallback (كشف إمكانات النظام)
Detect capabilities before using modern visual features, and provide fallbacks:
```python
import platform, sys
IS_WIN7 = sys.getwindowsversion().major == 6 and sys.getwindowsversion().minor == 1
IS_32BIT = platform.architecture()[0] == "32bit"
```
- ✅ **Windows 7 / 32-bit support:** no acrylic/mica/composition; fall back to solid colors + standard frames
- ✅ Detect at startup; branch visuals (glass effects → solid theme) rather than crashing
- ✅ Theme extraction: read the OS theme (light/dark/high-contrast) and map to your tokens
- ❌ Never assume modern Windows APIs exist — feature-detect, don't version-sniff blindly

### 9.4 Flet Runtime Smoke Verification (فحص تشغيل Flet)
Before declaring a Flet app working, run a startup smoke check:
```
1. Discover entrypoint  → main.py / app.py (inspect imports & deps)
2. Launch               → run and confirm the window APPEARS and is RESPONSIVE
3. Blank-window check   → if window is blank: check deps installed, entrypoint correct,
                          Flet version (local vs CI), rendering backend
4. Version compare      → local flet --version vs CI flet version (mismatches cause blank output)
```
- ✅ A spawned process with exit code 0 is **not** proof — verify a responsive, non-blank window
- ❌ Never mark "runs" without visual confirmation

---

## 10. Accessibility (إمكانية الوصول)

### 10.1 Checklist
- [ ] All interactive elements keyboard-accessible
- [ ] Focus visible on every focusable element
- [ ] Tab order follows visual order
- [ ] Color contrast ≥ 4.5:1 (light), ≥ 4.5:1 (dark)
- [ ] Screen reader: Narrator (Windows), VoiceOver (macOS)
- [ ] High contrast mode supported
- [ ] Text scalable to 200% without loss of functionality
- [ ] All icons have accessible names
- [ ] Error messages associated with input fields
- [ ] No keyboard traps

### 10.2 Keyboard Navigation
- Tab: forward through controls
- Shift+Tab: backward
- Arrow keys: within composite widgets
- Enter/Space: activate
- Escape: close/cancel
- Alt+letter: menu access (legacy)

---

## 11. Design Spec Workflow (سير عمل مواصفة التصميم)

Research-backed spec produced **before** implementation. Ground every choice in a cited source — never invent guidelines.

### 11.1 Reference Sources (مصادر مرجعية)
| Source | Use for |
|--------|---------|
| **Apple HIG** | macOS patterns, controls, layout, motion |
| **Fluent 2 (Microsoft)** | Windows tokens, density, iconography |
| **Material 3 (Google)** | Android patterns, state layers, color roles |
| **Nielsen heuristics** | Usability, error prevention, match-to-world |

### 11.2 Spec Sections (أقسام المواصفة)
```
1. Information architecture  → what screens/panes exist and how they nest
2. Navigation strategy       → sidebar / tabs / menus; primary vs secondary
3. Spacing grid              → base unit (4/8pt), margins, gutters, density
4. Components                → which platform controls; when custom vs native
5. Theme tokens              → bg / surface / text / accent / border / radius / font
6. Accessibility             → contrast, focus order, keyboard map, screen reader
7. RTL / LTR                 → mirror layout; which elements must NOT mirror
```

### 11.3 Safety Rules (قواعد السلامة)
- ✅ Design changes are **presentation-only** — never alter behavior, permissions, licensing, or security during design work
- ✅ Destructive controls (delete / move / restore / license actions) are **visually isolated** and require explicit confirmation
- ✅ Preserve Windows (and any legacy OS) compatibility in the spec's constraints section
- ✅ Produce a spec document, not just mockups — implementation needs the rules

---

## 12. Verification Checklist (قائمة التحقق)

- [ ] Tested on target platform (Windows/macOS/Linux)
- [ ] Both light and dark themes
- [ ] High contrast mode
- [ ] All keyboard shortcuts work
- [ ] Focus order correct
- [ ] Screen reader announces all elements
- [ ] Window resize works (min/max)
- [ ] DPI scaling (100%, 150%, 200%)
- [ ] Multi-monitor support
- [ ] Performance: 60 FPS for animations
- [ ] Memory: no leaks on window open/close
- [ ] Crash recovery works
- [ ] All dialogs have cancel option
- [ ] Context menus have all expected actions

---

## Related Skills

- `$design-web` — for web interface design
- `$design-mobile` — for mobile app design
- `$design-figma` — for Figma design work
- `$testing-desktop` — for testing desktop applications
- `$code-engineering` — for code quality and architecture
