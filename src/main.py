from src.config import settings
from src.errors import LLMSystemError
from src.utils import setup_logger


def main() -> None:
    logger = setup_logger()

    logger.info("Starting LLM system")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    logger.info(f"LLM Model: {settings.llm_model}")

    # Placeholder for future LLM pipeline
    logger.info("System initialized successfully")


if __name__ == "__main__":
    try:
        main()
    except LLMSystemError as e:
        print(f"LLM system error: {e}")
        raise
