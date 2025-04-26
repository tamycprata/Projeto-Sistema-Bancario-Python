# Incluindo o limite máximo de 10 transações diárias e o registro da data e hora no extrato

from datetime import datetime

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
numero_operacoes = 0
LIMITE_DIARIO = 10
data_atual = datetime.now()
mascara_transacao = "%d/%m/%Y %H:%M"
mascara_extrato = "%d/%m/%Y"
data_ultima_operacao = ""

while True:

    if (data_ultima_operacao == "") or (data_atual.strftime(mascara_extrato) != data_ultima_operacao.strftime(mascara_extrato)):
        numero_operacoes = 0
        data_ultima_operacao = data_atual
    
    if numero_operacoes <= LIMITE_DIARIO :
        
        opcao = input(menu)
        
        if opcao == "d" or opcao == "D":
            valor = float(input("Informe o valor do depósito: "))

            if valor > 0:
                saldo += valor
                numero_operacoes += 1
                data_ultima_transacao = datetime.now()
                extrato += f"{data_atual.strftime(mascara_transacao)} - Depósito R$ {valor:.2f} \n"
                print(f"Depósito de RS {valor:.2f} realizado com sucesso! \n")
            else:
                print("Operação falhou! O valor informado é inválido.")

        elif opcao == "s" or opcao == "S":
            valor = float(input("Informe o valor do saque: "))
            excedeu_saldo = valor > saldo
            excedeu_limite = valor > limite
            excedeu_saques = numero_saques >= LIMITE_SAQUES

            if excedeu_saldo:
                print("Operação falhou! Você não tem saldo suficiente.")

            elif excedeu_limite:
                print("Operação falhou! O valor do saque excede o limite.")

            elif excedeu_saques:
                print("Operação falhou! Número máximo de saques excedido.")

            elif valor > 0:
                saldo -= valor
                numero_operacoes += 1
                data_ultima_transacao = datetime.now()
                extrato += f"{data_atual.strftime(mascara_transacao)} - Saque: R$ {valor:.2f}\n"
                numero_saques += 1
                print(f"Saque de RS {valor:.2f} realizado com sucesso! \n")
                data_ultima_transacao = datetime.now()

            else:
                print("Operação falhou! O valor informado é inválido.")

        elif opcao == "e" or opcao == "E":
            numero_operacoes += 1
            data_ultima_transacao = datetime.now()
            print("\n================ EXTRATO ================")
            # print("Não foram realizadas movimentações." if not extrato else extrato)
            print(datetime.now())
            print(f"Data: {data_atual.strftime(mascara_extrato)}")
            print(f"Saldo: R$ {saldo:.2f}")
            print(f"Limite: R$ {limite:.2f}\n")
            if extrato != '':
                print(extrato)
            print("==========================================")
       
        elif opcao == "q" or opcao == "Q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

    else:
        print("Você atingiu o limite de 10 transações diárias.")
        break
