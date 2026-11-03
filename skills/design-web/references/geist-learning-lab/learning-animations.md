# Learning Animations

Animation patterns specific to learning UIs: step transitions, feedback reveals, diagram animations, progress celebrations, and reduced-motion compliance.

## Core Principles

1. **Animate as feedback to user input** — Never autoplay. Animation responds to interaction.
2. **Animate `transform` + `opacity` only** — GPU-composited, no layout thrash.
3. **Respect `prefers-reduced-motion`** — Instant transitions for users who prefer it.
4. **150-300ms durations** — Tight, purposeful, not decorative.
5. **CSS transitions first** — Use Framer Motion only when CSS can't express the animation.

## Reduced Motion Hook

```tsx
// hooks/useReducedMotion.ts
"use client";

import { useState, useEffect } from "react";

export function useReducedMotion(): boolean {
  const [prefersReduced, setPrefersReduced] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setPrefersReduced(mq.matches);
    const handler = (e: MediaQueryListEvent) => setPrefersReduced(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  return prefersReduced;
}
```

## Step Transitions

When navigating between lesson steps in StepFlow:

```tsx
// CSS-only step transition
<div
  className="animate-in fade-in slide-in-from-right-4 duration-200"
  key={currentStepId} // Re-mount triggers animation
>
  {stepContent}
</div>
```

### With Framer Motion (if more control needed)

```tsx
import { motion, AnimatePresence } from "framer-motion";

const stepVariants = {
  enter: (direction: number) => ({
    x: direction > 0 ? 20 : -20,
    opacity: 0,
  }),
  center: {
    x: 0,
    opacity: 1,
  },
  exit: (direction: number) => ({
    x: direction < 0 ? 20 : -20,
    opacity: 0,
  }),
};

<AnimatePresence mode="wait" custom={direction}>
  <motion.div
    key={currentStepId}
    custom={direction}
    variants={stepVariants}
    initial="enter"
    animate="center"
    exit="exit"
    transition={{ duration: 0.2, ease: [0.25, 0.1, 0.25, 1] }}
  >
    {stepContent}
  </motion.div>
</AnimatePresence>
```

### Reduced Motion Fallback

```tsx
const reduced = useReducedMotion();

<AnimatePresence mode="wait">
  <motion.div
    key={currentStepId}
    initial={reduced ? false : { opacity: 0, x: 20 }}
    animate={{ opacity: 1, x: 0 }}
    exit={reduced ? undefined : { opacity: 0, x: -20 }}
    transition={{ duration: reduced ? 0 : 0.2 }}
  >
    {stepContent}
  </motion.div>
</AnimatePresence>
```

## Feedback Reveals

When showing correct/incorrect feedback after a quiz answer:

```tsx
// Feedback panel reveal
<div
  className={`
    rounded-md p-4
    animate-in fade-in slide-in-from-bottom-2 duration-200
    ${correct ? "bg-green-700/10 border border-green-700/30" : "bg-red-700/10 border border-red-700/30"}
  `}
  role="alert"
  aria-live="polite"
>
  {feedbackContent}
</div>
```

### Correct Answer Celebration (Subtle)

```tsx
// A brief scale pulse on the success icon — not confetti, not fireworks
<motion.div
  initial={{ scale: 0.8, opacity: 0 }}
  animate={{ scale: 1, opacity: 1 }}
  transition={{
    type: "spring",
    stiffness: 400,
    damping: 15,
  }}
>
  <CheckCircle className="text-green-700" size={24} />
</motion.div>
```

## Hint Reveals

Progressive hints slide in from below:

```tsx
// Each hint animates in when revealed
<div className="animate-in fade-in slide-in-from-bottom-1 duration-200">
  <div className="rounded-md bg-amber-700/5 border border-amber-700/20 px-4 py-3">
    {hintContent}
  </div>
</div>
```

## Diagram Animations

### SVG Element Transitions

For InteractiveDiagram elements that move in response to parameters:

```tsx
// SVG circle that moves when value changes
<circle
  cx={computedX}
  cy={computedY}
  r={8}
  fill="#0070F3"
  style={{
    transition: reduced ? "none" : "cx 200ms ease-out, cy 200ms ease-out",
  }}
/>

// SVG rect that resizes
<rect
  x={0}
  y={barTop}
  width={barWidth}
  height={barHeight}
  fill={highlighted ? "#46A758" : "#737373"}
  rx={2}
  style={{
    transition: reduced ? "none" : "all 150ms ease-out",
  }}
/>
```

### Array Visualization (Binary Search Example)

