# -*- coding: utf-8 -*-
######           Analisador Semantico    ######
# Autor 1: Lucas Vinicius dos Santos Assis
# Autor 2: Andressa Moura de Souza
# EXA 869 - MI - Processadores de Linguagem de Programacao
# ==============================================================================
# Implementacao do analisador semantico de um compilador em python

# Bibliotecas para entrada e saida de arquivos
import sys
import os.path

# Bliblioteca padrao de string
import string

import pilha

# Declarando Classe do Analisador Semantica
class AnalisadorSemantico ():
      # ========================== DECLARACAO DE METODOS DA CLASSE
  # Metodo construtor da classe
  def __init__(self):

    self.arquivo_entrada = "resp-lex.txt"
    self.arquivo_saida = "resp-sem.txt"

    self.tem_erro_semantico = False

    self.arquivo_saida = open(self.arquivo_saida, 'w')
    # Verifica se o arquivo de entrada existe no diretorio em questao
    if not os.path.exists(self.arquivo_entrada):
      print("Arquivo de entrada inexistente")
      self.arquivo_saida.write("Arquivo de entrada inexistente")
      return

    # Abre o arquivo de entrada do programa
    self.arquivo = open(self.arquivo_entrada, 'r')
    self.tokens = self.arquivo.readlines()
    self.arquivo.close()
    self.i = 0
    self.linha_atual = ""

    self.p = pilha.Pilha()
    
    #Tabelas Semanticas
    self.tabela_semantica = {}
    '''
    Dentro da tabela de registro devo colocar:
        * Cada vez que verifiquei a criacao de um novo registro
        este vira um novo dicionario que deve ser adicionado na
        tabela de registro
    '''
    self.registro_tab = {}
    
    '''
        Guardamos os tipos primitivos e os identificadores
    '''
    self.constantes_tab = {}
    '''
        Guardamos os tipos primitivos e os identificadores
    '''
    self.variaveisGlobais_tab = {}
    self.funcao_tab = {}
    self.algoritmo_tab = {}

    '''
        Construindo estrutura de tabela semantica de simbolos
    '''
    self.tabela_semantica["registro"] = self.registro_tab
    self.tabela_semantica["constantes"] = self.constantes_tab
    self.tabela_semantica["variaveisGlobais"] = self.variaveisGlobais_tab
    self.tabela_semantica["funcao"] = self.funcao_tab
    self.tabela_semantica["algoritmo"] = self.algoritmo_tab

  # Metodo para mudar arquivo de entrada
  def mudaEntrada(self, string):
    self.arquivo_entrada = string

  def getEntrada(self):
    return self.arquivo_entrada

  def getSaida(self):
    return self.arquivo_saida

  #Metodo que preenche o dicionario registro_tab
  def preencheRegistroTab(self):
      
      if("tok500_" in self.tokens[self.i]):
          
          #Busca o lexema nome do registro
          lexema = self.tokens[self.i].split("_")
          lexema = lexema[1]
          lexema = lexema.split("-")
          lexema = lexema[0]
          #Cria um dicionario de campos do registro para cada registro
          campos_registro_tab ={}
          
          self.registro_tab[lexema] = campos_registro_tab
          self.i += 1
          
          while(not "}" in self.tokens[self.i]):

              if("cadeia" in self.tokens[self.i] or
                 "inteiro" in self.tokens[self.i] or
                 "char" in self.tokens[self.i] or
                 "real" in self.tokens[self.i] or
                 "booleano" in self.tokens[self.i]):
                  #Busca o lexema do tipo primitivo
                  lexema = self.tokens[self.i].split("_")
                  lexema = lexema[1]
                  lexema = lexema.split("-")
                  lexema = lexema[0]
                  self.p.empilha(lexema)
                  self.i += 1

                  if("tok500_" in self.tokens[self.i]):
                      #Busca o lexema nome da variavel
                      lexema = self.tokens[self.i].split("_")
                      lexema = lexema[1]
                      lexema = lexema.split("-")
                      lexema = lexema[0]
                      
                      campo = self.p.desempilha()           
                      campos_registro_tab[lexema] = campo
                      
                      
              self.i += 1
      
  def preencheConstantesTab(self):
      if("Erro Lexico" in self.tokens[self.i]):
          self.i += 1

  def preencheVariaveisGlogaisTab(self):
      if("Erro Lexico" in self.tokens[self.i]):
          self.i += 1

  def preencheFuncaoTab(self):
      if("Erro Lexico" in self.tokens[self.i]):
          self.i += 1

  def preencheAlgoritmoTab(self):
      if("Erro Lexico" in self.tokens[self.i]):
          self.i += 1

  def analisa(self):

    while(not "$" in self.tokens[self.i]):
        
      #Caso seja encontrado um registro preenche registro_tab
      if("registro" in self.tokens[self.i]):
          self.i += 1
          self.preencheRegistroTab()
      else:
          self.i += 1
          
    print self.tabela_semantica
    '''        
      elif("constantes" in self.tokens[self.i]):
          
      elif("variaveis" in self.tokens[self.i]):
          print
      elif("funcao" in self.tokens[self.i]):
          print
      elif("algoritmo" in self.tokens[self.i]):
          print
    '''
      
    
