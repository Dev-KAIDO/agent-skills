# Progress & State Management

Progress tracking schema, localStorage adapter, spaced repetition scheduling, URL state for shareable explorations, and review queue.

## Progress Schema

### Data Model

```
Course → Module → Lesson → Step → Activity
```

Each activity is the smallest trackable unit:

```typescript
// lib/learning/types.ts

interface Activity {
  status: "not-started" | "in-progress" | "completed";
  attempts: number;
  lastAttemptAt: number | null;        // Unix timestamp
  confidence: "low" | "medium" | "high" | null;
  hintsUsed: number;
  score?: number;                       // Optional: 0-100
}

interface ReviewItem {
  key: string;                          // activity key or glossary term
  type: "quiz" | "glossary" | "checkpoint";
  question: string;
  answer: string;
  confidence: "low" | "medium" | "high";
  nextReviewAt: number;                 // Unix timestamp
  interval: number;                     // Days until next review
  reviewCount: number;
}

interface CourseProgress {
  courseSlug: string;
  startedAt: number;
  lastAccessedAt: number;
  completedModules: string[];
  currentLesson: string;               // "moduleSlug/lessonSlug"
  currentStep: number;
}
```

### Activity Keys

Activities are keyed by path: `"courseSlug/moduleSlug/lessonSlug/stepId"`

```
binary-search/basics/the-algorithm/step-1
binary-search/basics/the-algorithm/quickcheck-midpoint
binary-search/basics/edge-cases/checkpoint
```

## localStorage Adapter

### Storage Implementation

```typescript
// lib/learning/progress.ts

const STORAGE_KEY = "learning-progress";
const REVIEW_KEY = "learning-review-queue";

export function loadProgress(): Record<string, Activity> {
  if (typeof window === "undefined") return {};
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

export function saveProgress(activities: Record<string, Activity>): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(activities));
}

export function loadReviewQueue(): ReviewItem[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(REVIEW_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export function saveReviewQueue(items: ReviewItem[]): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(REVIEW_KEY, JSON.stringify(items));
}
```

### Progress Calculation

```typescript
// lib/learning/progress.ts

export function calculateProgress(
  activities: Record<string, Activity>,
  courseSlug: string
): { percentage: number; completed: number; total: number } {
  const courseActivities = Object.entries(activities).filter(
    ([key]) => key.startsWith(`${courseSlug}/`)
  );
  const total = courseActivities.length;
  if (total === 0) return { percentage: 0, completed: 0, total: 0 };
  const completed = courseActivities.filter(([, a]) => a.status === "completed").length;
  return {
    percentage: Math.round((completed / total) * 100),
    completed,
    total,
  };
}

export function getLastPosition(
  activities: Record<string, Activity>,
  courseSlug: string
): { moduleSlug: string; lessonSlug: string; step: number } | null {
  const courseActivities = Object.entries(activities)
    .filter(([key]) => key.startsWith(`${courseSlug}/`))
    .filter(([, a]) => a.status === "in-progress" || a.status === "completed")
    .sort(([, a], [, b]) => (b.lastAttemptAt || 0) - (a.lastAttemptAt || 0));

  if (courseActivities.length === 0) return null;

  const [key] = courseActivities[0];
  const parts = key.split("/");
  return {
    moduleSlug: parts[1],
    lessonSlug: parts[2],
    step: parseInt(parts[3]?.replace(/\D/g, "") || "0"),
  };
}
```

## Spaced Repetition Scheduler

### Scheduling Algorithm

Simple, effective, no external deps:

