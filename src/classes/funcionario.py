"""Funcionários da recepção e operações de atendimento."""

from .reserva import Reserva


class Funcionario:
    """Funcionário identificado pela matrícula."""

    def __init__(self, matricula: str, nome: str, cargo: str) -> None:
        """Crie um funcionário com matrícula, nome e cargo."""
        if not matricula.strip() or not nome.strip() or not cargo.strip():
            raise ValueError("Informe matrícula, nome e cargo do funcionário.")

        self._matricula = matricula.strip().upper()
        self.nome = nome.strip()
        self.cargo = cargo.strip()

    @property
    def matricula(self) -> str:
        """Retorne a matrícula do funcionário."""
        return self._matricula

    def realizar_checkin(self, reserva: Reserva) -> None:
        """Registre a entrada do hóspede na reserva."""
        reserva.checkin()

    def realizar_checkout(self, reserva: Reserva) -> None:
        """Registre a saída do hóspede na reserva."""
        reserva.checkout()

    def resumo(self) -> str:
        """Retorne a matrícula, o nome e o cargo do funcionário."""
        return f"{self.matricula} | {self.nome} | {self.cargo}"
