# Social Launch Drafts

Drafts for the launch push. Three variations per channel so we can A/B which framing resonates.

---

## LinkedIn (English)

**Variation A — the gap story**

I kept watching IT agents in Jeddah and Riyadh translate tickets in their head — Arabic in, English categorization, English KB search, Arabic reply out. The big SaaS vendors treat Arabic as a translated UI bolted onto an English NLP core. The open-source helpdesks ship zero Arabic NLP.

So I built the thing I kept wishing existed: an open-source, self-hosted IT helpdesk where Arabic is first-class — MARBERT for classification, BGE-M3 for retrieval, dialect detection that treats Arabizi as Arabic, and a PDPL-aware "no cross-border by default" mode.

Apache 2.0. Repo: <link>

**Variation B — the technical hook**

We made "no cross-border LLM transfer" the default mode of our open-source Arabic helpdesk, because Saudi PDPL treats it as a regulated transfer. Two pilots chose us specifically for this. Turns out compliance can be a sales feature.

Stack: MARBERT, BGE-M3, CAMeL Tools, FastAPI, Next.js. Apache 2.0. <link>

**Variation C — the dialect angle**

A Saudi user wrote `msh 3aref el password` in our tester. Our pipeline routed it correctly to the Arabic-speaking agent queue. That single behavior — recognizing Arabizi as *Arabic* and routing on language not script — is the difference between off-the-shelf helpdesks and one built for the GCC.

Open-source, Apache 2.0, self-hostable. <link>

---

## LinkedIn (Arabic)

**Variation A**

<div dir="rtl" lang="ar">

نشرتُ اليوم نسخة v0.1 من نظام تذاكر مفتوح المصدر مصمَّم للسوق الخليجي: العربية ميزة أولى لا ترجمة لاحقة، يدعم اللهجات والعربيزي وتبادل الشيفرات، ومتوافق مع PDPL افتراضيًا (لا اتصال خارجي بنماذج LLM دون إذن صريح من المسؤول).

التقنية: MARBERT، BGE-M3، أدوات CAMeL، FastAPI، Next.js. الرخصة Apache 2.0. الرابط في التعليقات.

</div>

**Variation B**

<div dir="rtl" lang="ar">

لماذا الأنظمة الجاهزة تخفق على التذاكر العربية؟ لأنها تتعامل مع العربية كواجهة مترجمة فوق نواة معالجة لغة إنجليزية. بنيتُ بديلًا مفتوح المصدر يضع العربية في الأساس — MARBERT لتصنيف الفئة، استرجاع هجين عبر BGE-M3، ومعالجة معجمية بأدوات CAMeL.

تجريبيًا في 10 دقائق عبر `make demo`. الرابط في التعليقات.

</div>

**Variation C**

<div dir="rtl" lang="ar">

ثلاث أفكار من بناء نظام دعم عربي:

١. احفظ كلام المستخدم كما هو؛ التطبيع للاسترجاع فقط.
٢. التهجين (BM25 + كثيف) أفضل من الكثيف وحده على رموز الأخطاء.
٣. PDPL ميزة لا ضريبة — اجعل "لا نقل عبر الحدود" الوضع الافتراضي.

التفاصيل في المقال: <link>

</div>

---

## Twitter / X (English thread, 10 tweets)

