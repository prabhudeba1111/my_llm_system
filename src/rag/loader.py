from pathlib import Path


def load_text_documents(directory: str) -> list[str]:
    texts = []

    for path in Path(directory).glob("*.txt"):
        texts.append(path.read_text(encoding="utf-8"))

    return texts