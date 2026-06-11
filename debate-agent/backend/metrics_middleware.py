"""
Prometheus metrics middleware for FastAPI.
"""

import time
from fastapi import Request
from backend.metrics import (
    http_requests_total,
    http_request_duration_seconds,
    http_requests_in_progress
)


async def metrics_middleware(request: Request, call_next):
    """Track HTTP request metrics."""
    method = request.method
    path = request.url.path

    # Skip metrics endpoint itself
    if path == "/metrics":
        return await call_next(request)

    http_requests_in_progress.labels(method=method, endpoint=path).inc()
    start = time.perf_counter()

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    except Exception:
        status_code = 500
        raise
    finally:
        duration = time.perf_counter() - start
        http_requests_total.labels(
            method=method, endpoint=path, status_code=str(status_code)
        ).inc()
        http_request_duration_seconds.labels(
            method=method, endpoint=path
        ).observe(duration)
        http_requests_in_progress.labels(
            method=method, endpoint=path
        ).dec()
