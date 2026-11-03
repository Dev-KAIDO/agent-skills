# Quiz & Assessment Components

Active recall components: inline questions, confidence rating, progressive hints, and misconception analysis. Assessment as a learning tool, not a test.

## QuickCheck

One question inline: MCQ, short answer, ordering, true/false. Instant feedback and explanation. "Try again" is the default path.

```tsx
// components/learning/QuickCheck.tsx
"use client";

import { useState } from "react";

type QuestionType = "mcq" | "short-answer" | "true-false";

interface QuickCheckProps {
  question: string;
  type: QuestionType;
  options?: string[]; // for MCQ
  correctAnswer: string;
  explanation: string;
  misconception?: string; // Why the wrong answer seems right
  onComplete?: (attempts: number, correct: boolean) => void;
}

export function QuickCheck({
  question,
  type,
  options,
  correctAnswer,
  explanation,
  misconception,
  onComplete,
}: QuickCheckProps) {
  const [answer, setAnswer] = useState("");
  const [attempts, setAttempts] = useState(0);
  const [result, setResult] = useState<"correct" | "incorrect" | null>(null);
  const [showExplanation, setShowExplanation] = useState(false);

  function handleCheck() {
    const isCorrect = answer.trim().toLowerCase() === correctAnswer.trim().toLowerCase();
    setAttempts((a) => a + 1);
    setResult(isCorrect ? "correct" : "incorrect");
    if (isCorrect) {
      setShowExplanation(true);
      onComplete?.(attempts + 1, true);
    }
  }

  function handleTryAgain() {
    setAnswer("");
    setResult(null);
  }

  return (
    <div className="my-6 rounded-lg border border-gray-400 bg-background-200 p-5">
      <p className="text-copy-14 font-medium mb-4">{question}</p>

      {/* MCQ options */}
      {type === "mcq" && options && (
        <div className="space-y-2 mb-4">
          {options.map((opt) => (
            <label
              key={opt}
              className={`
                flex items-center gap-3 rounded-md border px-4 py-3 cursor-pointer transition-colors
                ${answer === opt
                  ? result === "correct"
                    ? "border-green-700 bg-green-700/5"
                    : result === "incorrect"
                      ? "border-red-700 bg-red-700/5"
                      : "border-blue-700 bg-blue-700/5"
                  : "border-gray-400 hover:border-gray-300"
                }
              `}
            >
              <input
                type="radio"
                name="quickcheck"
                value={opt}
                checked={answer === opt}
                onChange={(e) => { setAnswer(e.target.value); setResult(null); }}
                className="accent-blue-700"
                disabled={result === "correct"}
              />
              <span className="text-copy-14">{opt}</span>
            </label>
          ))}
        </div>
      )}

      {/* True/False */}
      {type === "true-false" && (
        <div className="flex gap-3 mb-4">
          {["True", "False"].map((opt) => (
            <button
              key={opt}
              onClick={() => { setAnswer(opt); setResult(null); }}
              disabled={result === "correct"}
              className={`
                flex-1 rounded-md border px-4 py-3 text-sm font-medium transition-colors
                ${answer === opt
                  ? "border-blue-700 bg-blue-700/5 text-blue-700"
                  : "border-gray-400 text-gray-400 hover:border-gray-300"
                }
              `}
            >
              {opt}
            </button>
          ))}
        </div>
      )}

      {/* Short answer */}
      {type === "short-answer" && (
        <input
          type="text"
          value={answer}
          onChange={(e) => { setAnswer(e.target.value); setResult(null); }}
          disabled={result === "correct"}
          placeholder="Type your answer..."
          className="w-full rounded-md border border-gray-400 bg-background-100 px-4 py-2.5 text-copy-14 text-gray-1000 mb-4 outline-none focus:border-blue-700 transition-colors"
          onKeyDown={(e) => e.key === "Enter" && handleCheck()}
        />
      )}

      {/* Actions */}
      {result !== "correct" && (
        <div className="flex items-center gap-3">
          <button
            onClick={handleCheck}
            disabled={!answer}
            className="px-4 py-2 rounded-md bg-white text-black text-sm font-medium hover:bg-gray-200 transition-colors disabled:opacity-30"
          >
            Check
          </button>
          {result === "incorrect" && (
            <button
              onClick={handleTryAgain}
              className="px-4 py-2 rounded-md border border-gray-400 text-gray-400 text-sm hover:border-gray-300 transition-colors"
            >
              Try Again
            </button>
          )}
        </div>
      )}

      {/* Feedback */}
      {result && (
        <div
          className={`mt-4 rounded-md p-4 ${
            result === "correct"
              ? "bg-green-700/10 border border-green-700/30"
              : "bg-red-700/10 border border-red-700/30"
          }`}
          role="alert"
          aria-live="polite"
        >
          <p className={`text-label-14 font-medium mb-1 ${result === "correct" ? "text-green-700" : "text-red-700"}`}>
            {result === "correct" ? "Correct!" : "Not quite."}
          </p>
          {result === "incorrect" && misconception && (
            <p className="text-copy-14 text-gray-400 mb-1">
              <span className="text-amber-700">Common trap: </span>{misconception}
            </p>
          )}
          {showExplanation && (
            <p className="text-copy-14 text-gray-400">{explanation}</p>
          )}
          {result === "incorrect" && (
            <p className="text-copy-13 text-gray-400/60 mt-2">Try again — you can do this.</p>
          )}
        </div>
      )}

      {/* Attempts counter */}
      {attempts > 0 && (
        <p className="text-label-12 text-gray-400/40 mt-2">
          {attempts === 1 ? "1 attempt" : `${attempts} attempts`}
        </p>
      )}
    </div>
  );
}
```