```typescript
// lib/learning/spaced.ts

const INTERVALS: Record<string, number> = {
  low: 1,      // 1 day
  medium: 3,   // 3 days
  high: 7,     // 7 days
};

const PROMOTION: Record<string, string> = {
  low: "medium",
  medium: "high",
  high: "high",  // stays at high, interval doubles
};

const MS_PER_DAY = 86400000;

export function scheduleReview(
  item: ReviewItem,
  correct: boolean,
  newConfidence: "low" | "medium" | "high"
): ReviewItem {
  if (correct) {
    const promoted = PROMOTION[item.confidence] as "low" | "medium" | "high";
    const newInterval = item.confidence === "high"
      ? Math.min(item.interval * 2, 30) // Cap at 30 days
      : INTERVALS[promoted];

    return {
      ...item,
      confidence: promoted,
      interval: newInterval,
      nextReviewAt: Date.now() + newInterval * MS_PER_DAY,
      reviewCount: item.reviewCount + 1,
    };
  } else {
    // Reset to low
    return {
      ...item,
      confidence: "low",
      interval: INTERVALS.low,
      nextReviewAt: Date.now() + INTERVALS.low * MS_PER_DAY,
      reviewCount: item.reviewCount + 1,
    };
  }
}

export function getDueItems(items: ReviewItem[]): ReviewItem[] {
  const now = Date.now();
  return items
    .filter((item) => item.nextReviewAt <= now)
    .sort((a, b) => a.nextReviewAt - b.nextReviewAt);
}

export function addToReviewQueue(
  items: ReviewItem[],
  newItem: Omit<ReviewItem, "nextReviewAt" | "interval" | "reviewCount">
): ReviewItem[] {
  // Don't add duplicates
  if (items.some((i) => i.key === newItem.key)) return items;

  return [
    ...items,
    {
      ...newItem,
      interval: INTERVALS[newItem.confidence],
      nextReviewAt: Date.now() + INTERVALS[newItem.confidence] * MS_PER_DAY,
      reviewCount: 0,
    },
  ];
}
```

### Review Schedule Table

| Event | Confidence | Next Review |
|-------|-----------|-------------|
| First wrong answer | Low | +1 day |
| Correct, was Low | Medium | +3 days |
| Correct, was Medium | High | +7 days |
| Correct, was High | High | +14 days (doubles, cap 30) |
| Wrong at any level | Low | +1 day (reset) |

## URL State for Explorations

Shareable exploration state via URL search params. Learners can share "this specific configuration that demonstrates the edge case."

### Hook

```typescript
// hooks/useExplorationState.ts
// (Full implementation in explorable-explanations.md)

// Usage:
const [values, setValue, resetValues] = useExplorationState({
  learningRate: 0.1,
  arraySize: 10,
  showDuplicates: false,
  algorithm: "binary",
});

// URL becomes: ?learningRate=0.5&arraySize=100&showDuplicates=true&algorithm=linear
// Sharing this URL restores the exact exploration state
```

### What Goes in URL State

| Yes (URL) | No (localStorage) |
|-----------|-------------------|
| Slider values | Completion status |
| Toggle states | Number of attempts |
| Selected presets | Confidence ratings |
| Active tab/view | Hints used |
| Timeline position | Review queue |
| Diagram zoom/pan | Personal notes |

## Resume Flow

### How Resume Works

1. On course page load: call `getLastPosition(activities, courseSlug)`
2. If position found: show `<ResumeBanner />` with lesson title + step
3. On click: navigate to `/learn/{course}/{module}/{lesson}?step={n}`
4. Lesson page reads `step` from URL and initializes StepFlow at that index

### Implementation

```tsx
// app/learn/[courseSlug]/page.tsx
import { ResumeBanner } from "@/components/learning/ResumeBanner";
import { useProgressStore } from "@/lib/learning/progress-store";

export default function CoursePage({ params }: { params: { courseSlug: string } }) {
  const { activities } = useProgressStore();
  const lastPosition = getLastPosition(activities, params.courseSlug);

  return (
    <div className="mx-auto max-w-4xl px-6 py-8">
      {lastPosition && (
        <ResumeBanner
          lessonTitle={lastPosition.lessonSlug}
          stepNumber={lastPosition.step}
          stepTitle="..."
          onResume={() => {
            // Navigate to last position
          }}
        />
      )}
      {/* Course overview content */}
    </div>
  );
}
```

## Storage Upgrade Path

| Phase | Storage | Auth Required |
|-------|---------|--------------|
| **MVP** | localStorage only | No |
| **v2** | localStorage + optional server sync | Optional |
| **v3** | Server-first with localStorage cache | Yes |

Server sync uses the same Zustand store with a `sync` middleware that POSTs to an API route on changes.
