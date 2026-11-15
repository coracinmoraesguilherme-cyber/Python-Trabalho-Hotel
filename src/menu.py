"""Entrada e saída do sistema de hotel pelo terminal."""

from collections.abc import Callable
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from interfaces import Resumivel
from classes.funcionario import Funcionario
from classes.hospede import Hospede
from classes.hotel import Hotel
from classes.quarto import Quarto, QuartoLuxo, QuartoStandard, QuartoSuite
from classes.reserva import Reserva


class Menu:
    """Leia as opções do usuário e exiba os resultados do hotel."""

    def __init__(self, hotel: Hotel) -> None:
        """Vincule o terminal ao hotel que será administrado."""
        self._hotel = hotel

    def executar(self) -> None:
        """Mostre o menu até o usuário escolher sair."""
        acoes: dict[str, tuple[str, Callable[[], None]]] = {
            "1": ("Cadastrar hóspede", self._cadastrar_hospede),
            "2": ("Cadastrar funcionário", self._cadastrar_funcionario),
            "3": ("Cadastrar quarto", self._cadastrar_quarto),
            "4": ("Listar hóspedes e funcionários", self._listar_pessoas),
            "5": ("Listar quartos e serviços", self._listar_quartos),
            "6": ("Consultar disponibilidade", self._consultar_disponibilidade),
            "7": ("Criar reserva", self._criar_reserva),
            "8": ("Listar reservas", self._listar_reservas),
            "9": ("Buscar reserva pelo código", self._buscar_reserva),
            "10": ("Realizar check-in", self._realizar_checkin),
            "11": ("Realizar check-out", self._realizar_checkout),
            "12": ("Cancelar reserva", self._cancelar_reserva),
            "13": ("Relatório de ocupação", self._relatorio_ocupacao),
        }

        while True:
            print(f"\n=== {self._hotel.nome} | Gestão Hoteleira ===")
            for codigo, (rotulo, _) in acoes.items():
                print(f"{codigo:>2} - {rotulo}")
            print(" 0 - Sair")

            try:
                opcao = input("Escolha uma opção: ").strip()
                if opcao == "0":
                    break
                if opcao not in acoes:
                    print("Opção inválida. Escolha um número do menu.")
                    continue
                acoes[opcao][1]()
            except ValueError as erro:
                print(f"Erro: {erro}")
            except (EOFError, KeyboardInterrupt):
                break

        print("\nSistema encerrado.")

    def _cadastrar_hospede(self) -> None:
        nome = input("Nome do hóspede: ")
        cpf = input("CPF (11 dígitos): ")
        email = input("E-mail: ")
        telefone = input("Telefone (só dígitos): ")
        hospede = Hospede(nome, cpf, email, telefone)
        self._hotel.cadastrar_hospede(hospede)
        print("Hóspede cadastrado.")
        self._listar_resumos((hospede,))

    def _cadastrar_funcionario(self) -> None:
        matricula = input("Matrícula: ")
        nome = input("Nome do funcionário: ")
        cargo = input("Cargo: ")
        funcionario = Funcionario(matricula, nome, cargo)
        self._hotel.cadastrar_funcionario(funcionario)
        print("Funcionário cadastrado.")
        self._listar_resumos((funcionario,))

    def _cadastrar_quarto(self) -> None:
        categoria = input("Categoria [1 Standard | 2 Luxo | 3 Suíte]: ").strip()
        if categoria not in ("1", "2", "3"):
            raise ValueError("Escolha uma das categorias disponíveis.")

        numero = input("Número do quarto: ")
        capacidade = self._ler_inteiro("Capacidade")
        diaria = self._ler_valor("Valor-base da diária em reais")

        quarto: Quarto
        if categoria == "1":
            quarto = QuartoStandard(numero, capacidade, diaria)
        elif categoria == "2":
            quarto = QuartoLuxo(numero, capacidade, diaria)
        else:
            taxa_servico = self._ler_valor("Taxa de serviço por diária em reais")
            quarto = QuartoSuite(numero, capacidade, diaria, taxa_servico)

        self._hotel.adicionar_quarto(quarto)
        print(f"Quarto {quarto.numero} ({quarto.TIPO}) cadastrado.")

    def _listar_pessoas(self) -> None:
        print("\nHóspedes")
        self._listar_resumos(self._hotel.listar_hospedes())
        print("\nFuncionários")
        self._listar_resumos(self._hotel.listar_funcionarios())

    def _listar_quartos(self) -> None:
        quartos = self._hotel.listar_quartos()
        if not quartos:
            print("Nenhum quarto cadastrado.")
            return

        for quarto in quartos:
            uma_diaria = self._formatar_reais(quarto.calcular_valor_estadia(1))
            cinco_diarias = self._formatar_reais(quarto.calcular_valor_estadia(5))
            servicos = ", ".join(quarto.servicos_inclusos())
            situacao = "ativo" if quarto.ativo else "inativo"
            print(
                f"{quarto.numero} | {quarto.TIPO} | {quarto.capacidade} pessoa(s) | {situacao}\n"
                f"  1 diária {uma_diaria} | 5 diárias {cinco_diarias}\n"
                f"  Serviços inclusos: {servicos}"
            )

    def _consultar_disponibilidade(self) -> None:
        numero = input("Número do quarto: ")
        entrada, saida = self._ler_periodo()
        disponivel = self._hotel.verificar_disponibilidade(numero, entrada, saida)
        print("Quarto disponível." if disponivel else "Quarto indisponível para esse período.")

    def _criar_reserva(self) -> None:
        cpf = input("CPF do hóspede (11 dígitos): ")
        numero = input("Número do quarto: ")
        entrada, saida = self._ler_periodo()
        pessoas = self._ler_inteiro("Quantidade de pessoas")
        reserva = self._hotel.criar_reserva(cpf, numero, entrada, saida, pessoas)
        print("Reserva confirmada.")
        self._exibir_reserva(reserva)

    def _listar_reservas(self) -> None:
        self._listar_resumos(self._hotel.listar_reservas())

    def _buscar_reserva(self) -> None:
        codigo = input("Código da reserva: ")
        self._exibir_reserva(self._hotel.buscar_reserva(codigo))

    def _realizar_checkin(self) -> None:
        codigo = input("Código da reserva: ")
        matricula = input("Matrícula do funcionário: ")
        reserva = self._hotel.realizar_checkin(codigo, matricula)
        print("Check-in registrado.")
        self._listar_resumos((reserva,))

    def _realizar_checkout(self) -> None:
        codigo = input("Código da reserva: ")
        matricula = input("Matrícula do funcionário: ")
        reserva = self._hotel.realizar_checkout(codigo, matricula)
        print("Check-out registrado.")
        self._exibir_reserva(reserva)

    def _cancelar_reserva(self) -> None:
        codigo = input("Código da reserva: ")
        reserva = self._hotel.cancelar_reserva(codigo)
        print("Reserva cancelada.")
        self._listar_resumos((reserva,))

    def _relatorio_ocupacao(self) -> None:
        data = self._ler_data("Data do relatório")
        ativos, ocupados, disponiveis, taxa = self._hotel.relatorio_ocupacao(data)
        print(f"\nOcupação em {data:%d/%m/%Y}")
        print(f"Quartos ativos: {ativos}")
        print(f"Quartos ocupados/reservados: {ocupados}")
        print(f"Quartos disponíveis: {disponiveis}")
        print(f"Taxa de ocupação: {taxa:.2f}%".replace(".", ","))

    def _exibir_reserva(self, reserva: Reserva) -> None:
        self._listar_resumos((reserva,))
        print(f"Diárias: {reserva.diarias} | Valor total: {self._formatar_reais(reserva.valor_total)}")

    @staticmethod
    def _listar_resumos(itens: tuple[Resumivel, ...]) -> None:
        if not itens:
            print("Nenhum registro encontrado.")
            return
        for item in itens:
            print(item.resumo())

    def _ler_periodo(self) -> tuple[date, date]:
        entrada = self._ler_data("Data de entrada")
        saida = self._ler_data("Data de saída")
        return entrada, saida

    @staticmethod
    def _ler_data(rotulo: str) -> date:
        texto = input(f"{rotulo} (DD/MM/AAAA): ").strip()
        try:
            return datetime.strptime(texto, "%d/%m/%Y").date()
        except ValueError as erro:
            raise ValueError("Data inválida. Use DD/MM/AAAA.") from erro

    @staticmethod
    def _ler_inteiro(rotulo: str) -> int:
        texto = input(f"{rotulo}: ").strip()
        try:
            return int(texto)
        except ValueError as erro:
            raise ValueError(f"{rotulo} deve ser um número inteiro.") from erro

    @staticmethod
    def _ler_valor(rotulo: str) -> Decimal:
        texto = input(f"{rotulo}: ").strip().replace(",", ".")
        try:
            return Decimal(texto)
        except InvalidOperation as erro:
            raise ValueError("Valor inválido. Digite um valor como 180,00.") from erro

    @staticmethod
    def _formatar_reais(valor: Decimal) -> str:
        numero = f"{valor:,.2f}".translate(str.maketrans(",.", ".,"))
        return f"R$ {numero}"
