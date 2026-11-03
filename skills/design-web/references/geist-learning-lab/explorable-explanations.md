# Explorable Explanations

Interactive visual components for Bret-Victor-style explorations: parameter controls, live output, diagrams, comparisons, timelines, and concept maps.

## ParameterDock

A consistent control panel for sliders/toggles/selects with presets, reset, and URL state sharing.

```tsx
// components/learning/ParameterDock.tsx
"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { RotateCcw } from "@geist-ui/icons";

interface Param {
  key: string;
  label: string;
  type: "slider" | "toggle" | "select";
  min?: number;
  max?: number;
  step?: number;
  options?: { value: string; label: string }[];
  defaultValue: number | boolean | string;
}

interface Preset {
  label: string; // e.g. "Worst Case", "Edge Case"
  values: Record<string, number | boolean | string>;
}

interface ParameterDockProps {
  params: Param[];
  presets?: Preset[];
  values: Record<string, number | boolean | string>;
  onChange: (key: string, value: number | boolean | string) => void;
  onReset: () => void;
}

export function ParameterDock({ params, presets, values, onChange, onReset }: ParameterDockProps) {
  const router = useRouter();
  const searchParams = useSearchParams();

  // Sync to URL for sharing
  function shareState() {
    const sp = new URLSearchParams(searchParams);
    for (const [k, v] of Object.entries(values)) {
      sp.set(k, String(v));
    }
    router.replace(`?${sp.toString()}`, { scroll: false });
  }

  return (
    <div className="rounded-lg border border-gray-400 bg-background-200 p-4 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-label-14 font-medium">Parameters</h3>
        <div className="flex items-center gap-2">
          <button
            onClick={shareState}
            className="text-label-12 text-blue-700 hover:underline"
          >
            Share
          </button>
          <button
            onClick={onReset}
            className="rounded-md p-1.5 text-gray-400 hover:text-gray-1000 hover:bg-background-100 transition-colors"
            aria-label="Reset parameters"
          >
            <RotateCcw size={14} />
          </button>
        </div>
      </div>

      {/* Presets */}
      {presets && presets.length > 0 && (
        <div className="flex flex-wrap gap-2">
          <span className="text-label-12 text-gray-400 self-center">Try:</span>
          {presets.map((preset) => (
            <button
              key={preset.label}
              onClick={() => {
                for (const [k, v] of Object.entries(preset.values)) {
                  onChange(k, v);
                }
              }}
              className="rounded-full border border-gray-400 px-3 py-1 text-label-12 text-gray-400 hover:border-gray-300 hover:text-gray-1000 transition-colors"
            >
              {preset.label}
            </button>
          ))}
        </div>
      )}

      {/* Controls */}
      <div className="space-y-3">
        {params.map((param) => (
          <div key={param.key} className="space-y-1">
            <div className="flex items-center justify-between">
              <label className="text-label-12 text-gray-400" htmlFor={param.key}>
                {param.label}
              </label>
              <span className="text-label-12-mono text-gray-1000">
                {String(values[param.key])}
              </span>
            </div>
            {param.type === "slider" && (
              <input
                id={param.key}
                type="range"
                min={param.min}
                max={param.max}
                step={param.step}
                value={values[param.key] as number}
                onChange={(e) => onChange(param.key, Number(e.target.value))}
                className="w-full accent-blue-700 h-1.5"
              />
            )}
            {param.type === "toggle" && (
              <button
                id={param.key}
                role="switch"
                aria-checked={values[param.key] as boolean}
                onClick={() => onChange(param.key, !(values[param.key] as boolean))}
                className={`
                  relative h-5 w-9 rounded-full transition-colors
                  ${values[param.key] ? "bg-blue-700" : "bg-gray-400"}
                `}
              >
                <span className={`
                  absolute top-0.5 h-4 w-4 rounded-full bg-white transition-transform
                  ${values[param.key] ? "translate-x-4" : "translate-x-0.5"}
                `} />
              </button>
            )}
            {param.type === "select" && (
              <select
                id={param.key}
                value={values[param.key] as string}
                onChange={(e) => onChange(param.key, e.target.value)}
                className="w-full rounded-md border border-gray-400 bg-background-100 px-3 py-1.5 text-copy-14 text-gray-1000"
              >
                {param.options?.map((opt) => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </select>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
```

