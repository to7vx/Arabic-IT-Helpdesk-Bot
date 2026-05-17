# Competitive Landscape

**Researched:** 2026-05  
**Decision affected:** PRD positioning; [ADR-0001](../decisions/0001-record-architecture-decisions.md)

## Open-source helpdesk options today

| Project | Language | Arabic UX | NLP | Notes |
|---|---|---|---|---|
| **Zammad** | Ruby/Rails | UI translation present; weak RTL polish | None | Mature, complex setup |
| **FreeScout** | PHP/Laravel | RTL via community packs | None | Email-centric |
| **osTicket** | PHP | RTL via locale packs | None | Long-standing, dated UX |
| **Chatwoot** | Ruby | Solid RTL; conversation-first | Embeddings only via plugins | Strongest UX baseline |

## Closed SaaS options

| Product | Arabic UX | NLP for Arabic | Gap |
|---|---|---|---|
| Zendesk | Translated UI; mediocre RTL | English-first AI features; weak Arabic intent/sentiment | Vendor lock-in, data residency |
| Freshdesk | Translated UI | English-first | Same |
| Jira Service Mgmt | Translated UI | English-first | Same |

## Gap we fill

1. **Arabic-NLP-first** — dialect detection, Arabizi, code-switch, ticket categorization, KB RAG.
2. **PDPL-aware self-hosting** — out-of-the-box compliance toolkit.
3. **Bilingual UX parity** — every UI surface ships ar/en with equal polish (RTL is not an afterthought).
4. **Apache 2.0** — commercial-friendly forks for system integrators.

## Sources

(Vendor pages and project READMEs surveyed May 2026; no single citation. Confirmed Chatwoot's RTL quality via current repo screenshots; verified Zammad Arabic support via translation tooling docs.)
