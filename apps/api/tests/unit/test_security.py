"""Unit tests for hashing, TOTP, and JWT round-trips."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

# Ensure HS256 in tests so we don't need RSA keys on disk.
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["JWT_PRIVATE_KEY_PATH"] = str(Path(__file__).parent / "_dummy.pem")
os.environ["JWT_PUBLIC_KEY_PATH"] = str(Path(__file__).parent / "_dummy.pem")

from helpdesk.services.security import (  # noqa: E402
    decode_token,
    generate_totp_secret,
    hash_password,
    issue_tokens,
    verify_password,
    verify_totp,
)


def test_password_hash_and_verify() -> None:
    hashed = hash_password("HorseBatteryStapleCorrect!")
    assert verify_password("HorseBatteryStapleCorrect!", hashed)
    assert not verify_password("wrong", hashed)


def test_password_verify_rejects_garbage_hash() -> None:
    assert not verify_password("anything", "not-a-real-argon2-hash")


def test_totp_round_trip() -> None:
    import pyotp

    secret = generate_totp_secret()
    code = pyotp.TOTP(secret).now()
    assert verify_totp(secret, code)
    assert not verify_totp(secret, "000000")


def test_jwt_round_trip() -> None:
    pair = issue_tokens(sub="user-1", org_id="org-1", role="agent")
    assert pair.access_token and pair.refresh_token
    decoded = decode_token(pair.access_token, expected_type="access")
    assert decoded["sub"] == "user-1"
    assert decoded["org_id"] == "org-1"
    assert decoded["role"] == "agent"


def test_jwt_wrong_type_rejected() -> None:
    pair = issue_tokens(sub="u", org_id="o", role="agent")
    with pytest.raises(ValueError, match="expected access"):
        decode_token(pair.refresh_token, expected_type="access")
