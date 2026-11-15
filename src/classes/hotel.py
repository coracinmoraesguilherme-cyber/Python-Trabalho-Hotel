"""Cadastros, disponibilidade de quartos e reservas do hotel."""

from datetime import date

from .funcionario import Funcionario
from .hospede import Hospede
from .quarto import Quarto
from .reserva import Reserva


class Hotel:
    """Administre os objetos cadastrados e as operações de hospedagem."""

    def __init__(self, nome: str) -> None:
        """Inicialize o hotel com cadastros vazios."""
        self.nome = nome
        self._hospedes: dict[str, Hospede] = {}
        self._funcionarios: dict[str, Funcionario] = {}
        self._quartos: dict[str, Quarto] = {}
        self._reservas: dict[str, Reserva] = {}

    def cadastrar_hospede(self, hospede: Hospede) -> None:
        """Cadastre um hóspede usando o CPF como identificador único."""
        if hospede.cpf in self._hospedes:
            raise ValueError("Já existe um hóspede com esse CPF.")
        self._hospedes[hospede.cpf] = hospede

    def cadastrar_funcionario(self, funcionario: Funcionario) -> None:
        """Cadastre um funcionário usando a matrícula como identificador único."""
        if funcionario.matricula in self._funcionarios:
            raise ValueError("Já existe um funcionário com essa matrícula.")
        self._funcionarios[funcionario.matricula] = funcionario

    def adicionar_quarto(self, quarto: Quarto) -> None:
        """Adicione um quarto usando o número como identificador único."""
        if quarto.numero in self._quartos:
            raise ValueError("Já existe um quarto com esse número.")
        self._quartos[quarto.numero] = quarto

    def listar_hospedes(self) -> tuple[Hospede, ...]:
        """Retorne os hóspedes cadastrados em ordem de cadastro."""
        return tuple(self._hospedes.values())

    def listar_funcionarios(self) -> tuple[Funcionario, ...]:
        """Retorne os funcionários cadastrados em ordem de cadastro."""
        return tuple(self._funcionarios.values())

    def listar_quartos(self) -> tuple[Quarto, ...]:
        """Retorne os quartos cadastrados em ordem de cadastro."""
        return tuple(self._quartos.values())

    def listar_reservas(self) -> tuple[Reserva, ...]:
        """Retorne as reservas em ordem de criação, incluindo as canceladas."""
        return tuple(self._reservas.values())

    def buscar_hospede(self, cpf: str) -> Hospede:
        """Localize um hóspede pelo CPF."""
        hospede = self._hospedes.get(cpf)
        if hospede is None:
            raise ValueError("Hóspede não encontrado. Confira o CPF.")
        return hospede

    def buscar_funcionario(self, matricula: str) -> Funcionario:
        """Localize um funcionário pela matrícula."""
        funcionario = self._funcionarios.get(matricula.strip().upper())
        if funcionario is None:
            raise ValueError("Funcionário não encontrado. Confira a matrícula.")
        return funcionario

    def buscar_quarto(self, numero: str) -> Quarto:
        """Localize um quarto pelo número."""
        quarto = self._quartos.get(numero.strip().upper())
        if quarto is None:
            raise ValueError("Quarto não encontrado. Confira o número.")
        return quarto

    def buscar_reserva(self, codigo: str) -> Reserva:
        """Localize uma reserva pelo código gerado no cadastro."""
        reserva = self._reservas.get(codigo.strip().upper())
        if reserva is None:
            raise ValueError("Reserva não encontrada. Confira o código.")
        return reserva

    def verificar_disponibilidade(self, numero: str, entrada: date, saida: date) -> bool:
        """Verifique se o quarto ativo está livre durante todo o intervalo."""
        Reserva.validar_periodo(entrada, saida)
        quarto = self.buscar_quarto(numero)
        return quarto.ativo and not any(
            reserva.quarto is quarto and reserva.ocupa_periodo(entrada, saida)
            for reserva in self._reservas.values()
        )

    def criar_reserva(
        self,
        cpf: str,
        numero: str,
        entrada: date,
        saida: date,
        quantidade_pessoas: int,
    ) -> Reserva:
        """Vincule um hóspede cadastrado a um quarto disponível."""
        hospede = self.buscar_hospede(cpf)
        quarto = self.buscar_quarto(numero)
        if not self.verificar_disponibilidade(numero, entrada, saida):
            raise ValueError("Quarto indisponível para o período informado.")

        reserva = Reserva(hospede, quarto, entrada, saida, quantidade_pessoas)
        self._reservas[reserva.codigo] = reserva
        return reserva

    def realizar_checkin(self, codigo: str, matricula: str) -> Reserva:
        """Realize o check-in por meio de um funcionário cadastrado."""
        reserva = self.buscar_reserva(codigo)
        self.buscar_funcionario(matricula).realizar_checkin(reserva)
        return reserva

    def realizar_checkout(self, codigo: str, matricula: str) -> Reserva:
        """Realize o check-out por meio de um funcionário cadastrado."""
        reserva = self.buscar_reserva(codigo)
        self.buscar_funcionario(matricula).realizar_checkout(reserva)
        return reserva

    def cancelar_reserva(self, codigo: str) -> Reserva:
        """Localize a reserva e solicite seu cancelamento."""
        reserva = self.buscar_reserva(codigo)
        reserva.cancelar()
        return reserva

    def relatorio_ocupacao(self, data: date) -> tuple[int, int, int, float]:
        """Retorne os totais de quartos ativos, ocupados, livres e a taxa percentual."""
        total_ativos = sum(1 for quarto in self._quartos.values() if quarto.ativo)
        quartos_ocupados = {
            reserva.quarto.numero
            for reserva in self._reservas.values()
            if reserva.quarto.ativo and reserva.ocupa_data(data)
        }
        ocupados = len(quartos_ocupados)
        disponiveis = total_ativos - ocupados
        taxa = 100 * ocupados / total_ativos if total_ativos else 0.0
        return total_ativos, ocupados, disponiveis, taxa
