# خطة تجميع المهارات — المكتبة المكتملة

> **الإصدار:** 3.8
> **التاريخ:** 2026-11-06
> **المصدر:** 178 مهارة محلية + 116 مهارة من المستودع = **294 مهارة تاريخية**؛ لا تُستخدم هذه الأرقام لعدّ المهارات الحالية بعد الدمج. أضيفت مصادر vercel-labs وusestrix/strix داخل المجالات الموجودة.
> **النتيجة:** **19 مهارة شاملة** في `C:\Users\LENOVO\.kaido-skills\skills\`
> **الحالة:** ✅ **مكتملة ومُدققة + متسقة** — … · 3.7 strix · **3.8 تدقيق الاتساق (CONSISTENCY.md)**

---

## 🔗 تدقيق الاتساق (الإصدار 3.8 — 2026-11-06)

فحص شامل للتعارضات بين المجالات الـ19:
- **فحص رياضي/عتبات** على كل SKILL.md (p95، LCP، عتبات التنبيه، retry، تباين، سرعة اختبارات) → **تعارض واحد فقط**
- **أُصلح:** `devops` 6.2 كان يقول `P1 p95 > 2s` بينما golden signals و`project-management` يقولان `> 1s` → **موحّد على 1s** + أُضيف `P0: p99 > 5s`
- **`CONSISTENCY.md` جديد:** خريطة ملكية لكل موضوع متقاطع (مالك واحد + ذِكر سياقي مسموح) + جدول القواعد الرقمية المُتحقَّق من تطابقها + قاعدة الصيانة المستقبلية
- باقي المواضيع (a11y 4.5:1 · LCP 2.5s · retry=3 · عتبات الأخطاء · سرعة الاختبارات): **متطابقة أصلًا**

---

## 🛡️ دمج usestrix/strix (الإصدار 3.7 — 2026-11-05)

دراسة مستودع `usestrix/strix` (73k+ نجمة، رخصة **Apache-2.0**) → **9 مهارات اختبار اختراق آلي بالذكاء الاصطناعي** → دُمجت كلها في **`security-comprehensive`** (صفر مجالات جديدة):

- `references/strix/` — الملفات التسعة كاملة + `index.md` توجيهي
- مؤشر جديد في **9.3** من SKILL.md: CLI أساسي، قواعد (تصريح فقط، `-n` + `--max-budget`، خروج 0 ≠ تغطية كاملة)، وجدول توجيه لكل المهام
- الإسناد الكامل في **`CREDITS.md`** (Apache-2.0 — إشعار الرخصة محفوظ)

---

## 🔍 الفجوات المتبقية — تحليل وغلق (الإصدار 3.4 — 2026-11-05)

تحليل شامل للأوصاف الـ19 مقابل خريطة المجالات الشائعة → **3 فجوات حقيقية، كلها أُدمجت في مجالات موجودة (صفر مجالات جديدة):**

| الفجوة | أُدمجت في | المحتوى |
|---|---|---|
| **هندسة البيانات** (ETL/streaming/CDC) | `database-comprehensive` — قسم 9 | `references/data-engineering/` (4 ملفات): etl · streaming · data-quality · index |
| **الشبكات ولينكس** (DNS/TLS/systemd) | `devops-comprehensive` — قسم 11 | `references/networking-linux/` (3 ملفات): networking · linux · index |
| **SEO + التحليلات** | `design-web` — قسم 17 | `references/seo-analytics/` (3 ملفات): seo · analytics · index |

- أوصاف frontmatter الثلاثة حدُّثت للاكتشاف الصحيح
- **قرارات مُغلقة:** تطوير الألعاب والـ embedded/IoT خارج نطاق المكتبة (مكتبة مطوّرين)، تغطيتها عبر `multimedia-content` و`design-desktop` جزئيًا
- المجالات تبقى **19** بالضبط

---

## 🧪 الاختبارات الآلية + CI (الإصدار 3.3 — 2026-11-03)

- `tools/validate_skills.py` — 10 فحوصات، stdlib فقط (frontmatter، روابط ميتة، SKILL.md متداخل، صياغة Python/shell/JS، UTF-8، ملفات build متعقّدة، فحص أسرار، صحة JSON)
- `.github/workflows/validate.yml` — يشتغل على كل push و PR (ubuntu, Python 3.12, Node 20)
- **النتيجة:** PASS محليًا + **GitHub Actions: success** من أول تشغيل
- ملاحظة: رفع ملفات workflow يتطلب نطاق `workflow` في رمز GitHub (`gh auth refresh -s workflow`)

## 🕳️ تغطية الفجوات (الإصدار 3.3 — بدون أي مجال جديد)

| الفجوة | أُدمجت في | المحتوى |
|---|---|---|
| **AI Engineering** | `backend-comprehensive` — قسم 13 | `references/ai-engineering/` (6 ملفات): llm-apis · prompt-engineering · rag · vector-stores · agents · evals |
| **Data Science** | `database-comprehensive` — قسم 8 | `references/data-science/` (7 ملفات): pandas · notebooks · stats · feature-engineering · ml-basics · visualization · index |

- أوصاف frontmatter حدُّثت ليشمل المجالين (الاكتشاف الصحيح للمهارة)
- المجالات تبقى **19** — نفس أسلوب الدمج: مؤشرات مختصرة في SKILL.md + محتوى عميق في `references/`

---

## 📦 دمج مهارات vercel-labs (الإصدار 3.2 — 2026-11-03)

دراسة حساب `github.com/vercel-labs` كاملًا (100 مستودع) → 6 مستودعات تحتوي **13 مهارة** → دُمجت **بدون أي مجال جديد** داخل المجالات الـ19:

| المهارة الواردة | المستودع | أُدمجت في |
|---|---|---|
| `deploy-to-vercel` · `vercel-cli-with-tokens` · `vercel-optimize` | agent-skills | `deployment-comprehensive/references/vercel/` |
| `react-best-practices` · `composition-patterns` · `react-view-transitions` · `cra-to-next-migration` | agent-skills + migration-skills | `code-engineering/references/` |
| `react-native-skills` | agent-skills | `mobile-development/references/react-native-skills/` |
| `web-interface-guidelines` · `geist-learning-lab` | agent-skills + skill-geist-learning-labs | `design-web/references/` |
| `writing-guidelines` | agent-skills + writing-guidelines (MIT) | `documentation-comprehensive/references/` |
| `create-remotion-geist` | skill-remotion-geist | `multimedia-content/references/create-remotion-geist/` |
| `ucp` (agentic commerce) | agentic-commerce-skills | `integrations/references/ucp/` |

- الإسناد الكامل + ملاحظات الترخيص: **`CREDITS.md`**
- المحتوى كله في `references/` — المؤشرات أُضيفت في SKILL.md الخاص بكل مجال
- فحص بعد الدمج: frontmatter 19/19 + روابط مفقودة 0 + بدون SKILL.md متداخل

---

## 🔎 تدقيق شامل (الإصدار 3.1 — 2026-11-03)

فحوصات آلية على المكتبة كاملة + اختبارات تشغيل فعلية:

| الفحص | النتيجة |
|---|---|
| frontmatter صالح (name + description) | ✅ 19/19 |
| صلاحية ترميز UTF-8 لكل الملفات النصية | ✅ 100% |
| صياغة Python (46 ملف) | ✅ 46/46 |
| صياغة JavaScript (12 ملف) | ✅ 12/12 |
| الروابط الداخلية في SKILL.md | ✅ **126/126 بعد الإصلاح** (كانت 40 مفقودة) |
| تشغيل السكربتات (`--help`) | ✅ **43/47** — المتبقية4 تحتاج `playwright`/`pdf2image` (موثقة الآن في SKILL.md) |
| اختبارات تشغيل فعلية (بوابة الأمان، تخطيط الاختبارات، التشخيص، الماركداون) | ✅ 4/4 نتائج صحيحة |
| أسرار / مسارات جهاز في الملفات المستعادة | ✅ 0 |

### الإصلاحات التي أُنجزت في 3.1
1. **استعادة المكتبات المشتركة المفقودة** من الأصول (سلة المحذوفات):
   - `skills/_skill-governance/python_lib/` → `project_intel.py` + `skill_governance.py`
   - `skills/sdlc-system/python_lib/sdlc_common.py` → أُعيد بناؤها بالكامل (7 دوال: `load_artifact`, `write_artifact`, `list_from_payload`, `flatten_text`, `keyword_set`, `parse_simple_yaml`, `execute_configured_script`)
   - النتيجة: **7 سكربتات كانت ترمي `ModuleNotFoundError` أصبحت تعمل**
2. **استعادة 40 ملفًا مرجعيًا/سكربت مذكورًا في SKILL.md لكنه مفقود** (كلها من المهارات الأصلية):
   - `code-engineering`: 27 مرجعًا + `references/coding_standards/` + 9 سكربتات
   - `design-web`: `scripts/init-artifact.sh`, `scripts/bundle-artifact.sh`
   - `documentation-comprehensive`: `scripts/build_docs_sync_plan.py`
   - `cityofaiagents-operations`: `scripts/run_cityofaiagents_visual_gui_verification_ops.py`
3. **توثيق التبعيات:** `pdf2image` في documentation-comprehensive و`playwright` في testing-comprehensive.
4. **مزامنة مع GitHub:** سحب 4 commits (إعادة تصميم README + assets) — الآن محلي = `origin/main`.

---

## ✅ المكتبة النهائية (19 مهارة)

| # | المهارة | المجال | الأسطر | مراجع | سكربتات | الحالة |
|---|---------|--------|--------|-------|---------|--------|
| 1 | `design-web` | تصميم الويب | 533 | — | — | ✅ |
| 2 | `design-mobile` | تصميم المحمول | 384 | — | — | ✅ |
| 3 | `design-desktop` | تصميم سطح المكتب | 435 | — | — | ✅ |
| 4 | `design-figma` | Figma الكامل | 375 | 31 | 9 | ✅ |
| 5 | `security-comprehensive` | الأمان | 616 | 19 | 7 | ✅ |
| 6 | `agent-workflows` | منهجية عمل الوكلاء | 476 | — | — | ✅ |
| 7 | `testing-comprehensive` | الاختبار | 439 | 6 | 6 | ✅ |
| 8 | `backend-comprehensive` | الخلفية | 815 | — | — | ✅ |
| 9 | `deployment-comprehensive` | النشر | 565 | 330+ | 4 | ✅ |
| 10 | `documentation-comprehensive` | التوثيق | 456 | 3 | 60 | ✅ |
| 11 | `project-management` | إدارة المشاريع | 431 | — | — | ✅ |
| 12 | `database-comprehensive` | قواعد البيانات | 465 | — | — | ✅ |
| 13 | `code-engineering` | هندسة الكود | 418 | — | — | ✅ |
| 14 | `repair-stability` | الإصلاح والاستقرار | 327 | — | — | ✅ |
| 15 | `devops-comprehensive` | DevOps | 395 | 12 | 4 | ✅ |
| 16 | `multimedia-content` | الوسائط والمحتوى | 493 | 21 | 19 | ✅ |
| 17 | `integrations` | التكاملات | 410 | — | — | ✅ |
| 18 | `mobile-development` | تطوير المحمول | 592 | 72 | — | ✅ |
| 19 | `cityofaiagents-operations` | عمليات CityOfAIAgents | 480 | — | — | ✅ |

**الإجمالي: 19 مهارة / 9,036 سطرًا + ~500 ملف مرجع وسكربت**

---

## 🔧 سجل إصلاح الفجوات (الإصدار 3.0)

### أولاً: المهارات الـ 19 المفقودة — أُضيفت جميعها
| المهارة المفقودة | المهارة المضيفة | ما أُضيف |
|---|---|---|
| brand-guidelines | design-web | ألوان Anthropic + Poppins/Lora + قواعد الدوران |
| theme-factory | design-web | 10 ثيمات + theme-showcase + توليد مخصص |
| ux-audit | design-web | منهجية 3-tier + React 19 APIs |
| web-artifacts-builder | design-web | bundle.html + مكافحة AI slop |
| mcp-builder | backend-comprehensive | FastMCP + TS SDK + قواعد التسمية |
| realtime-sync | backend-comprehensive | WebTransport + CRDT + Outbox + backpressure |
| security-ownership-map | security-comprehensive | رسم بياني للملفين + bus factor + networkx |
| expo-tailwind-setup | design-mobile | NativeWind v5 + react-native-css |
| expo-ui-swiftui | design-mobile | Host + RNHostView |
| expo-ui-jetpack-compose | design-mobile | Host + LazyColumn + Icon |
| use-dom | mobile-development | 'use dom' + استراتيجية الترحيل |
| playwright-interactive | testing-comprehensive | js_repl + جلسات متpersistentة |
| flet-runtime-smoke-verifier | design-desktop | فحص بدء التشغيل + blank-window |
| project-frontend-architecture-builder | code-engineering | Zustand + TanStack + RHF |
| project-idea-research-intake | project-management | بحث مسبق + مقارنة منافسين |
| project-operations-ledger | code-engineering | .codex-project-intel/ + سجل العمليات |
| codex-component-capability-router | agent-workflows | إفصاح القدرات + التوجيه |
| skill-artifact-cleaner | integrations | backup-manifest + dry-run |
| skill-knowledge-updater | integrations | source allowlist + تصنيف الإشارة |

### ثانياً: إصلاح البيانات القديمة (تم جميعها)
- ✅ `tts-1` → **`gpt-4o-mini-tts-2025-12-15`** (الصوت الافتراضي `cedar`) في multimedia-content
- ✅ معرفات Claude القديمة (`claude-sonnet-4-5`/`opus-4-5`) → **`claude-opus-4-8`** + جدول التسعير الكامل في integrations
- ✅ `sentry-cli` القديم → **`sentry`** CLI الحديث مع `--json --fields` و`sentry schema`
- ✅ **EAS Workflow الخاطئ** (كان GitHub Actions YAML) → صيغة EAS الحقيقية مع schema-fetch discipline

### ثالثاً: المراجع والسكربتات المستعادة
- **security-comprehensive:** 19 مرجع + 7 سكربتات (ownership-map, remediation, secret-scan)
- **devops-comprehensive:** 12 مرجع + 4 سكربتات (CI analyzer, docker validation)
- **deployment-comprehensive:** 330+ مرجع (64 منتج Cloudflare) + 4 سكربتات (EAS validate/fetch)
- **testing-comprehensive:** 6 مراجع + 6 سكربتات (playwright, GUI orchestrator, PyQt)
- **documentation-comprehensive:** 60 سكربت (office pack/unpack, render_docx) + أمثلة + مراجع
- **multimedia-content:** 21 مرجع + 19 سكربت (TTS, transcribe, sora, screenshots, pet atlas)
- **mobile-development:** 72 مرجع (Reanimated, native-tabs, React 19, bundle analysis)
- **design-figma:** 31 مرجع + 9 سكربتات (figma-generate-library helpers)

### رابعاً: الفجوات الجزئية التي أُحسنت
- backend: OpenAPI codegen, pino advanced, ASP.NET app-model, Zod v4, MCP, Real-Time
- database: PG17/18 (async I/O, UUIDv7, HNSW), Supabase traps (user_metadata, security_invoker), Valkey (locks, queues, eviction)
- security: Ownership map, secure storage migration, security gate, threat model, remediation
- devops: IaC (Terraform/distroless/Trivy), golden signals, CI evidence gates
- testing: interactive testing, GUI suite routing, webapp-testing
- code-engineering: frontend architecture, ops ledger, SOLID, rapid-prototyper kill-criteria
- repair-stability: change-impact-mapper (distinct step), artifact contracts, evidence dedup
- agent-workflows: gate chain, capability routing, session memory, plan interrogation
- project-management: ADR, BPMN, traceability, OKR, research-intake, decision log
- cityofaiagents: design-spec workflow, pywinauto runner, doc evidence discipline

---

## ✅ التحقق النهائي
- **19/19** مهارة بـ frontmatter صالح (`name` + `description`)
- **19/19** من المهارات المفقودة أصبحت مغطاة
- **0** بيانات قديمة متبقية
- **0** مجلدات متداخلة (`references\references`) أو `__pycache__`

## إعداد opencode
- المسار: `C:\Users\LENOVO\.kaido-skills\skills`
- التكوين: `~/.config/opencode/opencode.jsonc` → `skills.paths`
- الاستدعاء: `$<skill-name>` في أي مشروع

---

## 📄 الخطوة التالية: دليل PDF عربي
دليل عصرى بالرسومات والألوان والتنسيق الجميل — يشمل كل مهارة، طريقة الاستدعاء `$<name>`، سلاسل المهارات، وأمثلة عملية.
