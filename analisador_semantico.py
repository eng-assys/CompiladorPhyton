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
          lexema_nomeReg = self.tokens[self.i][self.tokens[self.i].find('_')+1: self.tokens[self.i].find('->')]
          #Cria um dicionario de campos do registro para cada registro
          campos_registro_tab ={}
          
          self.registro_tab[lexema_nomeReg] = campos_registro_tab
          self.i += 1
          
          while(not "}" in self.tokens[self.i]):

              if("cadeia" in self.tokens[self.i] or
                 "inteiro" in self.tokens[self.i] or
                 "char" in self.tokens[self.i] or
                 "real" in self.tokens[self.i] or
                 "booleano" in self.tokens[self.i]):

                  #Busca o lexema do tipo primitivo
                  lexema_nomeTipo = self.tokens[self.i][self.tokens[self.i].find('_')+1: self.tokens[self.i].find('->')]
                  self.i += 1

                  if("tok500_" in self.tokens[self.i]):

                      #Busca o lexema nome da variavel
                      
                      lexema_nomeCamp = self.tokens[self.i][self.tokens[self.i].find('_')+1: self.tokens[self.i].find('->')]
                      
                      if(not self.registro_tab.get(lexema_nomeReg).has_key(lexema_nomeCamp)):
                        #Armazenando chave nome da variavel e valores tipo da variavel e categoria: 'campo_reg'
                        campos_registro = [lexema_nomeTipo, "campo_reg"]
                        campos_registro_tab[lexema_nomeCamp] = campos_registro
                        
                      else:
                        print ("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado em " + lexema_nomeReg + "\n")
                        self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado em " + lexema_nomeReg + "\n")
                        self.tem_erro_semantico = True
                      
              self.i += 1
              
  #Metodo que preenche o dicionario constantes_tab
  def preencheConstantesTab(self):

      while(not "}" in self.tokens[self.i]):

              if("cadeia" in self.tokens[self.i] or
                 "inteiro" in self.tokens[self.i] or
                 "char" in self.tokens[self.i] or
                 "real" in self.tokens[self.i] or
                 "booleano" in self.tokens[self.i]):

                  #Busca o lexema do tipo primitivo
                  lexema_nomeTipo = self.tokens[self.i][self.tokens[self.i].find('_')+1: self.tokens[self.i].find('->')]
                  self.i += 1

                  if("tok500_" in self.tokens[self.i]):

                      #Busca o lexema nome da variavel
                      
                      lexema_nomeCamp = self.tokens[self.i][self.tokens[self.i].find('_')+1: self.tokens[self.i].find('->')]
                      
                      if(not self.constantes_tab.has_key(lexema_nomeCamp)):
                        #Armazenando chave nome da variavel e valores tipo da variavel, categoria: 'campo_reg', escopo = 'global'
                        campos_const = [lexema_nomeTipo, "campo_const", "global"]
                        self.constantes_tab[lexema_nomeCamp] = campos_const
                        
                      else:
                        print ("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado em Constantes \n")
                        self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado em Constantes \n")
                        self.tem_erro_semantico = True
                      
              self.i += 1

  def preencheVariaveisGlogaisTab(self):
      self.i += 1

  def preencheFuncaoTab(self):
      self.i += 1

  def preencheAlgoritmoTab(self):
      self.i += 1

  def analisa(self):

    while(not "$" in self.tokens[self.i]):
            
      #Verifica qual tabela sera preenchida
      if("registro" in self.tokens[self.i]):
          self.i += 1
          self.preencheRegistroTab()
      elif("constantes" in self.tokens[self.i]):
        self.i += 1
        self.preencheConstantesTab()
      elif("variaveis" in self.tokens[self.i]):
        self.i += 1
        self.preencheVariaveisGlogaisTab()
      elif("funcao" in self.tokens[self.i]):
        self.i += 1
        self.preencheFuncaoTab()
      elif("algoritmo" in self.tokens[self.i]):
        self.i += 1
        self.preencheAlgoritmoTab()
      else:
          self.i += 1
    
    # Analise Semantica ja foi realizada, agora indica se foi compilado com sucesso
    if(self.tem_erro_semantico):
      print("Verifique os erros semanticos e tente compilar novamente")
      self.arquivo_saida.write("Verifique os erros semanticos e tente compilar novamente\n")
    else:
      print("Cadeia de tokens na analise semantica reconhecida com sucesso")
      self.arquivo_saida.write("Cadeia de tokens reconhecida com sucesso\n")

    print self.tabela_semantica

    # Fechando arquivo de saida
    self.arquivo_saida.close()
    
    '''        
      
    '''
      
    
