# Lesson Shell & Progress Components

The structural components that wrap every learning experience: layout, navigation, progress tracking, and resume functionality.

## LessonShell

Two/three-column responsive layout. Left: lesson nav + progress. Center: content (MDX + interactive blocks). Right (optional): lab panel.

```tsx
// components/learning/LessonShell.tsx
"use client";

import { ReactNode, useState } from "react";
import { ProgressRail } from "./ProgressRail";
import { Menu, X } from "@geist-ui/icons";

interface LessonShellProps {
  title: string;
  progress: number; // 0-100
  modules: Module[];
  currentLesson: string;
  children: ReactNode;
  labPanel?: ReactNode;
}

export function LessonShell({
  title,
  progress,
  modules,
  currentLesson,
  children,
  labPanel,
}: LessonShellProps) {
  const [navOpen, setNavOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background-100 text-gray-1000">
      {/* Sticky top bar */}
      <header className="sticky top-0 z-40 flex items-center justify-between border-b border-gray-400 bg-background-100/80 px-4 py-3 backdrop-blur-sm">
        <div className="flex items-center gap-3">
          <button
            onClick={() => setNavOpen(!navOpen)}
            className="rounded-md p-1.5 hover:bg-background-200 transition-colors lg:hidden"
            aria-label="Toggle navigation"
          >
            {navOpen ? <X size={18} /> : <Menu size={18} />}
          </button>
          <h1 className="text-label-14 font-medium truncate">{title}</h1>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-label-12-mono text-gray-400">{progress}%</span>
          <div className="h-1.5 w-24 rounded-full bg-background-200">
            <div
              className="h-full rounded-full bg-blue-700 transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Left: Progress rail / nav */}
        <aside
          className={`
            fixed inset-y-0 left-0 z-30 w-64 border-r border-gray-400 bg-background-100 pt-14
            transform transition-transform duration-200
            lg:relative lg:translate-x-0 lg:pt-0
            ${navOpen ? "translate-x-0" : "-translate-x-full"}
          `}
        >
          <ProgressRail
            modules={modules}
            currentLesson={currentLesson}
          />
        </aside>

        {/* Center: Lesson content */}
        <main className={`flex-1 px-6 py-8 ${labPanel ? "lg:max-w-3xl" : "mx-auto max-w-2xl"}`}>
          {children}
        </main>

        {/* Right: Lab panel (optional) */}
        {labPanel && (
          <aside className="hidden xl:block w-[440px] border-l border-gray-400 bg-background-200 p-6 overflow-y-auto sticky top-14 h-[calc(100vh-3.5rem)]">
            {labPanel}
          </aside>
        )}
      </div>

      {/* Overlay for mobile nav */}
      {navOpen && (
        <div
          className="fixed inset-0 z-20 bg-black/50 lg:hidden"
          onClick={() => setNavOpen(false)}
        />
      )}
    </div>
  );
}
```

## ProgressRail

Shows module map, current lesson, step dots, completion status. Collapses into drawer on mobile.

```tsx
// components/learning/ProgressRail.tsx
"use client";

import { CheckCircle, Circle, ArrowRight } from "@geist-ui/icons";

interface Step {
  slug: string;
  title: string;
  status: "completed" | "current" | "pending";
}

interface Module {
  slug: string;
  title: string;
  lessons: Step[];
}

interface ProgressRailProps {
  modules: Module[];
  currentLesson: string;
}

export function ProgressRail({ modules, currentLesson }: ProgressRailProps) {
  return (
    <nav className="p-4 space-y-6 overflow-y-auto h-full" aria-label="Course progress">
      {modules.map((mod) => (
        <div key={mod.slug}>
          <h3 className="text-label-12 text-gray-400 uppercase tracking-wider mb-3">
            {mod.title}
          </h3>
          <ul className="space-y-1">
            {mod.lessons.map((lesson) => (
              <li key={lesson.slug}>
                <a
                  href={`#${lesson.slug}`}
                  className={`
                    flex items-center gap-2.5 rounded-md px-3 py-2 text-copy-14 transition-colors
                    ${lesson.status === "current"
                      ? "bg-blue-700/10 text-blue-700 font-medium"
                      : lesson.status === "completed"
                        ? "text-gray-400 hover:text-gray-1000"
                        : "text-gray-400/60 hover:text-gray-400"
                    }
                  `}
                  aria-current={lesson.status === "current" ? "step" : undefined}
                >
                  {lesson.status === "completed" ? (
                    <CheckCircle size={14} className="text-green-700 shrink-0" />
                  ) : lesson.status === "current" ? (
                    <ArrowRight size={14} className="text-blue-700 shrink-0" />
                  ) : (
                    <Circle size={14} className="text-gray-400/40 shrink-0" />
                  )}
                  <span className="truncate">{lesson.title}</span>
                </a>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </nav>
  );
}
```

## StepFlow

Step-by-step lesson flow with gating, progress, and multiple modes.

```tsx
// components/learning/StepFlow.tsx
"use client";

