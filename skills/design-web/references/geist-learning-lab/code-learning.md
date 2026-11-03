# Code Learning Components

Interactive code editors, sandboxes, diff viewers, and challenge runners for teaching programming concepts.

## CodePlayground

Editable code snippet with "Run" and output. Supports read-only, guided (editable blanks only), and free modes.

```tsx
// components/learning/CodePlayground.tsx
"use client";

import { useState, useRef, KeyboardEvent } from "react";
import { Play, RotateCcw, Eye } from "@geist-ui/icons";

type PlaygroundMode = "read-only" | "guided" | "free";

interface CodePlaygroundProps {
  initialCode: string;
  language?: string;
  mode?: PlaygroundMode;
  editableRanges?: [number, number][]; // line ranges for "guided" mode
  onRun: (code: string) => Promise<{ output: string; error?: string }>;
  hints?: string[];
  testResults?: { passed: boolean; label: string }[];
}

export function CodePlayground({
  initialCode,
  language = "typescript",
  mode = "free",
  editableRanges,
  onRun,
  hints,
  testResults,
}: CodePlaygroundProps) {
  const [code, setCode] = useState(initialCode);
  const [output, setOutput] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [running, setRunning] = useState(false);
  const [showHints, setShowHints] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  async function handleRun() {
    setRunning(true);
    setError("");
    try {
      const result = await onRun(code);
      setOutput(result.output);
      if (result.error) setError(result.error);
    } catch (e) {
      setError(String(e));
    }
    setRunning(false);
  }

  function handleReset() {
    setCode(initialCode);
    setOutput("");
    setError("");
  }

  function handleKeyDown(e: KeyboardEvent) {
    // Cmd/Ctrl+Enter to run
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      handleRun();
    }
    // Tab to indent
    if (e.key === "Tab") {
      e.preventDefault();
      const textarea = textareaRef.current;
      if (textarea) {
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const newCode = code.substring(0, start) + "  " + code.substring(end);
        setCode(newCode);
        requestAnimationFrame(() => {
          textarea.selectionStart = textarea.selectionEnd = start + 2;
        });
      }
    }
  }

  return (
    <div className="my-6 rounded-lg border border-gray-400 overflow-hidden">
      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-2 bg-background-200 border-b border-gray-400">
        <div className="flex items-center gap-2">
          <span className="text-label-12-mono text-gray-400">{language}</span>
          {mode !== "free" && (
            <span className="rounded-full bg-blue-700/10 border border-blue-700/30 px-2 py-0.5 text-[10px] text-blue-700">
              {mode === "read-only" ? "Read Only" : "Guided"}
            </span>
          )}
        </div>
        <div className="flex items-center gap-1">
          {hints && hints.length > 0 && (
            <button
              onClick={() => setShowHints(!showHints)}
              className="rounded-md p-1.5 text-gray-400 hover:text-amber-700 transition-colors"
              aria-label="Show hints"
            >
              <Eye size={14} />
            </button>
          )}
          <button
            onClick={handleReset}
            className="rounded-md p-1.5 text-gray-400 hover:text-gray-1000 transition-colors"
            aria-label="Reset code"
          >
            <RotateCcw size={14} />
          </button>
          <button
            onClick={handleRun}
            disabled={running || mode === "read-only"}
            className="flex items-center gap-1.5 rounded-md bg-white px-3 py-1 text-black text-sm font-medium hover:bg-gray-200 transition-colors disabled:opacity-30"
          >
            <Play size={12} />
            {running ? "Running..." : "Run"}
          </button>
        </div>
      </div>

      {/* Code editor */}
      <div className="relative">
        <textarea
          ref={textareaRef}
          value={code}
          onChange={(e) => mode !== "read-only" && setCode(e.target.value)}
          onKeyDown={handleKeyDown}
          readOnly={mode === "read-only"}
          className="w-full bg-background-100 p-4 font-mono text-sm text-gray-1000 resize-none outline-none min-h-[160px] leading-relaxed"
          spellCheck={false}
          aria-label="Code editor"
        />

        {/* Hint overlay */}
        {showHints && hints && (
          <div className="absolute right-4 top-4 w-64 rounded-md border border-amber-700/30 bg-amber-700/5 p-3 space-y-2">
            <p className="text-label-12 text-amber-700">Hints</p>
            {hints.map((hint, i) => (
              <p key={i} className="text-copy-13 text-gray-400">
                {i + 1}. {hint}
              </p>
            ))}
          </div>
        )}
      </div>

      {/* Output */}
      {(output || error) && (
        <div className="border-t border-gray-400">
          <div className="flex items-center px-4 py-1.5 bg-background-200">
            <span className="text-label-12 text-gray-400">Console</span>
          </div>
          <div className="p-4 bg-background-100 font-mono text-sm min-h-[60px]">
            {error ? (
              <span className="text-red-700">{error}</span>
            ) : (
              <span className="text-gray-1000">{output}</span>
            )}
          </div>
        </div>
      )}

      {/* Test results */}
      {testResults && testResults.length > 0 && (
        <div className="border-t border-gray-400 px-4 py-3 bg-background-200 space-y-1.5">
          <p className="text-label-12 text-gray-400">Tests</p>
          {testResults.map((test, i) => (
            <div key={i} className="flex items-center gap-2">
              <span className={`h-2 w-2 rounded-full ${test.passed ? "bg-green-700" : "bg-red-700"}`} />
              <span className={`text-copy-13 ${test.passed ? "text-green-700" : "text-red-700"}`}>
                {test.label}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

## Keyboard Shortcuts (CodePlayground)

| Key | Action |
|-----|--------|
| `Cmd/Ctrl+Enter` | Run code |
| `Tab` | Indent 2 spaces |
| `Shift+Tab` | Dedent |
| `Cmd/Ctrl+Z` | Undo |

## DiffEditor

Before/after code diff with explanation callouts. Shows why a change fixes a bug.

```tsx
// components/learning/DiffEditor.tsx
"use client";

