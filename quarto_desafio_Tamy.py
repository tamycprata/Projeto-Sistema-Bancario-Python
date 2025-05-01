from abc import ABC, abstractmethod
from datetime import datetime
import textwrap
import re

class Cliente:
    def __init__(self, data_nascimento, endereco):
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(data_nascimento, endereco)
        self.cpf = cpf
        self.nome = nome

class Conta:
    def __init__(self, numero, agencia, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

        cliente.adicionar_conta(self)

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, "0001", cliente)

    #property
    def saldo(self):
        return(self._saldo)

    @property
    def numero(self):
        return (self._numero)

    @property
    def agencia(self):
        return(self._agencia)

    @property
    def cliente(self):
        return(self._cliente)

    @property
    def historico(self):
        return(self._historico)

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor  # Correção: Atualiza o saldo corretamente
            deposito = Deposito(valor)
            self.historico.adicionar_transacao(deposito)
            print(f"✅ Depósito de R$ {valor:.2f} realizado com sucesso na conta {self.numero}!")
            return True
        else:
            print("❌ Operação falhou! O valor informado para depósito é inválido.")
            return False

    @abstractmethod
    def sacar(self, valor):
        pass # Será implementado nas subclasses

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print(f"Conta: {self.numero}")
        print(f"Agência: {self.agencia}")
        print(f"Titular: {self.cliente.nome}")
        print(f"Saldo: R$ {self._saldo:.2f}") # Garante que o saldo atual seja exibido
        self.historico.listar_transacoes()
        print("==========================================")

class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, agencia, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self.numero_saques_realizados = 0

    @classmethod
    def nova_conta(cls, cliente, numero, limite, limite_saques):
        conta = cls(numero, "0001", cliente, limite, limite_saques)
        return conta

    @property
    def limite(self):
        return(self._limite)

    @property
    def limite_saques(self):
        return(self._limite_saques)

    def sacar(self, valor):
        excedeu_saldo = valor > self._saldo
        excedeu_limite = valor > self._limite
        excedeu_saques = self.numero_saques_realizados >= self._limite_saques

        if excedeu_saldo:
            print("❌ Operação falhou! Você não tem saldo suficiente.")
        elif excedeu_limite:
            print("❌ Operação falhou! O valor do saque excede o limite.")
        elif excedeu_saques:
            print("❌ Operação falhou! Número máximo de saques diários excedido.")
        elif valor > 0:
            self._saldo -= valor
            self.numero_saques_realizados += 1
            saque = Saque(valor)
            self.historico.adicionar_transacao(saque)
            print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso na conta {self.numero}!")
            return True
        else:
            print("❌ Operação falhou! O valor informado para saque é inválido.")
            return False

class Transacao(ABC):
    def __init__(self, valor):
        self.valor = valor
        self.data = datetime.now()

    @abstractmethod
    def __str__(self):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        super().__init__(valor)

    def __str__(self):
        return f"{self.data.strftime('%d/%m/%Y %H:%M')} - Depósito: R$ {self.valor:.2f}"

class Saque(Transacao):
    def __init__(self, valor):
        super().__init__(valor)

    def __str__(self):
        return f"{self.data.strftime('%d/%m/%Y %H:%M')} - Saque: R$ {self.valor:.2f}"

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def listar_transacoes(self):
        if self.transacoes:
            print("\nHistórico de Transações:")
            for transacao in self.transacoes:
                print(transacao)
        else:
            print("Não houve movimentações nesta conta.")

def menu():
    menu_str = """\n
        [1] Depositar
        [2] Sacar
        [3] Extrato
        [4] Novo cliente
        [5] Nova conta
        [6] Listar contas
        [7] Sair
        => """
    return input(textwrap.dedent(menu_str))

def validar_cpf(cpf, clientes):
    cpf = cpf.replace(".", "").replace("-", "")
    if not cpf.isdigit() or len(cpf) != 11 or cpf == cpf[0] * 11:
        return False, "❌ CPF inválido!"
    for cliente in clientes:
        if cliente.cpf == cpf:
            return False, "❌ Já existe um cliente com esse CPF."
    return True, ""

