"""Tests for webhook signing, CSV round-trip, and Slack signature verification."""

from __future__ import annotations

import hashlib
import hmac
import time
from unittest.mock import patch

from helpdesk.integrations.csv_io import export_rows, import_rows
from helpdesk.integrations.slack.handler import verify_signature
from helpdesk.integrations.webhook_dispatcher import sign


def test_webhook_signature_format() -> None:
    sig = sign(b'{"a":1}', "secret")
    assert sig.startswith("sha256=")
    expected = hmac.new(b"secret", b'{"a":1}', hashlib.sha256).hexdigest()
    assert sig == f"sha256={expected}"


def test_csv_roundtrip_preserves_arabic() -> None:
    rows = [
        {"id": "1", "title_ar": "الطابعة معطّلة", "title_en": "Printer broken"},
        {"id": "2", "title_ar": "خطأ VPN 720", "title_en": "VPN error 720"},
    ]
    blob = export_rows(rows, ["id", "title_ar", "title_en"])
    parsed = import_rows(blob)
    assert parsed[0]["title_ar"] == "الطابعة معطّلة"
    assert parsed[1]["title_en"] == "VPN error 720"


def test_slack_signature_verifies_valid_request() -> None:
    body = b"command=/ticket&text=new%20VPN%20down"
    ts = str(int(time.time()))
    with patch("helpdesk.integrations.slack.handler.get_settings") as get_settings:
        get_settings.return_value.slack_signing_secret.get_secret_value.return_value = "shh"
        base = f"v0:{ts}:".encode() + body
        sig = "v0=" + hmac.new(b"shh", base, hashlib.sha256).hexdigest()
        assert verify_signature(body=body, timestamp=ts, signature=sig)


def test_slack_signature_rejects_stale_timestamp() -> None:
    with patch("helpdesk.integrations.slack.handler.get_settings") as get_settings:
        get_settings.return_value.slack_signing_secret.get_secret_value.return_value = "shh"
        assert not verify_signature(body=b"x", timestamp="0", signature="anything")
