# Reading Support Components

Non-flashy, high-leverage components for reading comprehension: glossary popovers, callout variants, and worked examples with stepwise reveal.

## GlossaryPopover

Inline term definitions on hover/click. Includes "Add to Review" action for spaced repetition.

```tsx
// components/learning/GlossaryPopover.tsx
"use client";

import { useState, useRef, useEffect, ReactNode } from "react";
import { Plus } from "@geist-ui/icons";

interface GlossaryPopoverProps {
  term: string;
  definition: string;
  children: ReactNode; // The inline text to wrap
  onAddToReview?: (term: string) => void;
}

export function GlossaryPopover({ term, definition, children, onAddToReview }: GlossaryPopoverProps) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  // Close on outside click
  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    if (open) document.addEventListener("click", handleClick);
    return () => document.removeEventListener("click", handleClick);
  }, [open]);

  return (
    <span className="relative inline" ref={ref}>
      <button
        onClick={() => setOpen(!open)}
        className="border-b border-dashed border-blue-700/40 text-gray-1000 hover:border-blue-700 transition-colors cursor-help"
        aria-expanded={open}
        aria-haspopup="dialog"
      >
        {children}
      </button>

      {open && (
        <div
          className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 z-50 w-72 rounded-lg border border-gray-400 bg-background-200 p-4 shadow-lg animate-in fade-in zoom-in-95 duration-150"
          role="dialog"
          aria-label={`Definition of ${term}`}
        >
          <div className="flex items-start justify-between gap-2 mb-2">
            <h4 className="text-label-14 font-medium text-blue-700">{term}</h4>
            {onAddToReview && (
              <button
                onClick={() => onAddToReview(term)}
                className="rounded-md p-1 text-gray-400 hover:text-blue-700 transition-colors"
                aria-label={`Add "${term}" to review queue`}
              >
                <Plus size={14} />
              </button>
            )}
          </div>
          <p className="text-copy-14 text-gray-400">{definition}</p>
          {/* Arrow */}
          <div className="absolute left-1/2 -translate-x-1/2 top-full w-2 h-2 rotate-45 bg-background-200 border-r border-b border-gray-400" />
        </div>
      )}
    </span>
  );
}
```

### Mobile Behavior

On mobile (`< 650px`), the popover becomes a bottom sheet instead of hovering above:

```tsx
// Wrap popover content in a drawer for mobile
<Drawer open={open} onClose={() => setOpen(false)}>
  <Drawer.Content>
    <h4 className="text-label-16 font-medium mb-2">{term}</h4>
    <p className="text-copy-14 text-gray-400">{definition}</p>
  </Drawer.Content>
</Drawer>
```

## Callout

Geist Note/Alert variants adapted for learning context. Use sparingly — don't turn pages into a rainbow.

```tsx
// components/learning/Callout.tsx
import { ReactNode } from "react";
import { Info, AlertTriangle, CheckCircle, XCircle } from "@geist-ui/icons";

type CalloutType = "key-idea" | "pitfall" | "done" | "careful";

interface CalloutProps {
  type: CalloutType;
  title?: string;
  children: ReactNode;
}

const config: Record<CalloutType, {
  icon: typeof Info;
  defaultTitle: string;
  border: string;
  bg: string;
  iconColor: string;
  titleColor: string;
}> = {
  "key-idea": {
    icon: Info,
    defaultTitle: "Key Idea",
    border: "border-blue-700/30",
    bg: "bg-blue-700/5",
    iconColor: "text-blue-700",
    titleColor: "text-blue-700",
  },
  "pitfall": {
    icon: AlertTriangle,
    defaultTitle: "Common Pitfall",
    border: "border-amber-700/30",
    bg: "bg-amber-700/5",
    iconColor: "text-amber-700",
    titleColor: "text-amber-700",
  },
  "done": {
    icon: CheckCircle,
    defaultTitle: "You're Done",
    border: "border-green-700/30",
    bg: "bg-green-700/5",
    iconColor: "text-green-700",
    titleColor: "text-green-700",
  },
  "careful": {
    icon: XCircle,
    defaultTitle: "Careful",
    border: "border-red-700/30",
    bg: "bg-red-700/5",
    iconColor: "text-red-700",
    titleColor: "text-red-700",
  },
};

export function Callout({ type, title, children }: CalloutProps) {
  const c = config[type];
  const Icon = c.icon;

  return (
    <div className={`my-6 rounded-lg border ${c.border} ${c.bg} p-4`}>
      <div className="flex items-start gap-3">
        <Icon size={18} className={`${c.iconColor} shrink-0 mt-0.5`} />
        <div>
          <p className={`text-label-14 font-medium ${c.titleColor} mb-1`}>
            {title || c.defaultTitle}
          </p>
          <div className="text-copy-14 text-gray-400 [&>p]:mb-2 [&>p:last-child]:mb-0">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}
```

### When to Use Each Callout

