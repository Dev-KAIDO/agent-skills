# Pedagogical Framework

The learning design principles baked into every experience. These aren't suggestions — they're requirements. If the UI doesn't enforce at least one attempt+feedback cycle per chunk, it's just interactive decoration.

## The Learning Loop (Central Doctrine)

Every lesson repeats this cycle. No exceptions.

```
Orient → Attempt → Feedback → Explain → Extend → Checkpoint → Reflect
```

| Step | Duration | What Happens | Non-Negotiable? |
|------|---------|-------------|-----------------|
| **Orient** | 30 sec | What you'll learn, why it matters, expected time | Yes |
| **Attempt** | 1-3 min | Learner predicts, answers, edits, or explores | Yes |
| **Feedback** | Immediate | Specific response: correct/incorrect + why | Yes |
| **Explain** | 1-2 min | Short explanation anchored to their attempt | Yes |
| **Extend** | 1-2 min | Variation, edge case, or transfer task | Recommended |
| **Checkpoint** | 30 sec | Quick recall question | Yes |
| **Reflect** | 30 sec | "What changed in your understanding?" | Optional |

### Minimum Viable Lesson

A lesson that skips everything but the non-negotiables:

1. One sentence stating the learning objective
2. One interactive element (QuickCheck, CodePlayground, ParameterDock)
3. Feedback on the learner's input
4. One paragraph of explanation
5. One checkpoint question

This is the floor. Every lesson must have at least this.

## Progressive Disclosure Rules

### Default View: One Concept + One Action

The initial visible content should show:
- **What** the concept is (one sentence)
- **One thing** the learner does with it (interact, answer, try)

### Depth Affordances (collapsible)

Always available but hidden by default:

| Affordance | Reveals | Use When |
|-----------|---------|----------|
| "Why This Works" | Underlying mechanism/proof | After learner gets the basic concept |
| "Edge Cases" | Boundary conditions, exceptions | After successful first attempt |
| "Formal Definition" | Mathematical/academic phrasing | For rigorous learners |
| "Performance Notes" | Big-O, benchmarks, tradeoffs | For practical application |
| "History" | Who invented this, why | For context-hungry learners |

### What NOT to Hide

