"""OpenTelemetry tracing setup. No-op if OTLP endpoint is unset."""

from __future__ import annotations

import structlog

from helpdesk.config import Settings

logger = structlog.get_logger(__name__)


def configure_tracing(settings: Settings) -> None:
    if not settings.otel_exporter_otlp_endpoint:
        logger.info("tracing.disabled")
        return
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor

        provider = TracerProvider(
            resource=Resource.create({"service.name": settings.otel_service_name})
        )
        provider.add_span_processor(
            BatchSpanProcessor(
                OTLPSpanExporter(endpoint=f"{settings.otel_exporter_otlp_endpoint}/v1/traces")
            )
        )
        trace.set_tracer_provider(provider)
        logger.info("tracing.enabled", endpoint=settings.otel_exporter_otlp_endpoint)
    except Exception as exc:  # noqa: BLE001
        logger.warning("tracing.setup_failed", error=str(exc))
