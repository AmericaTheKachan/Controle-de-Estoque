import getpass
import oracledb
# Criar variável para chamar a senha
pw = getpass.getpass("Enter password: ")
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



resposta = str(input("Deseja cadastrar um produto?\n"))
while resposta == "Sim" or resposta == "sim":

    nome_do_produto=str(input('Digite o nome do produto: '))
    #codigo_do_produto=input('Digite o código do produto(8 dígitos): ')
    descricao_do_produto=str(input('Digite uma descrição do produto: '))
    valor_custo_do_produto=float(input('Digite o custo do produto: '))
    percent_custo_fixo=float(input('Digite a porcentagem do custo fixo: '))
    percent_comissao_de_vendas=float(input('Digite a porcentagem da comissão de vendas: '))
    percent_impostos=float(input('digite a porcentagem dos impostos: '))
    margem_de_lucro=float(input('Digite a margem de lucro em porcentagem: '))

    if (percent_custo_fixo+percent_comissao_de_vendas+percent_impostos+margem_de_lucro) == 100:
        valor_preco_de_venda=valor_custo_do_produto/0.0001
    elif (percent_custo_fixo+percent_comissao_de_vendas+percent_impostos+margem_de_lucro) > 100:
        valor_preco_de_venda=valor_custo_do_produto/(((percent_custo_fixo+percent_comissao_de_vendas+percent_impostos+margem_de_lucro)/100)-1)
    else:
        valor_preco_de_venda=valor_custo_do_produto/(1-((percent_custo_fixo+percent_comissao_de_vendas+percent_impostos+margem_de_lucro)/100))
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
    #percent_rentabilidade=margem_de_lucro



    if margem_de_lucro>20:
        print('Lucro alto')
    elif margem_de_lucro>10 and margem_de_lucro<=20:
        print('Lucro médio')
    elif margem_de_lucro>0 and margem_de_lucro<=10:
        print('Lucro baixo')
    elif margem_de_lucro==0:
        print('Lucro em Equilibrio')
    elif margem_de_lucro<0:
        print('prejuizo')
        
    print(f'    Preço de Venda \t{valor_preco_de_venda :.2f}   {percent_preco_de_venda :.1f}%\n\
        Custo de Aquisição \t{valor_custo_do_produto :.2f}     {percent_custo_do_produto :.1f}%\n\
        Receita Bruta \t{valor_receita_bruta :.2f}   {percent_receita_bruta :.1f}%\n\
        Custo Fixo \t        {valor_custo_fixo :.2f}  {percent_custo_fixo :.1f}%\n\
        Comissão de Vendas \t{valor_comissao_de_vendas :.2f}    {percent_comissao_de_vendas :.1f}%\n\
        Impostos \t        {valor_impostos :.2f}    {percent_impostos :.1f}%\n\
        Outros Custos \t{valor_outros_custos :.2f}   {percent_outros_custos :.1f}%\n\
        Rentabilidade \t{valor_rentabilidade :.2f}   {margem_de_lucro :.1f}%\n')
    resposta = str(input("Deseja cadastrar mais um produto?\n"))
print(f'Encerramento do cadastramento de produtos')





# Cria a tabela test
'''
cursor.execute ("""
CREATE TABLE estoque (
 codigo NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 nome_produto varchar2(60) NOT NULL,
 descricao_produto varchar2(60) NOT NULL,
 cp number(10) NOT NULL,
 cf number(10) NOT NULL,
 cv number(10) NOT NULL,
 iv number(10) NOT NULL,
 ml number(10) NOT NULL
)""")
'''
# Inserir Dados

sql_insert = """
INSERT INTO estoque (
    nome_produto, descricao_produto, cp, cf, cv, iv, ml
) VALUES (:1, :2, :3, :4, :5, :6, :7)
"""

dados = (
    nome_do_produto,
    descricao_do_produto,
    valor_custo_do_produto,
    percent_custo_fixo,
    percent_comissao_de_vendas,
    percent_impostos,
    margem_de_lucro
)

cursor.execute(sql_insert, dados)


#Limpar as linhas da tabela
#cursor.execute ("truncate table estoque")

#Excluir a tabela
#cursor.execute ("drop table estoque")

#Deletar uma linha 
#cursor.execute("delete from estoque where codigo=3")

# Exibir conteúdos
conexao.commit()
cursor.execute ("select * from estoque")

resultado = cursor.fetchall()
# Imprimir resultados
print(resultado)