## ConfidenceRating

After answering: "How confident were you?" Drives spaced repetition scheduling.

```tsx
// components/learning/ConfidenceRating.tsx
"use client";

type Confidence = "low" | "medium" | "high";

interface ConfidenceRatingProps {
  onRate: (confidence: Confidence) => void;
}

const levels: { value: Confidence; label: string; emoji: string; description: string }[] = [
  { value: "low", label: "Guessed", emoji: "🤔", description: "I wasn't sure — review tomorrow" },
  { value: "medium", label: "Mostly Sure", emoji: "👍", description: "I think I get it — review in 3 days" },
  { value: "high", label: "Confident", emoji: "💪", description: "I know this — review in 7 days" },
];

export function ConfidenceRating({ onRate }: ConfidenceRatingProps) {
  return (
    <div className="my-4 rounded-md bg-background-200 border border-gray-400 p-4">
      <p className="text-label-12 text-gray-400 mb-3">How confident were you?</p>
      <div className="flex gap-2">
        {levels.map((level) => (
          <button
            key={level.value}
            onClick={() => onRate(level.value)}
            className="flex-1 rounded-md border border-gray-400 px-3 py-2.5 text-center hover:border-gray-300 transition-colors group"
          >
            <p className="text-sm font-medium group-hover:text-gray-1000 text-gray-400 transition-colors">
              {level.label}
            </p>
            <p className="text-[11px] text-gray-400/60 mt-0.5">{level.description}</p>
          </button>
        ))}
      </div>
    </div>
  );
}
```

## Spaced Repetition Schedule

| Confidence | Review After | On Next Correct | On Incorrect |
|-----------|-------------|-----------------|-------------|
| Low | 1 day | → Medium interval | Reset to 1 day |
| Medium | 3 days | → High interval | → Low interval |
| High | 7 days | → 14 days | → Medium interval |

## HintLadder

Hints revealed progressively. Track how many hints used; reflect in progress.

