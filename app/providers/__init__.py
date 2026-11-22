"""Seleção do provider que gera a resposta final."""
import os

from .deterministic import DeterministicProvider


def get_provider(name=None):
    key = (name or os.getenv("HERMESERENAO_PROVIDER", "deterministic")).strip().lower()
    if key == "deterministic":
        return DeterministicProvider()
    if key == "openai":
        from importlib import import_module
        return import_module(".openai_provider", __package__).OpenAIProvider()
    raise ValueError(f"provider desconhecido: {key}")
