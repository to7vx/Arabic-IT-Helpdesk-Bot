"""LLM client abstraction.

Single entry point for every generative call. Provider is selected from
``LLM_PROVIDER``:

* ``disabled`` — every method returns a clearly-labeled stub. The UI
  surfaces this state so operators know AI features are inactive.
* ``claude`` — Anthropic. Prompt caching is on by default and the
  destination is logged to the cross_border_transfers table by the
  caller before invocation.
* ``jais`` — local Jais via Ollama or vLLM. No external transfer.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

import httpx
import structlog

from helpdesk.config import LLMProvider, get_settings

logger = structlog.get_logger(__name__)


@dataclass(slots=True)
class GenerationResult:
    text: str
    provider: str
    model: str
    cached: bool = False


async def generate(*, system: str, user: str, max_tokens: int = 400) -> GenerationResult:
    settings = get_settings()
    if settings.llm_provider is LLMProvider.disabled:
        return GenerationResult(
            text="[AI disabled — enable a provider in Admin → Compliance to use generative features.]",
            provider="disabled",
            model="none",
        )
    if settings.llm_provider is LLMProvider.claude:
        return await _claude(system=system, user=user, max_tokens=max_tokens)
    if settings.llm_provider is LLMProvider.jais:
        return await _jais(system=system, user=user, max_tokens=max_tokens)
    raise RuntimeError(f"unknown provider: {settings.llm_provider}")


# ---------------------------------------------------------------------------
# Claude
# ---------------------------------------------------------------------------

async def _claude(*, system: str, user: str, max_tokens: int) -> GenerationResult:
    settings = get_settings()
    try:
        from anthropic import AsyncAnthropic
    except ImportError as exc:
        raise RuntimeError("install the `llm` extra: `uv sync --extra llm`") from exc

    client = AsyncAnthropic(api_key=settings.anthropic_api_key.get_secret_value())
    extra: dict[str, object] = {}
    if settings.anthropic_prompt_cache:
        # Mark the system prompt as cacheable. Subsequent calls hit the cache.
        system_blocks = [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
        extra["system"] = system_blocks
    else:
        extra["system"] = system

    response = await client.messages.create(
        model=settings.anthropic_model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": user}],
        **extra,  # type: ignore[arg-type]
    )
    text = "".join(block.text for block in response.content if getattr(block, "text", None))
    cached = bool(getattr(response.usage, "cache_read_input_tokens", 0))
    return GenerationResult(text=text, provider="claude", model=settings.anthropic_model, cached=cached)


# ---------------------------------------------------------------------------
# Jais (local Ollama-compatible endpoint)
# ---------------------------------------------------------------------------

async def _jais(*, system: str, user: str, max_tokens: int) -> GenerationResult:
    settings = get_settings()
    url = f"{settings.jais_base_url.rstrip('/')}/api/chat"
    payload = {
        "model": settings.jais_model,
        "stream": False,
        "options": {"num_predict": max_tokens},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    async with httpx.AsyncClient(timeout=60.0) as http:
        for attempt in range(3):
            try:
                response = await http.post(url, json=payload)
                response.raise_for_status()
                body = response.json()
                text = body.get("message", {}).get("content", "")
                return GenerationResult(text=text, provider="jais", model=settings.jais_model)
            except (httpx.HTTPError, ValueError) as exc:
                if attempt == 2:
                    raise
                logger.warning("jais.retry", attempt=attempt, error=str(exc))
                await asyncio.sleep(0.5 * (attempt + 1))
    raise RuntimeError("unreachable")