import { useState, ReactNode } from "react";

type StepMode = "guided" | "explore" | "review";

interface Step {
  id: string;
  title: string;
  content: ReactNode;
  check?: () => boolean; // gating function for guided mode
}

interface StepFlowProps {
  steps: Step[];
  mode?: StepMode;
  onComplete?: () => void;
}

export function StepFlow({ steps, mode = "guided", onComplete }: StepFlowProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [completedSteps, setCompletedSteps] = useState<Set<string>>(new Set());

  const canProceed = mode === "explore" || mode === "review"
    || !steps[currentIndex]?.check
    || steps[currentIndex].check();

  function handleNext() {
    setCompletedSteps((prev) => new Set(prev).add(steps[currentIndex].id));
    if (currentIndex < steps.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      onComplete?.();
    }
  }

  function handleBack() {
    if (currentIndex > 0) setCurrentIndex(currentIndex - 1);
  }

  return (
    <div>
      {/* Step indicators */}
      <div className="flex items-center gap-2 mb-6" role="tablist" aria-label="Lesson steps">
        {steps.map((step, i) => (
          <button
            key={step.id}
            onClick={() => mode !== "guided" && setCurrentIndex(i)}
            disabled={mode === "guided" && i > currentIndex}
            className={`
              flex items-center gap-1.5 text-label-12 transition-colors
              ${i === currentIndex
                ? "text-blue-700"
                : completedSteps.has(step.id)
                  ? "text-green-700"
                  : "text-gray-400/60"
              }
              ${mode !== "guided" ? "cursor-pointer hover:text-gray-1000" : ""}
            `}
            role="tab"
            aria-selected={i === currentIndex}
          >
            <span className={`
              flex h-6 w-6 items-center justify-center rounded-full text-xs font-medium
              ${i === currentIndex
                ? "bg-blue-700 text-white"
                : completedSteps.has(step.id)
                  ? "bg-green-700/20 text-green-700"
                  : "bg-background-200 text-gray-400"
              }
            `}>
              {completedSteps.has(step.id) ? "✓" : i + 1}
            </span>
            <span className="hidden sm:inline">{step.title}</span>
          </button>
        ))}
      </div>

      {/* Step content */}
      <div className="min-h-[200px]" role="tabpanel">
        {steps[currentIndex]?.content}
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between mt-8 pt-4 border-t border-gray-400">
        <button
          onClick={handleBack}
          disabled={currentIndex === 0}
          className="px-4 py-2 rounded-md border border-gray-400 text-gray-400 text-sm hover:border-gray-300 transition-colors disabled:opacity-30"
        >
          Back
        </button>
        <span className="text-label-12-mono text-gray-400">
          {currentIndex + 1} / {steps.length}
        </span>
        <button
          onClick={handleNext}
          disabled={!canProceed}
          className="px-4 py-2 rounded-md bg-white text-black text-sm font-medium hover:bg-gray-200 transition-colors disabled:opacity-30"
        >
          {currentIndex === steps.length - 1 ? "Complete" : "Continue"}
        </button>
      </div>
    </div>
  );
}
```

## CheckpointCard

A "stop and do it" section that interrupts reading. Contains prompt, input UI, check, feedback.

```tsx
// components/learning/CheckpointCard.tsx
"use client";

