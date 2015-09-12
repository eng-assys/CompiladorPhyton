######           Analisador Sintatico    ######
# Autor 1: Lucas Vinicius dos Santos Assis
# Autora 1: Andressa Moura de Souza
# EXA 869 - MI - Processadores de Linguagem de Programacao
# ==============================================================================
# Implementacao do analisador sintatico de um compilador

# Bibliotecas para entrada e saida de arquivos
import sys
import os.path

# Bliblioteca padrao de string
import string

# Importando estrutura de dados pilha
from pilha import Pilha

# Importando classe construtora e possuidora da tabela sintatica
from tabela_sintatica import Tabela_Sintatica



# Declarando Classe do Analisador Sintatico
class AnalisadorSintatico():
  # ========================== DECLARACAO DE METODOS DA CLASSE
  # Metodo construtor da classe
  def __init__(self):
    self.arquivo_entrada = "resp-lex.txt"
    self.arquivo_saida = "resp-sint.txt"

  # Metodo para mudar arquivo de entrada
  def mudaEntrada(self, string):
    self.arquivo_entrada = string

  def getEntrada(self):
    return self.arquivo_entrada

  def getSaida(self):
    return self.arquivo_saida

  # Metodo que executa o analisador sintatico
  def analisa(self):

    p = Pilha() 
    p.empilha("$")
    p.empilha("<start>")

    tabela = GeraTabelaSintatica()
    tabela.gerar_tabela()
     
    # Abre o arquivo de saida do programa
    arquivo_saida = open(self.arquivo_saida, 'w')
    # Verifica se o arquivo de entrada existe no diretorio em questao
    if not os.path.exists(self.arquivo_entrada):
      arquivo_saida.write("Arquivo de entrada inexistente")
      return

    # Abre o arquivo de entrada do programa
    arquivo = open(self.arquivo_entrada, 'r')

    # Le o primeiro token
    linha_list_tok = arquivo.readline()

    # Variavel que indica o token_atual
    
    token_linha = linha_list_tok.split(' ')
    token_atual = token_linha[1]
      
    # Percorre o programa linha por linha
    while linha_list_tok:

      if(token_linha[0] == "tok500"):
        token_atual = token_linha[0]
        #print(token_atual)

      elif(token_linha[0] == "tok300"):
        token_atual = token_linha[0];
        #print(token_atual)
        
      elif(token_linha[0] == "tok400"):
        token_atual = token_linha[0];
        #print(token_atual)
        
      elif(token_linha[0] == "tok700"):
        token_atual = token_linha[0];
        #print(token_atual)
        
      else:
        token_atual = token_linha[1].replace("\n", "");
        #print(token_atual)

      prod_topo_pilha = p.desempilha()

      while(token_atual != prod_topo_pilha) :
        
        producoes = tabela.consultar_tabela_sintatica(prod_topo_pilha, token_atual)
        print (producoes)
        if(producoes[0] != "$"):
          for prod in range(len(producoes)):
            p.empilha(producoes[prod])
        elif producoes[0] == "x":
          print ("Erro sintatico")
          break
               
        prod_topo_pilha = p.desempilha()

      linha_list_tok = arquivo.readline() # Le proximo token
      token_linha = linha_list_tok.split(' ')
      if(len(token_linha) == 2):
        token_atual = token_linha[1]
      

    # Fim do arquivo de entrada
    arquivo.close()
    # Fim do arquivo de entrada
    arquivo_saida.close
    # ========================== FIM DO ANALISADOR LEXICO

# Executando o programa

analisador_sintatico = AnalisadorSintatico()
analisador_sintatico.analisa()
