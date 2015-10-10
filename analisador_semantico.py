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

  # Metodo para mudar arquivo de entrada
  def mudaEntrada(self, string):
    self.arquivo_entrada = string

  def getEntrada(self):
    return self.arquivo_entrada

  def getSaida(self):
    return self.arquivo_saida

   # Faz o cabecote de leitura apontar para o proximo token da lista
  def next_token(self):
    self.i += 1
    self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]

  def conteudo_token(self):
    return self.tokens[self.i][ : self.tokens[self.i].find('->')]

  # Metodo que imprime dicionarios de forma formatada
  def imprime_dicionario(self, dicionario):

    for chave in dicionario.keys():
      print("Chave: ", chave)
      print("Conteudo: ", dicionario[chave])
      print("\n")


  '''
    Preenche a tabela registro_tab com um dicionario
    de campos do registros para cada registro.
  '''
  def preencheRegistroTab(self):  
    if("tok500_" in self.tokens[self.i]):
        #Busca o lexema nome do registro
        lexema_nomeReg = self.conteudo_token()
        # Verifico se ja possuo um registro com esse mesmo nome
        # indico erro caso o mesmo jah tenha sido declarado anteriormente
        if( not lexema_nomeReg in self.registro_tab.keys() ):
          #Cria um dicionario de campos do registro para cada registro
          campos_registro_tab ={}
          
          self.registro_tab[lexema_nomeReg] = campos_registro_tab
          self.next_token()
          while(not "}" in self.tokens[self.i]):

              if("cadeia" in self.tokens[self.i] or
                 "inteiro" in self.tokens[self.i] or
                 "char" in self.tokens[self.i] or
                 "real" in self.tokens[self.i] or
                 "booleano" in self.tokens[self.i]):

                  #Busca o lexema do tipo primitivo
                  lexema_nomeTipo = self.conteudo_token()
                  self.next_token()

                  if("tok500_" in self.tokens[self.i]):

                      #Busca o lexema nome da variavel
                      
                      lexema_nomeCamp = self.conteudo_token()
                      
                      if( not lexema_nomeCamp in self.registro_tab.get(lexema_nomeReg).keys() ):
                        #Armazenando chave nome da variavel e valores tipo da variavel e categoria: 'campo_reg'
                        campos_registro = [lexema_nomeTipo, "campo_reg"]
                        campos_registro_tab[lexema_nomeCamp] = campos_registro
                        
                      else:
                        print ("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado em " + lexema_nomeReg + "- linha: "+self.linha_atual+"\n")
                        self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado em " + lexema_nomeReg + "- linha: "+self.linha_atual+"\n")
                        self.tem_erro_semantico = True
                      
              self.next_token()
        else: 
          print ("Erro Semantico: "+ lexema_nomeReg + " ja foi declarado como identificador de um registro " + " - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeReg + " ja foi declarado como identificador de um registro " + " - linha: "+self.linha_atual+"\n")
          self.tem_erro_semantico = True
  '''
    Preenche a tabela variaveisGlobais_tab e
    emite erros semanticos caso sejam encontrados duplicidade de nomes de variaveis
    ou atrbuicoes erradas.
  '''
  def preencheConstantesTab(self):
    # Caso nao existam constantes o dicionario sera vazio   
    while(not "}" in self.tokens[self.i]):

      if("cadeia" in self.tokens[self.i] or
         "inteiro" in self.tokens[self.i] or
         "char" in self.tokens[self.i] or
         "real" in self.tokens[self.i] or
         "booleano" in self.tokens[self.i]):

          #Busca o lexema do tipo primitivo
          lexema_nomeTipo = self.conteudo_token()
          self.next_token()
          
          if("tok500_" in self.tokens[self.i]):

              #Busca o lexema nome da variavel
              lexema_nomeCamp = self.conteudo_token()
              self.next_token()

              if(not lexema_nomeCamp in self.constantes_tab.keys() ):

                if( not lexema_nomeCamp in self.registro_tab.keys() ):
                  # capturo o token de atribuicao (=)
                  self.next_token()
                  valor_constante = self.conteudo_token()
                  # tipo declarado para constante deve ser igual ao valor que a mesma recebeu
                  if(("inteiro" in lexema_nomeTipo  and "tok300" in valor_constante) or
                     ("real" in lexema_nomeTipo and "tok301" in valor_constante)or
                     ("char" in lexema_nomeTipo and "tok400" in valor_constante) or
                     ("cadeia" in lexema_nomeTipo and "tok700" in valor_constante) or
                     (("booleano" in lexema_nomeTipo and "tok618" in valor_constante) or ("booleano" in lexema_nomeTipo and "tok619" in valor_constante))):

                    #Armazenando chave nome da variavel e valores tipo da variavel, categoria: 'campo_const', escopo = 'global'
                    campos_const = [lexema_nomeTipo, "campo_const_global", valor_constante]
                    self.constantes_tab[lexema_nomeCamp] = campos_const
                  else:
                    print ()
                    print ("Erro Semantico: Atribuicao de tipos nao esta correta para variavel: " + lexema_nomeCamp + " e o valor: "+ valor_constante +" - linha: "+self.linha_atual+"\n")
                    self.arquivo_saida.write("Erro Semantico: Atribuicao de tipos nao esta correta para variavel: " + lexema_nomeCamp + " e o valor: "+ valor_constante +" - linha: "+self.linha_atual+"\n")
                    self.tem_erro_semantico = True
                else: 
                  print ("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado como nome de registro - linha: "+self.linha_atual+"\n")
                  self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado como nome de registro - linha: "+self.linha_atual+"\n")
                  self.tem_erro_semantico = True
              else:
                print ("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado em Constantes - linha: "+self.linha_atual+"\n")
                self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado em Constantes - linha: "+self.linha_atual+"\n")
                self.tem_erro_semantico = True

      self.next_token()
  '''
    Preenche a tabela constantes_tab e
    emite erros semanticos caso sejam encontrados duplicidade de nomes de variaveis
    ou atrbuicoes erradas.
  '''
  def preencheVariaveisGlogaisTab(self, escopo, dicionario):
    categoria = ""
    linha = ""
    coluna = ""
    while(not "}" in self.tokens[self.i]):
      if("cadeia" in self.tokens[self.i] or
         "inteiro" in self.tokens[self.i] or
         "char" in self.tokens[self.i] or
         "real" in self.tokens[self.i] or
         "booleano" in self.tokens[self.i] or
         "tok500_" in self.tokens[self.i]):

          #Verificando se e um registro ou variavel global
          if("tok500_" in self.tokens[self.i]):
            categoria = ("var_registro_" + escopo)
          else:
            categoria = ("var_simples_" + escopo)
          
          #Busca o lexema do tipo primitivo
          lexema_nomeTipo = self.conteudo_token()
          self.next_token()
          # Pegando o nome da variavel analisada no momento
          lexema_nomeCamp = self.conteudo_token()
          #Busca o lexema nome da variavel
          self.next_token()
          # Verifico se jah nao declarei uma variavel global com o nome em questao
          if(not lexema_nomeCamp in dicionario.keys() ):
            # Verifico se jah nao declarei uma constante com o nome em questao
            if(not lexema_nomeCamp in self.constantes_tab.keys() ):
              # Verifico se jah nao declarei um registro com o nome em questao
              if( not lexema_nomeCamp in self.registro_tab.keys() ):

                #Verificando se e um vetor ou uma matriz
                if ( 'tok206_[' in self.tokens[self.i] ):
                  self.next_token()
                  categoria = "var_vetor_"
                  if ( 'tok300_' in self.tokens[self.i] ):
                    linha = self.conteudo_token()
                    self.next_token()
                    if ( 'tok207_]' in self.tokens[self.i] ):
                      self.next_token()
                      if ( 'tok206_[' in self.tokens[self.i] ):
                        self.next_token()
                        categoria = "var_matriz_"
                        if ( 'tok300_' in self.tokens[self.i] ):
                          coluna = self.conteudo_token()
                          self.next_token()
                        if ( 'tok207_]' in self.tokens[self.i] ):
                            self.next_token()
                      
                if('tok200_;' in self.tokens[self.i]):
                  #Armazenando chave nome da variavel e valores tipo da variavel, categoria: 'var_global' ou 'var_registro' ou 'var_vetor' ou 'var_matriz', escopo = 'global'
                  # Caso seja um vetor preciso guardar apenas o indicador do tamanho de linhas
                  if(categoria == "var_vetor_" ):
                    campos_var_global = [lexema_nomeTipo, categoria, linha]
                    # Caso seja um matriz preciso guardar os indicadores de tamanho de linhas e colunas
                  elif(categoria == "var_matriz_" ):
                    campos_var_global = [lexema_nomeTipo, categoria, [linha, coluna]]
                    # Se for uma variavel simples nesse ponto ela nao teve inicializacao
                  else:
                    campos_var_global = [lexema_nomeTipo, (categoria+escopo), "sem_inicializacao"]
                  dicionario[lexema_nomeCamp] = campos_var_global
                  
                elif( 'tok115_=' in self.tokens[self.i] ):
                  self.next_token()
                  if(("inteiro" in lexema_nomeTipo and "tok300" in self.tokens[self.i]) or
                     ("real" in lexema_nomeTipo and "tok301" in self.tokens[self.i])or
                     ("char" in lexema_nomeTipo and "tok400" in self.tokens[self.i]) or
                     ("cadeia" in lexema_nomeTipo and "tok700" in self.tokens[self.i]) or
                     (("booleano" in lexema_nomeTipo and "tok618" in self.tokens[self.i]) or ("booleano" in lexema_nomeTipo and "tok619" in self.tokens[self.i]))):
                    # Pegando conteudo da inicializacao da variavel simples
                    inicializao_valor = self.conteudo_token()
                    #Armazenando chave nome da variavel e valores tipo da variavel, categoria: 'var_global' ou 'var_registro' ou 'var_vetor' ou 'var_matriz', escopo = 'global'
                    campos_var_global = [lexema_nomeTipo, categoria, inicializao_valor]
                    dicionario[lexema_nomeCamp] = campos_var_global
                  else:
                    print ("Erro Semantico: Atribuicao de tipos nao esta correta para variavel " + lexema_nomeCamp + "- linha: "+self.linha_atual+"\n")
                    self.arquivo_saida.write("Erro Semantico: Atribuicao de tipos nao esta correta para variavel " + lexema_nomeCamp + "- linha: "+self.linha_atual+"\n")
                    self.tem_erro_semantico = True
              else: 
                print ("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado como nome de registro - linha: "+self.linha_atual+"\n")
                self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado como nome de registro - linha: "+self.linha_atual+"\n")
                self.tem_erro_semantico = True
            else:
              print ("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado em Constantes - linha: "+self.linha_atual+"\n")
              self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado em Constantes - linha: "+self.linha_atual+"\n")
              self.tem_erro_semantico = True
          else:
            print ("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado em Variaveis " + escopo + " - linha: "+self.linha_atual+"\n")
            self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado em Variaveis " + escopo + " - linha: "+self.linha_atual+"\n")
            self.tem_erro_semantico = True
                
      self.next_token()

  # todas as variaveis locais devem ser declaraddas ao inicio da declaracao de cada funcao
  def preencheFuncaoTab(self):
    # lista que guarda o conteudo da funcao
    conteudo_funcao = []
    # Armazeno o tipo de retorno da funcao em questao
    tipo_retorno = self.conteudo_token()
    # o tipo de retorno eh o primeiro elemento da lista de conteudo da funcao
    conteudo_funcao.append(tipo_retorno)
    # Armazena os parametros da funcao na ordem e quantidade em que eles foram declarados
    lista_parametros = []
    # Lista de parametros eh o segundo componente da lista de conteudo de funcoes
    conteudo_funcao.append( lista_parametros )
    self.next_token()
    # Armazeno o nome da funcao em questao
    nome_func = self.conteudo_token()
    # Verifico se o nome da funcao nao jah foi declarado como nome de funcao anteriormente
    if( not nome_func in self.funcao_tab.keys() ):
      # Avanco ao token '('
      self.next_token()
      self.next_token()

      if(not ')' in self.tokens[self.i]):
        # captura dos parametros de funcao - lembrando que estes nao podem ser repetidos entre si
        # mas podem ter nomes 
        while( not ')' in self.tokens[self.i] and not '{' in self.tokens[self.i]):
          # armazena todo o conteudo pertencente ao parametro analisado
          conteudo_param = []
          tipo_para = self.conteudo_token()
          self.next_token()
          nome_para = self.conteudo_token()
          self.next_token()

          conteudo_param.append(nome_para)
          conteudo_param.append(tipo_para)
          if(not ')' in self.tokens[self.i]):
            if(not ',' in self.tokens[self.i]):
              categoria = ""
              #Verificando se e um vetor ou uma matriz
              if ( 'tok206_[' in self.tokens[self.i] ):
                self.next_token()
                self.next_token()
                categoria = ("par-vetor-" + nome_func)
                if ( 'tok206_[' in self.tokens[self.i] ):
                  self.next_token()
                  self.next_token()
                  categoria = ("par-matriz-" + nome_func)
              # consumo a virgula
              self.next_token()
              conteudo_param.append(categoria)
            else:
              # consumo a virgula
              self.next_token()
              if ( ("inteiro" in tipo_para) or ("real" in tipo_para) or ("char" in tipo_para)  or ("cadeia" in tipo_para) or ("booleano" in tipo_para)):
                conteudo_param.append("par-simples-" + nome_func)
              else:
                if( tipo_para in self.registro_tab.keys() ):
                  conteudo_param.append("par-registro-" + nome_func)
                else:
                  print ("Erro Semantico: parametro "+ nome_para + " eh um tipo de registro nao declarado - linha: "+self.linha_atual+"\n")
                  self.arquivo_saida.write("Erro Semantico: parametro "+ nome_para + " eh um tipo de registro nao declarado - linha: "+self.linha_atual+"\n")
                  self.tem_erro_semantico = True
            # Adicionando o conteudo do parametro lido para a lista de parametros
          lista_parametros.append (conteudo_param)
      
      else:
        # consumo o ')' que nao foi consumido anteriormente
        self.next_token()
      # consumo o simbolo '{'
      self.next_token()
      variaveis_locais_tab = {}
      if("variaveis" in self.tokens[self.i]):
        self.next_token()
        self.preencheVariaveisGlogaisTab( "local", variaveis_locais_tab )
      # todas as variaveis locais devem ser declaraddas ao inicio da declaracao de funcao
      # adicionando a tabela de variaveis locais caso existam
      conteudo_funcao.append (variaveis_locais_tab)
      
      # o nome da funcao eh a chave para acessar o conteudo dessa funcao
      self.funcao_tab[nome_func] = conteudo_funcao

      # Faco analise dos elementos internos da funcao, apos a verificacao das variaveis locais
      self.dentro_funcao(nome_func)
      
    else:
      print ("Erro Semantico: "+ nome_func + " ja foi declarado como nome de funcao - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write("Erro Semantico: "+ nome_func + " ja foi declarado como nome de funcao - linha: "+self.linha_atual+"\n")
      self.tem_erro_semantico = True

  def dentro_funcao(self, nome_func):
    self.next_token()
    
  def preencheAlgoritmoTab(self):
    self.next_token()

  def analisa(self):

    while(not "$" in self.tokens[self.i]):
            
      #Verifica qual tabela sera preenchida
      if("registro" in self.tokens[self.i]):
        self.next_token()
        self.preencheRegistroTab()
      elif("constantes" in self.tokens[self.i]):
        self.next_token()
        self.preencheConstantesTab()
      elif("variaveis" in self.tokens[self.i]):
        self.next_token()
        self.preencheVariaveisGlogaisTab( "global", self.variaveisGlobais_tab )
      elif("funcao" in self.tokens[self.i]):
        self.next_token()
        self.preencheFuncaoTab()
      elif("algoritmo" in self.tokens[self.i]):
        self.next_token()
        self.preencheAlgoritmoTab()
      else:
          self.next_token()
    
    # Analise Semantica ja foi realizada, agora indica se foi compilado com sucesso
    if(self.tem_erro_semantico):
      print("Verifique os erros semanticos e tente compilar novamente")
      self.arquivo_saida.write("Verifique os erros semanticos e tente compilar novamente\n")
    else:
      print("Cadeia de tokens na analise semantica reconhecida com sucesso")
      self.arquivo_saida.write("Cadeia de tokens reconhecida com sucesso\n")

    print("\n+++Tabela de registros+++")
    self.imprime_dicionario(self.registro_tab)  
    print("+++Tabela de constantes+++")
    self.imprime_dicionario(self.constantes_tab)
    print("+++Tabela de variaveis globais+++")
    self.imprime_dicionario(self.variaveisGlobais_tab)
    print("+++Tabela de funcoes+++")
    self.imprime_dicionario(self.funcao_tab)
    print("+++Tabela de algoritmo+++")
    self.imprime_dicionario(self.algoritmo_tab)

    # Fechando arquivo de saida
    self.arquivo_saida.close()
    
    '''        
      
    '''
      
    
