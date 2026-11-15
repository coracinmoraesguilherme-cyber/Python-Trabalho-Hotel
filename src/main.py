"""Ponto de entrada do sistema de gestão hoteleira."""

from dados_ex import carregar_exemplos
from menu import Menu


def main() -> None:
    """Carregue os dados iniciais e abra o menu interativo."""
    hotel = carregar_exemplos()
    Menu(hotel).executar()


if __name__ == "__main__":
    main()