interface DiffLine {
  type: "added" | "removed" | "unchanged";
  content: string;
  annotation?: string; // inline explanation
}

interface DiffEditorProps {
  filename?: string;
  lines: DiffLine[];
  title?: string;
}

export function DiffEditor({ filename, lines, title }: DiffEditorProps) {
  return (
    <div className="my-6 rounded-lg border border-gray-400 overflow-hidden">
      {/* Header */}
      <div className="flex items-center gap-2 px-4 py-2 bg-background-200 border-b border-gray-400">
        {title && <span className="text-label-14 font-medium">{title}</span>}
        {filename && <span className="text-label-12-mono text-gray-400">{filename}</span>}
      </div>

      {/* Diff lines */}
      <div className="bg-background-100 overflow-x-auto">
        {lines.map((line, i) => (
          <div key={i}>
            <div
              className={`
                flex items-start px-4 py-0.5 font-mono text-sm leading-relaxed
                ${line.type === "added" ? "bg-green-700/5 text-green-700" : ""}
                ${line.type === "removed" ? "bg-red-700/5 text-red-700 line-through opacity-60" : ""}
                ${line.type === "unchanged" ? "text-gray-400" : ""}
              `}
            >
              <span className="w-6 shrink-0 text-gray-400/40 select-none text-right mr-3">
                {line.type === "added" ? "+" : line.type === "removed" ? "-" : " "}
              </span>
              <span className="flex-1 whitespace-pre">{line.content}</span>
            </div>
            {/* Annotation callout */}
            {line.annotation && (
              <div className="ml-12 mr-4 my-1 rounded-md bg-blue-700/5 border border-blue-700/20 px-3 py-1.5">
                <p className="text-copy-13 text-blue-700">{line.annotation}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
```

## TaskRunner

Mini coding challenge: prompt, editor, hidden tests, visible tests, feedback with failing case. One concept, one task.

```tsx
// components/learning/TaskRunner.tsx
"use client";

import { useState } from "react";
import { CodePlayground } from "./CodePlayground";

interface TestCase {
  input: string;
  expected: string;
  label: string;
  hidden?: boolean;
}

interface TaskRunnerProps {
  prompt: string;
  starterCode: string;
  language?: string;
  tests: TestCase[];
  runCode: (code: string, input: string) => Promise<string>;
  hints?: string[];
}

export function TaskRunner({
  prompt,
  starterCode,
  language,
  tests,
  runCode,
  hints,
}: TaskRunnerProps) {
  const [results, setResults] = useState<{ passed: boolean; label: string; actual?: string }[]>([]);
  const [allPassed, setAllPassed] = useState(false);

  async function handleRun(code: string) {
    const newResults: typeof results = [];
    let passed = true;

    for (const test of tests) {
      try {
        const actual = await runCode(code, test.input);
        const testPassed = actual.trim() === test.expected.trim();
        if (!testPassed) passed = false;
        if (!test.hidden || !testPassed) {
          newResults.push({
            passed: testPassed,
            label: test.label,
            actual: testPassed ? undefined : actual,
          });
        }
      } catch (e) {
        passed = false;
        newResults.push({ passed: false, label: test.label, actual: String(e) });
      }
    }

    setResults(newResults);
    setAllPassed(passed);

    const output = newResults
      .map((r) => `${r.passed ? "✓" : "✗"} ${r.label}${r.actual ? ` (got: ${r.actual})` : ""}`)
      .join("\n");

    return {
      output: passed ? `All tests passed!\n\n${output}` : output,
      error: passed ? undefined : "Some tests failed",
    };
  }

  return (
    <div className="my-8 space-y-4">
      {/* Task prompt */}
      <div className="rounded-lg border border-blue-700/30 bg-blue-700/5 p-4">
        <p className="text-label-12 text-blue-700 mb-1">Challenge</p>
        <p className="text-copy-14">{prompt}</p>
      </div>

      {/* Visible test cases */}
      <div className="space-y-1">
        <p className="text-label-12 text-gray-400">Test Cases</p>
        {tests.filter((t) => !t.hidden).map((test, i) => (
          <div key={i} className="flex items-center gap-2 text-copy-13-mono text-gray-400">
            <span>{test.label}:</span>
            <span className="text-gray-1000">input={test.input} → expected={test.expected}</span>
          </div>
        ))}
        {tests.some((t) => t.hidden) && (
          <p className="text-copy-13 text-gray-400/60">+ {tests.filter((t) => t.hidden).length} hidden tests</p>
        )}
      </div>

      {/* Editor */}
      <CodePlayground
        initialCode={starterCode}
        language={language}
        mode="free"
        onRun={handleRun}
        hints={hints}
        testResults={results}
      />

      {/* Success banner */}
      {allPassed && (
        <div className="rounded-md bg-green-700/10 border border-green-700/30 p-4" role="alert">
          <p className="text-label-14 text-green-700 font-medium">All tests passed!</p>
        </div>
      )}
    </div>
  );
}
```

## SnippetCopy

Uses Geist Snippet pattern: copy button, shell prompt stripping, dark bg.

```tsx
// components/learning/SnippetCopy.tsx
"use client";

import { useState } from "react";
import { Copy, Check } from "@geist-ui/icons";

interface SnippetCopyProps {
  text: string;
  prompt?: string; // e.g. "$" — stripped on copy
}

export function SnippetCopy({ text, prompt = "$" }: SnippetCopyProps) {
  const [copied, setCopied] = useState(false);

  function handleCopy() {
    // Strip prompt prefix for clipboard
    const clean = text.replace(new RegExp(`^\\${prompt}\\s*`, "gm"), "");
    navigator.clipboard.writeText(clean);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="my-4 flex items-center justify-between rounded-lg border border-gray-400 bg-background-100 px-4 py-3">
      <code className="font-mono text-sm text-gray-1000">
        <span className="text-gray-400 select-none mr-2">{prompt}</span>
        {text.replace(new RegExp(`^\\${prompt}\\s*`), "")}
      </code>
      <button
        onClick={handleCopy}
        className="rounded-md p-1.5 text-gray-400 hover:text-gray-1000 transition-colors shrink-0 ml-4"
        aria-label="Copy to clipboard"
      >
        {copied ? <Check size={14} className="text-green-700" /> : <Copy size={14} />}
      </button>
    </div>
  );
}
```

## Mode Decision Guide

| Learner Context | Mode | Why |
|----------------|------|-----|
| First exposure to concept | `read-only` | Focus on reading, not editing |
| Guided practice with scaffolding | `guided` | Editable blanks keep focus narrow |
| Free practice / challenges | `free` | Full autonomy for problem-solving |
| Review / reference | `read-only` + copy | Quick reference, no interaction needed |
