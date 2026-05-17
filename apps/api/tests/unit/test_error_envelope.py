"""Verify the bilingual error envelope shape."""

from __future__ import annotations

import pytest
from fastapi import FastAPI

from helpdesk.middleware.error_handler import (
    ConflictError,
    DomainError,
    ForbiddenError,
    NotFoundError,
    install_error_handlers,
)


@pytest.mark.parametrize(
    "exc,status,code",
    [
        (NotFoundError(), 404, "not_found"),
        (ForbiddenError(), 403, "forbidden"),
        (ConflictError(), 409, "conflict"),
    ],
)
def test_domain_error_status(exc: DomainError, status: int, code: str) -> None:
    assert exc.status_code == status
    assert exc.code == code
    assert exc.message_en
    assert exc.message_ar


def test_install_error_handlers_registers_all() -> None:
    app = FastAPI()
    install_error_handlers(app)
    # Sanity: at least the three handlers above.
    assert any(DomainError is h for h in app.exception_handlers)
