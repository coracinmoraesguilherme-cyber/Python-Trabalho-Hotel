# Sistema de Gestão Hoteleira

Trabalho de Programação Orientada a Objetos em Python. O sistema simula a recepção do Hotel Aurora. Pelo terminal, é possível cadastrar pessoas e quartos, reservar uma estadia, registrar check-in e check-out e consultar a ocupação por data.

## Integrantes

- 1- Danilo Nascimento | 
- 2- Guilherme C Moraes | 
- 3- Luan Victor dos Anjos | 
- 4- Lucas Martins | 
- 5- Enzo Barbarito | 

## Regras de negócio

- O CPF do hóspede, a matrícula do funcionário e o número do quarto são únicos no hotel. O CPF pode ser digitado com ou sem pontuação e é guardado só com os 11 dígitos. A validação confere apenas o tamanho e se todos os caracteres são dígitos, usando `len()` e `isdigit()`. Não há cálculo dos dígitos verificadores nem rejeição de sequências repetidas. O telefone tem um ou mais dígitos, sem exigir tamanho específico. O e-mail deve seguir o formato básico de um endereço.
- Uma reserva exige um hóspede cadastrado, um quarto ativo, entrada a partir de hoje, pelo menos uma diária e uma quantidade de pessoas entre 1 e a capacidade do quarto.
- O valor total é calculado na criação da reserva e fica fixo. Reajustar a diária do quarto só afeta as reservas criadas depois.
- A entrada conta como noite reservada e a saída marca o fim do intervalo. Uma nova reserva pode começar na data de saída da anterior.
- A reserva começa como **Confirmada**. O check-in só é aceito entre a data de entrada e a véspera da saída, e muda o status para **Em hospedagem**. O check-out muda esse status para **Finalizada**. A reserva guarda a data e o funcionário de cada atendimento. O cancelamento é permitido no estado **Confirmada** e libera o período.
- O check-out antes da data contratada libera as noites restantes do quarto. O valor contratado não muda.
- Enquanto o check-out não é registrado, o quarto continua ocupado, mesmo depois da data de saída contratada. Outra reserva do mesmo quarto só faz check-in depois desse check-out. A reserva consulta o próprio quarto antes de registrar a entrada. Essa proteção também vale para chamadas diretas a `Reserva.checkin()` e `Funcionario.realizar_checkin()`.
- Um quarto só pode ser desativado quando não tem reservas confirmadas nem em hospedagem. Cada reserva se registra no quarto ao terminar sua inicialização. O método `Quarto.desativar()` consulta essas referências e aplica a regra, inclusive quando chamado diretamente. Quarto inativo não recebe reservas nem check-in e fica fora do relatório.
- O relatório de ocupação considera os quartos ativos e os períodos reservados ou ocupados na data consultada. A taxa é o número de quartos ocupados ou reservados dividido pelo número de quartos ativos, em porcentagem.

| Categoria | Cálculo da estadia | Serviços inclusos |
| --- | --- | --- |
| Standard | Diária × número de noites | Wi-Fi |
| Luxo | Diária × número de noites. A partir de 5 noites, aplica 10% de desconto sobre o total. | Wi-Fi e café da manhã |
| Suíte | (Diária + taxa de serviço) × número de noites | Wi-Fi, café da manhã e roupão |

Os cálculos monetários usam `Decimal` e arredondamento para centavos.

## Mapeamento das entidades

| Classe | Dados principais | Ações e responsabilidades |
| --- | --- | --- |
| `Hotel` | Nome e dicionários de hóspedes, funcionários, quartos e reservas | Cadastra e busca objetos, verifica disponibilidade, coordena reservas, ativa e desativa quartos e calcula a ocupação. |
| `Hospede` | Nome, CPF, e-mail e telefone | Normaliza e valida o CPF, atualiza o contato e fornece um resumo do cadastro. |
| `Funcionario` | Matrícula, nome e cargo | Registra check-in e check-out de uma reserva, ficando gravado como responsável, e fornece um resumo do cadastro. |
| `Quarto` (abstrata) | Número, capacidade, valor-base da diária, estado ativo e referências às reservas | Valida a diária e a capacidade, protege a desativação e o check-in, define o contrato de cálculo da estadia e dos serviços inclusos e fornece um resumo. |
| `QuartoStandard` | Atributos herdados de `Quarto` | Calcula a estadia pela diária-base e inclui Wi-Fi. |
| `QuartoLuxo` | Atributos herdados e constantes `DESCONTO_5_DIAS` e `DIARIAS_PARA_DESCONTO` | Aplica o desconto a partir de 5 noites e inclui café da manhã. |
| `QuartoSuite` | Atributos herdados e taxa de serviço | Cobra a taxa por diária e inclui café da manhã e roupão. |
| `Reserva` | Código, hóspede, quarto, datas, quantidade de pessoas, valor contratado, status e registro dos atendimentos | Calcula as diárias, fixa o total, verifica períodos, informa se está em aberto ou em hospedagem e controla check-in, check-out e cancelamento. |
| `StatusReserva` (enum) | Confirmada, Em hospedagem, Finalizada e Cancelada | Lista os estados válidos de uma reserva. |
| `Ocupacao` (tupla nomeada) | Quartos ativos, ocupados, disponíveis e taxa | Resultado do relatório de ocupação. |
| `ErroHotel` e subclasses | Mensagem do erro | Separam os erros de regra de negócio dos defeitos de programação. |

O protocolo `Resumivel` define o método `resumo()`. `Hospede`, `Funcionario`, `Quarto` e `Reserva` atendem ao contrato por terem esse método.

O menu apresenta as exceções derivadas de `ErroHotel` como mensagens. `EOFError` e `KeyboardInterrupt` encerram a sessão. As demais exceções se propagam com o traceback para permitir investigar a falha.

## Como executar

Use Python 3.10 ou superior. O projeto usa apenas a biblioteca padrão. Abra o terminal na pasta `sistema-hotel-poo` e execute o comando abaixo.

```bash
python src/main.py
```

Em ambientes que usam o comando `python3`, execute `python3 src/main.py`. Digite **0** no menu para sair. Os cadastros são mantidos em memória durante a sessão. A cada execução, o programa carrega novamente os dados fictícios.
