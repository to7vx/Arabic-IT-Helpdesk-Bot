"""Bilingual error envelope. Every API error returns the same shape."""

from __future__ import annotations

from typing import Any

import structlog
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

logger = structlog.get_logger(__name__)


class DomainError(Exception):
    """Base class for application errors with bilingual messages."""

    status_code: int = 400
    code: str = "domain_error"
    message_en: str = "Request could not be completed."
    message_ar: str = "تعذّر إتمام الطلب."

    def __init__(self, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(self.message_en)
        self.details = details or {}


class NotFoundError(DomainError):
    status_code = 404
    code = "not_found"
    message_en = "Resource not found."
    message_ar = "المورد غير موجود."


class ForbiddenError(DomainError):
    status_code = 403
    code = "forbidden"
    message_en = "You do not have permission for this action."
    message_ar = "ليس لديك الصلاحية لتنفيذ هذا الإجراء."


class ConflictError(DomainError):
    status_code = 409
    code = "conflict"
    message_en = "Conflict with the current state."
    message_ar = "تعارض مع الحالة الحالية."


def _envelope(
    *,
    status: int,
    code: str,
    message_en: str,
    message_ar: str,
    details: dict[str, Any] | None = None,
) -> JSONResponse:
    body: dict[str, Any] = {
        "error": {"code": code, "message_en": message_en, "message_ar": message_ar}
    }
    if details:
        body["error"]["details"] = details
    return JSONResponse(status_code=status, content=body)


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def _domain(_: Request, exc: DomainError) -> JSONResponse:
        return _envelope(
            status=exc.status_code,
            code=exc.code,
            message_en=exc.message_en,
            message_ar=exc.message_ar,
            details=exc.details or None,
        )

    @app.exception_handler(HTTPException)
    async def _http(_: Request, exc: HTTPException) -> JSONResponse:
        return _envelope(
            status=exc.status_code,
            code=f"http_{exc.status_code}",
            message_en=str(exc.detail),
            message_ar=str(exc.detail),
        )

    @app.exception_handler(RequestValidationError)
    async def _validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        return _envelope(
            status=422,
            code="validation_error",
            message_en="Validation failed.",
            message_ar="فشل التحقق من المدخلات.",
            details={"errors": exc.errors()},
        )

    @app.exception_handler(Exception)
    async def _unhandled(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("api.unhandled_error", exc_type=type(exc).__name__)
        return _envelope(
            status=500,
            code="internal_error",
            message_en="An internal error occurred. The team has been notified.",
            message_ar="حدث خطأ داخلي. تم إبلاغ الفريق المعني.",
        )
