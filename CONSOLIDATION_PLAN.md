# خطة تجميع المهارات — المكتبة المكتملة

> **الإصدار:** 3.0
> **التاريخ:** 2026-10-27
> **المصدر:** 178 مهارة محلية + 116 مهارة من المستودع = **297 مهارة**
> **النتيجة:** **19 مهارة شاملة** في `C:\Users\LENOVO\.kaido-skills\skills\`
> **الحالة:** ✅ **مكتملة ومُدققة** — جميع الفجوات أُصلحت

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
