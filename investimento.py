import sqlite3
from datetime import *
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

# --------Funções auxiliares----------
# Determina o lucro ou prejuízo na venda de uma ação
def lucro_prejuizo(r):
    if r[4] == 'compra':
        return ' '
    elif r[4] == 'venda':
        lp = r[8] - (r[2]*r[9])
        return lp

#Calcula o lucro total por ativo
def lucro_total_do_ativo(r):
    soma = 0
    for i in r:
        if i[10] != ' ':
            soma += i[10]
    return soma

#Calcula o lucro da carteira
def lucro_total_carteira():
    codigos = ['ITSA4', 'WEGE3']
    total = 0
    for i in codigos:
        cursor.execute("SELECT codigo, data, quantidade, valor_unit, compra_venda, valor_operacao, tx_corretagem, tx_imposto, valor_final FROM investimentos WHERE codigo = ?", (i,))
        resultado = []
        while True:
            r = cursor.fetchone()
            if r == None:
                break
            r = list(r)
            r[1] = datetime.strptime(r[1], '%d/%m/%Y').date()
            resultado.append(r)
        organiza_datas(resultado)
        preco_medio(resultado)
        total += lucro_total_do_ativo(resultado)
    return total

# Calcula o preço médio das ações e determinar se as ações de venda resultaram em lucro ou prejuízo
def preco_medio(r):
    qtd_ant_total = 0 # Quantidade anterior total
    for i in range(len(r)):
        if i == 0:
            pm = r[i][8] / r[i][2]
            r[i].append(round(pm, 2))
            r[i].append(lucro_prejuizo(r[i]))
            qtd_ant_total += r[i][2]
        else:
            if r[i][4] == 'compra':
                pm = (qtd_ant_total*r[i-1][9] + r[i][8]) / (qtd_ant_total+r[i][2])
                r[i].append(round(pm, 2))
                r[i].append(lucro_prejuizo(r[i]))
                qtd_ant_total += r[i][2]
            elif r[i][4] == 'venda':
                pm = r[i-1][9]
                r[i].append(round(pm, 2))
                r[i].append(round(lucro_prejuizo(r[i]), 2))
                qtd_ant_total -= r[i][2]

# Organiza as ações por data da mais atual até a mais antiga
def organiza_datas(d):
    #organiza as datas
    for i in range(len(d)):
        for j in range(i+1, len(d)):
            if d[i][1] > d[j][1]:
                d[i], d[j] = d[j], d[i]
    #Transforma as datas em string
    for i in d:
        i[1] = i[1].strftime('%d/%m/%Y')

# Mostra os índicies das ações na ordem em que foram cadastradas
def visualizar_ids():
    cursor.execute("SELECT id, codigo, data FROM investimentos")
    resultado = []
    while True:
        r = cursor.fetchone()
        if r == None:
            break
        r = list(r)
        resultado.append(r)
    print(pd.DataFrame(resultado, columns=['Índice', 'Código', 'Data']))

# Quando uma determinada ação é deletada, atualiza os índicies das ações posteriores
def atualiza_ids(id):
    cursor.execute("SELECT id FROM investimentos")
    r = cursor.fetchall()
    for i in r:
        if i[0] > id:
            cursor.execute("UPDATE investimentos SET id = ? WHERE id = ?", (i[0]-1, i[0]))
            banco.commit()


