"""CSV import / export of tickets and KB articles.

Used by the admin UI and by operators migrating from Zendesk / Freshdesk.
We deliberately stick to UTF-8 with BOM so Excel on Windows opens
Arabic columns correctly.
"""

from __future__ import annotations

import csv
import io
from collections.abc import Iterable
from typing import Any


def export_rows(rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> bytes:
    buf = io.StringIO()
    buf.write("﻿")  # UTF-8 BOM for Excel on Windows
    writer = csv.DictWriter(buf, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return buf.getvalue().encode("utf-8")


def import_rows(blob: bytes) -> list[dict[str, str]]:
    text = blob.decode("utf-8-sig")  # tolerate Excel BOM
    return list(csv.DictReader(io.StringIO(text)))
