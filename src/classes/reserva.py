"""Período, valor e ciclo de vida de uma reserva."""

from datetime import date
from decimal import Decimal

from .hospede import Hospede
from .quarto import Quarto


class Reserva:
    """Vincule um hóspede a um quarto durante uma estadia."""

    CONFIRMADA = "Confirmada"
    EM_HOSPEDAGEM = "Em hospedagem"
    FINALIZADA = "Finalizada"
    CANCELADA = "Cancelada"
    _proximo_codigo = 1

    def __init__(
        self,
        hospede: Hospede,
        quarto: Quarto,
        entrada: date,
        saida: date,
        quantidade_pessoas: int,
    ) -> None:
        """Crie uma reserva confirmada para um período e ocupação válidos."""
        self.validar_periodo(entrada, saida)
        if not quarto.ativo:
            raise ValueError("O quarto está inativo.")
        if not 1 <= quantidade_pessoas <= quarto.capacidade:
            raise ValueError(f"Informe de 1 a {quarto.capacidade} pessoa(s) para esse quarto.")

        self._codigo = self.gerar_codigo()
        self._hospede = hospede
        self._quarto = quarto
        self._entrada = entrada
        self._saida = saida
        self._quantidade_pessoas = quantidade_pessoas
        self._status = self.CONFIRMADA

    @classmethod
    def gerar_codigo(cls) -> str:
        """Gere o próximo código de reserva usando o contador da classe."""
        codigo = f"R{cls._proximo_codigo:03d}"
        cls._proximo_codigo += 1
        return codigo

    @staticmethod
    def validar_periodo(entrada: date, saida: date) -> None:
        """Exija uma data de saída posterior à data de entrada."""
        if saida <= entrada:
            raise ValueError("A data de saída deve ser posterior à data de entrada.")

    @property
    def codigo(self) -> str:
        """Retorne o identificador da reserva."""
        return self._codigo

    @property
    def hospede(self) -> Hospede:
        """Retorne o hóspede titular da reserva."""
        return self._hospede

    @property
    def quarto(self) -> Quarto:
        """Retorne o quarto vinculado à reserva."""
        return self._quarto

    @property
    def entrada(self) -> date:
        """Retorne a primeira data da estadia."""
        return self._entrada

    @property
    def saida(self) -> date:
        """Retorne a data de saída da estadia."""
        return self._saida

    @property
    def quantidade_pessoas(self) -> int:
        """Retorne o número de pessoas informado na reserva."""
        return self._quantidade_pessoas

    @property
    def status(self) -> str:
        """Retorne o estado atual da reserva."""
        return self._status

    @property
    def diarias(self) -> int:
        """Calcule o número de noites entre entrada e saída."""
        return (self.saida - self.entrada).days

    @property
    def valor_total(self) -> Decimal:
        """Calcule o total pela regra da categoria do quarto reservado."""
        return self.quarto.calcular_valor_estadia(self.diarias)

    def ocupa_periodo(self, entrada: date, saida: date) -> bool:
        """Indique se esta reserva bloqueia o quarto no intervalo informado."""
        return self.status != self.CANCELADA and entrada < self.saida and self.entrada < saida

    def ocupa_data(self, data: date) -> bool:
        """Indique se a data pertence ao período ocupado pela reserva."""
        return self.status != self.CANCELADA and self.entrada <= data < self.saida

    def checkin(self) -> None:
        """Passe de confirmada para em hospedagem."""
        if self.status != self.CONFIRMADA:
            raise ValueError("O check-in exige uma reserva confirmada.")
        self._status = self.EM_HOSPEDAGEM

    def checkout(self) -> None:
        """Finalize uma reserva com check-in registrado."""
        if self.status != self.EM_HOSPEDAGEM:
            raise ValueError("O check-out exige um check-in já realizado.")
        self._status = self.FINALIZADA

    def cancelar(self) -> None:
        """Cancele uma reserva confirmada antes do check-in."""
        if self.status != self.CONFIRMADA:
            raise ValueError("Apenas reservas confirmadas podem ser canceladas.")
        self._status = self.CANCELADA

    def resumo(self) -> str:
        """Retorne identificação, período e estado da reserva."""
        return (
            f"{self.codigo} | {self.hospede.nome} | quarto {self.quarto.numero} "
            f"({self.quarto.TIPO}) | {self.entrada:%d/%m/%Y} a {self.saida:%d/%m/%Y} "
            f"| {self.quantidade_pessoas} pessoa(s) | {self.status}"
        )