# -------- Funções para manipular o Banco de Dados ------
# Cadastra uma ação
def cadastrar_operaçao(codigo, data, qtd, valor_unit, tipo_operacao, tx_corretagem):
    cursor.execute("SELECT * FROM investimentos")
    id = len(cursor.fetchall())
    açao = Investimento(codigo, data, qtd, valor_unit, tipo_operacao, tx_corretagem)
    açao.calcula_valor_operacao()
    açao.calcula_imposto()
    açao.calcula_valor_final()
    cursor.execute('''
            INSERT INTO investimentos (codigo, data, quantidade, valor_unit, compra_venda, valor_operacao, tx_corretagem, tx_imposto, valor_final, id)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (açao.codigo, açao.data, açao.quantidade, açao.valor_unitario, açao.compra_venda, açao.valor_operacao, açao.taxa_corretagem, round(açao.imposto, 2), round(açao.valor_final, 2), id))
    banco.commit()
    print('Ação Cadastrada!\n')

# Mostra todas as ações ordenadas por data em ordem decrescente
def visualizar_operaçoes_ordenado():
    cursor.execute("SELECT codigo, data, quantidade, valor_unit, compra_venda, valor_operacao, tx_corretagem, tx_imposto, valor_final FROM investimentos")
    resultado = []
    while True:
        r = cursor.fetchone()
        if r == None:
            break
        r = list(r)
        r[1] = datetime.strptime(r[1], '%d/%m/%Y').date()
        resultado.append(r)
    organiza_datas(resultado)
    colunas = ['Código', 'Data', 'quantidade', 'Valor unitário',  'Compra/Venda', 'Valor da operação', 'Corretagem', 'Imposto', 'Valor final']
    print(pd.DataFrame(resultado, columns=colunas))

# Detalhar um ativo
def detalhar_ativo(codigo):
    cursor.execute("SELECT codigo, data, quantidade, valor_unit, compra_venda, valor_operacao, tx_corretagem, tx_imposto, valor_final FROM investimentos WHERE codigo = ?", (codigo,))
    resultado = []
    while True:
        r = cursor.fetchone()
        if r == None:
            break
        r = list(r)
        r[1] = datetime.strptime(r[1], '%d/%m/%Y').date()
        resultado.append(r)
    organiza_datas(resultado)
    preco_medio(resultado)
    lucroTotalAtivo = lucro_total_do_ativo(resultado)
    colunas = ['Código', 'Data', 'quantidade', 'Valor unitário',  'Compra/Venda', 'Valor da operação', 'Corretagem', 'Imposto', 'Valor final', 'Preço Médio', 'Lucro/Prejuízo']
    print(f'{pd.DataFrame(resultado, columns=colunas)}\n\nLucro total de {codigo}: {lucroTotalAtivo}')

# Atualiza uma ação
def atualizar_ativo(id, atr, novo):
    cursor.execute("SELECT * FROM investimentos WHERE id = ?", (id,))
    r = cursor.fetchone()
    
    if atr == '1':
        cursor.execute("UPDATE investimentos SET codigo = ? WHERE id = ?", (novo, id))
        banco.commit()
    elif atr == '2':
        cursor.execute("UPDATE investimentos SET data = ? WHERE id = ?", (novo, id))
        banco.commit()
    elif atr == '3':
        qtd = int(novo)
        vlr_operacao = qtd * r[3]
        imposto = vlr_operacao * (0.03/100)
        if r[4] == 'compra':
            vlr_final = vlr_operacao + (r[6] + imposto)
        elif r[4] == 'venda':
            vlr_final = vlr_operacao - (r[6] + imposto)
        cursor.execute("UPDATE investimentos SET quantidade = ? WHERE id = ?", (qtd, id))
        cursor.execute("UPDATE investimentos SET valor_operacao = ? WHERE id = ?", (vlr_operacao, id))
        cursor.execute("UPDATE investimentos SET tx_imposto = ? WHERE id = ?", (imposto, id))
        cursor.execute("UPDATE investimentos SET valor_final = ? WHERE id = ?", (vlr_final, id))
        banco.commit()
    elif atr == '4':
        vlr_unit = float(novo)
        vlr_operacao = vlr_unit * r[2]
        imposto = vlr_operacao * (0.03/100)
        if r[4] == 'compra':
            vlr_final = vlr_operacao + (r[6] + imposto)
        elif r[4] == 'venda':
            vlr_final = vlr_operacao - (r[6] + imposto)
        cursor.execute("UPDATE investimentos SET valor_unit = ? WHERE id = ?", (vlr_unit, id))
        cursor.execute("UPDATE investimentos SET valor_operacao = ? WHERE id = ?", (vlr_operacao, id))
        cursor.execute("UPDATE investimentos SET tx_imposto = ? WHERE id = ?", (imposto, id))
        cursor.execute("UPDATE investimentos SET valor_final = ? WHERE id = ?", (vlr_final, id))
        banco.commit()
    elif atr == '5':
        if novo.lower() == 'compra':
            vlr_final = r[5] + (r[6] + r[7])
        elif novo.lower() == 'venda':
            vlr_final = r[5] - (r[6] + r[7])
        cursor.execute("UPDATE investimentos SET compra_venda = ? WHERE id = ?", (novo, id))
        cursor.execute("UPDATE investimentos SET valor_final = ? WHERE id = ?", (vlr_final, id))
        banco.commit()
    elif atr == '6':
        tx_corretagem = float(novo)
        if r[4] == 'compra':
            vlr_final = r[5] + (tx_corretagem + r[7])
        elif r[4] == 'venda':
            vlr_final = r[5] - (tx_corretagem + r[7])
        cursor.execute("UPDATE investimentos SET tx_corretagem = ? WHERE id = ?", (tx_corretagem, id))
        cursor.execute("UPDATE investimentos SET valor_final = ? WHERE id = ?", (vlr_final, id))
        banco.commit()
    print('Ação atualizada!')

# Apaga uma ação
def deletar_ativo(id):
    cursor.execute("DELETE FROM investimentos WHERE id = ?", (id,))
    banco.commit()
    atualiza_ids(id)
    print('Ação deletada!')
