import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)
            print("\n=== Deposito realizado com sucesso! ===")
        else:
            print("\n@@@ Operacao falhou! O valor informado e invalido. @@@")


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)
            print("\n=== Saque realizado com sucesso! ===")


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, agencia, cliente):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero, agencia):
        return cls(numero, agencia, cliente)

    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo

        if excedeu_saldo:
            print("\n@@@ Operacao falhou! Voce nao tem saldo suficiente. @@@")
            return False

        if valor <= 0:
            print("\n@@@ Operacao falhou! O valor informado e invalido. @@@")
            return False

        self.saldo -= valor
        return True

    def depositar(self, valor):
        if valor <= 0:
            return False

        self.saldo += valor
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    @classmethod
    def nova_conta(cls, cliente, numero, agencia):
        return cls(numero=numero, agencia=agencia, cliente=cliente)

    def sacar(self, valor):
        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == Saque.__name__
            ]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operacao falhou! O valor do saque excede o limite. @@@")
            return False

        if excedeu_saques:
            print("\n@@@ Operacao falhou! Numero maximo de saques excedido. @@@")
            return False

        return super().sacar(valor)

    def __str__(self):
        return textwrap.dedent(
            f"""\
            Agencia:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            """
        )


def menu():
    menu_texto = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuario
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto)).strip().lower()


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente nao possui conta cadastrada! @@@")
        return None

    if len(cliente.contas) == 1:
        return cliente.contas[0]

    print("\n=== Contas do cliente ===")
    for conta in cliente.contas:
        print(f"Agencia: {conta.agencia} | Conta: {conta.numero}")

    numero = input("Informe o numero da conta desejada: ").strip()
    if not numero.isdigit():
        print("\n@@@ Numero de conta invalido! @@@")
        return None

    numero_conta = int(numero)
    for conta in cliente.contas:
        if conta.numero == numero_conta:
            return conta

    print("\n@@@ Conta nao encontrada para este cliente! @@@")
    return None


def selecionar_cliente_conta(clientes):
    cpf = input("Informe o CPF do cliente (somente numero): ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente nao encontrado! @@@")
        return None, None

    conta = recuperar_conta_cliente(cliente)
    return cliente, conta


def criar_usuario(clientes):
    cpf = input("Informe o CPF (somente numero): ").strip()

    if filtrar_cliente(cpf, clientes):
        print("\n@@@ Ja existe usuario com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ").strip()
    data_nascimento_str = input("Informe a data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input(
        "Informe o endereco (logradouro, nro - bairro - cidade/sigla estado): "
    ).strip()

    try:
        data_nascimento = datetime.strptime(data_nascimento_str, "%d-%m-%Y").date()
    except ValueError:
        print("\n@@@ Data de nascimento invalida! Use o formato dd-mm-aaaa. @@@")
        return

    cliente = PessoaFisica(
        nome=nome,
        data_nascimento=data_nascimento,
        cpf=cpf,
        endereco=endereco,
    )
    clientes.append(cliente)
    print("\n=== Usuario criado com sucesso! ===")


def criar_conta(agencia, numero_conta, clientes, contas):
    cpf = input("Informe o CPF do usuario: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Usuario nao encontrado, fluxo de criacao de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta, agencia=agencia)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada! @@@")
        return

    for conta in contas:
        print("=" * 100)
        print(conta)


def exibir_extrato(conta):
    print("\n================ EXTRATO ================")

    if not conta.historico.transacoes:
        print("Nao foram realizadas movimentacoes.")
    else:
        for transacao in conta.historico.transacoes:
            print(
                f"{transacao['tipo']}:\tR$ {transacao['valor']:.2f}\t({transacao['data']})"
            )

    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")


def ler_valor_operacao(texto):
    valor_str = input(texto).strip().replace(",", ".")

    try:
        return float(valor_str)
    except ValueError:
        print("\n@@@ Valor invalido! @@@")
        return None


def main():
    AGENCIA = "0001"

    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            cliente, conta = selecionar_cliente_conta(clientes)
            if not conta:
                continue

            valor = ler_valor_operacao("Informe o valor do deposito: ")
            if valor is None:
                continue

            cliente.realizar_transacao(conta, Deposito(valor))

        elif opcao == "s":
            cliente, conta = selecionar_cliente_conta(clientes)
            if not conta:
                continue

            valor = ler_valor_operacao("Informe o valor do saque: ")
            if valor is None:
                continue

            cliente.realizar_transacao(conta, Saque(valor))

        elif opcao == "e":
            _, conta = selecionar_cliente_conta(clientes)
            if not conta:
                continue

            exibir_extrato(conta)

        elif opcao == "nu":
            criar_usuario(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(AGENCIA, numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operacao invalida, selecione novamente. @@@")


if __name__ == "__main__":
    main()
