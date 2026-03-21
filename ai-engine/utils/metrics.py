"""Métricas Prometheus para el motor de IA."""

from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    Info,
    generate_latest,
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    REGISTRY,
)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time

# --- Contadores ---
http_requests_total = Counter(
    "ai_http_requests_total",
    "Total de peticiones HTTP al AI engine",
    ["method", "endpoint", "status_code"],
)

ws_connections_total = Counter(
    "ai_ws_connections_total",
    "Total de conexiones WebSocket al AI engine",
)

robot_commands_total = Counter(
    "ai_robot_commands_total",
    "Total de comandos enviados a robots",
    ["command_type"],
)

decisions_total = Counter(
    "ai_decisions_total",
    "Total de decisiones tomadas por el motor de IA",
    ["decision_type"],
)

# --- Histogramas ---
http_request_duration = Histogram(
    "ai_http_request_duration_seconds",
    "Duración de peticiones HTTP en el AI engine",
    ["method", "endpoint"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
)

neural_inference_duration = Histogram(
    "ai_neural_inference_duration_seconds",
    "Duración de inferencias neuronales",
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
)

# --- Gauges ---
ws_active_connections = Gauge(
    "ai_ws_active_connections",
    "Conexiones WebSocket activas en el AI engine",
)

active_robots = Gauge(
    "ai_active_robots",
    "Robots activos gestionados por el motor de IA",
)

system_health = Gauge(
    "ai_system_health",
    "Salud del sistema de IA (0-100)",
)

cpu_usage = Gauge(
    "ai_cpu_usage_percent",
    "Uso de CPU del motor de IA",
)

memory_usage = Gauge(
    "ai_memory_usage_percent",
    "Uso de memoria del motor de IA",
)

# --- Info ---
ai_engine_info = Info(
    "ai_engine",
    "Información del motor de IA",
)
ai_engine_info.info({"version": "1.0.0", "framework": "fastapi"})


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware para recopilar métricas HTTP automáticamente."""

    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/metrics":
            return await call_next(request)

        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        endpoint = request.url.path
        method = request.method
        status = str(response.status_code)

        http_requests_total.labels(method=method, endpoint=endpoint, status_code=status).inc()
        http_request_duration.labels(method=method, endpoint=endpoint).observe(duration)

        return response


def metrics_endpoint():
    """Genera respuesta con métricas Prometheus."""
    return Response(
        content=generate_latest(REGISTRY),
        media_type=CONTENT_TYPE_LATEST,
    )
