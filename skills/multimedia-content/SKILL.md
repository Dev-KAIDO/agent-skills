---
name: multimedia-content
description: Complete multimedia content skill — generative art (p5.js), canvas design (PNG/PDF), animated GIFs, video generation (Sora), text-to-speech, audio transcription, screenshots, pet sprites, Jupyter notebooks, and web games. Use for ANY media or creative content generation task.
---

# Multimedia & Content — Complete Skill

## Overview

**Single skill for all media and creative content.** Merges `algorithmic-art`, `canvas-design`, `hatch-pet`, `sora`, `speech`, `transcribe`, `screenshot`, `slack-gif-creator`, `jupyter-notebook`, `develop-web-game`, and `imagegen`.

---

## 1. Generative Art (الفن التوليدي) — p5.js

### 1.1 Process
```
1. Philosophy  → 4-6 paragraphs on algorithmic idea
2. Concept     → visual metaphor (not copying artists)
3. Implement   → p5.js sketch with parameters
4. Viewer      → interactive HTML with controls
5. Seed        → deterministic randomness
```

### 1.2 Deterministic Randomness
```javascript
// Seed-based randomness (same seed = same art)
let seed = 42;

function setup() {
  randomSeed(seed);
  noiseSeed(seed);
  createCanvas(800, 800);
}

// Interactive controls
function draw() {
  background(20);
  for (let i = 0; i < 500; i++) {
    let x = random(width);
    let y = random(height);
    let n = noise(x * 0.01, y * 0.01);
    fill(n * 255, 100, 200, 150);
    circle(x, y, n * 20);
  }
}
```

### 1.3 Viewer Controls
```html
<!-- seed + parameter controls -->
<input type="range" id="seed" min="0" max="1000" value="42">
<button onclick="setSeed(random(1000))">Random</button>
<button onclick="regenerate()">Regenerate</button>
<button onclick="download()">Download PNG</button>
```

---

## 2. Canvas Design (تصميم اللوحة) — PNG/PDF

### 2.1 Design Philosophy
- Define aesthetic movement (minimalism, brutalism, art nouveau)
- 4-6 paragraphs describing visual approach
- Conceptual reference (not copying specific artists)
- Extreme craft (alignment, spacing, hierarchy)

### 2.2 Constraints
- ✅ Minimal text (labels, titles only)
- ✅ Fonts from `./canvas-fonts` directory
- ✅ No overlapping elements
- ✅ No ambiguous spacing
- ✅ No broken alignment
- ❌ No accidental colors (define palette first)

### 2.3 Second-Pass Refinement
```
Pass 1: Structure (layout, hierarchy, main elements)
Pass 2: Polish (spacing, colors, shadows, details)
Pass 3: QA (render at 100%, inspect every pixel)
```

---

## 3. Animated GIFs (صور متحركة) — Slack

### 3.1 Constraints
| Parameter | Slack Emoji | Slack Message |
|-----------|-------------|---------------|
| Size | 128×128 | 480×480 |
| FPS | 10-30 | 10-30 |
| Colors | 48-128 | 48-128 |
| Format | GIF89a | GIF89a |

### 3.2 Builder Pattern
```python
from core.gif_builder import GIFBuilder
from core.easing import ease_out_bounce

builder = GIFBuilder(width=128, height=128, fps=20, colors=64)

for frame_num in range(20):
    frame = compose_frame(frame_num, total=20)
    progress = frame_num / total
    eased = ease_out_bounce(progress)
    builder.add_frame(frame)

builder.save("output.gif")

# Validate Slack compatibility
from core.validators import is_slack_ready
assert is_slack_ready("output.gif")
```

---

## 4. Video Generation (توليد الفيديو) — Sora

### 4.1 Workflow
```
1. Plan       → single video or batch queue
2. Prompt      → detailed, specific description
3. Generate   → sora-2 model
4. Download   → BEFORE 1-hour link expiry!
5. Thumbnail  → extract frame for preview
```

### 4.2 Batch Queue (Local)
```python
# scripts/sora.py has local create-batch
# NOT the official Batch API — local queue system
videos = [
    {"prompt": "Aerial shot of city at sunset, cinematic"},
    {"prompt": "Product rotation on white background"},
]

for video in videos:
    job = sora.create(video["prompt"])
    # Track job status, download when ready
```

