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
    self.arquivo_saida = "log-sem.txt"

    self.tem_erro_semantico = False

    self.arquivo_saida = open(self.arquivo_saida, 'w')
    # Verifica se o arquivo de entrada existe no diretorio em questao
    if not os.path.exists(self.arquivo_entrada):
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
    self.variaveis_tab = {}
    self.funcao_tab = {}
    self.parametro_funcao_tab = {}
    # guarda o escopo analisado no momento
    self.funcao_analisada = ""
    # guarda os possiveis erros encontrados no código
    self.tabela_erros = []

   # Faz o cabecote de leitura apontar para o proximo token da lista
  def next_token(self):
    self.i += 1
    #print("token atual: ", self.tokens[self.i])
    self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]

  def conteudo_token(self):
    return self.tokens[self.i][ : self.tokens[self.i].find('->')]

  # Metodo que imprime dicionarios de forma formatada
  def imprime_dicionario(self, dicionario):

    for chave in dicionario.keys():
      self.arquivo_saida.write("Chave: " + chave+"\n")
      self.arquivo_saida.write("Conteudo: " + str(dicionario[chave]))
      self.arquivo_saida.write("\n\n")


  '''
    Preenche a tabela registro_tab com um dicionario
    de campos do registros para cada registro.
  '''
  def preencheRegistroTab(self):  # PERFEITO
    if("tok500_" in self.tokens[self.i]):
        #Busca o lexema nome do registro
        lexema_nomeReg = self.conteudo_token()
        # Verifico se ja possuo um registro com esse mesmo nome
        # indico erro caso o mesmo jah tenha sido declarado anteriormente
        if( not lexema_nomeReg in self.registro_tab.keys() ):
          self.arquivo_saida.write("Tipo registro criado: "+lexema_nomeReg+"\n")
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
                        self.arquivo_saida.write("Novo campo registro: " + lexema_nomeTipo + " " + lexema_nomeCamp+"\n")
                        # adiciono o nome campo de registro como chave para o seu tipo
                        campos_registro_tab[lexema_nomeCamp] = lexema_nomeTipo
                        
                      else:
                        self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado como campo de " + lexema_nomeReg+"\n")
                        self.arquivo_saida.write("Erro na linha: "+self.linha_atual+"\n")
                        self.tem_erro_semantico = True
                        while( not ";" in self.conteudo_token() ):
                          self.next_token()
                      
              self.next_token()
        else: 
          self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeReg + " ja foi declarado como um tipo registro\n")
          self.arquivo_saida.write("Erro na linha: "+self.linha_atual+"\n")
          self.tem_erro_semantico = True
          # percorro até o próximo registro ou a tabela de constantes
          while( not ("registro" in self.conteudo_token() or "constante" in self.conteudo_token() ) ):
            self.next_token()
  
  '''
    Preenche a tabela variaveisGlobais_tab e
    emite erros semanticos caso sejam encontrados duplicidade de nomes de variaveis
    ou atrbuicoes erradas.
  '''
  def preencheConstantesTab(self):
    # Caso nao existam constantes o dicionario sera vazio   
    while(not "}" in self.tokens[self.i]):
      erro_constante = False
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
              # o campo atual deve nao ter sido declarado anteriormente
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

                    self.arquivo_saida.write("Novo campo constante: " + lexema_nomeTipo + " " + lexema_nomeCamp+ " " + valor_constante +"\n")
                    # a chave do dicionario eh o nome do campo constante, o conteudo eh o tipo do campo seguido de seu valor
                    campos_const = [lexema_nomeTipo, valor_constante]
                    self.constantes_tab[lexema_nomeCamp] = campos_const
                  else:
                    self.arquivo_saida.write("Erro Semantico: Atribuicao de tipos nao esta correta para campo constante: " + lexema_nomeCamp + " e o valor: "+ valor_constante+"\n")
                    self.arquivo_saida.write("Erro na linha : "+self.linha_atual+"\n")
                    self.tem_erro_semantico = True
                    erro_constante = True
                else: 
                  self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado como tipo registro\n")
                  self.arquivo_saida.write("Erro na linha : "+self.linha_atual+"\n")
                  self.tem_erro_semantico = True
                  erro_constante = True
              else:
                self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado como campo contante \n")
                self.arquivo_saida.write("Erro na linha : "+self.linha_atual+"\n")
                self.tem_erro_semantico = True
                erro_constante = True

              if(erro_constante):
                while(not ";" in self.conteudo_token() ):
                  self.next_token()

      self.next_token()
  '''
    Preenche a tabela constantes_tab e
    emite erros semanticos caso sejam encontrados duplicidade de nomes de variaveis
    ou atrbuicoes erradas.
  '''
  def preencheVariaveisTab(self, escopo):
    # consumo o primeiro '{'
    self.next_token()
    erro_var = False

    dicionario_var = {}
    self.variaveis_tab[escopo] = dicionario_var
    self.arquivo_saida.write("\n=== Criando nova tabela de variaveis em escopo: "+escopo+" ===\n")
    while(not "}" in self.tokens[self.i]):
      categoria = ""
      linha = ""
      coluna = ""
      inicializao_valor = "sem_inicializacao"
      # dicionario que armazena os campos especificos da variavel
      campos_var = []
      #Busca o lexema do tipo primitivo
      lexema_nomeTipo = self.conteudo_token()
      #Verificando se e um registro ou variavel global
      if("tok500_" in lexema_nomeTipo):
        if( lexema_nomeTipo in self.registro_tab.keys() ):
          categoria = "registro"
        else:
          erro_var = True
          self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeTipo + " não foi declarado como registro\n")
          self.arquivo_saida.write("Erro na linha: "+self.linha_atual+"\n")
          self.tem_erro_semantico = True
          while( not ";" in self.conteudo_token() ):
            self.next_token()
      else:
        categoria = "simples"

      if(not erro_var):
        # consumindo o token de tipo de registro
        self.next_token()
        # Pegando o nome da variavel analisada no momento
        lexema_nomeCamp = self.conteudo_token()
        # consumindo o nome da variavel
        self.next_token()

        # Verifico se jah nao declarei esse campo de variavel anteriormente
        if(not lexema_nomeCamp in self.variaveis_tab[escopo].keys() ):
          # Verifico se jah nao declarei uma constante com o nome em questao
          if(not lexema_nomeCamp in self.constantes_tab.keys() ):
            # Verifico se jah nao declarei um registro com o nome em questao
            if( not lexema_nomeCamp in self.registro_tab.keys() ):
              #Verificando se e um vetor ou uma matriz
              if ( 'tok206_[' in self.tokens[self.i] ):
                self.next_token()
                categoria = "vetor"
                if ( 'tok300_' in self.tokens[self.i] ):
                  linha = self.conteudo_token()
                  self.next_token()
                  if ( 'tok207_]' in self.tokens[self.i] ):
                    self.next_token()
                    if ( 'tok206_[' in self.tokens[self.i] ):
                      self.next_token()
                      categoria = "matriz"
                      if ( 'tok300_' in self.tokens[self.i] ):
                        coluna = self.conteudo_token()
                        self.next_token()
                      if ( 'tok207_]' in self.tokens[self.i] ):
                          self.next_token()
    
              if( 'tok115_=' in self.tokens[self.i] ):
                self.next_token()
                # verifico se os tipos sao compativeis
                if(("inteiro" in lexema_nomeTipo and "tok300" in self.tokens[self.i]) or
                   ("real" in lexema_nomeTipo and "tok301" in self.tokens[self.i])or
                   ("char" in lexema_nomeTipo and "tok400" in self.tokens[self.i]) or
                   ("cadeia" in lexema_nomeTipo and "tok700" in self.tokens[self.i]) or
                   (("booleano" in lexema_nomeTipo and "tok618" in self.tokens[self.i]) or ("booleano" in lexema_nomeTipo and "tok619" in self.tokens[self.i]))):
                  # Pegando conteudo da inicializacao da variavel simples
                  inicializao_valor = self.conteudo_token()
                  self.next_token()
                  # Armazenando as informacoes de cada variavel
                  campos_var.append(lexema_nomeTipo)
                  campos_var.append(categoria)
                  campos_var.append(inicializao_valor)
                  campos_var.append(linha)
                  campos_var.append(coluna)
                  self.arquivo_saida.write("Novo campo variavel "+escopo+" criado - nome: "+lexema_nomeCamp+" | tipo: "+lexema_nomeTipo+" | categoria: "+categoria+" | valor inicial: "+inicializao_valor+" | linha: "+linha+" |  coluna: "+coluna+"\n\n")
                  # atribuindo ao dicionario de variaveis na chave correspondente o conteudo da variavel lida
                  dicionario_var[ lexema_nomeCamp ] = campos_var
                else:
                  self.next_token()
                  self.arquivo_saida.write("Erro Semantico: Atribuicao de tipos nao esta correta para variavel " + lexema_nomeCamp + "\n")
                  self.arquivo_saida.write("Erro na linha: "+self.linha_atual+"\n")
                  self.tem_erro_semantico = True
              else:
                # Armazenando as informacoes de cada variavel
                campos_var.append(lexema_nomeTipo)
                campos_var.append(categoria)
                campos_var.append(inicializao_valor)
                campos_var.append(linha)
                campos_var.append(coluna)
                self.arquivo_saida.write("Novo campo variavel "+escopo+" criado - nome: "+lexema_nomeCamp+" | tipo: "+lexema_nomeTipo+" | categoria: "+categoria+" | valor inicial: "+inicializao_valor+" | linha: "+linha+" |  coluna: "+coluna+"\n\n")
                # atribuindo ao dicionario de variaveis na chave correspondente o conteudo da variavel lida
                dicionario_var[ lexema_nomeCamp ] = campos_var
            else: 
              self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado como nome de registro \n")
              self.arquivo_saida.write("Erro na linha: "+self.linha_atual+"\n")
              self.tem_erro_semantico = True
              erro_var = True
          else:
            self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado em Constantes \n")
            self.arquivo_saida.write("Erro na linha: "+self.linha_atual+"\n")
            self.tem_erro_semantico = True
            erro_var = True
        else:
          self.arquivo_saida.write("Erro Semantico: "+ lexema_nomeCamp + " ja foi declarado em Variaveis " + escopo + "\n")
          self.arquivo_saida.write("Erro na linha: "+self.linha_atual+"\n")
          self.tem_erro_semantico = True
          erro_var = True
        if(erro_var):
          while( not ";" in self.conteudo_token() ):
            self.next_token()
      else:
        while( not ";" in self.conteudo_token() ):
          self.next_token()
              
      # consumo o ';'
      self.next_token()
    # consumo o '}'
    self.next_token()

  # todas as variaveis locais devem ser declaraddas ao inicio da declaracao de cada funcao
  def preencheFuncaoTab(self):

    # Armazeno o tipo de retorno da funcao em questao
    # LEMBRAR QUE PODE SER VETOR OU MATRIZ OU REGISTRO
    tipo_retorno = []
    # adicionando o tipo de retorno da funcao 
    tipo_retorno.append ( self.conteudo_token() )
    if("tok_500" in self.conteudo_token()):
      tipo_retorno_categoria = "registro"
      if (not self.conteudo_token() in self.registro_tab.keys()):
        print ("Erro Semantico: tipo "+ self.conteudo_token() + " não foi declarado como registro - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write("Erro Semantico: tipo "+ self.conteudo_token() + " não foi declarado como registro - linha: "+self.linha_atual+"\n")
        self.tem_erro_semantico = True
    else:
      tipo_retorno_categoria = "simples"
    
    self.next_token()
    if ( 'tok206_[' in self.tokens[self.i] ):
      self.next_token()
      self.next_token()
      tipo_retorno_categoria = ("vetor")
      if ( 'tok206_[' in self.tokens[self.i] ):
        self.next_token()
        self.next_token()
        tipo_retorno_categoria = ("matriz")
    # adicionando a categoria de retorno da funcao
    tipo_retorno.append (tipo_retorno_categoria)

    # Armazena os parametros da funcao na ordem e quantidade em que eles foram declarados
    lista_parametros = {}
    # Armazeno o nome da funcao em questao
    nome_func = self.conteudo_token()
    # Verifico se o nome da funcao nao jah foi declarado como nome de funcao anteriormente
    if( not nome_func in self.funcao_tab.keys() ):
      # o nome da funcao eh a chave para acessar o tipo de retorno dessa funcao
      self.funcao_tab[nome_func] = tipo_retorno
      # adicionando a lista de paramertro da funcao analisada para a tabela de parametros da funcao
      self.parametro_funcao_tab[nome_func] = lista_parametros
      # Avanco ao token '('
      self.next_token()
      self.next_token()

      if(not ')' in self.tokens[self.i]):
        # garante que se saiba a ordem em que os parametros apareceram
        posicao_param = 0
        while( not ')' in self.tokens[self.i] and not '{' in self.tokens[self.i]):
          categoria = ""
          # armazena todo o conteudo pertencente ao parametro analisado
          conteudo_param = []
          tipo_para = self.conteudo_token()
          self.next_token()
          nome_para = self.conteudo_token()
          self.next_token()
          if( "tok500_" in tipo_para ):
            categoria = "registro"
            if (not tipo_para in self.registro_tab.keys()):
              print ("Erro Semantico: tipo "+ tipo_para + "do parâmetro " + nome_para + " não foi declarado como registro - linha: "+self.linha_atual+"\n")
              self.arquivo_saida.write("Erro Semantico: tipo "+ tipo_para + "do parâmetro " + nome_para + " não foi declarado como registro - linha: "+self.linha_atual+"\n")
              self.tem_erro_semantico = True
          else:
            categoria = "simples"
    
          conteudo_param.append(tipo_para)
          if(not ')' in self.tokens[self.i]):
            if(not ',' in self.tokens[self.i]):
              #Verificando se e um vetor ou uma matriz
              if ( 'tok206_[' in self.tokens[self.i] ):
                self.next_token()
                self.next_token()
                categoria = ("vetor")
                if ( 'tok206_[' in self.tokens[self.i] ):
                  self.next_token()
                  self.next_token()
                  categoria = ("matriz")
          # consumo o ')'
          else: 
            self.next_token()
          # consumo a virgula
          if(',' in self.tokens[self.i]):
            self.next_token()
          # adicionando a categoria do parametro: simples, vetor, matriz, registro
          conteudo_param.append (categoria)
          # adicionando a posicao em que o parametro ocorreu
          conteudo_param.append (str(posicao_param))
          # adicionando o conteudo do parametro para a lista de parametros
          lista_parametros[nome_para] = conteudo_param
          # incremento a posicao do parametro
          posicao_param += 1
      else:
        # consumo o ')' que nao foi consumido anteriormente
        self.next_token()
      if("{" in self.conteudo_token()):
        # consumo o simbolo '{'
        self.next_token()
      elif(")" in self.conteudo_token()):
        # consumo o simbolo ')'
        self.next_token()
        # consumo o simbolo '{'
        self.next_token()

      self.arquivo_saida.write("\n+++Tabela de parâmetros da função "+nome_func+ "+++\n")
      self.imprime_dicionario(self.parametro_funcao_tab[nome_func])
      

      # caso a funcao tenha variaveis locais preciso armazenar suas informacoes
      if("variaveis" in self.tokens[self.i]):
        # consumo variaveis
        self.next_token()
        self.preencheVariaveisTab( nome_func )
        self.arquivo_saida.write("\n+++Tabela de variaveis locais da função "+nome_func+ "+++\n")
        self.imprime_dicionario(self.variaveis_tab[nome_func])
        self.arquivo_saida.write("\n++++++++++++++++++++++++++++++++\n")

      # indico que estou analisando a funcao com o nome nome_func no momento
      self.funcao_analisada = nome_func
      self.arquivo_saida.write("Declaração de comandos escopo: "+nome_func+"\n")
      self.decl_comandos()
      # fica faltando analisar se o tipo de retorno eh compativel c o retorno real
    else:
      print ("Erro Semantico: "+ nome_func + " ja foi declarado como nome de funcao - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write("Erro Semantico: "+ nome_func + " ja foi declarado como nome de funcao - linha: "+self.linha_atual+"\n")
      self.tem_erro_semantico = True



      #self.decl_comandos(nome_func)
  def preencheAlgoritmoTab(self):
    # consumo a primeira chave de algoritmo '{'
    self.next_token()
    if("variaveis" in self.tokens[self.i]):
      # consome a palavra variavel
      self.next_token()
      # Preenchendo as variaveis locais da funcao algoritmo
      self.preencheVariaveisTab( "algoritmo" )
      self.arquivo_saida.write("\n+++Tabela de variáveis locais em algoritmo criada+++\n")
      self.imprime_dicionario(self.variaveis_tab["algoritmo"])
      self.arquivo_saida.write("\n++++++++++++++++++++++++++++++++\n")
    
    # configurando a declaracao de comandos interna a funcao algoritmo
    # self.funcao_analisada = "algoritmo"
    # self.decl_comandos("algoritmo")

  # verifica se determinada variavel pertence ao escopo em questao
  # verifica tambem se ela foi declarada como registro, constante etc
  def retorna_de_escopo(self, variavel):
    informacoes_variavel = []
    virou_dict = False
    if( not variavel in self.constantes_tab.keys() ):

      if(not "algoritmo" in self.funcao_analisada):
        # verificando se a variavel foi declarada como variavel local da funcao
        if( variavel in self.variaveis_tab[self.funcao_analisada].keys() ):
          informacoes_variavel = self.variaveis_tab[self.funcao_analisada]
          virou_dict = True

        elif( variavel in self.parametro_funcao_tab[self.funcao_analisada].keys() ):
          informacoes_variavel = self.parametro_funcao_tab[self.funcao_analisada]
          virou_dict = True
        
        elif( variavel in self.variaveis_tab["global"].keys() ):
          informacoes_variavel = self.variaveis_tab["global"]
          virou_dict = True
      else:
        # verificando se a variavel foi declarada como variavel local de algoritmo
        if( variavel in self.variaveis_tab[self.funcao_analisada].keys() ):
          informacoes_variavel = self.variaveis_tab[self.funcao_analisada]
          virou_dict = True
        
        elif( variavel in self.variaveis_tab["global"].keys() ):
          informacoes_variavel = self.variaveis_tab["global"]
          virou_dict = True
    else:
      print ("Erro Semantico: "+ variavel + " é uma constante e não pode receber atribuições - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write("Erro Semantico: "+ variavel + " é uma constante e não pode receber atribuições - linha: "+self.linha_atual+"\n")
      self.tem_erro_semantico = True      
    # retorna lista com informacoes da variavel se encontrada
    if(virou_dict):
      return informacoes_variavel[variavel]
    # retorna lista vazia caso n tenha encontrada
    else:
      return informacoes_variavel
    
  # verifica se dois tipos sao compativeis
  def retorna_campo_registro(self, tipo_registro, campo):
    if( tipo_registro in self.registro_tab.keys() ):
      if ( campo in self.registro_tab[tipo_registro].keys() ):
        campo_tab = self.registro_tab[tipo_registro]
        return campo_tab[campo]
      else:
        print ("Erro Semantico: "+ campo + " não é um campo do tipo registro: " + tipo_registro + "- linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write("Erro Semantico: "+ campo + " não é um campo do tipo registro: " + tipo_registro + "- linha: "+self.linha_atual+"\n")
        self.tem_erro_semantico = True
    else:
      print ("Erro Semantico: "+ tipo_registro + " não foi declarado como um tipo registro: - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write("Erro Semantico: "+ tipo_registro + " não foi declarado como um tipo registro: - linha: "+self.linha_atual+"\n")
      self.tem_erro_semantico = True
    # caso o tipo registro nao exista ou nao exista o campo no tipo registro
    return []

    # Declaracao de comandos
    # ================================================================
  def decl_comandos(self):

    if('tok605_retorno' in self.tokens[self.i] or
       'tok205_}' in self.tokens[self.i]):
      return
    elif( 'tok607_se' in self.tokens[self.i] or
        'tok612_escreva' in self.tokens[self.i] or
        'tok611_leia' in self.tokens[self.i] or
        'tok609_enquanto' in self.tokens[self.i] or
        'tok610_para' in self.tokens[self.i] or
        'tok500_' in self.tokens[self.i]):
      self.comandos()
      self.decl_comandos()
      
  # <comandos> := <se_declaracao> | <enquanto_declaracao> | <para_declaracao> | <escreva_declaracao> | <leia_declaracao> | <atribuicao> | Ɛ
  def comandos(self):
    if( 'tok607_se' in self.tokens[self.i] ):
      self.se_declaracao()
    elif( 'tok612_escreva' in self.tokens[self.i] ):
      self.escreva_declaracao()
    elif( 'tok611_leia' in self.tokens[self.i] ):
      self.leia_declaracao()
    elif( 'tok609_enquanto' in self.tokens[self.i] ):
      self.enquanto_declaracao()
    elif( 'tok610_para' in self.tokens[self.i] ):
      self.para_declaracao()
    elif('tok500_' in self.tokens[self.i]):
      self.atribuicao()
      
  #<atribuicao> := token_identificador <identificador_imp_arm_deriva>  = <atribuicao_deriva>;
  def atribuicao(self):
    if('tok500_' in self.tokens[self.i]):
      self.next()
      self.identificador_imp_arm_deriva()
      if('tok115_=' in self.tokens[self.i]):
        self.next()
        self.atribuicao_deriva()
        if('tok200_;' in self.tokens[self.i]):
          self.next()

  #<atribuicao_deriva> := <exp_simples> | <chamada_funcao>
  def atribuicao_deriva(self):
    if('tok500_' in self.tokens[self.i]):
      self.chamada_funcao()
    elif('tok202_(' in self.tokens[self.i] or
         'tok101_+' in self.tokens[self.i] or
         'tok102_-' in self.tokens[self.i] or
         'tok500_' in self.tokens[self.i] or
         'tok300_' in self.tokens[self.i]):
      self.exp_simples()

  #<chamada_funcao> := funcao token_identificador (<decl_param_chamada>)
  def chamada_funcao(self):
    if('tok500_' in self.tokens[self.i]):
      self.next_token()
      if('tok202_(' in self.tokens[self.i]):
        self.next_token()
        self.decl_param_chamada()
        if('tok203_)' in self.tokens[self.i]):
          self.next_token()
      

  #<decl_param_chamada> := <decl_chamada> <chamada_param_deriva> | Ɛ
  def decl_param_chamada(self):
    if('tok203_)' in self.tokens[self.i]):
      return
    elif('tok500_' in self.tokens[self.i] or 'tok400_' in self.tokens[self.i] or 'tok700_' in self.tokens[self.i] or 'tok300_' in self.tokens[self.i] or 'tok301_' in self.tokens[self.i]):
      self.decl_chamada()
      self.chamada_param_deriva()
    
  #<decl_chamada> := token_identifcador<identificador_imp_arm_deriva> | <valor_primitivo>
  def decl_chamada(self):
    if('tok500_' in self.tokens[self.i]):
      self.next_token()
      self.identificador_imp_arm_deriva()
    elif('tok700_' in self.tokens[self.i] or 'tok400_' in self.tokens[self.i] or 'tok300_' in self.tokens[self.i] or 'tok301_' in self.tokens[self.i]):
      self.valor_primitivo()
    
  #<chamada_param_deriva> := , <decl_param_chamada> | Ɛ
  def chamada_param_deriva(self):
    if('tok203_)' in self.tokens[self.i]):
      return
    elif('tok201_,' in self.tokens[self.i]):
      self.next_token()
      self.decl_param_chamada()
     
  # <identificador_imp_arm_deriva> := .token_identificador | [<indice>]<matriz_chamada> | Ɛ    
  def identificador_imp_arm_deriva(self):
    if('tok200_;' in self.tokens[self.i] or
       'tok115_=' in self.tokens[self.i]or
       'tok201_,' in self.tokens[self.i] or
       'tok202_(' in self.tokens[self.i] or
       'tok203_)' in self.tokens[self.i] or
       'tok101_+' in self.tokens[self.i] or
       'tok102_-' in self.tokens[self.i] or
       'tok103_*' in self.tokens[self.i] or
       'tok104_/' in self.tokens[self.i] or
       'tok105_++' in self.tokens[self.i] or
       'tok106_--' in self.tokens[self.i] or
       'tok107_==' in self.tokens[self.i] or
       'tok108_!=' in self.tokens[self.i] or
       'tok109_>' in self.tokens[self.i] or
       'tok110_>=' in self.tokens[self.i] or
       'tok111_<' in self.tokens[self.i] or
       'tok112_<=' in self.tokens[self.i] or
       'tok113_&&' in self.tokens[self.i] or
       'tok114_||' in self.tokens[self.i] or
       'tok700_' in self.tokens[self.i] or
       'tok500_' in self.tokens[self.i] or
       'tok400_' in self.tokens[self.i] or
       'tok300_' in self.tokens[self.i] or
       'tok301_' in self.tokens[self.i] or
       'tok606_vazio' in self.tokens[self.i] or
       'tok617_cadeia' in self.tokens[self.i] or 
       'tok614_real' in self.tokens[self.i] or
       'tok613_inteiro' in self.tokens[self.i] or
       'tok616_char' in self.tokens[self.i] or
       'tok615_booleano' in self.tokens[self.i]):
          return ""
    elif("tok100_." in self.tokens[self.i]):
      self.next_token()
      if("tok500_" in self.tokens[self.i]):
        campo_reg = self.conteudo_token()
        self.next_token()
        return campo_reg
    elif("tok206_[" in self.tokens[self.i]):
      self.next_token()
      self.indice()
      if("tok207_]" in self.tokens[self.i]):
        self.next_token()
        self.matriz_chamada()
        return ""
    
  #<matriz_chamada> := [<indice>] | Ɛ
  def matriz_chamada(self):
    if("tok200_;" in self.tokens[self.i]):
      return
    elif("tok206_[" in self.tokens[self.i]):
      self.next_token()
      self.indice()
      if("tok207_]" in self.tokens[self.i]):
        self.next_token()
            
  #<indice> := token_inteiro | Ɛ
  def indice(self):
    if('tok207_]' in self.tokens[self.i]):
      return
    if('tok300_' in self.tokens[self.i]):
      self.next_token()
      
  # <se_declaracao> := se (<exp_rel_bol>) {<decl_comandos>}<senao_decl>
  def se_declaracao(self):
    if("tok607_se" in self.tokens[self.i]):
      self.next_token()
      if("tok202_(" in self.tokens[self.i]):
        self.next_token()
        self.exp_rel_bol()
        if("tok203_)" in self.tokens[self.i]):
          self.next_token()
          if('tok204_{' in self.tokens[self.i]):
            self.next_token()
            self.decl_comandos()
            if('tok205_}' in self.tokens[self.i]):
              self.next_token()
              self.senao_decl()
    
  # <senao_decl> := senao {<decl_comandos>} | Ɛ
  def senao_decl(self):
    if('tok607_se' in self.tokens[self.i] or
        'tok612_escreva' in self.tokens[self.i] or
        'tok611_leia' in self.tokens[self.i] or
        'tok609_enquanto' in self.tokens[self.i] or
        'tok610_para' in self.tokens[self.i] or
        'tok500_' in self.tokens[self.i] or
        'tok605_retorno' in self.tokens[self.i] or
        'tok205_}' in self.tokens[self.i]):
      return
    elif("tok608_senao" in self.tokens[self.i]):
      self.next_token()
      if('tok204_{' in self.tokens[self.i]):
        self.next_token()
        self.decl_comandos()
        if('tok205_}' in self.tokens[self.i]):
          self.next_token()
      
  # <enquanto_declaracao> := enquanto (<exp_rel_bol>) { <decl_comandos> }
  def enquanto_declaracao(self):
    if("tok609_enquanto" in self.tokens[self.i]):
      self.next_token()
      if("tok202_(" in self.tokens[self.i]):
        self.next_token()
        self.exp_rel_bol()
        if("tok203_)" in self.tokens[self.i]):
          self.next_token()
          if('tok204_{' in self.tokens[self.i]):
            self.next_token()
            self.decl_comandos()
            if('tok205_}' in self.tokens[self.i]):
              self.next_token()
    
  # <para_declaracao> := para (token_identificador = token_inteiro; token_identificador <op_relacional> token_inteiro; token_identificador <op_cont>) {<decl_comandos>}
  def para_declaracao(self):
    if("tok610_para" in self.tokens[self.i]):
      self.next_token()
      if("tok202_(" in self.tokens[self.i]):
        self.next_token()
        if("tok500_" in self.tokens[self.i]):
          self.next_token()
          if("tok115_=" in self.tokens[self.i]):
            self.next_token()
            if("tok300_" in self.tokens[self.i]):
              self.next_token()
              if("tok200_;" in self.tokens[self.i]):
                self.next_token()
                if("tok500_" in self.tokens[self.i]):
                  self.next_token()
                  self.op_relacional()
                  if("tok300_" in self.tokens[self.i]):
                    self.next_token()
                    if("tok200_;" in self.tokens[self.i]):
                      self.next_token()
                      if("tok500_" in self.tokens[self.i]):
                        self.next_token()
                        self.op_cont()
                        if("tok203_)" in self.tokens[self.i]):
                          self.next_token()
                          if("tok204_{" in self.tokens[self.i]):
                            self.next_token()
                            self.decl_comandos()
                            if("tok205_}" in self.tokens[self.i]):
                              self.next_token()
    
  # <leia_declaracao> := leia (<exp_leia>); 
  def leia_declaracao(self):
    if("tok611_leia" in self.tokens[self.i]):
      self.next_token()
      if("tok202_(" in self.tokens[self.i]):
        self.next_token()
        self.exp_leia()
        if("tok203_)" in self.tokens[self.i]):
          self.next_token()
          if("tok200_;" in self.tokens[self.i]):
            self.next_token()
    
  # <exp_leia> := <exp_armazena><exp_leia_deriva><exp_leia> | Ɛ
  def exp_leia(self):
    if("tok203_)" in self.tokens[self.i]):
      return
    elif("tok500_" in self.tokens[self.i]):
      self.exp_armazena()
      self.exp_leia_deriva()
      self.exp_leia()
      
  # <exp_leia_deriva> := ,<exp_armazena> | Ɛ
  def exp_leia_deriva(self):
    
    if("tok203_)" in self.tokens[self.i]):
      return
    elif("tok201_," in self.tokens[self.i]):
      self.next_token()
      self.exp_armazena()
                
  # <exp_armazena> := token_identificador <identificador_imp_arm_deriva>
  def exp_armazena(self):
    if("tok500_" in self.tokens[self.i]):
      self.next_token()
      self.identificador_imp_arm_deriva()
    
  # <escreva_declaracao> := escreva (<exp_escreva>);
  def escreva_declaracao(self):
    if("tok612_escreva" in self.tokens[self.i]):
      self.next_token()
      if("tok202_(" in self.tokens[self.i]):
        self.next_token()
        self.exp_escreva()
        if("tok203_)" in self.tokens[self.i]):
          self.next_token()
          if("tok200_;" in self.tokens[self.i]):
            self.next_token()
    
  # <exp_escreva> := <exp_imprime><exp_escreva_deriva><exp_escreva> | Ɛ
  def exp_escreva(self):
    if("tok203_)" in self.tokens[self.i]):
      return
    elif("tok700_" in self.tokens[self.i] or "tok400_" in self.tokens[self.i] or "tok500_" in self.tokens[self.i] or "(" in self.tokens[self.i]):
      self.exp_imprime()
      self.exp_escreva_deriva()
      self.exp_escreva()
    
  # <exp_escreva_deriva> := ,<exp_imprime> | Ɛ
  def exp_escreva_deriva(self):
    if("tok203_)" in self.tokens[self.i]):
      return
    elif("tok201_," in self.tokens[self.i]):
      self.next_token()
      self.exp_imprime()
    
  # <exp_imprime> := token_cadeia | token_char | token_identificador <identificador_imp_arm_deriva> | (<exp_simples>)
  def exp_imprime(self):
    if("tok700_" in self.tokens[self.i]):
      self.next_token()
    elif("tok400_" in self.tokens[self.i]):
      self.next_token()
    elif("tok500_" in self.tokens[self.i]):
      self.next_token()
      self.identificador_imp_arm_deriva()
    elif("tok202_(" in self.tokens[self.i]):
      self.next_token()
      self.exp_simples()
      if("tok203_)" in self.tokens[self.i]):
        self.next_token()
    
  # <exp_rel_bol> := <exp_boll> <op_relacional> <exp_boll> <exp_rel_deriva>
  def exp_rel_bol(self):
    #import pdb; pdb.set_trace() # Break do debbug
    if("tok500_" in self.tokens[self.i] or
       "tok300_" in self.tokens[self.i] or
       "tok202_(" in self.tokens[self.i]):
      self.exp_boll()
      self.op_relacional()
      self.exp_boll()
      self.exp_rel_deriva()
    
  #<exp_boll> := <termo><termo_deriva>
  def exp_boll(self):
    #import pdb; pdb.set_trace() # Break do debbug
    if("tok500_" in self.tokens[self.i] or
       "tok300_" in self.tokens[self.i] or
       "tok202_(" in self.tokens[self.i]):
        self.termo()
        self.termo_deriva()
    
  # <exp_simples> := <op_ss><termo><termo_deriva> | <termo><termo_deriva>
  def exp_simples(self):
    if("tok101_+" in self.tokens[self.i] or "tok102_-" in self.tokens[self.i]):
      self.op_ss()
      self.termo()
      self.termo_deriva()
    elif("tok500_" in self.tokens[self.i] or
       "tok300_" in self.tokens[self.i] or
       "tok202_(" in self.tokens[self.i]):
      self.termo()
      self.termo_deriva()
    
  # <op_relacional> := < | > | == | != | <= | >=
  def op_relacional(self):
    if("tok112_<=" in self.tokens[self.i] or "tok110_>=" in self.tokens[self.i] or "tok109_>" in self.tokens[self.i] or "tok111_<" in self.tokens[self.i] or "tok107_==" in self.tokens[self.i] or "tok108_!=" in self.tokens[self.i]):
      self.next_token()
      
  # <exp_rel_deriva> := <op_bolleano> <exp_simples> <op_relacional> <exp_simples> <exp_rel_deriva> | Ɛ
  def exp_rel_deriva(self):
    if("tok203_)" in self.tokens[self.i]):
      return
    elif("tok113_&&" in self.tokens[self.i] or "tok114_||" in self.tokens[self.i]):
      self.op_bolleano()
      self.exp_simples()
      self.op_relacional()
      self.exp_simples()
      self.exp_rel_deriva()
    
  # <op_ss> := + | -
  def op_ss(self):
    if("tok101_+" in self.tokens[self.i] or "tok102_-" in self.tokens[self.i]):
      self.next_token()
          
  # <termo> := <fator><fator_deriva>
  def termo(self):
    if('tok500_' in self.tokens[self.i] or 'tok300_' in self.tokens[self.i] or 'tok202_(' in self.tokens[self.i]):
      self.fator()
      self.fator_deriva()
    
  # <termo_deriva> := +<op_soma_deriva> | -<op_sub_deriva> | Ɛ
  def termo_deriva(self):
    if("tok112_<=" in self.tokens[self.i] or
             "tok110_>=" in self.tokens[self.i] or
             "tok109_>" in self.tokens[self.i] or
             "tok111_<" in self.tokens[self.i] or
             "tok107_==" in self.tokens[self.i] or
             "tok108_!=" in self.tokens[self.i] or
             "tok203_)" in self.tokens[self.i] or
             "tok200_;" in self.tokens[self.i] or
             "tok113_&&" in self.tokens[self.i] or
             "tok114_||" in self.tokens[self.i]):
        return
    elif('tok101_+' in self.tokens[self.i]):
      self.next_token()
      self.op_soma_deriva()
    elif('tok102_-' in self.tokens[self.i]):
      self.next_token()
      self.op_sub_deriva()
    
  # <op_bolleano> := && | || 
  def op_bolleano(self):
    if("tok113_&&" in self.tokens[self.i] or "tok114_||" in self.tokens[self.i]):
      self.next_token()
      
  # <fator> := token_identificador <identificador_imp_arm_deriva> | token_inteiro | (<exp_simples>) 
  def fator(self):
    if('tok500_' in self.tokens[self.i]):
      self.next_token()
      self.identificador_imp_arm_deriva()
    elif('tok300_' in self.tokens[self.i]):
      self.next_token()
    elif('tok202_(' in self.tokens[self.i]):
      self.next_token()
      self.exp_simples()
      if('tok203_)' in self.tokens[self.i]):
        self.next_token()
    
  # <fator_deriva> := <op_md><fator><fator_deriva> | Ɛ
  def fator_deriva(self):
    if("tok112_<=" in self.tokens[self.i] or
            not "tok110_>=" in self.tokens[self.i] or
            not "tok109_>" in self.tokens[self.i] or
            not "tok111_<" in self.tokens[self.i] or
            not "tok107_==" in self.tokens[self.i] or
            not "tok108_!=" in self.tokens[self.i] or
            not "tok101_+" in self.tokens[self.i] or
            not "tok102_-" in self.tokens[self.i] or
            not "tok105_++" in self.tokens[self.i] or
            not "tok106_--" in self.tokens[self.i] or
            not "tok113_&&" in self.tokens[self.i] or
            not "tok114_||" in self.tokens[self.i] or
            not "tok115_=" in self.tokens[self.i] or
            not "tok203_)" in self.tokens[self.i] or
            not "tok200_;" in self.tokens[self.i]):
                return
    elif("tok103_*" in self.tokens[self.i] or "tok104_/" in self.tokens[self.i]):
      self.op_md()
      self.termo()
    
  # <op_soma_deriva> := <termo><termo_deriva> | +
  def op_soma_deriva(self):
    if('tok101_+' in self.tokens[self.i]):
      self.next_token()
    elif("tok500_" in self.tokens[self.i] or
       "tok300_" in self.tokens[self.i] or
       "tok202_(" in self.tokens[self.i]):
      self.termo()
      self.termo_deriva()
    
  # <op_sub_deriva> := <termo><termo_deriva> | -
  def op_sub_deriva(self):
    if('tok102_-' in self.tokens[self.i]):
      self.next_token()
    elif("tok500_" in self.tokens[self.i] or
       "tok300_" in self.tokens[self.i] or
       "tok202_(" in self.tokens[self.i]):
      self.termo()
      self.termo_deriva()
    
  # <op_md> := * | /
  def op_md(self):
    if("tok103_*" in self.tokens[self.i] or "tok104_/" in self.tokens[self.i]):
      self.next_token()
    
  # <op_cont> := ++ | --
  def op_cont(self):
    if("tok105_++" in self.tokens[self.i] or "tok106_--" in self.tokens[self.i]):
      self.next_token()
    
  # <algoritmo_declaracao> :=  algoritmo {<deriva_cont_principal> }
  def algoritmo_declaracao(self):
    if ("tok600_algoritmo" in self.tokens[self.i]):
      self.next_token()
      if("tok204_{" in self.tokens[self.i]):
        self.next_token()
        self.deriva_cont_principal()
        if("tok205_}" in self.tokens[self.i]):
          self.next_token()
    
  # <deriva_cont_principal> := <variaveis_declaracao> <decl_comandos> | <decl_comandos> | Ɛ
  def deriva_cont_principal(self):
    if('tok205_}' in self.tokens[self.i]):
      return
    elif("tok601_variaveis" in self.tokens[self.i]):
      self.variaveis_declaracao()
      self.decl_comandos()
    elif('tok607_se' in self.tokens[self.i] or
         'tok612_escreva' in self.tokens[self.i] or
         'tok611_leia' in self.tokens[self.i] or
         'tok609_enquanto' in self.tokens[self.i] or
         'tok610_para' in self.tokens[self.i] or
         'tok500_' in self.tokens[self.i] or
         'tok605_retorno' in self.tokens[self.i]):
          self.decl_comandos()
    else:
      while('}' in self.tokens[self.i]):
        self.next_token()
    # ================================================================

    self.next_token()

  def analisa(self):

    while(not "$" in self.tokens[self.i]):
            
      #Verifica qual tabela sera preenchida
      if("registro" in self.tokens[self.i]):
        self.arquivo_saida.write("\n===Criando nova tabela de registros===\n")
        self.next_token()
        self.preencheRegistroTab()
      elif("constantes" in self.tokens[self.i]):

        self.arquivo_saida.write("\n+++Tabela de registros criada+++\n")
        self.imprime_dicionario(self.registro_tab)
        self.arquivo_saida.write("\n++++++++++++++++++++++++++++++++\n")
        self.arquivo_saida.write("\n")

        self.arquivo_saida.write("\n===Criando nova tabela de constantes===\n")
        self.next_token()
        self.preencheConstantesTab()
      elif("variaveis" in self.tokens[self.i]):
        self.arquivo_saida.write("\n+++Tabela de constantes criada+++\n")
        self.imprime_dicionario(self.constantes_tab)
        self.arquivo_saida.write("\n++++++++++++++++++++++++++++++++\n")
        self.arquivo_saida.write("\n")

        # consumo a palavra variaveis
        self.next_token()
        self.preencheVariaveisTab( "global" )

        self.arquivo_saida.write("\n+++Tabela de variáveis (só com as globais) criada+++\n")
        self.imprime_dicionario(self.variaveis_tab["global"])
        self.arquivo_saida.write("\n++++++++++++++++++++++++++++++++\n")
      elif("funcao" in self.tokens[self.i]):
        # consumo a palavra funcao
        self.next_token()
        self.preencheFuncaoTab()
      elif("algoritmo" in self.tokens[self.i]):
        self.next_token()
        self.preencheAlgoritmoTab()
      else:
          self.next_token()
    
    # Analise Semantica ja foi realizada, agora indica se foi compilado com sucesso
    if(self.tem_erro_semantico):
      self.arquivo_saida.write("Verifique os erros semanticos e tente compilar novamente\n")
    else:
      self.arquivo_saida.write("Cadeia de tokens reconhecida com sucesso\n")


    # Fechando arquivo de saida
    self.arquivo_saida.close()
    
    '''        
      
    '''
      
    