## LiveOutputPanel

Displays computed output with diff highlights, chart option, and "Explain this output" collapsible.

```tsx
// components/learning/LiveOutputPanel.tsx
"use client";

import { useState, ReactNode } from "react";
import { ChevronDown, ChevronRight, Copy, Check } from "@geist-ui/icons";

interface LiveOutputPanelProps {
  output: ReactNode;
  previousOutput?: ReactNode; // For diff highlighting
  explanation?: string;
  copyValue?: string;
}

export function LiveOutputPanel({ output, previousOutput, explanation, copyValue }: LiveOutputPanelProps) {
  const [showExplanation, setShowExplanation] = useState(false);
  const [copied, setCopied] = useState(false);

  function handleCopy() {
    if (copyValue) {
      navigator.clipboard.writeText(copyValue);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }

  return (
    <div className="rounded-lg border border-gray-400 bg-background-100 overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-400">
        <span className="text-label-12 text-gray-400">Output</span>
        {copyValue && (
          <button
            onClick={handleCopy}
            className="rounded-md p-1 text-gray-400 hover:text-gray-1000 transition-colors"
            aria-label="Copy output"
          >
            {copied ? <Check size={14} className="text-green-700" /> : <Copy size={14} />}
          </button>
        )}
      </div>

      {/* Output area */}
      <div className="p-4 font-mono text-sm min-h-[80px]">
        {output}
      </div>

      {/* What changed? */}
      {previousOutput && (
        <div className="border-t border-gray-400 px-4 py-2">
          <p className="text-label-12 text-amber-700">Changed from previous state</p>
        </div>
      )}

      {/* Explain this output */}
      {explanation && (
        <div className="border-t border-gray-400">
          <button
            onClick={() => setShowExplanation(!showExplanation)}
            className="flex w-full items-center gap-2 px-4 py-2.5 text-label-12 text-gray-400 hover:text-gray-1000 transition-colors"
          >
            {showExplanation ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
            Explain This Output
          </button>
          {showExplanation && (
            <div className="px-4 pb-3">
              <p className="text-copy-14 text-gray-400">{explanation}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

## ConceptExplorer

A diagram or illustration with hover/click hotspots that reveal definitions, intuition, mistakes, and examples.

```tsx
// components/learning/ConceptExplorer.tsx
"use client";

import { useState, ReactNode } from "react";

interface Hotspot {
  id: string;
  label: string;
  x: number; // percentage 0-100
  y: number;
  definition: string;
  intuition?: string;
  commonMistake?: string;
  example?: ReactNode;
}

interface ConceptExplorerProps {
  diagram: ReactNode; // SVG or image
  hotspots: Hotspot[];
  width?: number;
  height?: number;
}

