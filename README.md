<div dir="rtl">

# Kaido — مكتبة مهارات الوكيل الذكي

**مكتبة مهارات شاملة تعمل في أي مشروع opencode** — دمج 297 مهارة أصلية داخل 19 مهارة مجالية واحدة.

</div>

> A curated skills library for [opencode](https://opencode.ai) agents — **297 original skills consolidated into 19 comprehensive domain skills**, usable in any project via a single `$<skill-name>` invocation.

---

## <div dir="rtl">لماذا هذه المكتبة؟</div>

بدلاً من حمّل عشرات المهارات المتفرقة لكل مشروع، تحصل على **19 مهارة شاملة** تغطي كامل دورة العمل:

| | | |
|---|---|---|
| 🎨 التصميم | 💻 الهندسة | 🔒 الجودة والأمان |
| 📱 الجوال والوسيط | 🗄️ قواعد البيانات | 🧪 الاختبار |
| 🔧 الإصلاح | 🚀 النشر | 🔌 التكاملات |
| 📋 الإدارة | 🤖 أعمال الوكيل | 📄 التوثيق |
| ⚙️ العمليات | 🖥️ سطح المكتب | 🐹 DevOps |

---

## <div dir="rtl">التثبيت</div>

### 1 — انسخ المجلد

```bash
git clone https://github.com/KAIDO-agent/agent-skills.git
```

انسخ مجلد `skills/` إلى مكان دائم لا يُحذف مع حذف المشاريع:

```
C:\Users\<user>\.kaido-skills\skills\<skill-name>\SKILL.md
```

### 2 — سجّل المسار في opencode

أضف إلى ملف الإعدادات العام `~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "skills": {
    "paths": ["C:\\Users\\<user>\\.kaido-skills\\skills"]
  }
}
```

<br>

> المجلد **مستقل عن أي مشروع** — انسخه لأي جهاز آخر أو شاركه بنسخ المجلد فقط. يُحمّل تلقائياً عبر `skills.paths`.

---

## <div dir="rtl">كيف تستدعي مهارة؟</div>

في أي جلسة opencode، أي وكيل، أي نموذج — استخدم صيغة الدولار:

```text
$design-web build a landing page for a coffee brand
$backend-comprehensive design a REST API with rate limiting
$security-comprehensive review this PR for OWASP issues
$testing-comprehensive add e2e tests for the checkout flow
```

أسماء المهارات بالشرطات تعمل كما هي:

```text
$codex-session-start-router
$cityofaiagents-operations
$documentation-comprehensive
```

---

## <div dir="rtl">سلاسل المهارات</div>

معظم المهام تحتاج أكثر من مهارة. إليك أنماط ربط جاهزة:

```text
تصميم واجهة ويب:      $design-web  →  $code-engineering  →  $testing-comprehensive
بناء سمة خلفية جديدة:  $backend-comprehensive  →  $database-comprehensive  →  $security-comprehensive  →  $testing-comprehensive
إطلاق تطبيق جوال:      $design-mobile  →  $mobile-development  →  $deployment-comprehensive
إصلاح عميق مسبق:      $repair-stability  →  $testing-comprehensive  →  $devops-comprehensive
مراجعة أمان:           $security-comprehensive  →  $code-engineering  →  $testing-comprehensive
```

---

## <div dir="rtl">فهرس المهارات التسع عشر</div>

<div dir="ltr">

| # | Skill | المجال |
|---|-------|--------|
| 1 | `design-web` | تصميم الواجهات الأمامية الكامل |
| 2 | `design-mobile` | تصميم تطبيقات iOS / Android |
| 3 | `design-desktop` | تصميم تطبيقات سطح المكتب |
| 4 | `design-figma` | التكامل الكامل مع Figma |
| 5 | `code-engineering` | هندسة الكود ومقاييس الجودة |
| 6 | `backend-comprehensive` | تطوير الواجهات الخلفية |
| 7 | `database-comprehensive` | قواعد البيانات والتحليلات |
| 8 | `mobile-development` | تطوير تطبيقات Expo / React Native |
| 9 | `multimedia-content` | الوسائط والإبداع الرقمي |
| 10 | `testing-comprehensive` | الاختبار الشامل |
| 11 | `security-comprehensive` | الأمن السيبراني |
| 12 | `repair-stability` | الإصلاح والاستقرار |
| 13 | `devops-comprehensive` | DevOps والبنية التحتية |
| 14 | `deployment-comprehensive` | النشر والتسليم |
| 15 | `integrations` | التكاملات الخارجية |
| 16 | `project-management` | إدارة المشاريع |
| 17 | `agent-workflows` | منهجية عمل الوكيل |
| 18 | `documentation-comprehensive` | التوثيق |
| 19 | `cityofaiagents-operations` | عمليات CityOfAIAgents |

</div>

---

## <div dir="rtl">نصائح للمبتدئين</div>

1. **ابدأ بالمهمة الصحيحة** — استخدم `$codex-session-start-router` لتوجيه المهمة للمهارة المناسبة، أو استدعِ المهارة مباشرة بـ `$<name>`.
2. **السلسل أهم من المهارة الواحدة** — معظم المهام تحتاج 2–4 مهارات منسّقة. راجع قسم «سلاسل المهارات».
3. **اقرأ الـ frontmatter أولًا** — وصف المهارة في أول سطر يخبرك متى تُفعّل؛ إن وصف مهمتك يطابقها، فالمهارة مناسبة.
4. **المهارات التدقيقية لا تعدّل المشروع** — تُخرج النتائج والتوصيات فقط (مثل `security-comprehensive`, `testing-comprehensive`).
5. **أضف مشاريعك بنقاط** — المجلد `agent-skills` مستقل وقابل للنسخ؛ انسخه لأي مشروع وتأكّد من `opencode.jsonc`.
6. **تحقّق دائمًا** — بعد أي مهمة تحقق من النتائج/التراجع قبل الإجراء التالي.

---

## <div dir="rtl">البنية</div>

```text
agent-skills/
├── README.md                  # هذا الملف
├── CONSOLIDATION_PLAN.md      # خطة الدمج وسجل التحقق
└── skills/
    ├── design-web/
    │   ├── SKILL.md           # تعريف المهارة (frontmatter + المنهجية)
    │   ├── scripts/           # سكربتات جاهزة للتشغيل
    │   └── references/        # مراجع عميقة تُحمّل عند الحاجة
    ├── backend-comprehensive/
    ├── security-comprehensive/
    └── ... (19 مهارة)
```

كل مهارة تحمل `SKILL.md` صالحًا مع بيانات `name` و `description` صحيحة، بالإضافة إلى `scripts/` و `references/` عند الحاجة.

---

## <div dir="rtl">الترخيص</div>

انسخ، عدّل، وشارك بحرية. استخدمها كما تشاء في مشاريعك الشخصية والتجارية.

---

<div dir="rtl">

**Kaido** — دليل مكتبة المهارات · تعمل في أي مشروع opencode

</div>
