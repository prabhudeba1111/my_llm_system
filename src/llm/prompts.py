SYSTEM_PROMPT = (
    "You are a helpful, precise assistant."
    "Answer clearly and concisely."
)

def user_prompt(message: str) -> str:
    return f"user message: {message}\n"
