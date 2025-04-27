# Incluindo funções, contas e clientes
# Função depositar deve receber parâmetros por posição
# Função depositar deve receber parâmetros por nome
# Função extrato deve receber parâmetros por posição e por nome
# A função cadastrar cliente 

from datetime import datetime
import textwrap
import re

def menu():
    menu = """\n
        [1] Depositar
        [2] Sacar
        [3] Extrato
        [4] Novo cliente
        [5] Nova conta
        [6] Listar contas
        [7] Sair
        => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, mascara_transacao, numero_operacoes, /):
    if valor > 0:
        saldo += valor
        numero_operacoes += 1
        data_ultima_transacao = datetime.now()
        extrato += f"{data_ultima_transacao.strftime(mascara_transacao)} - Depósito R$ {valor:.2f} \n"
        print(f"✅ Depósito de RS {valor:.2f} realizado com sucesso!\n")
    else:
        print("❌ Operação falhou! O valor informado é inválido.")
    return saldo, extrato, data_ultima_transacao, numero_operacoes

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques, numero_operacoes, mascara_transacao):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("❌ Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("❌ Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("❌ Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        data_ultima_transacao = datetime.now()
        extrato += f"{data_ultima_transacao.strftime(mascara_transacao)} - Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        numero_operacoes += 1
        print(f"✅ Saque de RS {valor:.2f} realizado com sucesso!\n")

    else:
        print("❌ Operação falhou! O valor informado é inválido.")

    return saldo, limite, extrato, data_ultima_transacao, numero_operacoes

def exibir_extrato(saldo, limite, /, *, extrato, mascara_extrato, numero_operacoes):
    numero_operacoes += 1
    data_ultima_transacao = datetime.now()
    print("\n================ EXTRATO ================")
    print(f"Data: {data_ultima_transacao.strftime(mascara_extrato)}")
    print(f"Saldo: R$ {saldo:.2f}")
    print(f"Limite: R$ {limite:.2f}\n")
    if extrato != '':
        print(extrato)
        print("==========================================")

    return data_ultima_transacao, numero_operacoes

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cpf_valido, mensagem_cpf_valido = validar_cpf(cpf, clientes)
    if cpf_valido:
        nome_completo = input("Informe o nome completo: ")
        while True:
            data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
            data_valida, mensagem_data = validar_data(data_nascimento)
            if data_valida:
                break  # Se a data for válida, sai do loop
            else:
                print(mensagem_data)
        endereco = input("Informe a rua, número e complemento: ")
        bairro = input("Informe o Bairro: ")
        cidade = input("Informe a Cidade: ")
        estado = input("Informe o Estado: ")
        while True:
            cep = input("Informe o CEP (00000-000)")
            cep_valido, mensagem_cep = validar_cep(cep)
            if cep_valido:
                 break  # Se a data for válida, sai do loop
            else:
                print(mensagem_data)
            
        # Incluir cliente na lista
        clientes.append({ "cpf": cpf,
            "nome": nome_completo,
            "data_nascimento": data_nascimento,
            "endereco": endereco,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep })
            
        print("✅ Cliente cadastrado com sucesso!")
        
    else:
          print(mensagem_cpf_valido) 
         
    return clientes 

# Verifica se o CEP está no seguinte formato 00000-000
def validar_cep(cep):
    # Expressão regular para validar o formato 00000-000
    if re.fullmatch(r"\d{5}-\d{3}", cep):
        return True, ""
    else:
        return False, "❌ CEP inválido! O formato correto é 00000-000."

# Verifica se a data está no seguinte formato DD-MM-AAAA
def validar_data(data_nascimento):
    try:
        # Tenta converter a string para uma data usando o formato dd-mm-aaaa
        data = datetime.strptime(data_nascimento, "%d-%m-%Y")
        return True, ""
    except ValueError:
        return False, "❌ Data inválida! O formato deve ser dd-mm-aaaa."
    
# Verifica se é um cpf válido e se ele já está cadastrado
def validar_cpf(cpf, clientes):
    
    # Remove pontos e traços (caso venham formatados)
    cpf = cpf.replace(".", "").replace("-", "")
    
    # Verificar se só tem números
    if not cpf.isdigit():
        return False, "❌ CPF deve conter apenas números."
    
    # Verificar se tem 11 dígitos
    if len(cpf) != 11:
        return False, "❌ CPF deve ter 11 dígitos."
    
    # Verificar se todos os dígitos são iguais (ex: 111.111.111-11 não é válido)
    if cpf == cpf[0] * 11:
        return False, "❌ CPF inválido (todos os dígitos iguais)."
    
    # Calcular o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    primeiro_digito = (soma * 10) % 11
    if primeiro_digito == 10:
        primeiro_digito = 0

    if int(cpf[9]) != primeiro_digito:
        return False, "❌ Primeiro dígito verificador inválido."
    
    # Calcular o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    segundo_digito = (soma * 10) % 11
    if segundo_digito == 10:
        segundo_digito = 0

    if int(cpf[10]) != segundo_digito:
        return False, "❌ Segundo dígito verificador inválido."
    
    for cliente in clientes:
        if cliente["cpf"] == cpf:
            return False, "❌ Já existe um cliente com esse CPF."
        else:
            return False, "❌ Cadastro do cliente não encontrado."
    
    return True, ""

def criar_conta(agencia, numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    existe_cliente, mensagem = validar_cpf(cpf, clientes)
    if not existe_cliente:
        for cliente in clientes:
            if cliente["cpf"] == cpf:
                cliente_encontrado = cliente
                break
            else:
                print("❌ Cadastre o cliente por favor.")

        contas.append({"agencia": agencia, "numero_conta": numero_conta, "cliente": cliente })
        print(f"Agencia: {agencia}, Conta corrente: {numero_conta}, Cliente: {cliente}")
        print("✅ Conta cadastrada com sucesso!")
    else:
        print(mensagem)
    return contas


def listar_contas(contas):
    for conta in contas:
        linha = f"""\n
            Agência: {conta['agencia']}
            Conta Corrente: {conta['numero_conta']}
            Nome do Titular: {conta['cliente']['nome']}
            """
        print("=" *100)
        print(textwrap.dedent(linha))
    return

def main():

    LIMITE_SAQUES = 3
    LIMITE_DIARIO = 10
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    numero_operacoes = 0
    data_atual = datetime.now()
    mascara_transacao = "%d/%m/%Y %H:%M"
    mascara_extrato = "%d/%m/%Y"
    data_ultima_transacao = ""
    clientes = []
    contas = []

    while True:
        # Testa se existe a data da ultima transação ou se a data da ultima transação é diferente da data atual para iniciar o contator de transações do dia
        if (data_ultima_transacao == "") or (data_atual.strftime(mascara_extrato) != data_ultima_operacao.strftime(mascara_extrato)):
            numero_operacoes = 0
            data_ultima_operacao = data_atual

        # Testa se o numero de operações do dia já foi atingido
        if numero_operacoes <= LIMITE_DIARIO :
            
            opcao = menu()

            # Executa se for uma solicitação de Depósito
            if opcao == "1":
                valor = float(input("Informe o valor do depósito: "))
                saldo, extrato, data_ultima_transacao, numero_operacoes = depositar(saldo, valor, extrato, mascara_transacao, numero_operacoes)  

            # Executa se for uma solicitação de Saque
            elif opcao == "2":
                valor = float(input("Informe o valor do saque: "))
                saldo, limite, extrato, data_ultima_transacao, numero_operacoes = sacar(
                    saldo = saldo,
                    limite = limite,
                    valor = valor,
                    extrato = extrato,
                    limite_saques = LIMITE_SAQUES,
                    numero_saques = numero_saques,
                    numero_operacoes = numero_operacoes,
                    mascara_transacao = mascara_transacao)
                
            # Executa se for uma solicitação de extrato    
            elif opcao == "3":
                data_ultima_operacao, numero_operacoes = exibir_extrato(saldo , limite, 
                    extrato = extrato,
                    mascara_extrato = mascara_extrato, 
                    numero_operacoes = numero_operacoes)

            # Executa se for uma solicitação de inclusçao de um novo cliente no sistema
            elif opcao == "4":
                criar_cliente(clientes)    

            # Executa se for uma solicitação de criação de uma conta
            elif opcao == "5":
                numero_conta = len(contas) + 1
                print(f"numero conta  {numero_conta}")
                contas = criar_conta(AGENCIA, numero_conta, clientes, contas)
            
            # Executa para listar as contas de um cpf
            elif opcao == "6":
                listar_contas(contas)

            # Sai da aplicação
            elif opcao == "8":
                break
        
            else:
                print("❌ Operação inválida, por favor selecione novamente a operação desejada.")

        else:
            print("❌ Você atingiu o limite de 10 transações diárias.")
            break


main()