import { useState, ReactNode } from "react";

interface CheckpointCardProps {
  prompt: string;
  children: ReactNode; // The input/interaction UI
  onCheck: () => { correct: boolean; explanation: string };
  whatYouLearned?: string;
}

export function CheckpointCard({ prompt, children, onCheck, whatYouLearned }: CheckpointCardProps) {
  const [result, setResult] = useState<{ correct: boolean; explanation: string } | null>(null);

  function handleCheck() {
    setResult(onCheck());
  }

  return (
    <div className="my-8 rounded-lg border border-blue-700/40 bg-blue-700/5 p-6">
      <div className="flex items-start gap-3 mb-4">
        <span className="flex h-6 w-6 items-center justify-center rounded-full bg-blue-700 text-white text-xs font-bold shrink-0">?</span>
        <p className="text-copy-16 font-medium">{prompt}</p>
      </div>

      <div className="ml-9 space-y-4">
        {children}

        {!result && (
          <button
            onClick={handleCheck}
            className="px-4 py-2 rounded-md bg-white text-black text-sm font-medium hover:bg-gray-200 transition-colors"
          >
            Check Answer
          </button>
        )}

        {/* Feedback surface */}
        {result && (
          <div
            className={`rounded-md p-4 ${
              result.correct
                ? "bg-green-700/10 border border-green-700/30"
                : "bg-red-700/10 border border-red-700/30"
            }`}
            role="alert"
            aria-live="polite"
          >
            <p className={`text-label-14 font-medium mb-1 ${result.correct ? "text-green-700" : "text-red-700"}`}>
              {result.correct ? "Correct" : "Not Quite"}
            </p>
            <p className="text-copy-14 text-gray-400">{result.explanation}</p>
          </div>
        )}

        {result?.correct && whatYouLearned && (
          <div className="rounded-md bg-background-200 p-4 border border-gray-400">
            <p className="text-label-12 text-gray-400 mb-1">What You Learned</p>
            <p className="text-copy-14">{whatYouLearned}</p>
          </div>
        )}
      </div>
    </div>
  );
}
```

## ResumeBanner

Detects last completed step and offers "Resume Step 7: ..." after returning to a course.

```tsx
// components/learning/ResumeBanner.tsx
"use client";

import { ArrowRight } from "@geist-ui/icons";

interface ResumeBannerProps {
  lessonTitle: string;
  stepNumber: number;
  stepTitle: string;
  onResume: () => void;
}

export function ResumeBanner({ lessonTitle, stepNumber, stepTitle, onResume }: ResumeBannerProps) {
  return (
    <div className="flex items-center justify-between rounded-lg border border-blue-700/30 bg-blue-700/5 px-4 py-3 mb-6">
      <div>
        <p className="text-label-12 text-blue-700 mb-0.5">Continue Where You Left Off</p>
        <p className="text-copy-14">
          <span className="text-gray-400">{lessonTitle}</span>
          {" · "}
          <span className="font-medium">Step {stepNumber}: {stepTitle}</span>
        </p>
      </div>
      <button
        onClick={onResume}
        className="flex items-center gap-1.5 rounded-md bg-blue-700 px-3 py-1.5 text-sm text-white font-medium hover:bg-blue-600 transition-colors"
      >
        Resume <ArrowRight size={14} />
      </button>
    </div>
  );
}
```

## Responsive Behavior

| Breakpoint | Nav | Content | Lab Panel |
|-----------|-----|---------|-----------|
| Mobile (<650px) | Drawer overlay | Full width, px-4 | Hidden (below content as tab) |
| Tablet (650-1280px) | Fixed sidebar 240px | Fluid, max-w-2xl | Hidden or drawer |
| Desktop (1280px+) | Fixed sidebar 256px | Fluid, max-w-3xl | Fixed 440px right panel |

## Keyboard Navigation

| Key | Action |
|-----|--------|
| `←` / `→` | Previous / next step (in StepFlow) |
| `Enter` | Check answer (when checkpoint focused) |
| `Escape` | Close mobile nav drawer |
| `Tab` | Standard focus progression through interactive elements |
