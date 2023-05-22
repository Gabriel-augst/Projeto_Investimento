# Arquivo para configuração do Banco de Dados
import sqlite3

banco = sqlite3.connect('investimento.db') # Cria o banco
cursor = banco.cursor() # Cria objeto cursor para executar comandos SQL e receber dados do banco
# Cria a tabela investimentos
cursor.execute('''
        CREATE TABLE investimentos(
            codigo text,
            data text,
            quantidade integer,
            valor_unit real,
            compra_venda text,
            valor_operacao real,
            tx_corretagem real,
            tx_imposto real,
            valor_final real
        )
''')

cursor.close() # Fecha o cursor
banco.close() # Fecha a conexão com o Banco
