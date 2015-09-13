######           Analisador Sintatico    ######
# Autor 1: Lucas Vinicius dos Santos Assis
# Autora 1: Andressa Moura de Souza
# EXA 869 - MI - Processadores de Linguagem de Programacao
# ==============================================================================
# Implementacao do analisador sintatico de um compilador
# Cada codigo citado a seguir representa um tipo de token
# Essa codificacao eh usada no arquivo de saida que contem os 
# resultados de operacao do analisador lexico
# tok1 - Operador
#   tok100 - Operador Ponto
#   tok101 - Operador Mais
#   tok102 - Operador Menos
#   tok103 - Operador Vezes
#   tok104 - Operador Barra
#   tok105 - Operador Mais Mais
#   tok106 - Operador MenosMenos
#   tok107 - Operador IgualIgual
#   tok108 - Operador Diferente
#   tok109 - Operador MaiorQue
#   tok110 - Operador MaiorIgualQue
#   tok111 - Operador Menor
#   tok112 - Operador MenorIgualQue
#   tok113 - Operador E
#   tok114 - Operador OU
#   tok115 - Operador Igual

# tok2 - Delimitador
#   tok200 - Delimitador PontoVirgula
#   tok201 - Delimitador Virgula,3e4y
#   tok202 - Delimitador ParenteseEsquedo
#   tok203 - Delimitador ParenteseDireito
#   tok204 - Delimitador ChaveEsqueda
#   tok205 - Delimitador ChaveDireita
#   tok206 - Delimitador ColcheteEsquerdo
#   tok207 - Delimitador ColcheteDireito

# tok300 - Numero

# tok400 - Caractere Constante

# tok500 - Identificador

# tok6 - Palavra reservada
#   tok600 - Palavra reservada algoritmo
#   tok601 - Palavra reservada variaveis
#   tok602 - Palavra reservada constantes
#   tok603 - Palavra reservada registro
#   tok604 - Palavra reservada funcao
#   tok605 - Palavra reservada retorno
#   tok606 - Palavra reservada vazio
#   tok607 - Palavra reservada se
#   tok608 - Palavra reservada senao
#   tok609 - Palavra reservada enquanto
#   tok610 - Palavra reservada para
#   tok611 - Palavra reservada leia
#   tok612 - Palavra reservada escreva
#   tok613 - Palavra reservada inteiro
#   tok614 - Palavra reservada real
#   tok615 - Palavra reservada booleano
#   tok616 - Palavra reservada char
#   tok617 - Palavra reservada cadeia
#   tok618 - Palavra reservada verdadeiro
#   tok619 - Palavra reservada falso

# tok700 - Cadeia constante
# ========================== ERROS LEXICOS
# Simbolo nao pertencente ao conjunto de simbolos terminais da linguagem
# Identificador Mal formado
# Tamanho do identificador
# Numero mal formado
# Fim de arquivo inesperado (comentario de bloco nao fechado)
# Caractere ou string mal formados
# ==============================================================================

# Incluindo caracteres especiais no programa
# -*- coding: utf-8 -*-

# Bibliotecas para entrada e saida de arquivos
import sys
import os.path

# Bliblioteca padrao de string
import string
import pilha
import tabela_sintatica



# Declarando Classe do Analisador Sintatico
class AnalisadorSintatico(object):
  # ========================== DECLARACAO DE METODOS DA CLASSE
  # Metodo construtor da classe
  def __init__(self):
    self.arquivo_entrada = "resp-lex.lo"
    self.arquivo_saida = "resp-sint.lo"

  # Metodo para mudar arquivo de entrada
  def mudaEntrada(self, string):
    self.arquivo_entrada = string

  def getEntrada(self):
    return self.arquivo_entrada

  def getSaida(self):
    return self.arquivo_saida

  # Metodo que executa o analisador sintatico
  def analisa(self):

    p = pilha.Pilha() 
    p.empilha("$")
    p.empilha("<start>")

    tabela = tabela_sintatica.Tabela_Sintatica()
    tabela.cria_tabela_sintatica()
    tabela.inicializar_tabela_sintatica()
    tabela.preenche_tabela_sintatica()
    
     
    # Abre o arquivo de saida do programa
    arquivo_saida = open('resp-sint.lo', 'w')
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
        print producoes
        print token_atual
        if(producoes[0] != "$" and producoes[0] != "x"):
          for prod in range(len(producoes)):
            p.empilha(producoes[prod])
        elif producoes[0] == "x":
          linha_list_tok = arquivo.readline()
          token_linha = linha_list_tok.split(' ')
          token_proximo = token_linha[1].replace("\n", "");
          arquivo_saida.write('Erro sintatico: '+token_atual +' nao esperado antes de '+ token_proximo +'\n')
          break
               
        prod_topo_pilha = p.desempilha()

      linha_list_tok = arquivo.readline() # Le proximo token
      token_linha = linha_list_tok.split(' ')
      if(len(token_linha) == 2):
        token_atual = token_linha[1]
      

    arquivo_saida.write('Compilado com sucesso!'+'\n')
    # Fim do arquivo de entrada
    arquivo.close()
    # Fim do arquivo de entrada
    arquivo_saida.close
    # ========================== FIM DO ANALISADOR LEXICO

# Executando o programa

#analisador_sintatico = AnalisadorSintatico()
#analisador_sintatico.analisa()
