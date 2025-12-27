from src.config import settings, validate_settings, resolved_config
from src.errors import LLMSystemError
from src.llm.client import get_llm_client
from src.llm.models import LLMFailure, LLMRequest
from src.llm.prompts import user_prompt
from src.utils import setup_logger


def run() -> int:
    logger = setup_logger("data/log_file.logs")
    validate_settings(settings)
    logger.debug(f"Resolved config: {resolved_config(settings)}")
    try:
        logger.info("Starting LLM system")

        logger.info("System initialized successfully")

        client = get_llm_client()

        request = LLMRequest(
            prompt=user_prompt("How to drink water?"),
        )

        result = client.generate(request)

        if isinstance(result, LLMFailure):
            logger.error(f"LLM failure: {result.reason}")
            return result.error_type.exit_code

        logger.info(f"LLM output: {result.text}")
        return 0

    except LLMSystemError as e:
        logger.critical(str(e))
        return e.exit_code

    except Exception:
        logger.exception("Unexpected failure")
        return 2


if __name__ == "__main__":
    raise SystemExit(run())
