import os
from investimento import *

def menu():
    print('Menu:\n1-Cadastrar uma ação\n2-Mostar todas as ações')
    print('3-Mostrar apenas uma ação\n4-Atualizar uma ação\n5-Apagar uma ação')

def main():
    while True:
        menu()
        op = input('Opção: ')
        # Cadastrar uma ação
        if op == '1':
            codigo = input('Digite o código da ação: ').upper()
            data = input('Digite a data da operação: ')
            qtd = int(input('Digite a quantidade que você deseja comprar: '))
            valor_unit = float(input('Digite o valor unitário dessa ação: '))
            tipo_operacao = input('Digite o tipo da operação(Compra/Venda): ').lower()
            tx_corretagem = float(input('Digite o valor da taxa de corretagem: '))
            cadastrar_açao(codigo, data, qtd, valor_unit, tipo_operacao, tx_corretagem)
        # Mostrar todas as ações cadastradas
        elif op == '2':
            visualizar_açoes_ordenado()
        # Mostrar uma ação
        elif op == '3':
            visualizar_ids()
            id_acao = int(input('Digite o índice da ação que deseja vizualizar: '))
            visualizar_uma_açao(id_acao)
        # Atualizar as informações de uma ação
        elif op == '4':
            visualizar_ids()
            id_acao = input('Digite o índice da ação que deseja atualizar: ')
            print('Qual informação deseja mudar?')
            atributo = input('1-Código\n2-Data\n3-Quantidade\n4-Valor unitário\n5-Tipo da operação\n6-Taxa de corretagem\n')
            novo_valor = input('Digite o novo valor: ')
            atualizar_açao(id_acao, atributo, novo_valor)
        # Deletar uma ação
        elif op == '5':
            visualizar_ids()
            id_acao = int(input('Digite o índice da ação que deseja deletar: ').upper())
            deletar_açao(id_acao)
        
        opcao2 = input('Deseja continuar? (S-Sim, N-Não): ')
        if opcao2.upper() == 'S':
            os.system('clear')
        elif opcao2.upper() == 'N':
            break


if __name__ == '__main__':
    main()
