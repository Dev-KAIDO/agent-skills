---
name: testing-comprehensive
description: Complete testing skill — web testing (Playwright, e2e), desktop GUI testing (pytest-qt, visual regression), test planning, test data management, flaky test stabilization, failure recording, repair retesting, contract testing, and CI test integration. Use for ANY testing activity across all platforms.
---

# Testing Comprehensive — Complete Skill

## Overview

**Single skill for all testing.** Covers web, desktop, API, and contract testing. Merges `webapp-testing`, `playwright`, `playwright-interactive`, `gui-test-orchestrator`, `gui-visual-regression`, `gui-failure-recorder`, `gui-flake-stabilizer`, `gui-repair-runner`, `gui-test-data-sandbox`, `desktop-e2e-automation`, `pyqt-test-engine`, `scraper-contract-tester`, `cityofaiagents-qa-validation`, and `sdlc-qa`.

---

## 1. Test Strategy (استراتيجية الاختبار)

### 1.1 Test Pyramid
```
        /  E2E  \        ← Few, slow, expensive (Playwright, Cypress)
       / Integration \    ← Moderate (API tests, DB tests)
      /    Unit Tests  \  ← Many, fast, cheap (Jest, pytest)
```

### 1.2 Test Types
| Type | Scope | Speed | Tool |
|------|-------|-------|------|
| Unit | Single function/class | < 100ms | Jest, pytest, vitest |
| Integration | Module interaction | < 1s | supertest, pytest |
| E2E | Full user flow | < 30s | Playwright, Cypress |
| Visual | Screenshot comparison | < 10s | Playwright, Percy |
| Contract | API schema | < 1s | Pact, openapi-validator |
| Performance | Load/stress | Variable | k6, Artillery |
| Security | Vulnerability | Variable | ZAP, Snyk |

### 1.3 What to Test
- ✅ Business logic (core functionality)
- ✅ Edge cases (empty, null, max, min, special chars)
- ✅ Error handling (network fail, invalid input, permission denied)
- ✅ User flows (registration, login, CRUD, payment)
- ✅ Regression (bug fixes should have tests)
- ❌ Don't test: third-party code, trivial getters/setters, UI styling pixel-perfect

---

## 2. Web Testing (اختبار الويب)

### 2.1 Playwright Workflow
```javascript
// Basic test structure
const { test, expect } = require('@playwright/test');

test('user can login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[data-testid="email"]', 'user@test.com');
  await page.fill('[data-testid="password"]', 'password123');
  await page.click('[data-testid="submit"]');
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toContainText('Welcome');
});
```

### 2.2 Best Practices
- **Wait for:** `networkidle` before inspection
- **Selectors:** `data-testid` > semantic (`role`, `label`) > CSS (avoid XPath)
- **Assertions:** specific (`toHaveText`) not just visible
- **Independent tests:** each test sets up its own state
- **Clean up:** close browser after all tests
- **Re-snapshot:** after navigation, re-query elements

### 2.3 Common Patterns
```javascript
// Page Object pattern
class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.locator('[data-testid="email"]');
    this.passwordInput = page.locator('[data-testid="password"]');
    this.submitButton = page.locator('[data-testid="submit"]');
    this.errorMessage = page.locator('[role="alert"]');
  }
  async login(email, password) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}

// Fixture for authenticated state
test.beforeEach(async ({ page }) => {
  await page.goto('/login');
  // ... login setup
});
```

### 2.4 API Testing
```javascript
// Direct API testing (faster than UI)
const response = await request.post('/api/users', {
  data: { name: 'Test', email: 'test@example.com' },
  headers: { Authorization: `Bearer ${token}` },
});
expect(response.status()).toBe(201);
const body = await response.json();
expect(body.name).toBe('Test');
```

---

## 3. Desktop GUI Testing (اختبار GUI)

### 3.1 Test Planning
```json
{
  "level": "smoke|screen-state|user-flow|business-continuity",
  "scope": "specific feature or screen",
  "evidence": {
    "screenshots": true,
    "step_traces": true,
    "assertions": "visual + functional"
  },
  "sandbox": {
    "isolated_data": true,
    "no_production_touch": true
  }
}
```

### 3.2 pytest-qt (PyQt/PySide)
```python
def test_button_click(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Find button and click
    button = window.findChild(QPushButton, "submit_btn")
    qtbot.mouseClick(button, Qt.LeftButton)
    
    # Verify result
    assert window.status_label.text() == "Success"
    assert window.result_list.count() > 0
```

