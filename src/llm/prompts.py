SYSTEM_PROMPT = (
    "You are a helpful, precise assistant."
    "Answer clearly and concisely."
)

def user_prompt(message: str) -> str:
    return f"user message: {message}\n"

def rag_prompt(context: list[str], question: str) -> str:
    joined_context = " ".join(context)

    return f"""
You are an assistant answering questions using ONLY the context provided. If the answer is not contained in the context, say "I don't know".

Context:
{joined_context}

Question:
{question}

Answer using ONLY the context above, do not add any external information.
    """.strip()