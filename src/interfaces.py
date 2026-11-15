"""Contratos usados para exibir objetos do sistema."""

from typing import Protocol


class Resumivel(Protocol):
    """Qualquer objeto capaz de fornecer um resumo em texto."""

    def resumo(self) -> str:
        """Retorne uma descrição curta do objeto."""
        ...