- Information needed to proceed to the next step
- The current task/question
- Feedback on the learner's attempt
- Navigation (where am I, what's next)

## Active Recall vs Passive Reading

### QuickCheck Placement

Embed QuickChecks every **2-5 minutes of reading time** (roughly every 300-600 words or every 1-2 concept sections).

| Content Length | QuickChecks |
|---------------|-------------|
| Short section (1-2 paragraphs) | 1 at end |
| Medium section (3-5 paragraphs) | 1 mid + 1 end |
| Long section (6+ paragraphs) | 1 every 2-3 paragraphs |

### Question Type Selection

| Goal | Question Type | Why |
|------|--------------|-----|
| Recall a fact | Short answer | Higher recall effort = better retention |
| Distinguish similar concepts | MCQ with misconception traps | Forces discrimination |
| Check understanding | True/False with explanation | Quick but shallow |
| Apply knowledge | CodePlayground task | Deepest learning |
| Predict behavior | "What happens if..." + reveal | Tests mental model |

### After Correct Answer, Still Explain

Even when the learner gets it right, show a one-sentence confirmation:
- Reinforces the correct mental model
- Catches lucky guesses
- Adds nuance they might have missed

## Spaced Repetition (Lightweight)

Not a full LMS. Simple, localStorage-based review queue.

### What Gets Queued

- Glossary terms the learner "stars"
- QuickCheck questions they got wrong
- Checkpoint questions
- Items they rate "Low confidence"

### Scheduling

```
confidence === "low"    → review in 1 day
confidence === "medium" → review in 3 days
confidence === "high"   → review in 7 days

On correct review:
  low → medium interval (3 days)
  medium → high interval (7 days)
  high → 14 days

On incorrect review:
  Any → reset to low interval (1 day)
```

### UI Pattern

- "Due for Review" badge on course home page
- Review page shows items as QuickCheck cards
- After review session: progress summary

## Multiple Representations

Every concept should be presented in at least **2 of these 5 forms**:

| Representation | Component | Best For |
|---------------|-----------|----------|
| **Text** | Prose, Callout | Definitions, context |
| **Code** | CodePlayground, SnippetCopy | Implementation, syntax |
| **Visual** | InteractiveDiagram, ConceptExplorer | Spatial relationships, flow |
| **Interactive** | ParameterDock, sliders, toggles | Cause-and-effect, ranges |
| **Data/Example** | Table, real dataset, concrete case | Grounding abstract concepts |

### Representation Switcher Pattern

Use tabs to let learners view the same concept in different forms:

```tsx
<Tabs defaultValue="visual">
  <Tabs.List>
    <Tabs.Tab value="visual">Visual</Tabs.Tab>
    <Tabs.Tab value="code">Code</Tabs.Tab>
    <Tabs.Tab value="math">Math</Tabs.Tab>
    <Tabs.Tab value="data">Data</Tabs.Tab>
  </Tabs.List>
  <Tabs.Content value="visual"><InteractiveDiagram ... /></Tabs.Content>
  <Tabs.Content value="code"><CodePlayground ... /></Tabs.Content>
  <Tabs.Content value="math"><p>f(x) = ...</p></Tabs.Content>
  <Tabs.Content value="data"><DataTable ... /></Tabs.Content>
</Tabs>
```

## Scaffolded Complexity

### The Pattern

Start with the simplest possible example. Add one dimension of complexity at a time.

| Level | What Changes | Example (Binary Search) |
|-------|-------------|------------------------|
| 1. Minimal | Smallest valid input | Array of 5 sorted numbers |
| 2. Scale | Larger input | Array of 100 numbers |
| 3. Edge case | Boundary conditions | Target not in array, duplicates |
| 4. Performance | Efficiency matters | Compare to linear search on 10M items |
| 5. Generalization | Abstract the pattern | Binary search on any monotonic function |

### Implementation

- Each level is a step in StepFlow
- Previous level's example stays visible as reference
- New level highlights what changed (use BeforeAfterSplit)

## Immediate Feedback Loops

| Interaction | Feedback Timing | Feedback Type |
|------------|----------------|---------------|
| Slider drag | < 100ms | Live output update |
| Toggle flip | < 100ms | Instant visual change |
| Code run | < 2s | Console output + test results |
| Quiz answer | Instant | Green/red panel + explanation |
| Step navigation | < 200ms | Content transition |

If feedback takes > 2 seconds, show a loading skeleton (delay skeleton render by 150-300ms to avoid flash).

## "Aha Moment" Patterns (Detailed)

### 1. Prediction Gap

```
1. Show setup: "Here's a function with a stale closure..."
2. Ask: "What will console.log print?"
3. Learner answers (QuickCheck short-answer)
4. Reveal actual output
5. If wrong → "Most people expect X because... but Y happens because..."
6. If right → "You got it! The key insight is..."
```

### 2. Contrast Pair

```
1. Show two nearly identical code snippets side-by-side (BeforeAfterSplit)
2. Highlight the single difference
3. Ask: "Which one has the bug?"
4. Reveal: different output/behavior
5. Explain the subtle mechanism
```

### 3. Slider to Failure

```
1. Working system with ParameterDock
2. Learner explores: everything works fine at defaults
3. Challenge: "Try to break it by changing the learning rate"
4. Learner drags slider until output diverges
5. "This is why X matters: beyond Y, the system Z"
```

### 4. Time Travel

```
1. Algorithm visualization (InteractiveDiagram)
2. TimelineExplorer with step-by-step scrubber
3. Learner can go forward and backward
4. At each step: show invariants, state, and what changed
5. QuickCheck: "What will happen at step N?"
```

### 5. Misconception Trap (Safe)

```
1. MCQ with a deliberately tempting wrong answer
2. The wrong answer matches a common misconception
3. If chosen: "Many people pick this because... but actually..."
4. MistakeAnalyzer offers specific misconception patterns
5. Corrective explanation with contrast to the right answer
```

## Content Voice for Learning

| Do | Don't |
|----|-------|
| "What do you think happens?" | "As you can see..." |
| "Try changing the value" | "Observe the following" |
| "Most people expect X" | "Obviously, X" |
| "The key insight is..." | "It's trivial to show..." |
| "You got it!" | "Correct." |
| "Not quite — here's why" | "Wrong." |
| "Let's build intuition" | "The proof is left as an exercise" |
