from src.config import settings
from src.errors import LLMSystemError
from src.llm.client import get_llm_client
from src.llm.models import LLMFailure, LLMRequest
from src.llm.prompts import user_prompt
from src.utils import setup_logger


def run() -> int:
    logger = setup_logger()

    try:
        logger.info("Starting LLM system")
        logger.info(f"Environment: {settings.environment}")
        logger.info(f"LLM Provider: {settings.llm_provider}")
        logger.info(f"LLM Model: {settings.llm_model}")

        # Placeholder for future LLM pipeline
        logger.info("System initialized successfully")

        client = get_llm_client()

        request = LLMRequest(
            prompt=user_prompt("How to drink water?"),
        )

        result = client.generate(request)

        if isinstance(result, LLMFailure):
            logger.error(
                f"LLM failure: {result.reason}, retryable = {result.retryable}"
            )
            return 1

        logger.info(f"LLM output: {result.text}")
        return 0

    except Exception:
        logger.exception("Unexpected failure")
        return 2


if __name__ == "__main__":
    raise SystemExit(run())
