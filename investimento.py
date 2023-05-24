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
        self.preco_medio = None

    def calcula_valor_operacao(self):
        self.valor_operacao = self.quantidade * self.valor_unitario

    def calcula_imposto(self):
        self.imposto = self.valor_operacao * (0.03/100)

    def calcula_valor_final(self):
        if self.compra_venda == 'compra':
            self.valor_final = self.valor_operacao + (self.taxa_corretagem + self.imposto)
        elif self.compra_venda == 'venda':
            self.valor_final = self.valor_operacao - (self.taxa_corretagem + self.imposto)

    def calcula_preco_medio(self):
        cursor.execute("SELECT * FROM investimentos")
        if len(cursor.fetchall()) <= 0:
            self.preco_medio = self.valor_final / self.quantidade
        else:
            qtd_ant_total, pm_anterior = busca_valores_banco()
            if self.compra_venda == 'compra':
                self.preco_medio = (qtd_ant_total*pm_anterior + self.valor_final) / (qtd_ant_total+self.quantidade)
            elif self.compra_venda == 'venda':
                self.preco_medio = pm_anterior

def busca_valores_banco():
    # Essa função deve determinar a soma das quantidades da ações anteriores e buscar o preço médio da ação anterior
    cursor.execute("SELECT * FROM investimentos")
    r = cursor.fetchall()
    qtd_total = 0
    for i in range(len(r)):
        if r[i][4] == 'compra':
            qtd_total += r[i][2]
        elif r[i][4] == 'venda':
            qtd_total -= r[i][2]
    return qtd_total, r[len(r)-1][9]

# -------- Funções para manipular o Banco de Dados ------
# Cadastra uma ação
def cadastrar_açao(codigo, data, qtd, valor_unit, tipo_operacao, tx_corretagem):
    açao = Investimento(codigo, data, qtd, valor_unit, tipo_operacao, tx_corretagem)
    açao.calcula_valor_operacao()
    açao.calcula_imposto()
    açao.calcula_valor_final()
    açao.calcula_preco_medio()
    cursor.execute('''
            INSERT INTO investimentos (codigo, data, quantidade, valor_unit, compra_venda, valor_operacao, tx_corretagem, tx_imposto, valor_final, preco_medio)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (açao.codigo, açao.data, açao.quantidade, açao.valor_unitario, açao.compra_venda, açao.valor_operacao, açao.taxa_corretagem, round(açao.imposto, 2), round(açao.valor_final, 2), round(açao.preco_medio, 2)))
    banco.commit()
    print('Ação Cadastrada!\n')

# Mostra todas as ações
def visualizar_açoes():
    cursor.execute("SELECT * FROM investimentos")
    resultado = cursor.fetchall()
    if len(resultado) == 0:
        return 'Nenhuma ação cadastrada'
    else:
        colunas = ['Código', 'Data', 'quantidade', 'Valor unitário',  'Compra/Venda', 'Valor da operação', 'Corretagem', 'Imposto', 'Valor final', 'Preço Médio']
        resultado_df = pd.DataFrame(resultado, columns=colunas)
        return resultado_df

# Mostra uma ação
def visualizar_uma_açao(cod):
    cursor.execute("SELECT * FROM investimentos WHERE codigo = ?", (cod,))
    resultado = cursor.fetchall()
    if len(resultado) == 0:
        return 'Nenhuma ação cadastrada'
    else:
        colunas = ['Código', 'Data', 'quantidade', 'Valor unitário',  'Compra/Venda', 'Valor da operação', 'Corretagem', 'Imposto', 'Valor final', 'Preço Médio']
        resultado_df = pd.DataFrame(resultado, columns=colunas)
        return resultado_df

# Atualiza uma ação
def atualizar_açao(cod, atr, novo):
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

# Apaga uma ação
def deletar_açao(cod):
    cursor.execute("DELETE FROM investimentos WHERE codigo = ?", (cod,))
    banco.commit()
    print('Ação deletada!')

# Busca o código das ações
def codigo_das_açoes():
    cursor.execute("SELECT codigo FROM investimentos")
    print('Códigos disponiveis: ', end='')
    resultado = cursor.fetchall()
    for i in resultado:
        print(i[0], end=' ')
    print()
