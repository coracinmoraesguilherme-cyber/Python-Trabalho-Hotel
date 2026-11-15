"""Dados fictícios para a demonstração no terminal."""

from datetime import date, timedelta

from classes.funcionario import Funcionario
from classes.hospede import Hospede
from classes.hotel import Hotel
from classes.quarto import QuartoLuxo, QuartoStandard, QuartoSuite


def carregar_exemplos() -> Hotel:
    """Prepare um hotel com cadastros e duas reservas de demonstração."""
    hotel = Hotel("Hotel Aurora")

    ana = Hospede("Ana Lima", "00000000191", "ana@example.com", "11000000001")
    bruno = Hospede("Bruno Alves", "00000000272", "bruno@example.com", "11000000002")
    hotel.cadastrar_hospede(ana)
    hotel.cadastrar_hospede(bruno)
    hotel.cadastrar_funcionario(Funcionario("F001", "Clara Souza", "Recepcionista"))
    hotel.cadastrar_funcionario(Funcionario("F002", "Diego Costa", "Supervisor"))

    hotel.adicionar_quarto(QuartoStandard("101", 2, 180))
    hotel.adicionar_quarto(QuartoLuxo("201", 3, 300))
    hotel.adicionar_quarto(QuartoSuite("301", 4, 450, taxa_servico=60))

    hoje = date.today()
    hotel.criar_reserva(ana.cpf, "101", hoje, hoje + timedelta(days=2), 1)
    hotel.criar_reserva(bruno.cpf, "201", hoje + timedelta(days=1), hoje + timedelta(days=6), 2)
    return hotel
