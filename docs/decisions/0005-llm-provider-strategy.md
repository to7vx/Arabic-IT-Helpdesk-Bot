# 5. LLM provider strategy

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

We want generative features (ticket summary, KB answer synthesis, agent draft replies) but must respect PDPL data-residency rules and let operators turn the LLM off entirely.

See [research/arabic-llms.md](../research/arabic-llms.md) and [research/saudi-pdpl.md](../research/saudi-pdpl.md).

## Decision

Single `LLMClient` interface with three providers:

| Provider | When to choose | Default model |
|---|---|---|
| `claude` | Best quality, cloud-friendly, US/EU tenants | `claude-opus-4-7` (latest at time of decision) |
| `jais` | In-Kingdom self-hosted, sovereignty required | `jais-30b-chat` via vLLM or Ollama |
| `disabled` | No generation; encoder-only NLP | n/a |

Every NLP feature must function in `disabled` mode (degraded but useful). UI clearly labels AI-generated output.

## Consequences

* Operators pick provider in admin UI; default is `disabled` to avoid surprise PDPL transfers on first run.
* Prompt-caching is mandatory on Claude provider (see [claude-api skill]).
* All prompts live in `nlp/generation/prompts.py` with bilingual variants; changes require an eval-suite delta review.
* We do not target GPT-4 / OpenAI; users who want it can plug into `claude` by swapping endpoint in a future ADR.
