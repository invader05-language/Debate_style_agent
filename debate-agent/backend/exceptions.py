"""
统一错误类型定义 for Multi-AI Debate Agent.
"""


class DebateAgentError(Exception):
    """基础异常类"""
    code: str = "UNKNOWN_ERROR"
    message: str = "An unknown error occurred"
    status_code: int = 500
    retryable: bool = False

    def __init__(self, message: str = None, code: str = None,
                 status_code: int = None, retryable: bool = None):
        if message:
            self.message = message
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code
        if retryable is not None:
            self.retryable = retryable
        super().__init__(self.message)


class AgentError(DebateAgentError):
    """AI Agent 调用错误"""
    code = "AGENT_ERROR"
    message = "AI agent call failed"
    status_code = 502


class AgentTimeoutError(AgentError):
    """Agent 超时"""
    code = "AGENT_TIMEOUT"
    message = "AI agent request timed out"
    retryable = True


class AgentRateLimitError(AgentError):
    """Agent 限流"""
    code = "AGENT_RATE_LIMIT"
    message = "AI agent rate limit exceeded"
    retryable = True


class AgentAuthError(AgentError):
    """Agent 认证失败"""
    code = "AGENT_AUTH_ERROR"
    message = "AI agent authentication failed"
    retryable = False


class ExecutionError(DebateAgentError):
    """代码执行错误"""
    code = "EXECUTION_ERROR"
    message = "Code execution failed"
    status_code = 500


class SandboxError(ExecutionError):
    """沙箱执行错误"""
    code = "SANDBOX_ERROR"
    message = "Sandbox execution failed"


class ValidationError(DebateAgentError):
    """输入验证错误"""
    code = "VALIDATION_ERROR"
    message = "Input validation failed"
    status_code = 422
    retryable = False


class NotFoundError(DebateAgentError):
    """资源不存在"""
    code = "NOT_FOUND"
    message = "Resource not found"
    status_code = 404
    retryable = False


class ConflictError(DebateAgentError):
    """状态冲突"""
    code = "CONFLICT"
    message = "State conflict"
    status_code = 409
    retryable = False


class DatabaseError(DebateAgentError):
    """数据库错误"""
    code = "DATABASE_ERROR"
    message = "Database operation failed"
    status_code = 500
    retryable = True


class CacheError(DebateAgentError):
    """缓存错误"""
    code = "CACHE_ERROR"
    message = "Cache operation failed"
    status_code = 500
    retryable = True
