"""Async embedding (re)indexing for KB articles."""

from __future__ import annotations

from helpdesk.workers.celery_app import app


@app.task(name="helpdesk.workers.tasks.embedding.reindex_kb")
def reindex_kb(_org_id: str) -> dict[str, int]:
    # The real implementation lives alongside nlp.embeddings.model. This
    # task is the queue entry point; the workhorse function lives in
    # helpdesk.nlp.retrieval.indexer and lands with Phase 7b.
    return {"reindexed": 0}
