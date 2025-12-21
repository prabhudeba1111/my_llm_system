class LLMSystemError(Exception):
    """Base exception for all LLM system errors."""


class ConfigurationError(LLMSystemError):
    """Raised when configuration is invalid or missing."""


class LLMExecutionError(LLMSystemError):
    """Raised when an LLM call or pipeline fails."""
