import sqlite3
import pandas as pd

# Conexão com o banco SQLite
banco = sqlite3.connect('investimento.db')
cursor = banco.cursor()

# Classe investimento
class Investimento:
    def __init__(self, codigo=None, data=None, quantidade=None, valor_unitario=None, compra_venda=None, taxa_corretagem=None):
        self.codigo = codigo
        self.data = data
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario
        self.compra_venda = compra_venda
        self.taxa_corretagem = taxa_corretagem
        self.valor_operacao = None
        self.imposto = None
        self.valor_final = None

    def calcula_valor_operacao(self):
        self.valor_operacao = self.quantidade * self.valor_unitario

    def calcula_imposto(self):
        self.imposto = self.valor_operacao * (0.03/100)

    def calcula_valor_final(self):
        if self.compra_venda == 'compra':
            self.valor_final = self.valor_operacao + (self.taxa_corretagem + self.imposto)
        elif self.compra_venda == 'venda':
            self.valor_final = self.valor_operacao - (self.taxa_corretagem + self.imposto)

# -------- Funções para manipular o Banco de Dados ------
def cadastrar_acao(codigo, data, qtd, valor_unit, tipo_operacao, tx_corretagem):
    açao = Investimento(codigo, data, qtd, valor_unit, tipo_operacao, tx_corretagem)
    açao.calcula_valor_operacao()
    açao.calcula_imposto()
    açao.calcula_valor_final()
    
    cursor.execute('''
            INSERT INTO investimentos (codigo, data, quantidade, valor_unit, compra_venda, valor_operacao, tx_corretagem, tx_imposto, valor_final)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (açao.codigo, açao.data, açao.quantidade, açao.valor_unitario, açao.compra_venda, açao.valor_operacao, açao.taxa_corretagem, açao.imposto, açao.valor_final))
    banco.commit()
    print('Ação Cadastrada!\n')

def visualizar_açoes():
    cursor.execute("SELECT * FROM investimentos")
    resultado = cursor.fetchall()
    colunas = ['Código', 'Data', 'quantidade', 'Valor unitário',  'Compra/Venda', 'Valor da operação', 'Corretagem', 'Imposto', 'Valor final']
    resultado_df = pd.DataFrame(resultado, columns=colunas)
    return resultado_df

def vizualizar_uma_acao(cod):
    cursor.execute("SELECT * FROM investimentos WHERE codigo = ?", (cod,))
    resultado = cursor.fetchall()
    colunas = ['Código', 'Data', 'quantidade', 'Valor unitário',  'Compra/Venda', 'Valor da operação', 'Corretagem', 'Imposto', 'Valor final']
    resultado_df = pd.DataFrame(resultado, columns=colunas)
    return resultado_df

def atualizar_acao(cod, atr, novo):
    cursor.execute("SELECT * FROM investimentos WHERE codigo = ?", (cod,))
    r = cursor.fetchone()
    
    if atr == '1':
        cursor.execute("UPDATE investimentos SET codigo = ? WHERE codigo = ?", (novo, cod))
        banco.commit()
    elif atr == '2':
        cursor.execute("UPDATE investimentos SET data = ? WHERE codigo = ?", (novo, cod))
        banco.commit()
    elif atr == '3':
        qtd = int(novo)
        vlr_operacao = qtd * r[3]
        imposto = vlr_operacao * (0.03/100)
        if r[4] == 'compra':
            vlr_final = vlr_operacao + (r[6] + imposto)
        elif r[4] == 'venda':
            vlr_final = vlr_operacao - (r[6] + imposto)
        cursor.execute("UPDATE investimentos SET quantidade = ? WHERE codigo = ?", (qtd, cod))
        cursor.execute("UPDATE investimentos SET valor_operacao = ? WHERE codigo = ?", (vlr_operacao, cod))
        cursor.execute("UPDATE investimentos SET tx_imposto = ? WHERE codigo = ?", (imposto, cod))
        cursor.execute("UPDATE investimentos SET valor_final = ? WHERE codigo = ?", (vlr_final, cod))
        banco.commit()
    elif atr == '4':
        vlr_unit = float(novo)
        vlr_operacao = vlr_unit * r[2]
        imposto = vlr_operacao * (0.03/100)
        if r[4] == 'compra':
            vlr_final = vlr_operacao + (r[6] + imposto)
        elif r[4] == 'venda':
            vlr_final = vlr_operacao - (r[6] + imposto)
        cursor.execute("UPDATE investimentos SET valor_unit = ? WHERE codigo = ?", (vlr_unit, cod))
        cursor.execute("UPDATE investimentos SET valor_operacao = ? WHERE codigo = ?", (vlr_operacao, cod))
        cursor.execute("UPDATE investimentos SET tx_imposto = ? WHERE codigo = ?", (imposto, cod))
        cursor.execute("UPDATE investimentos SET valor_final = ? WHERE codigo = ?", (vlr_final, cod))
        banco.commit()
    elif atr == '5':
        if novo.lower() == 'compra':
            vlr_final = r[5] + (r[6] + r[7])
        elif novo.lower() == 'venda':
            vlr_final = r[5] - (r[6] + r[7])
        cursor.execute("UPDATE investimentos SET compra_venda = ? WHERE codigo = ?", (novo, cod))
        cursor.execute("UPDATE investimentos SET valor_final = ? WHERE codigo = ?", (vlr_final, cod))
        banco.commit()
    elif atr == '6':
        tx_corretagem = float(novo)
        if r[4] == 'compra':
            vlr_final = r[5] + (tx_corretagem + r[7])
        elif r[4] == 'venda':
            vlr_final = r[5] - (tx_corretagem + r[7])
        cursor.execute("UPDATE investimentos SET tx_corretagem = ? WHERE codigo = ?", (tx_corretagem, cod))
        cursor.execute("UPDATE investimentos SET valor_final = ? WHERE codigo = ?", (vlr_final, cod))
        banco.commit()
    print('Ação atualizada!')

def deletar_acao(cod):
    cursor.execute("DELETE FROM investimentos WHERE codigo = ?", (cod,))
    banco.commit()
    print('Ação deletada!')

def codigo_das_acoes():
    cursor.execute("SELECT codigo FROM investimentos")
    print('Códigos disponiveis: ', end='')
    while True:
        resultado = cursor.fetchone()
        if resultado == None:
            break
        print(resultado[0], end=' ')
    print()