def validar_data(data_nascimento):
    try:
        datetime.strptime(data_nascimento, "%d-%m-%Y")
        return True, ""
    except ValueError:
        return False, "❌ Data inválida! O formato deve ser dd-mm-aaaa."

def validar_cep(cep):
    if re.fullmatch(r"\d{5}-\d{3}", cep):
        return True, ""
    else:
        return False, "❌ CEP inválido! O formato correto é 00000-000."

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cpf_valido, mensagem_cpf_valido = validar_cpf(cpf, clientes)
    if not cpf_valido:
        print(mensagem_cpf_valido)
        return clientes

    nome_completo = input("Informe o nome completo: ")
    while True:
        data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
        data_valida, mensagem_data = validar_data(data_nascimento)
        if data_valida:
            break
        else:
            print(mensagem_data)
    endereco = input("Informe o endereço completo: (rua, número e complemento): ")

    cliente = PessoaFisica(cpf, nome_completo, data_nascimento, endereco)
    clientes.append(cliente)
    print("✅ Cliente cadastrado com sucesso!")
    return clientes

def criar_conta(agencia, numero_conta, clientes, contas):
    cpf_cliente = input("Informe o CPF do cliente para esta conta: ")
    cliente_encontrado = None
    for cliente in clientes:
        if cliente.cpf == cpf_cliente:
            cliente_encontrado = cliente
            break

    if cliente_encontrado:
        conta = ContaCorrente(numero_conta, agencia, cliente_encontrado)
        contas.append(conta)
        print(f"✅ Conta corrente {numero_conta} criada para o cliente {cliente_encontrado.nome} (Agência: {agencia}).")
    else:
        print("❌ Cliente não encontrado!")
    return contas

def listar_contas(contas):
    if not contas:
        print("❌ Não há contas cadastradas.")
        return
    print("\n================ EXTRATO DA CONTAS ================")
    for conta in contas:
        print(f"Agência: {conta.agencia}")
        print(f"Conta Corrente: {conta.numero}")
        print(f"Titular: {conta.cliente.nome}")
        print("=" * 40)
    print("==================================================")

def main():
    AGENCIA = "0001"
    clientes = []
    contas = []
    numero_conta_atual = 1

    while True:
        opcao = menu()

        if opcao == "1": # Depositar
            if not contas:
                print("Não há contas cadastradas para depósito.")
                continue
            numero_conta_deposito = int(input("Informe o número da conta para depósito: "))
            valor_deposito = float(input("Informe o valor do depósito: "))
            conta_encontrada = next((conta for conta in contas if conta.numero == numero_conta_deposito), None)
            if conta_encontrada:
                conta_encontrada.depositar(valor_deposito)
            else:
                print("❌ Conta não encontrada.")

        elif opcao == "2": # Sacar
            if not contas:
                print("Não há contas cadastradas para saque.")
                continue
            numero_conta_saque = int(input("Informe o número da conta para saque: "))
            valor_saque = float(input("Informe o valor do saque: "))
            conta_encontrada = next((conta for conta in contas if conta.numero == numero_conta_saque), None)
            if conta_encontrada and isinstance(conta_encontrada, ContaCorrente):
                conta_encontrada.sacar(valor_saque)
            elif not conta_encontrada:
                print("❌ Conta não encontrada.")
            else:
                print("❌ Operação de saque não disponível para este tipo de conta.")

        elif opcao == "3": # Extrato
            if not contas:
                print("Não há contas cadastradas para exibir o extrato.")
                continue
            numero_conta_extrato = int(input("Informe o número da conta para exibir o extrato: "))
            conta_encontrada = next((conta for conta in contas if conta.numero == numero_conta_extrato), None)
            if conta_encontrada:
                conta_encontrada.exibir_extrato()
            else:
                print("❌ Conta não encontrada.")

        elif opcao == "4": # Novo cliente
            clientes = criar_cliente(clientes)

        elif opcao == "5": # Nova conta
            contas = criar_conta(AGENCIA, numero_conta_atual, clientes, contas)
            numero_conta_atual += 1

        elif opcao == "6": # Listar contas
            listar_contas(contas)

        elif opcao == "7": # Sair
            print("👋 Obrigado por utilizar o sistema!")
            break
        
        else:
            print("❌ Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()