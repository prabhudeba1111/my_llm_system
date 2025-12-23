import os

import pytest

from src.llm.client import get_llm_client
from src.llm.local import LocalLLM
from src.llm.mock import MockLLM


def test_factory_mock(monkeypatch):
    monkeypatch.setenv("LLM_MODE", "mock")

    client = get_llm_client()
    assert isinstance(client, MockLLM)


def test_factory_local(monkeypatch):
    monkeypatch.setenv("LLM_MODE", "local")

    client = get_llm_client()
    assert isinstance(client, LocalLLM)


def test_factory_invalid(monkeypatch):
    monkeypatch.setenv("LLM_MODE", "invalid")

    with pytest.raises(ValueError):
        get_llm_client()