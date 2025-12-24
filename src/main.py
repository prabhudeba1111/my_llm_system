from src.config import settings
from src.llm.client import get_llm_client
from src.llm.models import LLMFailure, LLMRequest
from src.llm.prompts import rag_prompt
from src.rag.pipeline import RAGPipeline
from src.utils import setup_logger


def run() -> int:
    logger = setup_logger()

    try:
        logger.debug("Starting LLM system")
        logger.debug(f"Environment: {settings.environment}")
        logger.debug(f"LLM Provider: {settings.llm_provider}")
        logger.debug(f"LLM Model: {settings.llm_model}")
        logger.debug(f"LLM Mode: {settings.llm_mode}")

        # Placeholder for future LLM pipeline
        logger.info("System initialized successfully")

        user_question = "What is python?"
        rag = RAGPipeline(docs_path="data")
        context = rag.retrieve(user_question)
        request = LLMRequest(prompt=rag_prompt(context, user_question))

        client = get_llm_client()

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