### 3.3 Visual Regression
```python
# Screenshot comparison
def test_dashboard_visual(qtbot, baseline_dir):
    window = DashboardWindow()
    qtbot.addWidget(window)
    window.show()
    
    # Capture screenshot
    screenshot = window.grab()
    screenshot.save("current.png")
    
    # Compare with baseline
    diff = compare_images("baseline.png", "current.png", 
                          mask_dynamic_regions=True)
    assert diff.score < 0.01  # Less than 1% difference
```

### 3.4 E2E Desktop (PyAutoGUI)
```python
# Desktop automation
import pyautogui

def test_desktop_flow():
    # Launch app
    subprocess.Popen(["./myapp.exe"])
    time.sleep(2)
    
    # Find and click elements
    button = pyautogui.locateOnScreen("button.png")
    assert button is not None, "Button not found"
    pyautogui.click(button)
    
    # Verify result
    screenshot = pyautogui.screenshot()
    assert check_element(screenshot, "success_indicator.png")
```

---

## 4. Test Data Management (إدارة بيانات الاختبار)

### 4.1 Sandbox Rules
- ✅ Isolated test databases
- ✅ Temporary config files
- ✅ Synthetic test data (no real PII)
- ✅ Cleanup after tests
- ❌ Never test against production
- ❌ Never use real user data
- ❌ Never leave test artifacts in shared storage

### 4.2 Test Data Patterns
```python
# Factory pattern
class UserFactory:
    @staticmethod
    def create(role="user", **overrides):
        defaults = {
            "name": "Test User",
            "email": f"test-{uuid4()}@example.com",
            "role": role,
            "active": True,
        }
        defaults.update(overrides)
        return create_user(**defaults)

# Clean fixture
@pytest.fixture
def test_user(db_session):
    user = UserFactory.create()
    yield user
    db_session.delete(user)
    db_session.commit()
```

---

## 5. Failure Recording (تسجيل الفشل)

### 5.1 What to Record
```json
{
  "test_name": "test_login_flow",
  "timestamp": "2026-01-01T12:00:00Z",
  "status": "failed",
  "error_type": "AssertionError",
  "error_message": "Expected 'Welcome' but got ''",
  "traceback": "...",
  "screenshot": "failures/test_login_20260101.png",
  "steps": [
    {"action": "goto", "value": "/login"},
    {"action": "fill", "field": "email", "value": "test@test.com"},
    {"action": "click", "element": "submit"}
  ],
  "environment": {
    "os": "Windows 11",
    "browser": "Chrome 120",
    "viewport": "1920x1080"
  },
  "severity": "high",
  "confidence": 0.95
}
```

### 5.2 Storage Structure
```
.codex-project-intel/gui/
├── failures/
│   ├── 2026-01-01_login_failure/
│   │   ├── screenshot.png
│   │   ├── trace.json
│   │   └── error.log
│   └── ...
├── screenshots/
├── gui_failure_catalog.json
└── visual_regression_report.json
```

---

## 6. Flaky Test Stabilization (تثبيت الاختبارات المتخبطة)

### 6.1 Common Causes
| Cause | Fix |
|-------|-----|
| Event loop leakage | Close all async resources |
| Timer/race condition | Use explicit waits, not sleep |
| Teardown gap | Proper fixture cleanup |
| Focus issues | Explicit focus before interaction |
| Delayed rendering | Wait for element visibility |
| Network dependency | Mock or use local server |
| Order dependency | Make tests independent |

### 6.2 Stabilization Process
```
1. IDENTIFY   → which tests are flaky (run 10x, note failures)
2. CLASSIFY   → cause (timing, dependency, resource, etc.)
3. DIAGNOSE   → root cause analysis
4. FIX        → address the cause (not just add sleep)
5. VERIFY     → run 20x, confirm stable
6. MONITOR    → track flakiness over time
```

---

## 7. Repair Retesting (إعادة اختبار بعد الإصلاح)

### 7.1 Process
```
1. Read original failure    → understand what was broken
2. Apply fix                → narrow scope repair
3. Re-run original test     → must pass now
4. Re-run related tests     → no regression
5. Run full suite           → comprehensive check
6. Document evidence        → before/after comparison
```

### 7.2 Retest Checklist
- [ ] Original failing test passes
- [ ] Related tests pass
- [ ] No new failures introduced
- [ ] Visual evidence (screenshots) captured
- [ ] Fix is in narrow scope (no side effects)

---

## 8. Contract Testing (اختبار العقود)

### 8.1 When to Use
- API integrations (frontend ↔ backend)
- Microservices communication
- Third-party API integrations
- Data format validation

