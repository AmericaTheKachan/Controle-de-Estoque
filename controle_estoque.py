import os
import oracledb
import getpass

# Criar variável para chamar a senha
pw = getpass.getpass("Insira a senha: ")
# Criar conexão
try:
    conexao = oracledb.connect(
    user='system',
    password=pw,
    dsn="localhost/XEPDB1")

except Exception as erro:
    print ('Erro em conexão', erro)
else:
    print ("Conectado", conexao.version)
# Criar Cursor
cursor = conexao.cursor()

# Criar Tabela
cursor.execute ("""
CREATE TABLE estoque (
    codigo NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_produto varchar2(60) NOT NULL,
    descricao_produto varchar2(100) NOT NULL,
    custo_produto number(9,2) NOT NULL,
    custo_fixo number(9,2) NOT NULL,
    comissa_venda number(9,2) NOT NULL,
    imposto_venda number(9,2) NOT NULL,
    rentabilidade number(9,2) NOT NULL
)""")
conexao.commit()                # Salvar mudanças

def limparTerminal():           # Limpar o terminal
    return os.system('cls' if os.name == 'nt' else 'clear')

def criarBarra():               # Criar barras no terminal
    return print('-' * 31)

def menu():                     # Menu de seleção principal
    print('======= <<< ''\033[1;96m''Estoque''\033[0;0m'' >>> =======')
    print('| [''\033[1;36m' '1' '\033[0;0m''] - ''\033[1m' 'Cadastrar Produto' '\033[0;0m''     |')
    print('| [''\033[1;31m' '2' '\033[0;0m''] - ''\033[1;31m' 'Remover Produto' '\033[0;0m''       |')
    print('| [''\033[1;31m' '3' '\033[0;0m''] - ''\033[1;31m' 'Listar Produtos' '\033[0;0m''       |')
    print('| [''\033[1;36m' '0' '\033[0;0m''] - ''\033[1m' 'Encerrar' '\033[0;0m''              |')
    print('-------------------------------')
    x = int(input('\033[1;36m''Insira a opção: ''\033[0;0m'))
    print('-------------------------------')
    return x

def cadastrarProduto():         # Cadastrar produto
    limparTerminal()

    # Recebe as informações do produto
    print('======= < ''\033[1;96m''Cadastrar Produto''\033[0;0m'' > =======')
    nome_do_produto = str(input('Nome do produto: '))
    descricao_do_produto = str(input('Descrição do produto: '))
    valor_custo_do_produto = float(input('Custo do produto (R$): '))
    percent_custo_fixo = float(input('Custo fixo (%): '))
    percent_comissao_de_vendas = float(input('Comissão de vendas (%): '))
    percent_impostos = float(input('Impostos (%): '))
    percent_rentabilidade = float(input('Rentabilidade (%): '))

    # Calculo do preço de venda do produto
    if (percent_custo_fixo+percent_comissao_de_vendas+percent_impostos+percent_rentabilidade) == 100:
        valor_preco_de_venda=valor_custo_do_produto/0.0001
    elif (percent_custo_fixo+percent_comissao_de_vendas+percent_impostos+percent_rentabilidade) > 100:
        valor_preco_de_venda=valor_custo_do_produto/(((percent_custo_fixo+percent_comissao_de_vendas+percent_impostos+percent_rentabilidade)/100)-1)
    else:
        valor_preco_de_venda=valor_custo_do_produto/(1-((percent_custo_fixo+percent_comissao_de_vendas+percent_impostos+percent_rentabilidade)/100))

    # Define o percentual
    percent_preco_de_venda=100

    percent_custo_do_produto=(valor_custo_do_produto*100)/valor_preco_de_venda

    valor_receita_bruta=valor_preco_de_venda-valor_custo_do_produto
    percent_receita_bruta=percent_preco_de_venda-percent_custo_do_produto

    valor_custo_fixo=(percent_custo_fixo/100)*valor_preco_de_venda

    valor_comissao_de_vendas=(percent_comissao_de_vendas/100)*valor_preco_de_venda

    valor_impostos=(percent_impostos/100)*valor_preco_de_venda

    valor_outros_custos=valor_custo_fixo+valor_comissao_de_vendas+valor_impostos
    percent_outros_custos=percent_custo_fixo+percent_comissao_de_vendas+percent_impostos

    valor_rentabilidade=valor_receita_bruta-valor_outros_custos

    limparTerminal()

    if percent_rentabilidade>20:
        classificao_lucro = '\033[1;92m''Lucro Alto''\033[0;0m'
    elif percent_rentabilidade>10 and percent_rentabilidade<=20:
        classificao_lucro = '\033[1;92m''Lucro Médio''\033[0;0m'
    elif percent_rentabilidade>0 and percent_rentabilidade<=10:
        classificao_lucro = '\033[1;92m''Lucro Baixo''\033[0;0m'
    elif percent_rentabilidade==0:
        classificao_lucro = '\033[1;93m''Lucro em Equilíbrio''\033[0;0m'
    elif percent_rentabilidade<0:
        classificao_lucro = '\033[1;91m''Prejuízo''\033[0;0m'
    
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

    print(f'Produto: {nome_do_produto}\nDescrição: {descricao_do_produto}\nClassificação: {classificao_lucro}\n')

    for item in tabela_valores:
        print('|',
              item[0],' '*(18-len(item[0])) + '|',
              item[1],' '*(12-len(item[1])) + '|',
              item[2],' '*(12-len(item[2])) + '|')
        
    while True:
        confirmarCadastro = int(input('\nConfirmar Cadastro:\n1 - Confirmar\n2 - Refazer\n0 - Cancelar\nOpção: '))
        if confirmarCadastro == 1:
            sql_insert = """
            INSERT INTO estoque (
                nome_produto, 
                descricao_produto, 
                custo_produto, 
                custo_fixo, 
                comissa_venda, 
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
            limparTerminal()
            criarBarra()
            print('\033[1;92m''      Produto Cadastrado!''\033[0;0m')
            criarBarra()
            break
        elif confirmarCadastro == 2:
            cadastrarProduto()
            break
        elif confirmarCadastro == 0:
            limparTerminal()
            criarBarra()
            print('\033[1;91m''      Cadastro Cancelado!''\033[0;0m')
            criarBarra()
            break
        else:
            print('Opção inválida!')

def removerProduto():           # Remover produto
    print('Opção selecionada = 2 (remover produto)')

def listarProdutos():           # Listar produtos
    print('Opção selecionada = 3 (listar produtos)')


limparTerminal()                # Código principal
while True:
    opcao = menu()

    if opcao == 1:
        cadastrarProduto()
    elif opcao == 2:
        removerProduto()
        limparTerminal()
    elif opcao == 3:
        listarProdutos()
        limparTerminal()
    elif opcao == 0:
        limparTerminal()
        criarBarra()
        print('\033[1;96m''      Programa finalizado!''\033[0;0m')
        criarBarra()
        break
    else:
        limparTerminal()
        criarBarra()
        print('\033[1;31m''    Insira uma opção válida!''\033[0;0m')
        criarBarra()

# ------------------------------
# Mostrar produtos
# cursor.execute ("select * from estoque")
# resultado = cursor.fetchall()
# print(resultado)

# Deletar uma linha 
# cursor.execute("delete from estoque where codigo=n")