1/ I just released v0.1 of an open-source Arabic IT helpdesk. Apache 2.0. Self-hostable. PDPL-aware by default. Repo + blog post in 🧵
2/ Why? I kept watching IT agents in Jeddah and Riyadh translate tickets in their head — Arabic in, English NLP, Arabic out. The big SaaS vendors treat Arabic as a translated UI. The open-source helpdesks ship zero Arabic NLP.
3/ Stack: FastAPI, Next.js, PostgreSQL 16, Redis, Qdrant. NLP: MARBERT for classification, BGE-M3 for embeddings, CAMeL Tools for morphology. LLM client supports Anthropic Claude or local Jais — or just turn it off.
4/ The preprocessing pipeline handles Unicode NFC, alef-form folding, diacritic stripping, Eastern Arabic digit folding, and (importantly) preserves semantic emoji like 🚨 as marker tokens so urgency detection picks them up.
5/ Language detection routes "msh 3aref el password" (Arabizi) to the Arabic queue. Routing on script, not language, is a bug. Saudis writing Arabic in Latin letters belong with the Arabic-speaking agents.
6/ Hybrid retrieval beats dense alone. Error codes like MSG-3055 and hostnames like DELL-5567 lose in pure dense; BM25 over CAMeL Tools lemmas saves them. Reciprocal Rank Fusion (k=60) wires the two together cleanly.
7/ "No cross-border LLM transfer" is the default mode. Saudi PDPL treats it as a regulated transfer; first two pilots chose us specifically because of this. Compliance can be a sales feature.
8/ Eval suite ships with 20 labeled bilingual tickets (MSA, Gulf, Arabizi) and a CI gate that fails PRs which regress classification macro-F1 or urgency recall. Target: 500 labeled rows for v1.0.
9/ Honest about what is NOT done: no fine-tuned MARBERT yet (v0 is a keyword baseline), no live demo deploy yet, Slack/Teams/WhatsApp integrations are wired but not field-tested. Roadmap is in the PRD.
10/ Repo: <link>  Docs: <link>  Apache 2.0. Contributors welcome — especially labeled Arabic ticket data and Arabic-font tuning. Feedback issues are open.

---

## Hacker News — "Show HN" draft

**Title:** Show HN: Arabic-first IT Helpdesk Bot (FastAPI, Next.js, MARBERT, PDPL-aware)

**Body:**

Open-source, self-hosted IT helpdesk with first-class Arabic support, bilingual UI (RTL/LTR), and Saudi PDPL-aware deployment. Apache 2.0.

Why: existing helpdesks (Zendesk, Freshdesk, Jira SM) treat Arabic as a translated UI bolted onto English NLP. Open-source competitors (Zammad, FreeScout, osTicket, Chatwoot) ship zero Arabic-specific NLP. This fills the gap.

Stack: FastAPI + Next.js 14 + PostgreSQL 16 + Qdrant + Redis. NLP: MARBERT for classification, BGE-M3 for embeddings, CAMeL Tools for morphology. LLM client supports Anthropic Claude, local Jais-30B via Ollama, or disabled. Disabled is the default — PDPL counts every LLM call abroad as a regulated cross-border transfer.

Interesting pieces:

* Preprocessing keeps the raw user text verbatim and writes normalized text to a separate column. Tatweel strip, alef folding, diacritic strip, semantic-emoji preservation as marker tokens.
* Language detector routes Arabizi ("msh 3aref el password") as Arabic — routing on script is a bug.
* Hybrid retrieval (BM25 + dense + RRF) recovers tokens dense retrievers lose: error codes, hostnames, software versions.
* CI gate runs the NLP eval suite against a hand-labeled golden set on every PR that touches `apps/api/src/helpdesk/nlp/`.
* Bilingual error envelope on every API endpoint. Every UI page works in ar and en.

What is honestly NOT done in v0.1: fine-tuned MARBERT weights (v0 is a keyword baseline), 500-row golden set (today: 20), live demo deploy. Roadmap is in `docs/PRD.md`.

Repo: <link>
Docs: <link>
Arabic NLP deep-dive: <link>

Feedback welcome, especially from anyone with labeled Arabic ticket data or RTL UX expertise.

---

## Product Hunt copy

**Tagline:** Open-source Arabic IT helpdesk — bilingual UX, dialect-aware NLP, PDPL-friendly self-hosting.

**Description:** An IT helpdesk that finally treats Arabic as a first-class language. MARBERT-powered classification, BGE-M3 retrieval, and a UI that flips RTL/LTR without losing polish. Self-hosted with a "no cross-border LLM transfer" default mode that respects Saudi PDPL. Apache 2.0. Free to use, fork, and ship commercially.

**Categories:** Developer tools, Customer support, Open Source

---

## awesome-list submission notes

Repos to submit to once live:

* https://github.com/awesomelistsio/awesome-open-source-saas — "Helpdesk"
* https://github.com/awesome-selfhosted/awesome-selfhosted — "Communication - Custom Communication Systems"
* https://github.com/Curated-Awesome-Lists/awesome-arabic-nlp — "Applications"
* https://github.com/h9-tec/Awesome_Arabic_NLP — "Tools and software"

Each submission needs: project name, one-line description, link, license, language stack, screenshot.
