import os # Importa módulos do sistema operacional
import sqlite3 # Importa módulos do banco de dados
import numpy as np 
# ----- alfaveto ----------------

t =  ['Z','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

# ----- Conexão com o banco -----
try:
    conexao = sqlite3.connect("controle_estoque.db")
except sqlite3.Error as erro:
    print ('Erro em conexão:', erro)
else:
    print ("Conectado com sucesso")
cursor = conexao.cursor()

# ----- Criação da tabela -----
try:
    criarTabela = """CREATE TABLE  estoque  (
	             codigo 	INTEGER NOT NULL,
	             nome_produto 	varchar2(60) NOT NULL,
	             descricao_produto 	varchar2(100) NOT NULL,
	             custo_produto 	number(9, 2) NOT NULL,
	             custo_fixo 	number(9, 2) NOT NULL,
	             comissao_venda 	number(9, 2) NOT NULL,
	             imposto_venda 	number(9, 2) NOT NULL,
	             rentabilidade 	number(9, 2) NOT NULL,
	             PRIMARY KEY(codigo AUTOINCREMENT)
                )"""
    cursor.execute(criarTabela)
    conexao.commit()
except sqlite3.Error as erro:        # Printa o erro causado no banco de dados (corrigir bugs)
    print('Erro encontrado:', erro)

# ----- Personalização -----

def limparTerminal():                # Limpar o terminal
    return os.system('cls' if os.name == 'nt' else 'clear')

def criarBarra(vezes):               # Criar barras no terminal (-----...)
    return print('-' * vezes)

# ----- Cálculo principal do sistema -----

def calculosProduto(nome_do_produto, descricao_do_produto, percent_custo_fixo, percent_comissao_de_vendas, percent_impostos, percent_rentabilidade, valor_custo_do_produto):
    valor_preco_de_venda=valor_custo_do_produto/(1-((percent_custo_fixo+percent_comissao_de_vendas+percent_impostos+percent_rentabilidade)/100)) # Cálculo do preço de venda

    percent_preco_de_venda=100 # Define o percentual (100%)

    # ----- Cálculo dos valores -----
    percent_custo_do_produto=(valor_custo_do_produto*100)/valor_preco_de_venda 

    valor_receita_bruta=valor_preco_de_venda-valor_custo_do_produto
    percent_receita_bruta=percent_preco_de_venda-percent_custo_do_produto

    valor_custo_fixo=(percent_custo_fixo/100)*valor_preco_de_venda

    valor_comissao_de_vendas=(percent_comissao_de_vendas/100)*valor_preco_de_venda

    valor_impostos=(percent_impostos/100)*valor_preco_de_venda

    valor_outros_custos=valor_custo_fixo+valor_comissao_de_vendas+valor_impostos
    percent_outros_custos=percent_custo_fixo+percent_comissao_de_vendas+percent_impostos

    valor_rentabilidade=valor_receita_bruta-valor_outros_custos

    # ----- Cálculo da classificação de lucro -----
    if percent_rentabilidade > 20:
        classificao_lucro = '\033[1;92m''Lucro Alto''\033[0;0m'
    elif percent_rentabilidade > 10 and percent_rentabilidade <= 20:
        classificao_lucro = '\033[1;92m''Lucro Médio''\033[0;0m'
    elif percent_rentabilidade > 0 and percent_rentabilidade <= 10:
        classificao_lucro = '\033[1;92m''Lucro Baixo''\033[0;0m'
    elif percent_rentabilidade == 0:
        classificao_lucro = '\033[1;93m''Lucro em Equilíbrio''\033[0;0m'
    elif percent_rentabilidade < 0:
        classificao_lucro = '\033[1;91m''Prejuízo''\033[0;0m'
    else:
        classificao_lucro = '\033[1;90m''Indefinido''\033[0;0m'
        
    tabela_valores = [
        ['Descrição',            'Valores',                           'Porcentagens'],
        ['Preço de Venda',     (f'R${valor_preco_de_venda:.2f}'),     (f'{percent_preco_de_venda:.2f}%')],
        ['Custo de Aquisição', (f'R${valor_custo_do_produto:.2f}'),   (f'{percent_custo_do_produto:.2f}%')],
        ['Receita Bruta',      (f'R${valor_receita_bruta:.2f}'),      (f'{percent_receita_bruta:.2f}%')],
        ['Custo Fixo',         (f'R${valor_custo_fixo:.2f}'),         (f'{percent_custo_fixo:.2f}%')],
        ['Comissão de Vendas', (f'R${valor_comissao_de_vendas:.2f}'), (f'{percent_comissao_de_vendas:.2f}%')],
        ['Impostos',           (f'R${valor_impostos:.2f}'),           (f'{percent_impostos:.2f}%')],
        ['Outros Custos',      (f'R${valor_outros_custos:.2f}'),      (f'{percent_outros_custos:.2f}%')],
        ['Rentabilidade',      (f'R${valor_rentabilidade:.2f}'),      (f'{percent_rentabilidade:.2f}%')]
    ]
    letras = [letra for letra in descricao_do_produto]
    descricaoDescriptografada=[]
    for letra in letras:
        if letra in t:
            indice = t.index(letra)
            descricaoDescriptografada.append(indice)

    tp=int(len(descricao_do_produto)/2)
    pSuperior=[]
    pInferior=[]
    for i in range(len(descricaoDescriptografada)):
        if i % 2 ==0:
            pSuperior.append(descricaoDescriptografada[i])
        else:
            pInferior.append(descricaoDescriptografada[i])

    p=np.array([pSuperior, pInferior])

    matrizInversa=np.array([[42, -63], [-21, 84]])

    matrizDescriptorafada=np.array(matrizInversa@p)

    lista1Linha=[]
    for x in range(tp):
        v=matrizDescriptorafada[:,x]
        lista1Linha.append(v[0])
        lista1Linha.append(v[1])

    pmodulo=[]
    for z in lista1Linha:
        if z < 0:
            abs(z)
            z = z%26
            pmodulo.append(z)
        else:
            z = z%26
            pmodulo.append(z)

    descricaoDescriptografada=[]
    for num in pmodulo:
        for letra in t:
            if num == t.index(letra):
                descricaoDescriptografada.append(letra)

    descricao_do_produto=''.join(descricaoDescriptografada)
    # ----- Print da tabela do produto -----
    print(f'Produto: {nome_do_produto}\nDescrição: {descricao_do_produto}\nClassificação: {classificao_lucro}')
    criarBarra(53)

    for item in tabela_valores:
        print('|',
            item[0],' '*(18-len(item[0])) + '|',
            item[1],' '*(13-len(item[1])) + '|',
            item[2],' '*(12-len(item[2])) + '|')
    print('=' * 53)

# ----- Menus -----

def menuPrincipal():               # Menu principal/inicial do sistema
    print('======= <<< ''\033[1;96m''Estoque''\033[0;0m'' >>> =======')
    print('| [''\033[1;36m' '1' '\033[0;0m''] - ''\033[1m' 'Cadastrar Produto' '\033[0;0m''     |')
    print('| [''\033[1;36m' '2' '\033[0;0m''] - ''\033[1m' 'Editar Produto' '\033[0;0m''        |')
    print('| [''\033[1;36m' '3' '\033[0;0m''] - ''\033[1m' 'Remover Produto' '\033[0;0m''       |')
    print('| [''\033[1;36m' '4' '\033[0;0m''] - ''\033[1m' 'Listar Produtos' '\033[0;0m''       |')
    print('| [''\033[1;36m' '0' '\033[0;0m''] - ''\033[1m' 'Encerrar' '\033[0;0m''              |')
    print('-------------------------------')
    x = input('\033[1;36m''Insira a opção: ''\033[0;0m')
    return x

def menuCadastroProduto():         # Menu de cadastro de produto
    limparTerminal()
    # ----- Recebe as informações do produto ------
    print('=============== < ''\033[1;96m''Cadastrar Produto''\033[0;0m'' > ===============')
    nome_do_produto = str(input('Nome do produto: '))
    descricao_do_produto = str(input('Descrição do produto: ')).upper()
    letras = [letra for letra in descricao_do_produto]
    descricaoCriptografada=[]
    for letra in letras:
        if letra in t:
            indice = t.index(letra)
            descricaoCriptografada.append(indice)

    if len(descricaoCriptografada)%2!=0:
        descricaoCriptografada.append(descricaoCriptografada[-1])

    matriz = np.array([[4, 3], [1, 2]])

    tp=int(len(descricaoCriptografada)/2)
    pSuperior=[]
    pInferior=[]
    for i in range(len(descricaoCriptografada)):
        if i % 2 ==0:
            pSuperior.append(descricaoCriptografada[i])
        else:
            pInferior.append(descricaoCriptografada[i])

    p=np.array([pSuperior, pInferior])

    matrizCriptorafada=np.array(matriz@p)

    lista1Linha=[]
    for x in range(tp):
        v=matrizCriptorafada[:,x]
        lista1Linha.append(v[0])
        lista1Linha.append(v[1])

    pmodulo=[]
    for z in lista1Linha:
        if z < 0:
            while z >= 0:
                z += 26
            pmodulo.append(z)
        else:
            z = z%26
            pmodulo.append(z)

    descricaoCriptografada=[]
    for num in pmodulo:
        for letra in t:
            if num == t.index(letra):
                descricaoCriptografada.append(letra)

    descricao_do_produto=str(''.join(descricaoCriptografada))
    while True:
        valor_custo_do_produto = float(input('Custo do produto (R$): '))
        if valor_custo_do_produto <= 0:
            print('\033[1;91m''Custo do Produto não pode ser zero!''\033[0;0m')
        else:
            break
    while True: # While para garantir que o usuário digite um valor menor que 100%
        percent_custo_fixo = float(input('Custo fixo (%): '))
        percent_comissao_de_vendas = float(input('Comissão de vendas (%): '))
        percent_impostos = float(input('Impostos (%): '))
        percent_rentabilidade = float(input('Rentabilidade (%): '))
        if (percent_custo_fixo+percent_comissao_de_vendas+percent_impostos+percent_rentabilidade) < 100:
            break
        else:
            print('\033[1;91m''A soma dos percentuais não pode chegar em 100%!''\033[0;00m')

    limparTerminal()
    print('=============== < ''\033[1;96m''Cadastrar Produto''\033[0;0m'' > ===============')
    calculosProduto(nome_do_produto, descricao_do_produto, percent_custo_fixo, percent_comissao_de_vendas, percent_impostos, percent_rentabilidade, valor_custo_do_produto)
        
    while True: # While para confirmação de cadastro
        confirmarCadastro = input('\nConfirmar Cadastro:\n[''\033[1;92m''1''\033[0;00m''] - Confirmar\n[''\033[1;93m''2''\033[0;00m''] - Refazer\n[''\033[1;91m''0''\033[0;00m''] - Cancelar\nOpção: ')
        if confirmarCadastro == '1':
            sql_insert = """
            INSERT INTO estoque (
                nome_produto, 
                descricao_produto, 
                custo_produto, 
                custo_fixo, 
                comissao_venda, 
                imposto_venda, 
                rentabilidade
                ) VALUES (:1, :2, :3, :4, :5, :6, :7)
            """

            dados = (
                nome_do_produto,
                descricao_do_produto,
                valor_custo_do_produto,
                percent_custo_fixo,
                percent_comissao_de_vendas,
                percent_impostos,
                percent_rentabilidade
            )
            cursor.execute(sql_insert, dados)
            conexao.commit()
            cursor.execute("select codigo from estoque order by codigo desc limit 1")
            codigoCadastrado = cursor.fetchone()
            
            limparTerminal()
            criarBarra(31)
            print('\033[1;92m''      Produto Cadastrado!''\033[0;0m')
            print('\033[1;95m'f'     Código do Produto: {codigoCadastrado[0]}''\033[0;0m')
            criarBarra(31)
            break
        elif confirmarCadastro == '2':
            menuCadastroProduto()
            break
        elif confirmarCadastro == '0':
            limparTerminal()
            criarBarra(31)
            print('\033[1;91m''      Cadastro Cancelado!''\033[0;0m')
            criarBarra(31)
            break
        else:
            print('\033[1;91m''\nOpção inválida!''\033[0;0m')

def menuEditarProduto():            # Menu de editar produtos
    limparTerminal()
    while True:
        print('======= <<< ''\033[0;93m''Editar Produto''\033[0;0m'' >>> =======')
        print('| [''\033[0;93m' '1' '\033[0;0m''] - ''\033[1m' 'Editar nome' '\033[0;0m''                        |')
        print('| [''\033[0;93m' '2' '\033[0;0m''] - ''\033[1m' 'Editar descrição' '\033[0;0m''                   |')
        print('| [''\033[0;93m' '3' '\033[0;0m''] - ''\033[1m' 'Editar custo do produto' '\033[0;0m''            |')
        print('| [''\033[0;93m' '4' '\033[0;0m''] - ''\033[1m' 'Editar percentual de custo fixo' '\033[0;0m''    |')
        print('| [''\033[0;93m' '5' '\033[0;0m''] - ''\033[1m' 'Editar percentual de comissão' '\033[0;0m''      |')
        print('| [''\033[0;93m' '6' '\033[0;0m''] - ''\033[1m' 'Editar percentual de imposto' '\033[0;0m''       |')
        print('| [''\033[0;93m' '7' '\033[0;0m''] - ''\033[1m' 'Editar percentual de rentabilidade' '\033[0;0m'' |')
        print('| [''\033[0;93m' '0' '\033[0;0m''] - ''\033[1m' 'Voltar' '\033[0;0m''                             |')
        print('---------------------------------------')
        x = input('\033[0;93m''Insira a opção: ''\033[0;0m')
        if x == '1':
            limparTerminal()
            editarNome()
        elif x == '2':
            limparTerminal()
            editarDescricao()
        elif x == '3':
            limparTerminal()
            editarCp()
        elif x == '4':
            limparTerminal()
            editarCf()
        elif x == '5':
            limparTerminal()
            editarCv()
        elif x == '6':
            limparTerminal()
            editarIv()
        elif x == '7':
            limparTerminal()
            editarRent()
        elif x == '0':
            limparTerminal()
            break
        else:
            limparTerminal()
            criarBarra()
            print('\033[1;31m''    Insira uma opção válida!''\033[0;0m')
            criarBarra()

def menuRemoverProduto():               # Menu de remover produto
    limparTerminal()
    while True:
        print('======= <<< ''\033[0;91m''Remover Produto''\033[0;0m'' >>> =======')
        print('| [''\033[0;91m' '1' '\033[0;0m''] - ''\033[1m' 'Selecionar Produto' '\033[0;0m''            |')
        print('| [''\033[1;91m' '2' '\033[0;0m''] - ''\033[1m' 'Zerar Produtos' '\033[0;0m''                |')
        print('| [''\033[0;91m' '0' '\033[0;0m''] - ''\033[1m' 'Voltar' '\033[0;0m''                        |')
        print('---------------------------------------')
        x = input('\033[0;91m''Insira a opção: ''\033[0;0m')
        if x == '1':
            limparTerminal()
            deletarProduto()
        elif x == '2':
            limparTerminal()
            zerarProdutos()
        elif x == '0':
            limparTerminal()
            break
        else:
            limparTerminal()
            criarBarra(39)
            print('\033[1;31m''      Insira uma opção válida!''\033[0;0m')
            criarBarra(39)

def menuListarProdutos():           # Menu de listar produtos
    limparTerminal()
    while True:
        print('======= <<< ''\033[0;92m''Produtos''\033[0;0m'' >>> =======')
        print('| [''\033[0;92m' '1' '\033[0;0m''] - ''\033[1m' 'Listar Produtos' '\033[0;0m''        |')
        print('| [''\033[1;92m' '2' '\033[0;0m''] - ''\033[1m' 'Pesquisar Produtos' '\033[0;0m''     |')
        print('| [''\033[0;92m' '0' '\033[0;0m''] - ''\033[1m' 'Voltar' '\033[0;0m''                 |')
        print('--------------------------------')
        x = input('\033[0;92m''Insira a opção: ''\033[0;0m')
        if x == '1':
            limparTerminal()
            listarTodosProdutos()
        elif x == '2':
            limparTerminal()
            pesquisarProdutos()
        elif x == '0':
            limparTerminal()
            break
        else:
            limparTerminal()
            criarBarra(32)
            print('\033[1;31m''    Insira uma opção válida!''\033[0;0m')
            criarBarra(32)

# ----- Sub-menus -----
def listarTodosProdutos():
    cursor.execute('select * from estoque')
    listaProdutos = cursor.fetchall()
    if len(listaProdutos) == 0:
        criarBarra(32)
        print('\033[1;31m''    Nenhum produto encontrado''\033[0;0m')
        criarBarra(32)
    else:
        for produto in listaProdutos:
            codigo_produto = produto[0]
            nome_do_produto = produto[1]
            descricao_do_produto = produto[2]
            valor_custo_do_produto = produto[3]
            percent_custo_fixo = produto[4]
            percent_comissao_de_vendas = produto[5]
            percent_impostos = produto[6]
            percent_rentabilidade = produto[7]

            print('\n' + '=' * 52)
            print('Código: ''\033[1;95m'f'{codigo_produto}''\033[0;0m')
            calculosProduto(nome_do_produto, descricao_do_produto, percent_custo_fixo, percent_comissao_de_vendas, percent_impostos, percent_rentabilidade, valor_custo_do_produto)

def pesquisarProdutos():
    while True:
        print('Digite "sair" para sair')
        print('========= < ''\033[1;92m''Pesquisar Produto''\033[0;0m'' > =========')
        codigoPesquisa = input('Insira o código do produto: ')
        if codigoPesquisa.lower() == 'sair':
            limparTerminal()
            break
        else:
            try:
                cursor.execute(f"select * from estoque where codigo = {codigoPesquisa}")
                produtoPesquisado = cursor.fetchall()
            except:
                limparTerminal()
                print('========= <<< ''\033[0;91m''Erro''\033[0;0m'' >>> =========')
                print('\033[1;91m''Opção Inválida (somente números)''\033[0;0m')
                break

        limparTerminal()
        if produtoPesquisado:
            codigo_produto = produtoPesquisado[0][0]
            nome_do_produto = produtoPesquisado[0][1]
            descricao_do_produto = produtoPesquisado[0][2]
            valor_custo_do_produto = produtoPesquisado[0][3]
            percent_custo_fixo = produtoPesquisado[0][4]
            percent_comissao_de_vendas = produtoPesquisado[0][5]
            percent_impostos = produtoPesquisado[0][6]
            percent_rentabilidade = produtoPesquisado[0][7]

            print('=============== < ''\033[1;92m''Pesquisar Produto''\033[0;0m'' > ===============')
            print('Código: ''\033[1;95m'f'{codigo_produto}''\033[0;0m')   
            calculosProduto(nome_do_produto, descricao_do_produto, percent_custo_fixo, percent_comissao_de_vendas, percent_impostos, percent_rentabilidade, valor_custo_do_produto)
            break
        else:
            limparTerminal()
            print('========= <<< ''\033[0;91m''Erro''\033[0;0m'' >>> =========')
            print('\033[1;91m''     Produto não encontrado!''\033[0;0m')
            break
def editarNome():
    while True:
        print('Digite "sair" para sair')
        print('========= < ''\033[1;92m''Editar Nome''\033[0;0m'' > =========')
        codigoEdicao = input('Insira o código do produto: ')
        if codigoEdicao.lower() == 'sair':
            limparTerminal()
            break
        else:
            edicao_nome = str(input('Novo nome do produto: '))
            limparTerminal()
            print('========== <<< ''\033[0;91m''ALERTA''\033[0;0m'' >>> ==========')
            print('\033[0;91m'f'Deseja editar o nome do produto {codigoEdicao} do estoque?''\033[0;0m')
            print('====================================')
            print('| [''\033[0;91m' '1' '\033[0;0m''] - ''\033[1m' 'Confirmar' '\033[0;0m''                  |')
            print('| [''\033[0;91m' '0' '\033[0;0m''] - ''\033[1m' 'Cancelar' '\033[0;0m''                   |')
            print('------------------------------------')
            opcao = input('\033[0;91m''Opção: ''\033[0;0m')
            if opcao == '1':
                cursor.execute(f"select 1 from estoque where codigo = {codigoEdicao}")
                produtoExiste = cursor.fetchone()
                if produtoExiste:
                    cursor.execute(f"update estoque set nome_produto = '{edicao_nome}' where codigo = {codigoEdicao}")
                    conexao.commit()
                    limparTerminal()
                    print('-' * 39)
                    print('\033[1;91m''            Nome alterado!''\033[0;0m')
                    print('-' * 39)
                    break
                else:
                    limparTerminal()
                    print('============== < ''\033[0;91m''Erro''\033[0;0m'' > ===============')
                    print('\033[1;91m''        Produto não encontrado!''\033[0;0m')
                    break
            elif opcao == '0':
                limparTerminal()
                print('-' * 39)
                print('\033[1;91m''            Ação Cancelada!''\033[0;0m')
                print('-' * 39)
                break
            else:
                limparTerminal()
                print('-' * 36)
                print('\033[1;91m''           Opção Inválida!''\033[0;0m')
                print('-' * 36)
def editarDescricao():
     while True:
        print('Digite "sair" para sair')
        print('========= < ''\033[1;92m''Editar descrição''\033[0;0m'' > =========')
        codigoEdicao = input('Insira o código do produto: ')
        if codigoEdicao.lower() == 'sair':
            limparTerminal()
            break
        else:
            edicao_descricao = str(input('Nova descrição do produto: ')).upper()
            letras = [letra for letra in edicao_descricao]
            descricaoCriptografada=[]
            for letra in letras:
                if letra in t:
                    indice = t.index(letra)
                    descricaoCriptografada.append(indice)

            if len(descricaoCriptografada)%2!=0:
                descricaoCriptografada.append(descricaoCriptografada[-1])

            matriz = np.array([[4, 3], [1, 2]])

            tp=int(len(descricaoCriptografada)/2)
            pSuperior=[]
            pInferior=[]
            for i in range(len(descricaoCriptografada)):
                if i % 2 ==0:
                    pSuperior.append(descricaoCriptografada[i])
                else:
                    pInferior.append(descricaoCriptografada[i])

            p=np.array([pSuperior, pInferior])

            matrizCriptorafada=np.array(matriz@p)

            lista1Linha=[]
            for x in range(tp):
                v=matrizCriptorafada[:,x]
                lista1Linha.append(v[0])
                lista1Linha.append(v[1])

            pmodulo=[]
            for z in lista1Linha:
                if z < 0:
                    while z >= 0:
                        z += 26
                    pmodulo.append(z)
                else:
                    z = z%26
                    pmodulo.append(z)

            descricaoCriptografada=[]
            for num in pmodulo:
                for letra in t:
                    if num == t.index(letra):
                        descricaoCriptografada.append(letra)

            edicao_descricao=str(''.join(descricaoCriptografada))
            limparTerminal()
            print('========== <<< ''\033[0;91m''ALERTA''\033[0;0m'' >>> ==========')
            print('\033[0;91m'f'Deseja editar a descrição do produto {codigoEdicao} do estoque?''\033[0;0m')
            print('====================================')
            print('| [''\033[0;91m' '1' '\033[0;0m''] - ''\033[1m' 'Confirmar' '\033[0;0m''                  |')
            print('| [''\033[0;91m' '0' '\033[0;0m''] - ''\033[1m' 'Cancelar' '\033[0;0m''                   |')
            print('------------------------------------')
            opcao = input('\033[0;91m''Opção: ''\033[0;0m')
            if opcao == '1':
                cursor.execute(f"select 1 from estoque where codigo = {codigoEdicao}")
                produtoExiste = cursor.fetchone()
                if produtoExiste:
                    cursor.execute(f"update estoque set descricao_produto = '{edicao_descricao}' where codigo = {codigoEdicao}")
                    conexao.commit()
                    limparTerminal()
                    print('-' * 39)
                    print('\033[1;91m''            Descrição alterada!''\033[0;0m')
                    print('-' * 39)
                    break
                else:
                    limparTerminal()
                    print('============== < ''\033[0;91m''Erro''\033[0;0m'' > ===============')
                    print('\033[1;91m''        Produto não encontrado!''\033[0;0m')
                    break
            elif opcao == '0':
                limparTerminal()
                print('-' * 39)
                print('\033[1;91m''            Ação Cancelada!''\033[0;0m')
                print('-' * 39)
                break
            else:
                limparTerminal()
                print('-' * 36)
                print('\033[1;91m''           Opção Inválida!''\033[0;0m')
                print('-' * 36)
def editarCp():
     while True:
        print('Digite "sair" para sair')
        print('========= < ''\033[1;92m''Editar custo fixo''\033[0;0m'' > =========')
        codigoEdicao = input('Insira o código do produto: ')
        if codigoEdicao.lower() == 'sair':
            limparTerminal()
            break
        else:
            try:
                cursor.execute(f"select * from estoque where codigo = {codigoEdicao}")
                produtoExiste = cursor.fetchone()
            except:
                limparTerminal()
                print('========= <<< ''\033[0;91m''Erro''\033[0;0m'' >>> =========')
                print('\033[1;91m''Opção Inválida (somente números)''\033[0;0m')
                break
        while True:
            valor_custo_do_produto = float(input('Novo custo do produto (R$): '))
            if valor_custo_do_produto <= 0:
                print('\033[1;91m''Custo do Produto não pode ser zero!''\033[0;0m')
            else:
                break
        limparTerminal()
        print('========== <<< ''\033[0;91m''ALERTA''\033[0;0m'' >>> ==========')
        print('\033[0;91m'f'Deseja editar o custo do produto {codigoEdicao} do estoque?''\033[0;0m')
        print('====================================')
        print('| [''\033[0;91m' '1' '\033[0;0m''] - ''\033[1m' 'Confirmar' '\033[0;0m''                  |')
        print('| [''\033[0;91m' '0' '\033[0;0m''] - ''\033[1m' 'Cancelar' '\033[0;0m''                   |')
        print('------------------------------------')
        opcao = input('\033[0;91m''Opção: ''\033[0;0m')
        if opcao == '1':
            cursor.execute(f"select 1 from estoque where codigo = {codigoEdicao}")
            if produtoExiste:
                cursor.execute(f"update estoque set custo_produto = '{valor_custo_do_produto}' where codigo = {codigoEdicao}")
                conexao.commit()
                limparTerminal()
                print('-' * 39)
                print('\033[1;91m''            Custo do produto alterado!''\033[0;0m')
                print('-' * 39)
                break
            else:
                limparTerminal()
                print('============== < ''\033[0;91m''Erro''\033[0;0m'' > ===============')
                print('\033[1;91m''        Produto não encontrado!''\033[0;0m')
                break
        elif opcao == '0':
            limparTerminal()
            print('-' * 39)
            print('\033[1;91m''            Ação Cancelada!''\033[0;0m')
            print('-' * 39)
            break
        else:
            limparTerminal()
            print('-' * 36)
            print('\033[1;91m''           Opção Inválida!''\033[0;0m')
            print('-' * 36)
def editarCf():
    while True:
        print('Digite "sair" para sair')
        print('========= < ''\033[1;92m''Editar custo fixo''\033[0;0m'' > =========')
        codigoEdicao = input('Insira o código do produto: ')
        if codigoEdicao.lower() == 'sair':
            limparTerminal()
            break
        else:
            try:
                cursor.execute(f"select * from estoque where codigo = {codigoEdicao}")
                produtoPesquisado = cursor.fetchall()
            except:
                limparTerminal()
                print('========= <<< ''\033[0;91m''Erro''\033[0;0m'' >>> =========')
                print('\033[1;91m''Opção Inválida (somente números)''\033[0;0m')
                break

        limparTerminal()
        if produtoPesquisado:
            percent_comissao_de_vendas = produtoPesquisado[0][5]
            percent_impostos = produtoPesquisado[0][6]
            percent_rentabilidade = produtoPesquisado[0][7]
        while True:
            percent_custo_fixo = float(input('Novo percentual de custo fixo do produto (R$): '))
            if (percent_custo_fixo+percent_comissao_de_vendas+percent_impostos+percent_rentabilidade) < 100:
                break
            else:
                print('\033[1;91m''A soma dos percentuais não pode chegar em 100%!''\033[0;00m')
        limparTerminal()
        print('========== <<< ''\033[0;91m''ALERTA''\033[0;0m'' >>> ==========')
        print('\033[0;91m'f'Deseja editar o custo fixo do produto {codigoEdicao} do estoque?''\033[0;0m')
        print('====================================')
        print('| [''\033[0;91m' '1' '\033[0;0m''] - ''\033[1m' 'Confirmar' '\033[0;0m''                  |')
        print('| [''\033[0;91m' '0' '\033[0;0m''] - ''\033[1m' 'Cancelar' '\033[0;0m''                   |')
        print('------------------------------------')
        opcao = input('\033[0;91m''Opção: ''\033[0;0m')
        if opcao == '1':
            cursor.execute(f"select 1 from estoque where codigo = {codigoEdicao}")
            produtoExiste = cursor.fetchone()
            if produtoExiste:
                cursor.execute(f"update estoque set custo_fixo = '{percent_custo_fixo}' where codigo = {codigoEdicao}")
                conexao.commit()
                limparTerminal()
                print('-' * 39)
                print('\033[1;91m''            Custo fixo do produto alterado!''\033[0;0m')
                print('-' * 39)
                break
            else:
                limparTerminal()
                print('============== < ''\033[0;91m''Erro''\033[0;0m'' > ===============')
                print('\033[1;91m''        Produto não encontrado!''\033[0;0m')
                break
        elif opcao == '0':
            limparTerminal()
            print('-' * 39)
            print('\033[1;91m''            Ação Cancelada!''\033[0;0m')
            print('-' * 39)
            break
        else:
            limparTerminal()
            print('-' * 36)
            print('\033[1;91m''           Opção Inválida!''\033[0;0m')
            print('-' * 36)
def editarCv():
    while True:
        print('Digite "sair" para sair')
        print('========= < ''\033[1;92m''Editar comissão de venda''\033[0;0m'' > =========')
        codigoEdicao = input('Insira o código do produto: ')
        if codigoEdicao.lower() == 'sair':
            limparTerminal()
            break
        else:
            try:
                cursor.execute(f"select * from estoque where codigo = {codigoEdicao}")
                produtoPesquisado = cursor.fetchall()
            except:
                limparTerminal()
                print('========= <<< ''\033[0;91m''Erro''\033[0;0m'' >>> =========')
                print('\033[1;91m''Opção Inválida (somente números)''\033[0;0m')
                break

        limparTerminal()
        if produtoPesquisado:
            percent_custo_fixo = produtoPesquisado[0][4]
            percent_impostos = produtoPesquisado[0][6]
            percent_rentabilidade = produtoPesquisado[0][7]

        while True:
            percent_comissao_de_vendas = float(input('Novo percentual de comissão de venda do produto (R$): '))
            if (percent_custo_fixo+percent_comissao_de_vendas+percent_impostos+percent_rentabilidade) < 100:
                break
            else:
                print('\033[1;91m''A soma dos percentuais não pode chegar em 100%!''\033[0;00m')
        limparTerminal()
        print('========== <<< ''\033[0;91m''ALERTA''\033[0;0m'' >>> ==========')
        print('\033[0;91m'f'Deseja editar a comissão de venda do produto {codigoEdicao} do estoque?''\033[0;0m')
        print('====================================')
        print('| [''\033[0;91m' '1' '\033[0;0m''] - ''\033[1m' 'Confirmar' '\033[0;0m''                  |')
        print('| [''\033[0;91m' '0' '\033[0;0m''] - ''\033[1m' 'Cancelar' '\033[0;0m''                   |')
        print('------------------------------------')
        opcao = input('\033[0;91m''Opção: ''\033[0;0m')
        if opcao == '1':
            cursor.execute(f"select 1 from estoque where codigo = {codigoEdicao}")
            produtoExiste = cursor.fetchone()
            if produtoExiste:
                cursor.execute(f"update estoque set comissao_venda = '{percent_comissao_de_vendas}' where codigo = {codigoEdicao}")
                conexao.commit()
                limparTerminal()
                print('-' * 39)
                print('\033[1;91m''            Comissão de venda do produto alterado!''\033[0;0m')
                print('-' * 39)
                break
            else:
                limparTerminal()
                print('============== < ''\033[0;91m''Erro''\033[0;0m'' > ===============')
                print('\033[1;91m''        Produto não encontrado!''\033[0;0m')
                break
        elif opcao == '0':
            limparTerminal()
            print('-' * 39)
            print('\033[1;91m''            Ação Cancelada!''\033[0;0m')
            print('-' * 39)
            break
        else:
            limparTerminal()
            print('-' * 36)
            print('\033[1;91m''           Opção Inválida!''\033[0;0m')
            print('-' * 36)
def editarIv():
    while True:
        print('Digite "sair" para sair')
        print('========= < ''\033[1;92m''Editar imposto de venda''\033[0;0m'' > =========')
        codigoEdicao = input('Insira o código do produto: ')
        if codigoEdicao.lower() == 'sair':
            limparTerminal()
            break
        else:
            try:
                cursor.execute(f"select * from estoque where codigo = {codigoEdicao}")
                produtoPesquisado = cursor.fetchall()
            except:
                limparTerminal()
                print('========= <<< ''\033[0;91m''Erro''\033[0;0m'' >>> =========')
                print('\033[1;91m''Opção Inválida (somente números)''\033[0;0m')
                break

        limparTerminal()
        if produtoPesquisado:
            percent_custo_fixo = produtoPesquisado[0][4]
            percent_comissao_de_vendas = produtoPesquisado[0][5]
            percent_rentabilidade = produtoPesquisado[0][7]

        while True:
            percent_impostos = float(input('Novo percentual de imposto de venda do produto (R$): '))
            if (percent_custo_fixo+percent_comissao_de_vendas+percent_impostos+percent_rentabilidade) < 100:
                break
            else:
                print('\033[1;91m''A soma dos percentuais não pode chegar em 100%!''\033[0;00m')
        limparTerminal()
        print('========== <<< ''\033[0;91m''ALERTA''\033[0;0m'' >>> ==========')
        print('\033[0;91m'f'Deseja editar a imposto de venda do produto {codigoEdicao} do estoque?''\033[0;0m')
        print('====================================')
        print('| [''\033[0;91m' '1' '\033[0;0m''] - ''\033[1m' 'Confirmar' '\033[0;0m''                  |')
        print('| [''\033[0;91m' '0' '\033[0;0m''] - ''\033[1m' 'Cancelar' '\033[0;0m''                   |')
        print('------------------------------------')
        opcao = input('\033[0;91m''Opção: ''\033[0;0m')
        if opcao == '1':
            cursor.execute(f"select 1 from estoque where codigo = {codigoEdicao}")
            produtoExiste = cursor.fetchone()
            if produtoExiste:
                cursor.execute(f"update estoque set imposto_venda = '{percent_impostos}' where codigo = {codigoEdicao}")
                conexao.commit()
                limparTerminal()
                print('-' * 39)
                print('\033[1;91m''            Imposto de venda do produto alterado!''\033[0;0m')
                print('-' * 39)
                break
            else:
                limparTerminal()
                print('============== < ''\033[0;91m''Erro''\033[0;0m'' > ===============')
                print('\033[1;91m''        Produto não encontrado!''\033[0;0m')
                break
        elif opcao == '0':
            limparTerminal()
            print('-' * 39)
            print('\033[1;91m''            Ação Cancelada!''\033[0;0m')
            print('-' * 39)
            break
        else:
            limparTerminal()
            print('-' * 36)
            print('\033[1;91m''           Opção Inválida!''\033[0;0m')
            print('-' * 36)
def editarRent():
    while True:
        print('Digite "sair" para sair')
        print('========= < ''\033[1;92m''Editar rentabilidade''\033[0;0m'' > =========')
        codigoEdicao = input('Insira o código do produto: ')
        if codigoEdicao.lower() == 'sair':
            limparTerminal()
            break
        else:
            try:
                cursor.execute(f"select * from estoque where codigo = {codigoEdicao}")
                produtoPesquisado = cursor.fetchall()
            except:
                limparTerminal()
                print('========= <<< ''\033[0;91m''Erro''\033[0;0m'' >>> =========')
                print('\033[1;91m''Opção Inválida (somente números)''\033[0;0m')
                break

        limparTerminal()
        if produtoPesquisado:
            percent_custo_fixo = produtoPesquisado[0][4]
            percent_comissao_de_vendas = produtoPesquisado[0][5]
            percent_impostos = produtoPesquisado[0][6]

        while True:
            percent_rentabilidade = float(input('Novo percentual de rentabilidade do produto (R$): '))
            if (percent_custo_fixo+percent_comissao_de_vendas+percent_impostos+percent_rentabilidade) < 100:
                break
            else:
                print('\033[1;91m''A soma dos percentuais não pode chegar em 100%!''\033[0;00m')
        limparTerminal()
        print('========== <<< ''\033[0;91m''ALERTA''\033[0;0m'' >>> ==========')
        print('\033[0;91m'f'Deseja editar a rentabilidade do produto {codigoEdicao} do estoque?''\033[0;0m')
        print('====================================')
        print('| [''\033[0;91m' '1' '\033[0;0m''] - ''\033[1m' 'Confirmar' '\033[0;0m''                  |')
        print('| [''\033[0;91m' '0' '\033[0;0m''] - ''\033[1m' 'Cancelar' '\033[0;0m''                   |')
        print('------------------------------------')
        opcao = input('\033[0;91m''Opção: ''\033[0;0m')
        if opcao == '1':
            cursor.execute(f"select 1 from estoque where codigo = {codigoEdicao}")
            produtoExiste = cursor.fetchone()
            if produtoExiste:
                cursor.execute(f"update estoque set rentabilidade = '{percent_rentabilidade}' where codigo = {codigoEdicao}")
                conexao.commit()
                limparTerminal()
                print('-' * 39)
                print('\033[1;91m''            rentabilidade do produto alterado!''\033[0;0m')
                print('-' * 39)
                break
            else:
                limparTerminal()
                print('============== < ''\033[0;91m''Erro''\033[0;0m'' > ===============')
                print('\033[1;91m''        Produto não encontrado!''\033[0;0m')
                break
        elif opcao == '0':
            limparTerminal()
            print('-' * 39)
            print('\033[1;91m''            Ação Cancelada!''\033[0;0m')
            print('-' * 39)
            break
        else:
            limparTerminal()
            print('-' * 36)
            print('\033[1;91m''           Opção Inválida!''\033[0;0m')
            print('-' * 36)
def deletarProduto():
    while True:
        codigoRemocao = input('Insira o código do produto: ')
        limparTerminal()
        if codigoRemocao.isdigit():
            print('========== <<< ''\033[0;91m''ALERTA''\033[0;0m'' >>> ==========')
            print('\033[0;91m'f'Deseja remover o produto {codigoRemocao} do estoque?''\033[0;0m')
            print('====================================')
            print('| [''\033[0;91m' '1' '\033[0;0m''] - ''\033[1m' 'Confirmar' '\033[0;0m''                  |')
            print('| [''\033[0;91m' '0' '\033[0;0m''] - ''\033[1m' 'Cancelar' '\033[0;0m''                   |')
            print('------------------------------------')
            opcao = input('\033[0;91m''Opção: ''\033[0;0m')
            if opcao == '1':
                cursor.execute(f"select 1 from estoque where codigo = {codigoRemocao}")
                produtoExiste = cursor.fetchone()
                if produtoExiste:
                    cursor.execute(f"delete from estoque where codigo = {codigoRemocao}")
                    conexao.commit()
                    limparTerminal()
                    criarBarra(39)
                    print('\033[1;91m''            Produto excluido!''\033[0;0m')
                    criarBarra(39)
                    break
                else:
                    limparTerminal()
                    print('============== < ''\033[0;91m''Erro''\033[0;0m'' > ===============')
                    print('\033[1;91m''        Produto não encontrado!''\033[0;0m')
                    break
            elif opcao == '0':
                limparTerminal()
                criarBarra(39)
                print('\033[1;91m''            Ação Cancelada!''\033[0;0m')
                criarBarra(39)
                break
            else:
                limparTerminal()
                criarBarra(36)
                print('\033[1;91m''           Opção Inválida!''\033[0;0m')
                criarBarra(36)
        else:
            print('\033[1;91m''Digite apenas números!''\033[0;0m')
            criarBarra(29)


def zerarProdutos():
    while True:
        print('========== <<< ''\033[0;91m''ALERTA''\033[0;0m'' >>> ==========')
        print('\033[0;91m''Deseja zerar os produtos do estoque?''\033[0;0m')
        print('====================================')
        print('| [''\033[0;91m' '1' '\033[0;0m''] - ''\033[1m' 'Confirmar' '\033[0;0m''                  |')
        print('| [''\033[0;91m' '0' '\033[0;0m''] - ''\033[1m' 'Cancelar' '\033[0;0m''                   |')
        print('------------------------------------')
        opcao = input('\033[0;91m''Opção: ''\033[0;0m')
        if opcao == '1':
            try:
                cursor.execute("delete from estoque")
                conexao.commit()
                limparTerminal()
                criarBarra(39)
                print('\033[1;91m''            Estoque Zerado!''\033[0;0m')
                criarBarra(39)
                break
            except sqlite3.Error as erro:
                print('Erro ao zerar produtos:', erro)
        elif opcao == '0':
            limparTerminal()
            criarBarra(39)
            print('\033[1;91m''            Ação Cancelada!''\033[0;0m')
            criarBarra(39)
            break
        else:
            limparTerminal()
            criarBarra(36)
            print('\033[1;91m''           Opção Inválida!''\033[0;0m')
            criarBarra(36)

# ----- Estrutura principal -----
limparTerminal()                # Código principal
while True:
    opcao = menuPrincipal()

    if opcao == '1':            # Menu de cadastro
        menuCadastroProduto()      
    elif opcao == '2':          # Menu de editar
        menuEditarProduto()    
    elif opcao == '3':          # Menu de remover
        menuRemoverProduto()
    elif opcao == '4':          # Menu de listagem
        menuListarProdutos()
    elif opcao == '0':          # Encerrar programa
        limparTerminal()
        criarBarra(31)
        print('\033[1;96m''      Programa Finalizado!''\033[0;0m')
        criarBarra(31)
        break
    else:                       # Opção inválida
        limparTerminal()
        criarBarra(31)
        print('\033[1;31m''    Insira uma opção válida!''\033[0;0m')
        criarBarra(31)

# ----- Observações -----

'''
Mostrar produtos
cursor.execute("select * from estoque")
resultado = cursor.fetchall()

Deletar tudo
cursor.execute("delete from estoque")

Selecionar ultimo ID
cursor.execute("select codigo from estoque order by codigo desc limit 1")

Deletar uma linha 
cursor.execute("delete from estoque where codigo = n")
'''