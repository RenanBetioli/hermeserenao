"""Contrato comum de provider."""


class Provider:
    name = "base"

    def answer(self, question, hits):
        """Recebe a pergunta e os trechos recuperados; devolve o payload da API."""
        raise NotImplementedError