```tsx
// components/learning/HintLadder.tsx
"use client";

import { useState } from "react";
import { ChevronDown } from "@geist-ui/icons";

interface HintLadderProps {
  hints: string[];
  showAnswer?: string;
  onHintUsed?: (hintIndex: number) => void;
}

export function HintLadder({ hints, showAnswer, onHintUsed }: HintLadderProps) {
  const [revealedCount, setRevealedCount] = useState(0);

  function revealNext() {
    if (revealedCount < hints.length) {
      const next = revealedCount + 1;
      setRevealedCount(next);
      onHintUsed?.(next - 1);
    }
  }

  const labels = ["Nudge", "Getting Closer", "Almost There", "Full Hint"];

  return (
    <div className="my-4 space-y-2">
      {/* Revealed hints */}
      {hints.slice(0, revealedCount).map((hint, i) => (
        <div
          key={i}
          className="rounded-md bg-amber-700/5 border border-amber-700/20 px-4 py-3 animate-in fade-in slide-in-from-bottom-1 duration-200"
        >
          <p className="text-label-12 text-amber-700 mb-0.5">
            Hint {i + 1}: {labels[i] || `Hint ${i + 1}`}
          </p>
          <p className="text-copy-14">{hint}</p>
        </div>
      ))}

      {/* Show next hint button */}
      {revealedCount < hints.length && (
        <button
          onClick={revealNext}
          className="flex items-center gap-1.5 text-label-12 text-amber-700 hover:text-amber-600 transition-colors"
        >
          <ChevronDown size={12} />
          Show Hint {revealedCount + 1} of {hints.length}
          <span className="text-gray-400/40 ml-1">
            ({hints.length - revealedCount} remaining)
          </span>
        </button>
      )}

      {/* Show answer (after all hints or explicitly) */}
      {showAnswer && revealedCount >= hints.length && (
        <div className="rounded-md bg-background-200 border border-gray-400 px-4 py-3">
          <p className="text-label-12 text-gray-400 mb-0.5">Answer</p>
          <p className="text-copy-14">{showAnswer}</p>
        </div>
      )}

      {/* Usage indicator */}
      {revealedCount > 0 && (
        <p className="text-label-12 text-gray-400/40">
          {revealedCount} of {hints.length} hints used
        </p>
      )}
    </div>
  );
}
```

## MistakeAnalyzer

When wrong, offers likely misconception options to build learner metacognition.

```tsx
// components/learning/MistakeAnalyzer.tsx
"use client";

import { useState } from "react";

interface Misconception {
  id: string;
  label: string; // e.g. "I mixed up X and Y"
  explanation: string;
}

interface MistakeAnalyzerProps {
  misconceptions: Misconception[];
  onSelect?: (id: string) => void;
}

export function MistakeAnalyzer({ misconceptions, onSelect }: MistakeAnalyzerProps) {
  const [selected, setSelected] = useState<string | null>(null);
  const active = misconceptions.find((m) => m.id === selected);

  return (
    <div className="my-4 rounded-md border border-red-700/20 bg-red-700/5 p-4 space-y-3">
      <p className="text-label-12 text-red-700">What went wrong? (It's OK — this is how learning works)</p>

      <div className="space-y-2">
        {misconceptions.map((m) => (
          <button
            key={m.id}
            onClick={() => {
              setSelected(m.id);
              onSelect?.(m.id);
            }}
            className={`
              w-full text-left rounded-md border px-4 py-2.5 text-copy-14 transition-colors
              ${selected === m.id
                ? "border-red-700/40 bg-red-700/10 text-gray-1000"
                : "border-gray-400 text-gray-400 hover:border-gray-300"
              }
            `}
          >
            {m.label}
          </button>
        ))}
      </div>

      {/* Explanation for selected misconception */}
      {active && (
        <div className="rounded-md bg-background-200 border border-gray-400 p-3 animate-in fade-in duration-200">
          <p className="text-label-12 text-gray-400 mb-1">Here's what happened</p>
          <p className="text-copy-14">{active.explanation}</p>
        </div>
      )}
    </div>
  );
}
```

## Assessment Placement Guidelines

| Context | Component | Frequency |
|---------|-----------|-----------|
| Inline during reading | QuickCheck (MCQ or T/F) | Every 2-5 min of content |
| After explanation section | QuickCheck (short answer) | After key concepts |
| After quiz answer | ConfidenceRating | After every correct QuickCheck |
| When stuck on a task | HintLadder | Available on all TaskRunner/CheckpointCard |
| After incorrect answer | MistakeAnalyzer | When common misconceptions exist |
| End of lesson | Checkpoint with multiple QuickChecks | 1 per lesson |

## Design Rules

- **"Try Again" is always the default path** — don't punish mistakes
- **After correct answer, still show explanation** — reinforce understanding
- **Hints are a resource, not shame** — count them but don't judge
- **Misconception selection is voluntary** — builds metacognition when used
- **Green/Red feedback surfaces are consistent** — same layout everywhere
- **Focus moves to feedback region** — `aria-live="polite"` or explicit focus
