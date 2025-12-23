import asyncio

from src.llm.async_client import get_async_llm_client
from src.llm.models import LLMRequest


async def main():
    llm = get_async_llm_client()

    objects = ["chair", "table", "bed", "sofa", "carpet", "curtains"]

    requests = [
        LLMRequest(prompt=f"Tell me about {i} in 10 words") for i in objects
    ]

    results = await asyncio.gather(
        *(llm.generate(request) for request in requests)
    )

    for i, result in enumerate(results):
        print(f"{i} -> {result}")

if __name__ == "__main__":
    asyncio.run(main())