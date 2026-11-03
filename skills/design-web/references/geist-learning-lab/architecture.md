# Architecture & Patterns

Next.js App Router structure, MDX content system, state management, and file organization for learning apps.

## App Router Structure

### Route Hierarchy

```
app/
├── layout.tsx                    → Root layout (fonts, theme, global providers)
├── page.tsx                      → Landing / course picker
├── learn/
│   ├── layout.tsx                → Learn layout (catalog chrome)
│   ├── page.tsx                  → Course catalog + resume banner
│   └── [courseSlug]/
│       ├── layout.tsx            → Course layout (progress rail sidebar)
│       ├── page.tsx              → Course overview (modules, progress, review queue)
│       ├── review/
│       │   └── page.tsx          → Spaced repetition review page
│       └── [moduleSlug]/
│           ├── layout.tsx        → Module layout (optional)
│           ├── page.tsx          → Module overview
│           └── [lessonSlug]/
│               └── page.tsx      → Lesson shell + content
```

### Layout Nesting

Each layout adds a layer of chrome:

```tsx
// app/layout.tsx — Root: fonts, theme, global CSS
import localFont from "next/font/local";

const geistSans = localFont({ src: "./fonts/GeistVF.woff", variable: "--font-sans" });
const geistMono = localFont({ src: "./fonts/GeistMonoVF.woff", variable: "--font-mono" });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className={`${geistSans.variable} ${geistMono.variable} font-sans bg-background-100 text-gray-1000 antialiased`}>
        {children}
      </body>
    </html>
  );
}
```

```tsx
// app/learn/[courseSlug]/layout.tsx — Course: sidebar + progress rail
import { ProgressRail } from "@/components/learning/ProgressRail";

export default function CourseLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { courseSlug: string };
}) {
  // Load course data, modules, progress
  return (
    <div className="flex min-h-screen">
      <aside className="hidden lg:block w-64 border-r border-gray-400 bg-background-100">
        <ProgressRail modules={modules} currentLesson={currentLesson} />
      </aside>
      <main className="flex-1">{children}</main>
    </div>
  );
}
```

## Content System: MDX

### File Structure

```
content/
├── courses/
│   ├── binary-search/
│   │   ├── course.json           → { title, description, modules: [...] }
│   │   ├── basics/
│   │   │   ├── what-is-binary-search.mdx
│   │   │   ├── the-algorithm.mdx
│   │   │   └── edge-cases.mdx
│   │   └── advanced/
│   │       ├── lower-bound.mdx
│   │       └── rotated-arrays.mdx
│   └── react-hooks/
│       ├── course.json
│       └── ...
```

### course.json Schema

```json
{
  "title": "Binary Search",
  "description": "Master the divide-and-conquer search algorithm.",
  "modules": [
    {
      "slug": "basics",
      "title": "Fundamentals",
      "lessons": [
        { "slug": "what-is-binary-search", "title": "What Is Binary Search?" },
        { "slug": "the-algorithm", "title": "The Algorithm" },
        { "slug": "edge-cases", "title": "Edge Cases" }
      ]
    },
    {
      "slug": "advanced",
      "title": "Advanced Patterns",
      "lessons": [
        { "slug": "lower-bound", "title": "Lower Bound" },
        { "slug": "rotated-arrays", "title": "Rotated Arrays" }
      ]
    }
  ]
}
```

### MDX Component Mapping

```tsx
// lib/mdx-components.tsx
import { CodePlayground } from "@/components/learning/CodePlayground";
import { QuickCheck } from "@/components/learning/QuickCheck";
import { Callout } from "@/components/learning/Callout";
import { ParameterDock } from "@/components/learning/ParameterDock";
import { CheckpointCard } from "@/components/learning/CheckpointCard";
import { GlossaryPopover } from "@/components/learning/GlossaryPopover";
import { WorkedExample } from "@/components/learning/WorkedExample";
import { BeforeAfterSplit } from "@/components/learning/BeforeAfterSplit";
import { HintLadder } from "@/components/learning/HintLadder";
import { DiffEditor } from "@/components/learning/DiffEditor";
import { ConceptExplorer } from "@/components/learning/ConceptExplorer";

export const mdxComponents = {
  CodePlayground,
  QuickCheck,
  Callout,
  ParameterDock,
  CheckpointCard,
  GlossaryPopover,
  WorkedExample,
  BeforeAfterSplit,
  HintLadder,
  DiffEditor,
  ConceptExplorer,
};
```

### MDX Setup with next-mdx-remote

```tsx
// app/learn/[courseSlug]/[moduleSlug]/[lessonSlug]/page.tsx
import { MDXRemote } from "next-mdx-remote/rsc";
import { mdxComponents } from "@/lib/mdx-components";
import { readFile } from "fs/promises";
import path from "path";

interface Props {
  params: { courseSlug: string; moduleSlug: string; lessonSlug: string };
}

export default async function LessonPage({ params }: Props) {
  const mdxPath = path.join(
    process.cwd(),
    "content/courses",
    params.courseSlug,
    params.moduleSlug,
    `${params.lessonSlug}.mdx`
  );
  const source = await readFile(mdxPath, "utf-8");

  return (
    <article className="mx-auto max-w-2xl px-6 py-8">
      <MDXRemote source={source} components={mdxComponents} />
    </article>
  );
}
```