| Type | Use For | Example |
|------|---------|---------|
| `key-idea` | Core concepts the learner must remember | "The key insight is that closures capture variables by reference, not value." |
| `pitfall` | Common mistakes to avoid | "Don't use `==` for object comparison in Java — it compares references, not values." |
| `done` | Congratulations / section complete | "You've completed the basics of binary search!" |
| `careful` | Dangerous operations or critical warnings | "This operation is destructive and cannot be undone." |

### Callout Frequency Rules

- **Max 2 callouts per lesson section** — more than that dilutes their impact
- **Don't stack callouts** — separate with at least 2-3 paragraphs of content
- **Use `key-idea` most** — it's the workhorse
- **Use `careful` least** — only for genuine danger

## WorkedExample

Stepwise reveal of a solution. Learner can try each step first, then reveal.

```tsx
// components/learning/WorkedExample.tsx
"use client";

import { useState, ReactNode } from "react";
import { ChevronRight, ChevronDown, Eye, EyeOff } from "@geist-ui/icons";

interface ExampleStep {
  label: string;
  content: ReactNode;
  tryPrompt?: string; // e.g. "Try to figure out the next step before revealing"
}

interface WorkedExampleProps {
  title: string;
  steps: ExampleStep[];
  revealMode?: "one-at-a-time" | "all-at-once";
}

export function WorkedExample({ title, steps, revealMode = "one-at-a-time" }: WorkedExampleProps) {
  const [revealedCount, setRevealedCount] = useState(1); // Step 1 always visible
  const [showAll, setShowAll] = useState(false);

  const visibleCount = showAll ? steps.length : revealedCount;

  function revealNext() {
    if (revealMode === "all-at-once") {
      setShowAll(true);
    } else {
      setRevealedCount((c) => Math.min(c + 1, steps.length));
    }
  }

  return (
    <div className="my-6 rounded-lg border border-gray-400 bg-background-200 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-400">
        <h4 className="text-label-14 font-medium">{title}</h4>
        <button
          onClick={() => setShowAll(!showAll)}
          className="flex items-center gap-1.5 text-label-12 text-gray-400 hover:text-gray-1000 transition-colors"
        >
          {showAll ? <EyeOff size={12} /> : <Eye size={12} />}
          {showAll ? "Hide Steps" : "Show All"}
        </button>
      </div>

      {/* Steps */}
      <div className="divide-y divide-gray-400/40">
        {steps.slice(0, visibleCount).map((step, i) => (
          <div key={i} className="px-4 py-4 animate-in fade-in slide-in-from-top-1 duration-200">
            <div className="flex items-start gap-3">
              <span className="flex h-6 w-6 items-center justify-center rounded-full bg-background-100 text-label-12 text-gray-400 shrink-0 border border-gray-400">
                {i + 1}
              </span>
              <div className="flex-1">
                <p className="text-label-14 font-medium mb-2">{step.label}</p>
                <div className="text-copy-14 text-gray-400">{step.content}</div>
              </div>
            </div>
          </div>
        ))}

        {/* "Try before revealing" prompt + reveal button */}
        {visibleCount < steps.length && (
          <div className="px-4 py-4">
            {steps[visibleCount]?.tryPrompt && (
              <p className="text-copy-14 text-blue-700 mb-3">
                {steps[visibleCount].tryPrompt}
              </p>
            )}
            <button
              onClick={revealNext}
              className="flex items-center gap-1.5 text-label-12 text-gray-400 hover:text-gray-1000 transition-colors"
            >
              {revealMode === "all-at-once" ? (
                <><ChevronDown size={12} /> Show All Remaining Steps</>
              ) : (
                <><ChevronRight size={12} /> Show Step {visibleCount + 1}</>
              )}
            </button>
          </div>
        )}

        {/* All done */}
        {visibleCount === steps.length && (
          <div className="px-4 py-3 bg-green-700/5">
            <p className="text-label-12 text-green-700">Complete — all {steps.length} steps shown</p>
          </div>
        )}
      </div>
    </div>
  );
}
```

## MDX Integration Pattern

All reading support components work as MDX shortcodes:

```mdx
{/* In lesson .mdx file */}

A <GlossaryPopover term="closure" definition="A function that captures variables from its enclosing scope">closure</GlossaryPopover> allows inner functions to access outer variables even after the outer function returns.

<Callout type="key-idea">
  Closures capture variables by **reference**, not by value. This means if the outer variable changes, the closure sees the new value.
</Callout>

<WorkedExample title="Closure Step by Step">
  {[
    { label: "Define outer function", content: <code>function outer() {'{'} let x = 10; ... {'}'}</code> },
    { label: "Define inner function", content: <code>function inner() {'{'} return x; {'}'}</code>, tryPrompt: "What does inner() return if x changes?" },
    { label: "Return inner", content: <code>return inner;</code> },
  ]}
</WorkedExample>

<Callout type="pitfall">
  In a loop, all closures share the same variable. Use `let` (block-scoped) instead of `var` to get per-iteration closures.
</Callout>
```
