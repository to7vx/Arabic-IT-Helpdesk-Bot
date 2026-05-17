"""Arabic NLP pipeline.

Importing this package is cheap; heavy model loading is deferred until the
first call. Every public function gracefully degrades when optional
dependencies (torch, sentence-transformers, camel-tools) are missing, so
the API stays usable in lightweight deployments where AI is disabled.
"""

PREPROCESSING_VERSION = "v1"
"""Bump whenever preprocessing changes; recorded on every ai_suggestions row."""

MODEL_VERSION = "v0"
"""Logical version of the bundled classifier weights. ``v0`` means
"untrained baseline" — heuristics + pretrained zero-shot."""
