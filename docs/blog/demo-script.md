# Demo Video Script (3:30)

A storyboard for a 3-and-a-half-minute walkthrough. Asciinema for the CLI portions, a screen recorder for the UI portions. The script below is what the narrator says.

---

**[00:00 — 00:15] Cold open**

Visual: blank terminal.

Narration: "Most IT helpdesks treat Arabic as a translated UI bolted onto an English NLP core. This one was built the other way around."

---

**[00:15 — 00:35] Install**

Visual: terminal types

```
git clone https://github.com/USER/arabic-helpdesk-bot
cd arabic-helpdesk-bot
cp .env.example .env
make demo
```

Narration: "Three commands. About eight minutes on a laptop. By the end you have Postgres, Redis, Qdrant, MinIO, the FastAPI backend, the worker, and the Next.js web app — with bilingual sample data."

---

**[00:35 — 01:05] Open the portal in Arabic**

Visual: browser at `localhost:3000`, Arabic RTL. Hover over the language toggle in the top-end corner.

Narration: "The default locale is Arabic. The whole UI is RTL — the inbox, the form, the keyboard shortcuts. One click toggles to English."

Visual: click toggle. UI flips to LTR.

---

**[01:05 — 01:45] Submit a ticket in Saudi dialect**

Visual: switch back to Arabic. Open "New ticket".

Type: `الـ VPN ما يشتغل من البيت 🚨`

Visual: as typing, the AI suggests categories in a side panel: `network-vpn` 91%, then `network-internet` 7%.

Narration: "Live category prediction as the user types. Notice the urgent emoji — it survives normalization as a marker token, which is why urgency lights up immediately."

Visual: submit. Ticket created.

---

**[01:45 — 02:30] Agent view with AI Copilot**

Visual: switch to the agent workspace at `/agent/<id>`. Split pane: ticket on the start side, AI Copilot on the end.

Narration: "The agent sees the ticket and an AI Copilot panel — auto-generated three-sentence summary, suggested category with confidence, top KB articles with relevance scores, urgency and sentiment signals, dialect, language."

Visual: hover over the KB suggestions. Click "Draft reply". Show generated draft with citations.

---

**[02:30 — 03:00] Arabizi handling**

Visual: open a new ticket. Type `msh 3aref el password bta3 el wifi`.

Visual: language detected: `ar`. Dialect: `arabizi`. Category: `network-wifi`.

Narration: "Arabizi — Arabic written in Latin letters — is recognized as Arabic and routed to the Arabic-speaking agent queue. Routing on script instead of language is a bug we wanted to fix."

---

**[03:00 — 03:20] PDPL toolkit**

Visual: navigate to Admin → Compliance.

Visual: panel shows `LLM_PROVIDER: disabled`, transfer log empty, consent inventory active.

Narration: "Out of the box, no data leaves the Kingdom. Enabling Claude or any other cloud LLM requires an explicit cross-border confirmation that is logged in the transfer ledger."

---

**[03:20 — 03:30] Outro**

Visual: GitHub repo page.

Narration: "Open source, Apache 2.0, self-hosted. The link's in the description. PRs welcome."

---

## Recording checklist

- [ ] Fresh `make demo` so the sample data renders consistently.
- [ ] Browser at 1440x900 with the OS in dark mode.
- [ ] Disable browser extensions that add UI chrome.
- [ ] Use a system Arabic font (IBM Plex Sans Arabic is bundled).
- [ ] Record at 1080p, 30 fps.
- [ ] Mic levels: -14 LUFS target.
