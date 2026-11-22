"""Adaptadores de exemplo. Não autenticam nem enviam dados para lugar algum."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Adapter:
    name: str
    capability: str
    status: str = "stub"


ADAPTERS = [
    Adapter("notion", "ler e indexar páginas"),
    Adapter("slack", "receber menções em canais"),
    Adapter("google", "agenda e documentos"),
    Adapter("github", "issues e repositórios"),
]


def describe():
    return [a.__dict__ for a in ADAPTERS]