```tsx
// Highlighting array elements during algorithm steps
{array.map((value, i) => {
  const isActive = i >= low && i <= high;
  const isMid = i === mid;
  const isFound = i === targetIndex;

  return (
    <rect
      key={i}
      x={i * (barWidth + gap)}
      y={0}
      width={barWidth}
      height={barHeight}
      rx={2}
      fill={
        isFound ? "#46A758"
        : isMid ? "#0070F3"
        : isActive ? "#737373"
        : "#737373"
      }
      opacity={isActive ? 1 : 0.2}
      style={{
        transition: reduced ? "none" : "fill 200ms, opacity 200ms",
      }}
    />
  );
})}
```

## Progress Animations

### Progress Bar Fill

```tsx
<div className="h-1.5 w-full rounded-full bg-background-200 overflow-hidden">
  <div
    className="h-full rounded-full bg-blue-700"
    style={{
      width: `${percentage}%`,
      transition: "width 500ms ease-out",
    }}
  />
</div>
```

### Step Completion Dot

```tsx
// Dot transitions from gray to green when step completes
<span
  className={`
    h-2.5 w-2.5 rounded-full transition-colors duration-300
    ${completed ? "bg-green-700" : current ? "bg-blue-700" : "bg-gray-400/40"}
  `}
/>
```

### Lesson Completion

```tsx
// Subtle celebration: check icon with spring + progress bar completes
<motion.div
  initial={{ scale: 0, rotate: -45 }}
  animate={{ scale: 1, rotate: 0 }}
  transition={{ type: "spring", stiffness: 300, damping: 20 }}
  className="flex items-center justify-center h-12 w-12 rounded-full bg-green-700/10"
>
  <CheckCircle className="text-green-700" size={28} />
</motion.div>
```

## Collapsible/Disclosure Animations

For "Why This Works", "Edge Cases", and other progressive disclosure panels:

```tsx
// CSS Grid height animation (no fixed height needed)
<div
  className="grid transition-[grid-template-rows] duration-200 ease-out"
  style={{ gridTemplateRows: isOpen ? "1fr" : "0fr" }}
>
  <div className="overflow-hidden">
    <div className="py-3">{content}</div>
  </div>
</div>
```

## Popover/Tooltip Animations

For GlossaryPopover and ConceptExplorer hotspot panels:

```tsx
// Scale-in from origin point
<div className="animate-in fade-in zoom-in-95 duration-150">
  {popoverContent}
</div>

// Or with Framer Motion for exit animation
<AnimatePresence>
  {isOpen && (
    <motion.div
      initial={{ opacity: 0, scale: 0.95, y: 4 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95, y: 4 }}
      transition={{ duration: 0.15 }}
    >
      {popoverContent}
    </motion.div>
  )}
</AnimatePresence>
```

## BeforeAfterSplit Divider

The draggable divider in BeforeAfterSplit should move smoothly with the cursor — no transition needed (it follows the mouse directly). But the initial appearance should fade in:

```tsx
<div
  className="absolute top-0 bottom-0 w-0.5 bg-blue-700 animate-in fade-in duration-300"
  style={{ left: `${splitPosition}%` }}
/>
```

## Animation Duration Reference

| Animation | Duration | Easing | When |
|-----------|---------|--------|------|
| Step transition | 200ms | ease-out | Navigate between steps |
| Feedback reveal | 200ms | ease-out | Show correct/incorrect |
| Hint reveal | 200ms | ease-out | Show next hint |
| Popover open | 150ms | ease-out | Open glossary/hotspot |
| Popover close | 150ms | ease-in | Close glossary/hotspot |
| Disclosure expand | 200ms | ease-out | Open "Why This Works" |
| Diagram element move | 200ms | ease-out | Respond to parameter change |
| Progress bar fill | 500ms | ease-out | Progress update |
| Success icon | spring(400, 15) | spring | Correct answer celebration |
| Completion check | spring(300, 20) | spring | Lesson complete |

## CSS Animation Utilities

Use Tailwind's built-in animation utilities where possible:

```
animate-in           → Trigger entrance animation
fade-in              → Opacity 0 → 1
slide-in-from-top-N  → translateY(-Npx) → 0
slide-in-from-bottom-N → translateY(Npx) → 0
slide-in-from-left-N → translateX(-Npx) → 0
slide-in-from-right-N → translateX(Npx) → 0
zoom-in-95           → scale(0.95) → 1
duration-150         → 150ms
duration-200         → 200ms
duration-300         → 300ms
```

Combine them: `animate-in fade-in slide-in-from-bottom-2 duration-200`

## What NOT to Animate

- **Page loads** — Content should be instantly visible, not staggered in
- **Text appearing** — No typewriter effects. Text is text.
- **Scroll-triggered animations** — Distraction, not pedagogy
- **Looping/idle animations** — Nothing moves unless the learner caused it
- **Confetti/particles** — We're teaching, not celebrating a purchase
- **Color cycling** — Colors are semantic signals, not decoration