### 4.3 Character References (Reusable)
```python
# Create non-human character reference
reference = sora.create_character_reference(
    name="Mascot",
    description="Friendly blue robot with round eyes"
)
# Use reference in multiple videos for consistency
```

### 4.4 Operations Beyond Create (عمليات إضافية)
| Intent | Operation |
|--------|-----------|
| Targeted change to a completed video (preserve shot) | **edit** |
| Next beat / continuation of a completed video | **extend** |
| Check progress of a running generation | **status** |
| List past generations | **list** |
| Fetch files before link expiry (~1h) | **download** |
| Remove a generation | **delete** |

**Decision rule:** iterate on a completed shot → `edit`; continue the timeline → `extend`. For edits, explicitly list invariants ("same shot, same camera, change only X").

### 4.5 CLI (scripts/sora.py)
```bash
python scripts/sora.py create --prompt "..." --use-case commercial --scene indoor --camera dolly
python scripts/sora.py create-batch prompts.txt        # local concurrent queue (NOT the official Batch API)
python scripts/sora.py edit <video-id> --prompt-file change.txt --no-augment
```
- Prefer **CLI augmentation flags** (`--use-case`, `--scene`, `--camera`) over stuffing the prompt
- Pass `--prompt-file` for long prompts; add `--no-augment` with a structured prompt file to skip auto-enhancement
- `create-batch` is a local queue — do not confuse with the official Batch API
- ⚠️ **Download assets before the ~1-hour link expires**
- Requires `OPENAI_API_KEY` and Sora API access

---

## 5. Text-to-Speech (تحويل النص لكلام)

### 5.1 Model & Voices (محدث)
- **Default model:** `gpt-4o-mini-tts-2025-12-15` — supports `instructions` for tone/pace/delivery
- **Default voice:** `cedar` (warm, composed). For a brighter tone use `marin`.
- **Built-in voices only.** Custom voice creation is out of scope.
- Legacy `tts-1` / `tts-1-hd` are deprecated and do NOT support `instructions`.

```python
# scripts/text_to_speech.py
from openai import OpenAI
client = OpenAI()

response = client.audio.speech.create(
    model="gpt-4o-mini-tts-2025-12-15",
    voice="cedar",              # or marin for brighter tone
    input="Welcome to the application!",
    instructions="Tone: Warm and composed. Pacing: Moderate.",
    response_format="mp3",
)
response.stream_to_file("welcome.mp3")
```

### 5.2 Voice Selection
| Voice | Character | Best For |
|-------|-----------|----------|
| **cedar** | Warm, composed | Default — narration, assistants |
| **marin** | Brighter | Marketing, onboarding, energetic |
| **alloy** | Neutral | General purpose |
| **echo** | Deep | Long narration, audiobooks |
| **shimmer** | Soft | Calm UI, accessibility reads |

### 5.3 Batch Mode (JSONL)
```jsonl
{"input":"Thank you for calling. Please hold.","voice":"cedar","response_format":"mp3","out":"hold.mp3"}
{"input":"For sales, press 1. For support, press 2.","voice":"marin","instructions":"Tone: Clear and neutral. Pacing: Slow.","response_format":"wav"}
```
Run: `python scripts/text_to_speech.py --batch input.jsonl`

### 5.4 Requirements
- `OPENAI_API_KEY` environment variable
- Live API calls (no offline mode)
- Collect inputs up front: exact verbatim text, voice, delivery style, format
- Iterate with ONE targeted change (voice / speed / instructions), then re-check
- Disclose to end users that the voice is AI-generated

---

## 6. Audio Transcription (تفريغ الصوت)

### 6.1 Models (محدث)
| Task | Model | Notes |
|------|-------|-------|
| Fast transcription (default) | `gpt-4o-mini-transcribe` | `--response-format text` |
| Higher accuracy | `gpt-4o-transcribe` | longer audio, noisy input |
| Speaker labels / diarization | `gpt-4o-transcribe-diarize` | `--response-format diarized_json` |

