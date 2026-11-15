"""Hierarquia de quartos, preços e serviços inclusos."""

from abc import ABC, abstractmethod
from decimal import ROUND_HALF_UP, Decimal

Preco = Decimal | float | int


class Quarto(ABC):
    """Defina os dados e o contrato das categorias de quarto."""

    TIPO = "Quarto"
    CENTAVO = Decimal("0.01")
    PRECO_MAXIMO = Decimal("999999999999.99")

    def __init__(
        self, numero: str, capacidade: int, valor_diaria: Preco, ativo: bool = True
    ) -> None:
        """Crie um quarto com identificação, capacidade e preço-base."""
        if not numero.strip():
            raise ValueError("Informe o número do quarto.")
        if capacidade < 1:
            raise ValueError("A capacidade do quarto deve ser maior que zero.")

        self._numero = numero.strip().upper()
        self._capacidade = capacidade
        self.valor_diaria = valor_diaria
        self.ativo = ativo

    @property
    def numero(self) -> str:
        """Retorne o número do quarto."""
        return self._numero

    @property
    def capacidade(self) -> int:
        """Retorne o número máximo de pessoas no quarto."""
        return self._capacidade

    @property
    def valor_diaria(self) -> Decimal:
        """Retorne o valor-base de uma diária."""
        return self._valor_diaria

    @valor_diaria.setter
    def valor_diaria(self, valor: Preco) -> None:
        """Atualize a diária com um preço positivo em centavos."""
        diaria = self._normalizar_preco(valor)
        if diaria == 0:
            raise ValueError("O valor da diária deve ser de pelo menos R$ 0,01.")
        self._valor_diaria = diaria

    @staticmethod
    def _normalizar_preco(valor: Preco) -> Decimal:
        preco = Decimal(str(valor))
        if not preco.is_finite() or not 0 <= preco <= Quarto.PRECO_MAXIMO:
            raise ValueError("Informe um preço válido entre R$ 0,00 e R$ 999.999.999.999,99.")
        return preco.quantize(Quarto.CENTAVO, rounding=ROUND_HALF_UP)

    def _valor_base(self, diarias: int) -> Decimal:
        if diarias < 1:
            raise ValueError("A estadia deve ter pelo menos uma diária.")
        return self.valor_diaria * diarias

    @abstractmethod
    def calcular_valor_estadia(self, diarias: int) -> Decimal:
        """Calcule o valor total conforme a categoria do quarto."""

    @abstractmethod
    def servicos_inclusos(self) -> tuple[str, ...]:
        """Retorne os serviços incluídos na categoria do quarto."""


class QuartoStandard(Quarto):
    """Quarto com Wi-Fi e preço fixo por diária."""

    TIPO = "Standard"

    def calcular_valor_estadia(self, diarias: int) -> Decimal:
        """Multiplique o valor da diária pelo número de noites."""
        return self._valor_base(diarias)

    def servicos_inclusos(self) -> tuple[str, ...]:
        """Retorne os serviços do quarto Standard."""
        return ("Wi-Fi",)


class QuartoLuxo(Quarto):
    """Quarto com café da manhã e desconto em estadias longas."""

    TIPO = "Luxo"
    DESCONTO_5_DIAS = Decimal("0.10")

    def calcular_valor_estadia(self, diarias: int) -> Decimal:
        """Aplique 10% de desconto ao total a partir de cinco diárias."""
        total = self._valor_base(diarias)
        if diarias >= 5:
            total *= 1 - self.DESCONTO_5_DIAS
        return total.quantize(self.CENTAVO, rounding=ROUND_HALF_UP)

    def servicos_inclusos(self) -> tuple[str, ...]:
        """Retorne os serviços do quarto Luxo."""
        return ("Wi-Fi", "café da manhã")


class QuartoSuite(Quarto):
    """Quarto com café da manhã, roupão e taxa de serviço por diária."""

    TIPO = "Suíte"

    def __init__(
        self,
        numero: str,
        capacidade: int,
        valor_diaria: Preco,
        taxa_servico: Preco,
        ativo: bool = True,
    ) -> None:
        """Inicialize os dados comuns e guarde a taxa de serviço."""
        super().__init__(numero, capacidade, valor_diaria, ativo)
        self._taxa_servico = self._normalizar_preco(taxa_servico)

    def calcular_valor_estadia(self, diarias: int) -> Decimal:
        """Some a taxa de serviço para cada diária da estadia."""
        return self._valor_base(diarias) + self._taxa_servico * diarias

    def servicos_inclusos(self) -> tuple[str, ...]:
        """Retorne os serviços da suíte."""
        return ("Wi-Fi", "café da manhã", "roupão")
