"""Provider padrão: devolve os trechos recuperados, sem modelo."""
from .base import Provider


class DeterministicProvider(Provider):
    name = "deterministic"

    def answer(self, question, hits):
        return {
            "question": question,
            "answers": hits,
            "mode": "busca determinística (sem LLM)",
        }
