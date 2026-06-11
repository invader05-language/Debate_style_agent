"""
FastAPI 全局错误处理中间件 + API 限流.
"""

import uuid
import time
import logging
from collections import defaultdict
from typing import Dict, List

from fastapi import Request
from fastapi.responses import JSONResponse

from backend.exceptions import DebateAgentError

logger = logging.getLogger(__name__)


# ── Request ID Middleware ──────────────────────────────────────────

async def request_id_middleware(request: Request, call_next):
    """Inject a unique request ID into every request/response."""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# ── Error Handlers ─────────────────────────────────────────────────

async def debate_agent_error_handler(request: Request, exc: DebateAgentError):
    """Handle custom business exceptions."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(
        f"Business error: {exc.code} - {exc.message} "
        f"[request_id={request_id}]"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "retryable": exc.retryable,
                "request_id": request_id,
            }
        }
    )


async def generic_error_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.exception(f"Unhandled error: {exc} [request_id={request_id}]")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "retryable": False,
                "request_id": request_id,
            }
        }
    )


# ── Rate Limiter ───────────────────────────────────────────────────

class RateLimiter:
    """
    Sliding window rate limiter with configurable limits per endpoint.

    Supports:
    - Global default limit (requests_per_minute)
    - Per-endpoint overrides (endpoint_limits)
    - Automatic cleanup of expired entries to prevent memory leaks
    """

    def __init__(self, requests_per_minute: int = 60,
                 endpoint_limits: Dict[str, int] = None,
                 cleanup_interval: int = 300):
        self.default_rpm = requests_per_minute
        self.endpoint_limits = endpoint_limits or {}
        self.cleanup_interval = cleanup_interval
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self._last_cleanup = time.time()

    def _get_limit(self, endpoint: str = None) -> int:
        """Get rate limit for an endpoint."""
        if endpoint and endpoint in self.endpoint_limits:
            return self.endpoint_limits[endpoint]
        return self.default_rpm

    def _cleanup_expired(self) -> None:
        """Remove expired entries to prevent memory leaks."""
        now = time.time()
        if now - self._last_cleanup < self.cleanup_interval:
            return

        window_start = now - 60
        expired_keys = []
        for key, timestamps in self.requests.items():
            self.requests[key] = [t for t in timestamps if t > window_start]
            if not self.requests[key]:
                expired_keys.append(key)

        for key in expired_keys:
            del self.requests[key]

        self._last_cleanup = now

    async def check(self, client_ip: str, endpoint: str = None) -> bool:
        """
        Check if request is within rate limit.

        Args:
            client_ip: Client IP address
            endpoint: Optional endpoint path for per-endpoint limits

        Returns:
            True if allowed, False if rate limited
        """
        self._cleanup_expired()

        now = time.time()
        window_start = now - 60
        key = f"{client_ip}:{endpoint}" if endpoint else client_ip
        limit = self._get_limit(endpoint)

        # Clean expired entries for this key
        self.requests[key] = [t for t in self.requests[key] if t > window_start]

        if len(self.requests[key]) >= limit:
            return False

        self.requests[key].append(now)
        return True

    def get_remaining(self, client_ip: str, endpoint: str = None) -> int:
        """Get remaining requests in current window."""
        key = f"{client_ip}:{endpoint}" if endpoint else client_ip
        limit = self._get_limit(endpoint)
        now = time.time()
        window_start = now - 60
        current = len([t for t in self.requests[key] if t > window_start])
        return max(0, limit - current)


# Global rate limiter instance with per-endpoint overrides
rate_limiter = RateLimiter(
    requests_per_minute=60,
    endpoint_limits={
        "/api/debates": 30,          # Debate creation is expensive
        "/api/debates/*/execute": 10, # Execution is very expensive
        "/api/memories/search": 60,   # Search is lightweight
    }
)


async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware with remaining-requests header."""
    client_ip = request.client.host if request.client else "unknown"
    endpoint = request.url.path

    if not await rate_limiter.check(client_ip, endpoint):
        request_id = getattr(request.state, "request_id", "unknown")
        logger.warning(f"Rate limit exceeded for {client_ip} on {endpoint} [request_id={request_id}]")
        return JSONResponse(
            status_code=429,
            content={
                "error": {
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": "Too many requests. Please try again later.",
                    "retryable": True,
                    "request_id": request_id,
                }
            },
            headers={"Retry-After": "60"}
        )

    response = await call_next(request)
    # Add rate limit headers to successful responses
    remaining = rate_limiter.get_remaining(client_ip, endpoint)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Limit"] = str(rate_limiter._get_limit(endpoint))
    return response
