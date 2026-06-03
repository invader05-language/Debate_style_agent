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

from exceptions import DebateAgentError

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
    """滑动窗口限流器"""

    def __init__(self, requests_per_minute: int = 60):
        self.rpm = requests_per_minute
        self.requests: Dict[str, List[float]] = defaultdict(list)

    async def check(self, client_ip: str) -> bool:
        """检查是否超过限流。返回 True 表示允许，False 表示限流。"""
        now = time.time()
        window_start = now - 60

        # 清理过期记录
        self.requests[client_ip] = [
            t for t in self.requests[client_ip] if t > window_start
        ]

        if len(self.requests[client_ip]) >= self.rpm:
            return False

        self.requests[client_ip].append(now)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=60)


async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware."""
    client_ip = request.client.host if request.client else "unknown"

    if not await rate_limiter.check(client_ip):
        request_id = getattr(request.state, "request_id", "unknown")
        logger.warning(f"Rate limit exceeded for {client_ip} [request_id={request_id}]")
        return JSONResponse(
            status_code=429,
            content={
                "error": {
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": "Too many requests. Please try again later.",
                    "retryable": True,
                    "request_id": request_id,
                }
            }
        )

    return await call_next(request)