### 8.2 Local Fixture Testing
```python
# Test parser against fixtures (no network)
def test_parse_user_response():
    fixture = load_fixture("api/user_response.json")
    result = parse_user_response(fixture)
    assert result.name == "Test User"
    assert result.email == "test@example.com"

# Validate against schema
def test_response_schema(fixture):
    schema = load_schema("openapi.yaml")
    errors = validate(fixture, schema)
    assert errors == []
```

### 8.3 Rules
- ✅ Use local fixtures (deterministic)
- ✅ Test edge cases (empty, missing fields, extra fields)
- ✅ Validate schema compliance
- ❌ Avoid live network in tests (unless explicitly approved)

---

## 9. CI Test Integration (تكامل اختبارات CI)

### 9.1 CI Pipeline
```yaml
test:
  stages:
    - lint
    - unit        # Fast, blocking
    - integration # Medium, blocking
    - e2e         # Slow, may be non-blocking
    - security    # Scan, report
    - visual      # Screenshot comparison
  
  parallel:
    unit: 4    # Split unit tests across 4 workers
    e2e: 2     # Split E2E across 2 workers
```

### 9.2 Test Failure Analysis
| Classification | Action |
|---------------|--------|
| Test bug (bad assertion) | Fix test |
| Code bug (real failure) | Fix code |
| Environment issue | Fix CI config |
| Flaky (intermittent) | Stabilize test |
| Timeout (slow) | Optimize or increase timeout |
| Infrastructure | Fix CI infra |

---

## 10. Interactive & Assisted Testing (الاختبار التفاعلي)

### 10.1 Persistent Browser Sessions (playwright-interactive)
Use a **persistent JS REPL session** (e.g. `js_repl`) when debugging UI iteratively:
```javascript
// Handles persist ACROSS turns — no relaunch between fixes
const browser = await chromium.launch({ headless: false });
const page = await browser.newPage();
await page.goto('http://localhost:3000');
// ... tweak code, re-run only the changed cells, state survives
page;   // still alive next turn
```
- **Electron support:** attach to running Electron apps
- **Kernel reset discipline:** full reset when switching apps or state gets dirty
- **Sandbox:** requires sandbox-disabled REPL config; enable in `config.toml`
- Best for: fast iterative UI debugging where relaunching per iteration is too slow
- Normal test suites still use `@playwright/test` (this REPL is for exploration, not CI)

### 10.2 CLI & Server Tooling
```bash
# playwright-cli wrapper (from this skill's scripts/)
bash scripts/playwright_cli.sh --headed           # headed visual inspection
bash scripts/playwright_cli.sh snapshot           # a11y snapshot after navigation

# Multi-server lifecycle (webapp-testing) — start/stop app + API together
python scripts/with_server.py \
  --cmd "npm run dev" --url http://localhost:3000 \
  --cmd "python api.py" --url http://localhost:8000 \
  -- python tests/e2e.py
```
- **Always:** `wait_for_load_state('networkidle')` before inspecting; re-snapshot after navigation; close the browser
- Examples in `examples/`: `element_discovery.py`, `static_html_automation.py`, `console_logging.py`

### 10.3 GUI Suite Routing (سطح المكتب)
```
Plan      → scripts/run_gui_test_orchestrator.py  (references/gui_testing_contract_orchestrator.md)
PyQt runs → scripts/run_pyqt_test_engine.py       (references/gui_testing_contract_pyqt.md)
  ├─ fail → failure recorder  → gui_failure_catalog.json
  ├─ flaky→ flake stabilizer  → root-cause fix (not sleeps)
  └─ fixed→ gui-repair-runner → retest ORIGINAL failing test
```

---

## 11. Verification Checklist (قائمة التحقق)

- [ ] Test strategy defined (what to test, what not to)
- [ ] Tests are independent (no order dependency)
- [ ] Tests are deterministic (same result every run)
- [ ] Tests are fast (unit < 100ms, e2e < 30s)
- [ ] Test data is isolated (sandbox, no production)
- [ ] Failures are recorded with evidence (screenshots, traces)
- [ ] Flaky tests identified and stabilized
- [ ] CI pipeline runs tests automatically
- [ ] Test coverage adequate (critical paths covered)
- [ ] Visual regression baselines exist
- [ ] API contract tests pass
- [ ] Performance tests within thresholds
- [ ] Security scans completed
- [ ] All results classified: passed / failed / inconclusive

---

## Related Skills

- `$repair-stability` — for fixing broken tests
- `$security-comprehensive` — for security testing
- `$backend-comprehensive` — for API test design
- `$agent-workflows` — for TDD methodology
- `$devops-comprehensive` — for CI/CD integration
