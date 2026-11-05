# Consistency Map — خريطة الاتساق ومصادر الحقيقة

> **الغرض:** لكل موضوع متقاطع **مالك واحد** (source of truth). أي تعديل على قاعدة مشتركة يُعدَّل **هنا أولًا** ثم في المالك، والبقية مجرد سياق/إشارات.
> آخر تدقيق: 2026-11-06 · تدقيق رياضي/عتبات + بنيوي — **تعارض واحد فقط وُجد وأُصلح** (انظر الأسفل).

---

## 1. ملكية المواضيع المتقاطعة (Ownership)

| الموضوع | المالك الوحيد | ذِكر سياقي مسموح (لا يُعدّل القاعدة) |
|---|---|---|
| إمكانية الوصول (a11y / WCAG) | `design-web` | design-mobile · design-desktop · design-figma · code-engineering · testing |
| عتبات API والأداء العام (p95) | `backend-comprehensive` (الهدف) + `devops-comprehensive` (التنبيه) | project-management (تعكس عتبات devops حرفيًا) |
| Core Web Vitals (LCP/CLS/INP) | `design-web` | deployment (قائمة ما بعد النشر) |
| الأسرار والمفاتيح | `security-comprehensive` | deployment · devops (سيناريوهات نشر فقط) |
| منهجية الاختبارات | `testing-comprehensive` | agent-workflows (TDD) · devops (CI) · code (تخطيط) |
| CI/CD | `devops-comprehensive` | deployment (قوالب نشر) · testing (تشغيل اختبارات) · database (ترحيل) |
| التخزين المؤقت (أنماط التطبيق) | `backend-comprehensive` | database (Redis تشغيليًا) · mobile (client cache) |
| المصادقة والتفويض (قواعد) | `security-comprehensive` | backend (تنفيذ فعلي) · database (سياسات مستوى الصف) |
| معالجة الأخطاء والاسترداد | `backend-comprehensive` (الأنماط) | repair-stability (إصلاح عند الفشل) |
| السجلات/المراقبة | `devops-comprehensive` | backend (تسجيل التطبيق) · security (أحداث أمنية) |
| triage الخطورة (Critical→…) | `security-comprehensive` (للمسح الأمني) | repair-stability (للحوادث) |

## 2. قواعد رقمية مُتحقَّق من تطابقها (لا تُغيَّر في مكان واحد فقط)

| القاعدة | القيمة | المواضع (كلها متطابقة) |
|---|---|---|
| هدف أداء API | p95 < 200ms | backend L39 · project-management L97 |
| توفر الخدمة | 99.9% | backend L40 · project-management L99 |
| عتبات التنبيه P0/P1/P2 | 5%/5min · 1%/15min · 0.1%/1hr | devops 6.2 · project-management L411-413 |
| تنبيه الكمون P1 | p95 > 1s لـ 10 دقائق | devops 6.2 · devops golden signals · project-management P1 |
| LCP | < 2.5s | design-web CWV · deployment L567 |
| تباين الألوان AA | 4.5:1 (نص عادي) · 3:1 (كبير) | design-web · design-mobile · design-desktop · testing |
| سرعة الاختبار | unit < 100ms · e2e < 30s | testing · agent-workflows |
| محاولات إعادة المحاولة | max 3 + backoff أُسّي | backend L365 · repair-stability L135 |
| نشر تدريجي | 1% → 10% → (50%) → 100% | devops (مبسّط) · deployment (مفصّل) — متوافقان |

## 3. التعارض الذي وُجد وأُصلح

| قبل | بعد |
|---|---|
| `devops` 6.2: `P1 latency p95 > 2s` — يتعارض مع golden signals `p95 > 1s` و`project-management` P1 `p95 > 1s` | **موحّد على `> 1s for 10 minutes`** + أُضيف `P0: p99 > 5s` ليطابق project-management، + تعليق "canonical — mirrored in project-management" |

## 4. قاعدة صيانة مستقبلية

1. عند تغيير أي قيمة في الجدول أعلاه → غيّرها في **المالك + كل المواضع المذكورة**، ثم حدّث هذا الملف.
2. عند إضافة مجال/مهارة جديدة تحمل موضوعًا متقاطعًا → أضِف سطرًا في القسم 1 أولًا.
3. الفحص الآلي (`tools/validate_skills.py`) يغطي البنية؛ **هذا الملف هو فحص المعنى** — يُراجَع عند كل دمج جديد.
