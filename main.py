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
            codigo = input('Digite o código da ação: ')
            data = input('Digite a data da operação: ')
            qtd = int(input('Digite a quantidade que você deseja comprar: '))
            valor_unit = float(input('Digite o valor unitário dessa ação: '))
            tipo_operacao = input('Digite o tipo da operação(Compra/Venda): ').lower()
            tx_corretagem = float(input('Digite o valor da taxa de corretagem: '))
            cadastrar_acao(codigo, data, qtd, valor_unit, tipo_operacao, tx_corretagem)
        # Mostrar todas as ações cadastradas
        elif op == '2':
            print(f'\n{visualizar_açoes()}\n')
        # Mostrar uma ação
        elif op == '3':
            codigo_das_acoes()
            cod_acao = input('Digite o código da ação que deseja vizualizar: ')
            print(f'\n{vizualizar_uma_acao(cod_acao)}\n')
        # Atualizar as informações de uma ação
        elif op == '4':
            codigo_das_acoes()
            cod_acao = input('Digite o código da ação que deseja atualizar: ')
            print('Qual informação deseja mudar?')
            atributo = input('1-Código\n2-Data\n3-Quantidade\n4-Valor unitário\n5-Tipo da operação\n6-Taxa de corretagem\n')
            novo_valor = input('Digite o novo valor: ')
            atualizar_acao(cod_acao, atributo, novo_valor)
        # Deletar uma ação
        elif op == '5':
            codigo_das_acoes()
            cod_acao = input('Digite o código da ação que deseja apagar: ')
            deletar_acao(cod_acao)
        
        opcao2 = input('Digite \'S\' para continuar ou \'N\' para parar: ')
        if opcao2.upper() == 'S':
            os.system('clear')
        elif opcao2.upper() == 'N':
            break

if __name__ == '__main__':
    main()
