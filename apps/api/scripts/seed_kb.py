"""Seed bilingual KB articles into the database.

Markdown source lives under ``data/kb-seed/{ar,en}``. Articles paired by slug
are merged into a single :class:`KbArticle` row. Standalone articles are
loaded with a placeholder title in the missing language and flagged with a
``needs-translation`` tag for editorial follow-up.
"""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
from typing import Any

from sqlalchemy import select

from helpdesk.db import models
from helpdesk.db.session import session_scope

REPO_ROOT = Path(__file__).resolve().parents[3]
KB_ROOT = REPO_ROOT / "data" / "kb-seed"


def parse_article(path: Path) -> dict[str, Any]:
    """Parse a tiny front-matter + body markdown file."""
    text = path.read_text(encoding="utf-8")
    title = path.stem.replace("-", " ").title()
    tags: list[str] = []
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            header, body = text[3:end], text[end + 4 :].lstrip("\n")
            for line in header.strip().splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    if k.strip() == "title":
                        title = v.strip()
                    elif k.strip() == "tags":
                        tags = [t.strip() for t in v.strip().strip("[]").split(",") if t.strip()]
    return {"slug": path.stem, "title": title, "body": body.strip(), "tags": tags}


async def seed(demo: bool) -> None:
    if not KB_ROOT.exists():
        print(f"No KB seed directory at {KB_ROOT}; nothing to do.")
        return

    en_articles = {p.stem: parse_article(p) for p in (KB_ROOT / "en").glob("*.md")} if (KB_ROOT / "en").exists() else {}
    ar_articles = {p.stem: parse_article(p) for p in (KB_ROOT / "ar").glob("*.md")} if (KB_ROOT / "ar").exists() else {}
    slugs = sorted(set(en_articles) | set(ar_articles))

    async with session_scope() as session:
        org = await session.scalar(select(models.Organization).where(models.Organization.slug == "default"))
        if org is None:
            print("No default organization. Run seed_db.py first.")
            return

        loaded, skipped = 0, 0
        for slug in slugs:
            existing = await session.scalar(
                select(models.KbArticle).where(
                    models.KbArticle.org_id == org.id, models.KbArticle.slug == slug
                )
            )
            if existing is not None:
                skipped += 1
                continue
            en = en_articles.get(slug, {})
            ar = ar_articles.get(slug, {})
            tags = sorted(set(en.get("tags", []) + ar.get("tags", [])))
            if not en:
                tags.append("needs-translation-en")
            if not ar:
                tags.append("needs-translation-ar")
            article = models.KbArticle(
                org_id=org.id,
                slug=slug,
                title_en=en.get("title") or f"[EN missing] {ar.get('title', slug)}",
                title_ar=ar.get("title") or f"[AR مفقود] {en.get('title', slug)}",
                body_en=en.get("body") or "_Translation pending._",
                body_ar=ar.get("body") or "_الترجمة قيد الإعداد._",
                tags=tags or None,
                is_public=True,
            )
            session.add(article)
            loaded += 1
        print(f"KB seed: loaded={loaded} skipped={skipped} total_slugs={len(slugs)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    asyncio.run(seed(demo=args.demo))


if __name__ == "__main__":
    main()
