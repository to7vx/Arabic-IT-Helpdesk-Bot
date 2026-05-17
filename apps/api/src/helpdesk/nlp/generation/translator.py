"""Bilingual ar↔en translation through the LLM client."""

from __future__ import annotations

from helpdesk.nlp.generation.llm_client import generate
from helpdesk.nlp.generation.prompts import TRANSLATE_SYSTEM
from helpdesk.nlp.preprocessing.language_detect import detect


async def translate(text: str, target_lang: str) -> dict[str, str]:
    source_lang = detect(text).primary
    if source_lang == target_lang:
        return {"text": text, "source_lang": source_lang, "target_lang": target_lang}
    result = await generate(
        system=TRANSLATE_SYSTEM.format(target_lang="Arabic" if target_lang == "ar" else "English"),
        user=text,
        max_tokens=600,
    )
    return {"text": result.text, "source_lang": source_lang, "target_lang": target_lang}