export function ConceptExplorer({ diagram, hotspots, width = 600, height = 400 }: ConceptExplorerProps) {
  const [activeSpot, setActiveSpot] = useState<string | null>(null);
  const active = hotspots.find((h) => h.id === activeSpot);

  return (
    <div className="my-6 rounded-lg border border-gray-400 bg-background-200 overflow-hidden">
      {/* Diagram area */}
      <div className="relative" style={{ maxWidth: width }}>
        {diagram}
        {hotspots.map((spot) => (
          <button
            key={spot.id}
            onClick={() => setActiveSpot(activeSpot === spot.id ? null : spot.id)}
            className={`
              absolute h-7 w-7 -translate-x-1/2 -translate-y-1/2 rounded-full
              flex items-center justify-center text-xs font-bold
              transition-all duration-150
              ${activeSpot === spot.id
                ? "bg-blue-700 text-white scale-110 ring-2 ring-blue-700/30"
                : "bg-background-100 border border-gray-400 text-gray-400 hover:border-blue-700 hover:text-blue-700"
              }
            `}
            style={{ left: `${spot.x}%`, top: `${spot.y}%` }}
            aria-label={spot.label}
            aria-expanded={activeSpot === spot.id}
          >
            {hotspots.indexOf(spot) + 1}
          </button>
        ))}
      </div>

      {/* Detail panel */}
      {active && (
        <div className="border-t border-gray-400 p-4 space-y-3 animate-in fade-in slide-in-from-bottom-2 duration-150">
          <h4 className="text-label-14 font-medium text-blue-700">{active.label}</h4>
          <p className="text-copy-14">{active.definition}</p>
          {active.intuition && (
            <div className="rounded-md bg-background-100 p-3">
              <p className="text-label-12 text-gray-400 mb-1">Intuition</p>
              <p className="text-copy-14">{active.intuition}</p>
            </div>
          )}
          {active.commonMistake && (
            <div className="rounded-md bg-amber-700/5 border border-amber-700/20 p-3">
              <p className="text-label-12 text-amber-700 mb-1">Common Mistake</p>
              <p className="text-copy-14">{active.commonMistake}</p>
            </div>
          )}
          {active.example && (
            <div className="rounded-md bg-background-100 p-3">
              <p className="text-label-12 text-gray-400 mb-1">Example</p>
              {active.example}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

## InteractiveDiagram

SVG/Canvas-based visual that responds to parameter inputs. Animate only `transform`/`opacity`.

```tsx
// components/learning/InteractiveDiagram.tsx
"use client";

import { useReducedMotion } from "@/hooks/useReducedMotion";
import { ReactNode } from "react";

interface InteractiveDiagramProps {
  width?: number;
  height?: number;
  children: (ctx: { animate: boolean }) => ReactNode;
}

export function InteractiveDiagram({
  width = 600,
  height = 300,
  children,
}: InteractiveDiagramProps) {
  const prefersReduced = useReducedMotion();

  return (
    <div className="my-6 rounded-lg border border-gray-400 bg-background-100 overflow-hidden">
      <svg
        viewBox={`0 0 ${width} ${height}`}
        className="w-full h-auto"
        role="img"
        aria-label="Interactive diagram"
      >
        {children({ animate: !prefersReduced })}
      </svg>
    </div>
  );
}

// Hook for reduced motion
// hooks/useReducedMotion.ts
export function useReducedMotion(): boolean {
  if (typeof window === "undefined") return false;
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}
```

### Diagram Animation Rules

| Rule | Implementation |
|------|---------------|
| Only animate `transform` + `opacity` | GPU-composited, no layout thrash |
| Respect reduced motion | `useReducedMotion()` → instant transitions |
| Durations 150-300ms | Tight, purposeful, not decorative |
| Animate on user input only | No autoplay; feedback to interaction |
| CSS transitions preferred | Use `transition` prop on SVG elements |
| Framer Motion if needed | `animate={{ opacity, x, y, scale }}` only |

## BeforeAfterSplit

Split-view with draggable divider for comparing refactors, optimizations, algorithm steps.

```tsx
// components/learning/BeforeAfterSplit.tsx
"use client";

import { useState, useRef, useCallback, ReactNode } from "react";

interface BeforeAfterSplitProps {
  before: ReactNode;
  after: ReactNode;
  beforeLabel?: string;
  afterLabel?: string;
}

export function BeforeAfterSplit({
  before,
  after,
  beforeLabel = "Before",
  afterLabel = "After",
}: BeforeAfterSplitProps) {
  const [split, setSplit] = useState(50);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleDrag = useCallback((e: React.MouseEvent) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    setSplit(Math.max(10, Math.min(90, x)));
  }, []);

  return (
    <div className="my-6 rounded-lg border border-gray-400 overflow-hidden">
      {/* Labels */}
      <div className="flex border-b border-gray-400">
        <span className="flex-1 px-4 py-2 text-label-12 text-gray-400 text-center">{beforeLabel}</span>
        <span className="flex-1 px-4 py-2 text-label-12 text-gray-400 text-center">{afterLabel}</span>
      </div>

      {/* Split view */}
      <div
        ref={containerRef}
        className="relative flex min-h-[200px] cursor-col-resize"
        onMouseMove={(e) => e.buttons === 1 && handleDrag(e)}
      >
        <div className="overflow-hidden" style={{ width: `${split}%` }}>
          <div className="p-4 bg-background-100 h-full">{before}</div>
        </div>
        {/* Divider */}
        <div className="absolute top-0 bottom-0 w-0.5 bg-blue-700 z-10" style={{ left: `${split}%` }}>
          <div className="absolute top-1/2 -translate-x-1/2 -translate-y-1/2 h-8 w-4 rounded-full bg-blue-700 flex items-center justify-center">
            <span className="text-white text-[10px]">⇔</span>
          </div>
        </div>
        <div className="overflow-hidden flex-1">
          <div className="p-4 bg-background-200 h-full">{after}</div>
        </div>
      </div>
    </div>
  );
}
```

## TimelineExplorer

Interactive timeline with scrubber, event cards, and "compare two points" mode.

```tsx
// components/learning/TimelineExplorer.tsx
"use client";

import { useState } from "react";

interface TimelineEvent {
  id: string;
  label: string;
  description: string;
  detail?: string;
}

interface TimelineExplorerProps {
  events: TimelineEvent[];
  initialIndex?: number;
}

export function TimelineExplorer({ events, initialIndex = 0 }: TimelineExplorerProps) {
  const [index, setIndex] = useState(initialIndex);
  const current = events[index];

  return (
    <div className="my-6 rounded-lg border border-gray-400 bg-background-200 p-4 space-y-4">
      {/* Scrubber */}
      <div className="space-y-2">
        <input
          type="range"
          min={0}
          max={events.length - 1}
          value={index}
          onChange={(e) => setIndex(Number(e.target.value))}
          className="w-full accent-blue-700"
          aria-label="Timeline scrubber"
        />
        {/* Dots */}
        <div className="flex justify-between px-1">
          {events.map((evt, i) => (
            <button
              key={evt.id}
              onClick={() => setIndex(i)}
              className={`
                h-2.5 w-2.5 rounded-full transition-colors
                ${i === index ? "bg-blue-700" : i < index ? "bg-green-700" : "bg-gray-400/40"}
              `}
              aria-label={evt.label}
            />
          ))}
        </div>
      </div>

      {/* Event card */}
      <div className="rounded-md bg-background-100 p-4 border border-gray-400">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-label-12-mono text-blue-700">Step {index + 1}/{events.length}</span>
          <h4 className="text-label-14 font-medium">{current.label}</h4>
        </div>
        <p className="text-copy-14 text-gray-400">{current.description}</p>
        {current.detail && (
          <p className="text-copy-14 mt-2">{current.detail}</p>
        )}
      </div>
    </div>
  );
}
```

## ConceptMap

Clickable nodes with labeled edges. Node click opens side panel with definition, examples, and lesson links.

```tsx
// components/learning/ConceptMap.tsx
"use client";

import { useState } from "react";

interface ConceptNode {
  id: string;
  label: string;
  x: number; // percentage
  y: number;
  definition: string;
  examples?: string[];
  lessonLink?: string;
}

interface ConceptEdge {
  from: string;
  to: string;
  label?: string;
}

interface ConceptMapProps {
  nodes: ConceptNode[];
  edges: ConceptEdge[];
  highlightPath?: string[]; // recommended learning path
}

export function ConceptMap({ nodes, edges, highlightPath }: ConceptMapProps) {
  const [activeNode, setActiveNode] = useState<string | null>(null);
  const active = nodes.find((n) => n.id === activeNode);

  return (
    <div className="my-6 rounded-lg border border-gray-400 bg-background-200 overflow-hidden">
      <div className="relative min-h-[300px]">
        {/* SVG edges */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none">
          {edges.map((edge) => {
            const from = nodes.find((n) => n.id === edge.from);
            const to = nodes.find((n) => n.id === edge.to);
            if (!from || !to) return null;
            const isHighlighted = highlightPath?.includes(from.id) && highlightPath?.includes(to.id);
            return (
              <g key={`${edge.from}-${edge.to}`}>
                <line
                  x1={`${from.x}%`} y1={`${from.y}%`}
                  x2={`${to.x}%`} y2={`${to.y}%`}
                  stroke={isHighlighted ? "#0070F3" : "#737373"}
                  strokeWidth={isHighlighted ? 2 : 1}
                  opacity={isHighlighted ? 1 : 0.4}
                />
                {edge.label && (
                  <text
                    x={`${(from.x + to.x) / 2}%`}
                    y={`${(from.y + to.y) / 2}%`}
                    className="text-[10px] fill-gray-400"
                    textAnchor="middle"
                  >
                    {edge.label}
                  </text>
                )}
              </g>
            );
          })}
        </svg>

        {/* Nodes */}
        {nodes.map((node) => (
          <button
            key={node.id}
            onClick={() => setActiveNode(activeNode === node.id ? null : node.id)}
            className={`
              absolute -translate-x-1/2 -translate-y-1/2 px-3 py-1.5 rounded-md text-label-12
              transition-all duration-150
              ${activeNode === node.id
                ? "bg-blue-700 text-white scale-105"
                : highlightPath?.includes(node.id)
                  ? "bg-blue-700/10 border border-blue-700/40 text-blue-700 hover:bg-blue-700/20"
                  : "bg-background-100 border border-gray-400 text-gray-400 hover:border-gray-300"
              }
            `}
            style={{ left: `${node.x}%`, top: `${node.y}%` }}
          >
            {node.label}
          </button>
        ))}
      </div>

      {/* Detail panel */}
      {active && (
        <div className="border-t border-gray-400 p-4 space-y-2">
          <h4 className="text-label-14 font-medium">{active.label}</h4>
          <p className="text-copy-14 text-gray-400">{active.definition}</p>
          {active.examples && (
            <ul className="list-disc list-inside text-copy-14 text-gray-400 space-y-1">
              {active.examples.map((ex, i) => <li key={i}>{ex}</li>)}
            </ul>
          )}
          {active.lessonLink && (
            <a href={active.lessonLink} className="text-label-12 text-blue-700 hover:underline">
              Go to lesson →
            </a>
          )}
        </div>
      )}
    </div>
  );
}
```

## URL State Pattern

All explorable components should support shareable state via URL search params:

```tsx
// hooks/useExplorationState.ts
"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { useCallback, useMemo } from "react";

export function useExplorationState<T extends Record<string, string | number | boolean>>(
  defaults: T
): [T, (key: keyof T, value: T[keyof T]) => void, () => void] {
  const router = useRouter();
  const searchParams = useSearchParams();

  const values = useMemo(() => {
    const result = { ...defaults };
    for (const key of Object.keys(defaults)) {
      const param = searchParams.get(key);
      if (param !== null) {
        const defaultVal = defaults[key];
        if (typeof defaultVal === "number") (result as any)[key] = Number(param);
        else if (typeof defaultVal === "boolean") (result as any)[key] = param === "true";
        else (result as any)[key] = param;
      }
    }
    return result;
  }, [searchParams, defaults]);

  const set = useCallback((key: keyof T, value: T[keyof T]) => {
    const sp = new URLSearchParams(searchParams);
    sp.set(String(key), String(value));
    router.replace(`?${sp.toString()}`, { scroll: false });
  }, [searchParams, router]);

  const reset = useCallback(() => {
    router.replace("?", { scroll: false });
  }, [router]);

  return [values, set, reset];
}
```
