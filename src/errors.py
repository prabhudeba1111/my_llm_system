class LLMSystemError(Exception):
    """Base exception for all LLM system errors."""
    code = "ERR_UNKNOWN"
    retryable: bool = False
    exit_code: int = 2

    def __init__(self, user_message: str, internal_message: str | None = None):
        self.user_message = user_message
        self.internal_message = internal_message or user_message
        super().__init__(self.internal_message)

    def __str__(self) -> str:
        return f"{self.code}: {self.internal_message}"


class CallerError(LLMSystemError):
    code = "ERR_CALLER"
    retryable = False
    exit_code = 1


class TransientError(LLMSystemError):
    code = "ERR_TRANSIENT"
    retryable = True
    exit_code = 1


class FatalError(LLMSystemError):
    code = "ERR_FATAL"
    retryable = False
    exit_code = 2


def is_retryable(error_type: type[LLMSystemError]) -> bool:
    """
    Determine whether an error type should trigger a retry.
    """
    return error_type.retryable
