class LLMSystemError(Exception):
    """Base exception for all LLM system errors."""
    retryable: bool = False
    exit_code: int = 2


class CallerError(LLMSystemError):
    retryable = False
    exit_code = 1


class TransientError(LLMSystemError):
    retryable = True
    exit_code = 1


class FatalError(LLMSystemError):
    retryable = False
    exit_code = 2