- ⚠️ **Prompting is NOT supported** for `gpt-4o-transcribe-diarize` — no `prompt=` argument
- Use `--chunking-strategy auto` for long files; the CLI chunks and merges

### 6.2 CLI
```bash
python scripts/transcribe_diarize.py interview.mp3 \
  --model gpt-4o-transcribe-diarize \
  --response-format diarized_json

# Fast path
python scripts/transcribe_diarize.py interview.mp3 --response-format text
```

### 6.3 Process
```
1. Input    → audio/video file (mp3, wav, mp4, m4a)
2. Process  → chunk → transcribe → merge (diarization optional)
3. Output   → timestamped text with speaker labels
```

### 6.4 Speaker Hints
```python
# Provide known speakers for better diarization
transcribe(
    "interview.mp3",
    speakers=["Alice (interviewer)", "Bob (developer)"],
    language="en",
    timestamps=True
)
```

### 6.5 Output Formats
- Plain text (simple)
- SRT/VTT (subtitles with timestamps)
- diarized JSON (structured with speakers)
- Markdown (formatted with speaker headings)

---

## 7. Screenshots (لقطات الشاشة)

### 7.1 Capture Types
| Type | Use |
|------|-----|
| Full screen | Complete desktop state |
| Window | Specific application |
| Region | UI element or error area |
| Element | DOM element (via Playwright, not OS) |

### 7.2 OS-Level Capture (Windows)
```powershell
# PowerShell screen capture
Add-Type -AssemblyName System.Windows.Forms,System.Drawing

$bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
$bitmap.Save("C:\temp\screenshot.png")
```

### 7.3 macOS Capture (لقطات ماك)
```bash
# One-time permission preflight (Screen Recording) — avoids repeated prompts
bash scripts/ensure_macos_permissions.sh

# Capture a specific app's window
bash scripts/ensure_macos_permissions.sh && \
  python3 scripts/take_screenshot.py --app "AppName"

# Temporary directory output
bash scripts/ensure_macos_permissions.sh && \
  python3 scripts/take_screenshot.py --app "<App>" --mode temp

# Full screen
python3 scripts/take_screenshot.py
```
**Rules:** run the permission preflight first; save under the project's screenshot directory (never random temp paths); prefer the app-targeted capture over full screen when the window is what matters.

### 7.4 When to Use
- OS-level: desktop apps, games, system dialogs
- Browser-level: Playwright `page.screenshot()` (preferred for web)
- Tool priority: in-app tool capability → OS capture script → generic fallback

---

## 8. Pet Sprites (أطقم الحيوانات الأليفة)

### 8.1 Atlas Structure
```
Atlas: 1536×1872 pixels
Cell: 192×208 pixels
Grid: 8 columns × 9 rows = 72 cells

States (rows):
1. idle
2. running-right
3. running-left
4. waving
5. jumping
6. failed
7. waiting
8. running
9. review
```

### 8.2 Pipeline
```
1. extract_strip_frames  → extract from source art
2. inspect_frames        → verify frame quality
3. compose_atlas         → arrange in grid
4. validate_atlas        → check transparency, sizes
5. make_contact_sheet    → QA preview
6. render_animation_previews → verify motion
```

### 8.3 Rules
- ✅ Unused cells: full transparency
- ✅ Consistent cell size (192×208)
- ✅ Smooth animation (no frame jumps)
- ✅ QA review with contact sheet
- ❌ No cropping or stretching

---

## 9. Jupyter Notebooks (دفاتر جوبر)

### 9.1 Structure
```python
# Cell 1: Imports and setup
import pandas as pd
import matplotlib.pyplot as plt

# Cell 2: Load data
df = pd.read_csv("data.csv")

# Cell 3: Analysis
summary = df.describe()

# Cell 4: Visualization
fig, ax = plt.subplots(figsize=(10, 6))
df.plot(ax=ax)

# Cell 5: Conclusions (markdown cell)
# ## Conclusions
# - Finding 1
# - Finding 2
```

### 9.2 Best Practices
- Restart and run all before sharing
- Clear outputs (or commit them intentionally)
- One topic per notebook
- Markdown cells for narrative
- Requirements listed in first cell

---

## 10. Web Games (ألعاب الويب)

