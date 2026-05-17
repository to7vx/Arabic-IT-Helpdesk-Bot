# Why I built an Arabic IT Helpdesk Bot

I have spent more time than I care to admit watching IT agents in Jeddah and Riyadh translate tickets in their head — Arabic in, English categorization, English KB search, Arabic reply out. The big SaaS vendors treat Arabic as a translated UI bolted onto an English NLP core. The open-source helpdesks are great products that ship zero Arabic-specific NLP. The gap was obvious. So I built the thing I kept wishing existed.

## What it is

An open-source, self-hosted IT helpdesk with:

* **Arabic NLP first**, not as an afterthought. MARBERT and CAMeL Tools handle MSA, Gulf, Egyptian, and Levantine dialects; the preprocessor recognizes Arabizi (`msh 3aref el password`) and routes it as Arabic.
* **True bilingual UX**. Every page is fully usable in Arabic (RTL) and English (LTR) with the same polish. Dates flip between Hijri and Gregorian without losing context. The agent inbox keeps keyboard shortcuts working in both directions.
* **PDPL-aware out of the box**. Consent ledger, Data Subject Rights endpoints, cross-border transfer log, and a default mode that makes no outbound calls until an admin explicitly opts in.
* **Apache 2.0** licensed. Fork it, ship it commercially, embed it in your platform.

## Three things I learned

**Preserve the user's words.** Arabic normalization is necessary for retrieval and classification — fold `إ`, `أ`, `آ` to `ا`, drop diacritics, strip the kashida — but every step destroys information. We keep `description` verbatim and put normalized text in a separate column. Future-you, debugging a weird classification six months from now, will thank you.

**Hybrid > dense alone.** Pure dense retrieval loses on the kinds of tokens helpdesk tickets are full of: error codes (`MSG-3055`), software versions (`Outlook 2024`), hostnames. BM25 over morphology-lemmatized text picks those up cheaply. We fuse the two with Reciprocal Rank Fusion (k=60) and it is unreasonably effective.

**PDPL is a feature, not a tax.** Saudi Arabia's Personal Data Protection Law treats every LLM call abroad as a regulated cross-border transfer. We made "no transfer" the default. The first two pilot deployments specifically chose us because of this — it turned out to be a sales feature, not a constraint.

## What is not built yet

This is a v0.1 release. The MARBERT-based category classifier is the next major piece (today it ships a credible keyword baseline so the rest of the system works end-to-end). The golden evaluation set is at 20 examples; it needs to grow to ≥ 500 with two annotators per item before I trust the F1 numbers. Live demo deployment, Helm chart at HA scale, and the Slack/Teams/WhatsApp integrations are in the roadmap.

## How to try it

```bash
git clone https://github.com/USER/arabic-helpdesk-bot
cd arabic-helpdesk-bot
cp .env.example .env
make demo
```

In under 10 minutes you have a full stack with bilingual sample data at http://localhost:3000.

## How to contribute

Pull requests welcome. CONTRIBUTING.md covers commit conventions and the NLP eval gate. The most useful contributions right now: labeled Arabic ticket data (any dialect) for the golden set, Arabic font tuning for the UI, and KB articles in any IT domain.

The repo is at https://github.com/USER/arabic-helpdesk-bot. License is Apache 2.0. Feedback issues open.
