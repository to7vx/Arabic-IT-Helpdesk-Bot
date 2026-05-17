# Arabic Large Language Models

**Researched:** 2026-05  
**Decision affected:** [ADR-0005 LLM provider strategy](../decisions/0005-llm-provider-strategy.md)

## Question

For draft replies, ticket summarization, and KB answer synthesis: hosted LLM, open-weights LLM, or both?

## Candidates

| Model | Type | Notes |
|---|---|---|
| **Claude (Anthropic)** | Hosted, closed | Strong Arabic quality; PDPL data-transfer obligations apply |
| **Jais-30B** (G42 / Inception / Cerebras) | Open weights | 13B and 30B variants; "world's most advanced Arabic LLM" per Cerebras; ~395B tokens AR+EN pretraining |
| **AceGPT-v2** | Open weights | Continued-pretraining adaptation; last release Oct 2024 (now ~18 months old) |
| **GPT-4 / GPT-4o** | Hosted, closed | Strong Arabic but same compliance concerns |

## Empirical signal

* **Jais-30b-chat vs AceGPT-13b-chat:** Jais wins ~68% of head-to-heads on Arabic prompts in GPT-4-judged evals (G42 publication).
* **Commercial vs. open:** Claude / GPT-4 still lead average benchmarks but Jais is "on par with ChatGPT" on Arabic writing tasks per The Decoder coverage.
* **Stanford HELM-Arabic** (Dec 2025) confirms hosted closed models lead, with Jais the strongest open-weights option.

## Recommendation

* **Primary, cloud-friendly tenants:** Anthropic Claude (current default model per project guidance), with prompt caching for cost control.
* **Self-hosted / sovereign tenants:** Jais-30B via Ollama or vLLM. Lower quality acceptable trade-off for full data residency.
* All LLM calls go through a single `LLMClient` abstraction with a `provider` config knob (`claude` | `jais` | `acegpt` | `disabled`).
* **Disabled is a first-class mode** — every NLP feature must degrade gracefully to encoder-based predictions when no LLM is configured.

## PDPL implication

Sending personal data to a non-Kingdom LLM endpoint counts as cross-border transfer (see [saudi-pdpl.md](saudi-pdpl.md)). Operator must either (a) execute SDAIA-approved SCCs with the LLM vendor or (b) configure `provider=jais` and self-host. UI surfaces the active mode to administrators.

## Sources

- Cerebras, *Jais: a New Pinnacle in Open Arabic NLP*: https://www.cerebras.ai/blog/jais-a-new-pinnacle-in-open-arabic-nlp
- G42, *Jais-30B: Expanding the Horizon in Open-Source Arabic NLP*: https://www.g42.ai/resources/publications/Jais-30B
- *AceGPT, Localizing Large Language Models in Arabic* (arXiv:2309.12053): https://ar5iv.labs.arxiv.org/html/2309.12053
- Stanford CRFM, *HELM Arabic*: https://crfm.stanford.edu/2025/12/18/helm-arabic.html
- *Evaluating Arabic Large Language Models: A Survey of Benchmarks, Methods, and Gaps* (arXiv:2510.13430): https://arxiv.org/html/2510.13430v1
