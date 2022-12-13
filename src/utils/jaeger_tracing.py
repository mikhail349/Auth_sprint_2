from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from src.core.config import jaeger_settings


def configure_tracer() -> None:
    """Конфигурация трассировки."""
    if jaeger_settings.enable_tracing:
        trace.set_tracer_provider(
            TracerProvider(
                resource=Resource.create({SERVICE_NAME: "auth_service"})
            )
        )
        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(
                JaegerExporter(
                    agent_host_name=jaeger_settings.jaeger_host,
                    agent_port=jaeger_settings.jaeger_port,
                )
            )
        )