### 10.1 Development Loop
```
1. Implement small change
2. Run Playwright test (short input burst)
3. Screenshot + render_game_to_text
4. Review console errors
5. Repeat
```

### 10.2 Deterministic Testing Hook (خطاف زمني حتمي)
Expose a time-stepping hook so the Playwright client can advance the game deterministically instead of relying on wall-clock sleeps:
```javascript
window.advanceTime = (ms) => {
  let remaining = ms;
  while (remaining > 0) {
    const step = Math.min(remaining, 16.7);
    update(step);        // fixed-step update
    render();
    remaining -= step;
  }
};
```
- Client: `scripts/web_game_playwright_client.js`; action payloads: `references/action_payloads.json`
- **Verify multi-step interactions** (not just a single click), and **reset state between scenarios**
- Env: `WEB_GAME_CLIENT` and `WEB_GAME_ACTIONS` point at the client script and action payloads

### 10.3 progress.md Protocol (بروتوكول التقدم)
- Create `progress.md` if missing; **read it first** if it exists (including the original user request at the top)
- Append TODOs, notes, and gotchas after each meaningful chunk of work
- At the end of a session, leave TODOs and suggestions for the next agent

### 10.4 Game Architecture
```javascript
// Game loop (60 FPS target)
function gameLoop(timestamp) {
  const deltaTime = timestamp - lastTime;

  update(deltaTime);    // game logic
  render();             // draw to canvas

  lastTime = timestamp;
  requestAnimationFrame(gameLoop);
}

// Input handling
const keys = {};
window.addEventListener('keydown', e => keys[e.key] = true);
window.addEventListener('keyup', e => keys[e.key] = false);
```

---

## Bundled Tools (الأدوات المرفقة)

Deterministic scripts shipped with this skill — prefer them over ad-hoc code:

| Task | Script | Reference |
|------|--------|-----------|
| Text-to-speech (batch JSONL) | `scripts/text_to_speech.py` | `references/voice-directions.md`, `narration.md`, `ivr.md`, `voiceover.md` |
| Transcription + diarization | `scripts/transcribe_diarize.py` | `references/audio-api.md`, `api.md` |
| Sora video (create/edit/extend/batch) | `scripts/sora.py` | `references/video-api.md`, `cinematic-shots.md`, `social-ads.md`, `cli.md` |
| Screenshots (macOS / Windows) | `scripts/take_screenshot.py`, `scripts/take_screenshot.ps1`, `scripts/ensure_macos_permissions.sh` | — |
| Pet sprite atlas pipeline | `scripts/extract_strip_frames.py` → `inspect_frames.py` → `compose_atlas.py` → `validate_atlas.py` → `make_contact_sheet.py` → `render_animation_previews.py` | `references/qa-rubric.md`, `codex-pet-contract.md`, `animation-rows.md` |
| Pet run preparation | `scripts/prepare_pet_run.py` | — |
| Jupyter scaffold | `scripts/new_notebook.py` | `references/notebook-structure.md`, `experiment-patterns.md` |
| Web game test client | `scripts/web_game_playwright_client.js` | `references/action_payloads.json` |

Pet/atlas QA gate: `validate_atlas.py` + `qa/review.json` must pass before packaging as `pet.json`. Delegate visual generation to `$imagegen`.

---

## Verification Checklist (قائمة التحقق)

### For all media:
- [ ] Output renders correctly (inspect at 100%)
- [ ] No overlapping elements
- [ ] Colors match intended palette
- [ ] Animation smooth (no jank)
- [ ] File size reasonable (GIF < 1MB, images < 500KB)
- [ ] Format compatible with target platform
- [ ] Source code deterministic (same seed = same output)
- [ ] No copyright violations (original work only)
- [ ] Accessibility: alt text for images, captions for video

### For API-based (Sora, TTS):
- [ ] API key configured
- [ ] Assets downloaded before link expiry
- [ ] Batch jobs tracked to completion
- [ ] Costs estimated before generation

---

## Related Skills

- `$design-web` — for web interface design (not art)
- `$design-mobile` — for mobile app visuals
- `$documentation-comprehensive` — for embedding media in docs
- `$agent-workflows` — for deterministic art methodology
- `$code-engineering` — for game architecture
