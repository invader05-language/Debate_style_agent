"""
Prometheus metrics for Multi-AI Debate Agent.
Exposes /metrics endpoint for monitoring.
"""

import time
import logging
from typing import Optional
from prometheus_client import (
    Counter, Histogram, Gauge, Info, generate_latest, CONTENT_TYPE_LATEST
)

logger = logging.getLogger(__name__)

# ── Application Info ──────────────────────────────────────────────

app_info = Info("debate_agent", "Multi-AI Debate Agent application info")
app_info.info({
    "version": "0.4.0",
    "component": "backend"
})

# ── HTTP Metrics ──────────────────────────────────────────────────

http_requests_total = Counter(
    "debate_agent_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"]
)

http_request_duration_seconds = Histogram(
    "debate_agent_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

http_requests_in_progress = Gauge(
    "debate_agent_http_requests_in_progress",
    "Number of HTTP requests currently in progress",
    ["method", "endpoint"]
)

# ── Debate Metrics ────────────────────────────────────────────────

debates_total = Counter(
    "debate_agent_debates_total",
    "Total debates created",
    ["status"]
)

debate_duration_seconds = Histogram(
    "debate_agent_debate_duration_seconds",
    "Debate execution duration in seconds",
    buckets=[10, 30, 60, 120, 300, 600, 900]
)

debate_rounds_total = Counter(
    "debate_agent_debate_rounds_total",
    "Total debate rounds executed"
)

debate_active = Gauge(
    "debate_agent_debates_active",
    "Number of currently active debates"
)

# ── AI Agent Metrics ──────────────────────────────────────────────

agent_requests_total = Counter(
    "debate_agent_ai_requests_total",
    "Total AI agent requests",
    ["agent", "role", "status"]
)

agent_request_duration_seconds = Histogram(
    "debate_agent_ai_request_duration_seconds",
    "AI agent request duration in seconds",
    ["agent", "role"],
    buckets=[0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
)

agent_fallback_total = Counter(
    "debate_agent_ai_fallback_total",
    "Total agent fallback events",
    ["from_agent", "to_agent", "reason"]
)

# ── Memory Metrics ────────────────────────────────────────────────

memory_search_total = Counter(
    "debate_agent_memory_search_total",
    "Total memory searches",
    ["method", "status"]
)

memory_search_duration_seconds = Histogram(
    "debate_agent_memory_search_duration_seconds",
    "Memory search duration in seconds",
    ["method"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0]
)

memory_embeddings_total = Counter(
    "debate_agent_memory_embeddings_total",
    "Total embeddings generated",
    ["status"]
)

memory_count = Gauge(
    "debate_agent_memory_count",
    "Total memories stored"
)

# ── Execution Metrics ─────────────────────────────────────────────

executions_total = Counter(
    "debate_agent_executions_total",
    "Total code executions",
    ["language", "status"]
)

execution_duration_seconds = Histogram(
    "debate_agent_execution_duration_seconds",
    "Code execution duration in seconds",
    ["language"],
    buckets=[1.0, 5.0, 10.0, 30.0, 60.0, 120.0]
)

execution_retries_total = Counter(
    "debate_agent_execution_retries_total",
    "Total execution retry attempts"
)

# ── Cache Metrics ─────────────────────────────────────────────────

cache_operations_total = Counter(
    "debate_agent_cache_operations_total",
    "Total cache operations",
    ["operation", "result"]
)

cache_hit_ratio = Gauge(
    "debate_agent_cache_hit_ratio",
    "Cache hit ratio (rolling 5min)"
)

# ── Rate Limiter Metrics ─────────────────────────────────────────

rate_limit_hits_total = Counter(
    "debate_agent_rate_limit_hits_total",
    "Total rate limit rejections",
    ["endpoint"]
)

rate_limit_remaining = Gauge(
    "debate_agent_rate_limit_remaining",
    "Remaining rate limit capacity",
    ["client_ip", "endpoint"]
)

# ── WebSocket Metrics ─────────────────────────────────────────────

ws_connections_active = Gauge(
    "debate_agent_ws_connections_active",
    "Active WebSocket connections",
    ["debate_id"]
)

ws_messages_total = Counter(
    "debate_agent_ws_messages_total",
    "Total WebSocket messages sent",
    ["type"]
)


# ── Helper Context Manager ────────────────────────────────────────

class TimerContext:
    """Context manager for timing operations."""

    def __init__(self, histogram: Histogram, labels: dict):
        self.histogram = histogram.labels(**labels)
        self.start: Optional[float] = None

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        if self.start:
            duration = time.perf_counter() - self.start
            self.histogram.observe(duration)


def track_request(method: str, endpoint: str):
    """Track an HTTP request."""
    http_requests_in_progress.labels(method=method, endpoint=endpoint).inc()
    start = time.perf_counter()

    def finish(status_code: int):
        duration = time.perf_counter() - start
        http_requests_total.labels(
            method=method, endpoint=endpoint, status_code=str(status_code)
        ).inc()
        http_request_duration_seconds.labels(
            method=method, endpoint=endpoint
        ).observe(duration)
        http_requests_in_progress.labels(
            method=method, endpoint=endpoint
        ).dec()

    return finish
