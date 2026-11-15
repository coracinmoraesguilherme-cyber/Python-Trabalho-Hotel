"""Cadastro e contato dos hóspedes."""

import re


class Hospede:
    """Hóspede identificado pelo CPF."""

    def __init__(self, nome: str, cpf: str, email: str, telefone: str) -> None:
        """Crie um hóspede com dados de identificação e contato válidos."""
        if not nome.strip():
            raise ValueError("Informe o nome do hóspede.")
        if not self.validar_cpf(cpf):
            raise ValueError("O CPF deve ter exatamente 11 dígitos.")

        self.nome = nome.strip()
        self._cpf = cpf
        self.atualizar_contato(email, telefone)

    @property
    def cpf(self) -> str:
        """Retorne o CPF com os 11 dígitos."""
        return self._cpf

    @property
    def email(self) -> str:
        """Retorne o e-mail cadastrado."""
        return self._email

    @email.setter
    def email(self, novo_email: str) -> None:
        """Atualize o e-mail após validar seu formato básico."""
        novo_email = novo_email.strip()
        if not re.fullmatch(r"[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+", novo_email):
            raise ValueError("E-mail inválido. Use um formato como nome@exemplo.com.")
        self._email = novo_email

    @property
    def telefone(self) -> str:
        """Retorne o telefone cadastrado."""
        return self._telefone

    @staticmethod
    def validar_cpf(cpf: str) -> bool:
        """Confira se o CPF tem exatamente 11 dígitos."""
        return len(cpf) == 11 and cpf.isdigit()

    def atualizar_contato(self, email: str, telefone: str) -> None:
        """Atualize o e-mail e o telefone se ambos forem válidos."""
        if not telefone.isdigit():
            raise ValueError("O telefone deve conter apenas dígitos.")
        self.email = email
        self._telefone = telefone

    def resumo(self) -> str:
        """Retorne o CPF, o nome e os contatos do hóspede."""
        return f"{self.cpf} | {self.nome} | {self.email} | {self.telefone}"