## State Management

### Three Tiers

| Tier | What | Storage | Tool |
|------|------|---------|------|
| **Local UI** | Component interaction state (open/closed, selected tab) | React state | `useState`, `useReducer` |
| **Progress** | Lesson/step completion, attempts, confidence | localStorage → server | Zustand or Context |
| **Exploration** | Slider values, toggle states, selected views | URL search params | `useSearchParams` |

### Progress Store (Zustand)

```tsx
// lib/learning/progress-store.ts
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface Activity {
  status: "not-started" | "in-progress" | "completed";
  attempts: number;
  lastAttemptAt: number | null;
  confidence: "low" | "medium" | "high" | null;
  hintsUsed: number;
}

interface ProgressState {
  activities: Record<string, Activity>; // keyed by "courseSlug/moduleSlug/lessonSlug/stepId"
  getActivity: (key: string) => Activity;
  updateActivity: (key: string, update: Partial<Activity>) => void;
  completeActivity: (key: string, confidence?: "low" | "medium" | "high") => void;
  getCourseProgress: (courseSlug: string) => number; // percentage
}

const defaultActivity: Activity = {
  status: "not-started",
  attempts: 0,
  lastAttemptAt: null,
  confidence: null,
  hintsUsed: 0,
};

export const useProgressStore = create<ProgressState>()(
  persist(
    (set, get) => ({
      activities: {},

      getActivity(key) {
        return get().activities[key] || defaultActivity;
      },

      updateActivity(key, update) {
        set((state) => ({
          activities: {
            ...state.activities,
            [key]: { ...(state.activities[key] || defaultActivity), ...update },
          },
        }));
      },

      completeActivity(key, confidence) {
        set((state) => ({
          activities: {
            ...state.activities,
            [key]: {
              ...(state.activities[key] || defaultActivity),
              status: "completed",
              lastAttemptAt: Date.now(),
              confidence: confidence || null,
            },
          },
        }));
      },

      getCourseProgress(courseSlug) {
        const activities = get().activities;
        const courseActivities = Object.entries(activities).filter(
          ([key]) => key.startsWith(courseSlug + "/")
        );
        if (courseActivities.length === 0) return 0;
        const completed = courseActivities.filter(
          ([, a]) => a.status === "completed"
        ).length;
        return Math.round((completed / courseActivities.length) * 100);
      },
    }),
    { name: "learning-progress" }
  )
);
```

### URL State for Explorations

```tsx
// See explorable-explanations.md → useExplorationState hook
// All ParameterDock, slider, and toggle values sync to URL
// Enables sharing: "Look at this specific configuration"
```

## File Organization Summary

```
project/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── learn/
│       └── [courseSlug]/[moduleSlug]/[lessonSlug]/page.tsx
├── components/
│   └── learning/
│       ├── LessonShell.tsx
│       ├── ProgressRail.tsx
│       ├── StepFlow.tsx
│       ├── CheckpointCard.tsx
│       ├── ResumeBanner.tsx
│       ├── ParameterDock.tsx
│       ├── LiveOutputPanel.tsx
│       ├── ConceptExplorer.tsx
│       ├── InteractiveDiagram.tsx
│       ├── BeforeAfterSplit.tsx
│       ├── TimelineExplorer.tsx
│       ├── ConceptMap.tsx
│       ├── CodePlayground.tsx
│       ├── DiffEditor.tsx
│       ├── TaskRunner.tsx
│       ├── SnippetCopy.tsx
│       ├── QuickCheck.tsx
│       ├── ConfidenceRating.tsx
│       ├── HintLadder.tsx
│       ├── MistakeAnalyzer.tsx
│       ├── GlossaryPopover.tsx
│       ├── Callout.tsx
│       └── WorkedExample.tsx
├── content/
│   └── courses/
│       └── <courseSlug>/
│           ├── course.json
│           └── <moduleSlug>/<lessonSlug>.mdx
├── hooks/
│   ├── useExplorationState.ts
│   └── useReducedMotion.ts
├── lib/
│   ├── mdx-components.tsx
│   └── learning/
│       ├── progress-store.ts
│       ├── grading.ts
│       └── spaced.ts
└── public/
    └── fonts/
        ├── GeistVF.woff
        └── GeistMonoVF.woff
```

## Dependencies

```json
{
  "dependencies": {
    "next": "^15",
    "react": "^19",
    "next-mdx-remote": "^5",
    "@geist-ui/icons": "latest",
    "zustand": "^5",
    "framer-motion": "^12"
  },
  "devDependencies": {
    "tailwindcss": "^4",
    "@tailwindcss/typography": "latest"
  }
}
```
