# -*- coding: utf-8 -*-
######           Analisador Sintatico    ######
# Autor 1: Lucas Vinicius dos Santos Assis
# Autor 2: Andressa Moura de Souza
# EXA 869 - MI - Processadores de Linguagem de Programacao
# ==============================================================================
# Implementacao do analisador sintatico de um compilador

# Bibliotecas para entrada e saida de arquivos
import sys
import os.path

# Bliblioteca padrao de string
import string

# Declarando Classe do Analisador Sintatico
class AnalisadorSintatico():
  # ========================== DECLARACAO DE METODOS DA CLASSE
  # Metodo construtor da classe
  def __init__(self):
    
    self.arquivo_entrada = "resp-lex.txt"
    self.arquivo_saida = "resp-sint.txt"

    self.tem_erro_sintatico = False

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
    self.j = 0
    self.linha_atual = ""

    
  # Metodo para mudar arquivo de entrada
  def mudaEntrada(self, string):
    self.arquivo_entrada = string

  def getEntrada(self):
    return self.arquivo_entrada

  def getSaida(self):
    return self.arquivo_saida

  # CADA UMA DAS FUNCOES ABAIXO REPRESENTA UMA PRODUCAO DA GRAMATICA
  '''
    O algoritmo basico que foi seguindo para construir as funcoes representa 
    um analisador sintatico preditivo recursivo, segue o codigo abaixo:
    void A(){
      Escolha uma producao-A, A-> x1, x2, ... , xk 
      for(i = 1 ateh k){
        if(xi eh um nao terminal){
          ativa procedimento xi();
        }
        else if(xi igual ao simbolo de entrada a){
          avance a entrada ao proximo simbolo
        }
        else{
          ocorreu um erro
        }
      }
    }
  '''

  # <start> := <registro_declaracao><constantes_declaracao><variaveis_declaracao><funcao_declaracao><algoritmo_declaracao> 
  def start(self):
    
    
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    self.registro_declaracao()
    self.constantes_declaracao()
    self.variaveis_declaracao()
    self.funcao_declaracao()
    self.algoritmo_declaracao()
    
    if(self.tem_erro_sintatico):
      print("Verifique os erros sintaticos e tente compilar novamente")
      self.arquivo_saida.write("Verifique os erros sintaticos e tente compilar novamente\n")
    else:
      if("$" in self.tokens[self.i]):
        print("Cadeia de tokens reconhecida com sucesso")
        self.arquivo_saida.write("Cadeia de tokens reconhecida com sucesso\n")
      else:
        print("Fim de Programa Nao Encontrado!")
        self.arquivo_saida.write("Fim de Programa Nao Encontrado!")

    # Fechando arquivo de saida
    self.arquivo_saida.close()

  # <registro_declaracao> := registro token_identificador { <declaracao_reg> } <registro_declaracao> | Ɛ                   
  def registro_declaracao(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if( 'tok603_registro' in self.tokens[self.i] ):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      if( 'tok500_' in self.tokens[self.i] ):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        if( 'tok204_{' in self.tokens[self.i] ):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          self.declaracao_reg()
          if( 'tok205_}' in self.tokens[self.i] ):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
            self.registro_declaracao()
          else:
            print("Erro sintatico - Esperado '}'  - linha: "+self.linha_atual+"\n")
            self.arquivo_saida.write("Erro sintatico  - Esperado '}' - linha: "+self.linha_atual+"\n")
            print('Token problemático: '+self.tokens[self.i])
            self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
            self.tem_erro_sintatico = True
            while( not 'tok602_constantes' in self.tokens[self.i] or not 'tok603_registro' in self.tokens[self.i]):
              self.i += 1
              self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        else:
          print("Erro sintatico - Esperado '{' - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write("Erro sintatico - Esperado '{'  - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          self.tem_erro_sintatico = True
          while( not 'tok602_constantes' in self.tokens[self.i] or not 'tok603_registro' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Esperado um 'identificador' - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write("Erro sintatico  - Esperado um 'identificador' - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while( not 'tok602_constantes' in self.tokens[self.i] or not 'tok603_registro' in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        return
    elif ('tok602_constantes' in self.tokens[self.i]):
      return
    else:
      print("Erro sintatico - Esperado a palavra reservada 'registro'  - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write("Erro sintatico  - Esperado a palavra reservada 'registro'  - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      if( 'tok602_constantes' in self.tokens[self.i] or 'tok603_registro' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      while( not 'tok602_constantes' in self.tokens[self.i] or not 'tok603_registro' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        
  # <declaracao_reg> := <declaracao>; <declaracao_reg> | Ɛ                                                                 
  def declaracao_reg(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok205_}" in self.tokens[self.i]):
      return
    self.declaracao()
    if( 'tok200_;' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.declaracao_reg()
    else:
      print("Erro sintatico - Esperado ';'  - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write("Erro sintatico  - Esperado ';' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while( not "tok205_}" in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]


  # <declaracao> := <tipo_primitivo> token_identificador                                                                  
  def declaracao(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    self.tipo_primitivo()
    if( 'tok500_' in self.tokens[self.i] ):    
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      if('tok200_;' in self.tokens[self.i]):
        while('tok200_;' in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        print("Erro sintatico - ';' duplicado  - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write("Erro sintatico  - ';' duplicado - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True  
      else:
        print("Erro sintatico - Esperado um 'indentificador'  - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write("Erro sintatico  - Esperado um 'identificador' - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
      while( not 'tok200_;' in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      
        
  # <tipo_primitivo> := cadeia | real | inteiro | char | booleano                                                         
  def tipo_primitivo(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if( 'tok617_cadeia' in self.tokens[self.i] or 
      'tok614_real' in self.tokens[self.i] or
      'tok613_inteiro' in self.tokens[self.i] or
      'tok616_char' in self.tokens[self.i] or
      'tok615_booleano' in self.tokens[self.i]):

      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      if('tok200_;' in self.tokens[self.i]):
        while('tok200_;' in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        self.arquivo_saida.write("Erro sintatico - ';' duplicados:  - linha: "+self.linha_atual+"\n")
        print("Erro sintatico - ';' duplicados "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        print('Token problemático: '+self.tokens[self.i])
        self.tem_erro_sintatico = True
      self.arquivo_saida.write("Erro sintatico - Esperado as palavras reservadas 'cadeida' ou 'char' ou 'inteiro' ou 'real' ou 'booleano' - linha: "+self.linha_atual+"\n")
      print("Erro sintatico - Esperado as palavras reservadas 'cadeida' ou 'char' ou 'inteiro' ou 'real' ou 'booleano' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      print('Token problemático: '+self.tokens[self.i])
      self.tem_erro_sintatico = True
      while( not 'tok500_' in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        
  # <constantes_declaracao> := constantes { <declaracao_const>  }                                                          
  def constantes_declaracao(self):
    
        
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if( 'tok602_constantes' in self.tokens[self.i] ):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        if( 'tok204_{' in self.tokens[self.i] ):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          if( not "tok205_}" in self.tokens[self.i] ):
            self.declaracao_const()
          if( 'tok205_}' in self.tokens[self.i] ):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          else:
            print("Erro sintatico - Esperado '}' - linha: "+self.linha_atual+"\n")
            self.arquivo_saida.write("Erro sintatico  - Esperado '}' - linha: "+self.linha_atual+"\n")
            print('Token problemático: '+self.tokens[self.i])
            self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
            self.tem_erro_sintatico = True
            if('tok601_variaveis' in self.tokens[self.i]):
              self.i += 1
              self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
            while( not 'tok601_variaveis' in self.tokens[self.i]):
              self.i += 1
              self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        else:
          print("Erro sintatico - Esperado '{' - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write("Erro sintatico  - Esperado '{' - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          self.tem_erro_sintatico = True
          while( not 'tok601_variaveis' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - Esperado a palavras reservada 'constantes' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write("Erro sintatico  - Esperado as palavras reservadas 'constantes' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while( not 'tok601_variaveis' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        
  # <declaracao_const> := <declaracao> = <valor_primitivo>; <declaracao_const> | Ɛ                                        
  def declaracao_const(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok205_}" in self.tokens[self.i]):
      return
    self.declaracao()
    if( 'tok115_=' in self.tokens[self.i] ):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.valor_primitivo()
      if( 'tok200_;' in self.tokens[self.i] ):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        self.declaracao_const()
      else:
        self.arquivo_saida.write("Erro sintatico - Esperado símbolo ';' - linha: "+self.linha_atual+"\n")
        print("Erro sintatico - Esperado símbolo ';' - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        print('Token problemático: '+self.tokens[self.i])
        self.tem_erro_sintatico = True
        while( not 'tok205_}' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - Esperado '=' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write("Erro sintatico  - Esperado '=' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while( not 'tok205_}' in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]

  # <valor_primitivo> := token_cadeia | token_real | token_inteiro | token_char | verdadeiro | falso                       
  def valor_primitivo(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if( 'tok300_' in self.tokens[self.i] or 
      'tok301_' in self.tokens[self.i] or
      'tok700_' in self.tokens[self.i] or
      'tok400_' in self.tokens[self.i] or
      'tok618_verdadeiro' in self.tokens[self.i] or
      'tok619_falso' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      self.arquivo_saida.write("Erro sintatico - Esperado valor primitivo (numero, cadeia, char, verdadeiro ou falso):  - linha: "+self.linha_atual+"\n")
      print("Erro sintatico - Esperado valor primitivo (numero, cadeia, char, verdadeiro ou falso):  - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      print('Token problemático: '+self.tokens[self.i])
      self.tem_erro_sintatico = True
      while( not 'tok200_;' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        
      
  # <variaveis_declaracao> := variaveis { <declaracao_var> }                                                               
  def variaveis_declaracao(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if( 'tok601_variaveis' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      if( 'tok204_{' in self.tokens[self.i] ):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        # Indica que acabou a minha declaracao de registro
        if( not "tok205_}" in self.tokens[self.i] ):
          self.declaracao_var()
        if( 'tok205_}' in self.tokens[self.i] ):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        else:
          self.arquivo_saida.write("Erro sintatico - Esperado símbolo '}' ao final do bloco de variáveis - linha: "+self.linha_atual+"\n")
          print("Erro sintatico - Esperado símbolo '}' ao final do bloco de variáveis - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          print('Token problemático: '+self.tokens[self.i])
          self.tem_erro_sintatico = True
          if('tok604_funcao' in self.tokens[self.i] or "tok600_algoritmo" in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          while( not 'tok604_funcao' in self.tokens[self.i] or "tok600_algoritmo" in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Esperado símbolo '{' após a declaração de variáveis - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write("Erro sintatico - Esperado símbolo '{' após a declaração de variáveis - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while( not 'tok604_funcao' in self.tokens[self.i] or "tok600_algoritmo" in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - A declaracao do bloco de variáveis, mesmo que vazio, é obrigatória nessa linguagem - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write("Erro sintatico - A declaracao do bloco de variáveis, mesmo que vazio, é obrigatória nessa linguagem - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while( not 'tok604_funcao' in self.tokens[self.i] or "tok600_algoritmo" in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      
  # <declaracao_var> := <declaracao> <identificador_deriva>; <declaracao_var> | token_identificador token_identificador; <declaracao_var> | Ɛ 
  def declaracao_var(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    # No caso da declaração ser de um tipo registro, espero um identificador
    if( 'tok500_' in self.tokens[self.i] ):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      if( 'tok500_' in self.tokens[self.i] ):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        if( 'tok200_;' in self.tokens[self.i] ):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          if(not 'tok205_}' in self.tokens[self.i] ):
            self.declaracao_var()
        else:
          print("Erro sintatico - Esperado símbolo ';' após identificador nome do tipo registro declarado - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.arquivo_saida.write("Erro sintatico - Esperado símbolo ';' após identificador nome do tipo registro declarado - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          self.tem_erro_sintatico = True
          while( not 'tok617_cadeia' in self.tokens[self.i] or 
          not 'tok614_real' in self.tokens[self.i] or
          not 'tok613_inteiro' in self.tokens[self.i] or
          not 'tok616_char' in self.tokens[self.i] or
          not 'tok615_booleano' in self.tokens[self.i] or
          not 'tok500_' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Esperado identificador nome do tipo registro declarado - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperado identificador nome do tipo registro declarado - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while( not 'tok617_cadeia' in self.tokens[self.i] or 
          not 'tok614_real' in self.tokens[self.i] or
          not 'tok613_inteiro' in self.tokens[self.i] or
          not 'tok616_char' in self.tokens[self.i] or
          not 'tok615_booleano' in self.tokens[self.i] or
          not   'tok500_' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    elif('tok617_cadeia' in self.tokens[self.i] or 
          'tok614_real' in self.tokens[self.i] or
          'tok613_inteiro' in self.tokens[self.i] or
          'tok616_char' in self.tokens[self.i] or
          'tok615_booleano' in self.tokens[self.i]):
      self.declaracao()
      self.identificador_deriva()
      if( 'tok200_;' in self.tokens[self.i] ):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        if( not 'tok205_}' in self.tokens[self.i] ):
          self.declaracao_var()
      else:
        print("Erro sintatico - Esperado símbolo ';' após a declaração da varável simples, vetor ou matriz - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperado símbolo ';' após a declaração da varável simples, vetor ou matriz - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while( not 'tok617_cadeia' in self.tokens[self.i] or 
          not 'tok614_real' in self.tokens[self.i] or
          not 'tok613_inteiro' in self.tokens[self.i] or
          not 'tok616_char' in self.tokens[self.i] or
          not 'tok615_booleano' in self.tokens[self.i] or
          not 'tok500_' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      if('tok200_;' in self.tokens[self.i]):
        while('tok200_;' in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        self.arquivo_saida.write("Erro sintatico - ';' duplicados:  - linha: "+self.linha_atual+"\n")
        print("Erro sintatico - ';' duplicados "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        print('Token problemático: '+self.tokens[self.i])
        self.tem_erro_sintatico = True
      self.arquivo_saida.write("Erro sintatico - Esperado as palavras reservadas 'cadeida' ou 'char' ou 'inteiro' ou 'real' ou 'booleano' ou Tipo de Registro - linha: "+self.linha_atual+"\n")
      print("Erro sintatico - Esperado as palavras reservadas 'cadeida' ou 'char' ou 'inteiro' ou 'real' ou 'booleano' ou Tipo de Registro - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      print('Token problemático: '+self.tokens[self.i])
      self.tem_erro_sintatico = True
      while( not 'tok617_cadeia' in self.tokens[self.i] or 
          not 'tok614_real' in self.tokens[self.i] or
          not 'tok613_inteiro' in self.tokens[self.i] or
          not 'tok616_char' in self.tokens[self.i] or
          not 'tok615_booleano' in self.tokens[self.i] or
          not 'tok500_' in self.tokens[self.i] ):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      
  # <identificador_deriva> := [token_inteiro]<matriz> | <inicializacao> | Ɛ                                                
  def identificador_deriva(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok200_;' in self.tokens[self.i]):
      return
    elif ( 'tok206_[' in self.tokens[self.i] ):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      if ( 'tok300_' in self.tokens[self.i] ):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        if ( 'tok207_]' in self.tokens[self.i] ):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          self.matriz()
        else:
          print("Erro sintatico - Colchetes desbalanceados - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.arquivo_saida.write("Erro sintatico - Colchetes desbalanceados - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          self.tem_erro_sintatico = True
          while( not 'tok200_;' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Esperado número inteiro após a declaração de vetor ou matriz - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperado número inteiro após a declaração de vetor ou matriz - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while( not 'tok200_;' in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    elif('tok115_=' in self.tokens[self.i]):
          self.inicializacao()
    else:
      print("Erro sintatico - Esperado '[' ou '=' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado '[' ou '=' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while( not 'tok200_;' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      
  # <matriz> := [token_inteiro] | Ɛ                                                                                        
  def matriz(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok200_;' in self.tokens[self.i]):
      return
    elif ( 'tok206_[' in self.tokens[self.i] ):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      if ( 'tok300_' in self.tokens[self.i] ):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        if ( 'tok207_]' in self.tokens[self.i] ):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        else:
          print("Erro sintatico - Colchetes desbalanceados - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.arquivo_saida.write("Erro sintatico - Colchetes desbalanceados - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          self.tem_erro_sintatico = True
          while( not 'tok200_;' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Esperado número inteiro após a declaração de vetor ou matriz - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperado número inteiro após a declaração de vetor ou matriz - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while( not 'tok200_;' in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - Esperado '[' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado '[' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while( not 'tok200_;' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        
  # <inicializacao> := = <valor_primitivo> | Ɛ                                                                             
  def inicializacao(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok200_;' in self.tokens[self.i]):
      return
    elif('tok115_=' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.valor_primitivo()
        
  # <funcao_declaracao> := funcao <tipo_return> token_identificador (<decl_param>)  { <deriva_cont_funcao>  } <funcao_declaracao> | Ɛ 
  def funcao_declaracao(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if ("tok600_algoritmo" in self.tokens[self.i]):
      return
    elif('tok604_funcao' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.tipo_return()
      if( 'tok500_' in self.tokens[self.i] ):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        if( 'tok202_(' in self.tokens[self.i] ):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          if(not 'tok203_)' in self.tokens[self.i] ):
            self.decl_param()
          if( 'tok203_)' in self.tokens[self.i] ):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
            if( 'tok204_{' in self.tokens[self.i] ):
              self.i += 1
              self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
              if(not 'tok205_}' in self.tokens[self.i] ):
                self.deriva_cont_funcao()
              if( 'tok205_}' in self.tokens[self.i] ):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
                self.funcao_declaracao()
              else:
                print("Erro sintatico - Esperado símbolo '}' ao final do bloco da função, chaves desbalanceadas - linha: "+self.linha_atual+"\n")
                print('Token problemático: '+self.tokens[self.i])
                self.arquivo_saida.write("Erro sintatico - Esperado símbolo '}' ao final do bloco da função, chaves desbalanceadas - linha: "+self.linha_atual+"\n")
                self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
                self.tem_erro_sintatico = True
                while(not "tok600_algoritmo" in self.tokens[self.i] or
                  not 'tok604_funcao' in self.tokens[self.i]):
                  self.i += 1
                  self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
            else:
              print("Erro sintatico - Esperado símbolo '{' após o fechamento de parêntesis da declaração de parâmetros da função - linha: "+self.linha_atual+"\n")
              print('Token problemático: '+self.tokens[self.i])
              self.arquivo_saida.write("Erro sintatico - Esperado símbolo '{' após o fechamento de parêntesis da declaração de parâmetros da função - linha: "+self.linha_atual+"\n")
              self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
              self.tem_erro_sintatico = True
              while(not "tok600_algoritmo" in self.tokens[self.i] or
              not 'tok604_funcao' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          else:
            print("Erro sintatico - Esperado símbolo ')' ao final da declaração de parâmetros da função, parêntesis desbalanceados - linha: "+self.linha_atual+"\n")
            print('Token problemático: '+self.tokens[self.i])
            self.arquivo_saida.write("Erro sintatico - Esperado símbolo ')' ao final da declaração de parâmetros da função, parêntesis desbalanceados - linha: "+self.linha_atual+"\n")
            self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
            self.tem_erro_sintatico = True
            while( not "tok600_algoritmo" in self.tokens[self.i] or
            not 'tok604_funcao' in self.tokens[self.i]):
              self.i += 1
              self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        else:
          print("Erro sintatico - Esperado símbolo '(' no início da declaração de parâmetros da função - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.arquivo_saida.write("Erro sintatico - Esperado símbolo '(' no início da declaração de parâmetros da função - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          self.tem_erro_sintatico = True
          while("tok600_algoritmo" in self.tokens[self.i] or
            'tok604_funcao' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          while(not "tok600_algoritmo" in self.tokens[self.i] or
            not 'tok604_funcao' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Esperado identificador com o nome da função declarada - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperado identificador com o nome da função declarada - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not "tok600_algoritmo" in self.tokens[self.i] or
            not 'tok604_funcao' in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - Esperado palavra reservada funcao - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado palavra reservada funcao - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      if("tok600_algoritmo" in self.tokens[self.i] or
         'tok604_funcao' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      while(not "tok600_algoritmo" in self.tokens[self.i] or
             not 'tok604_funcao' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        
  # <tipo_return> := <tipo_primitivo> | vazio | token_identificador<identificador_param_deriva> 
  def tipo_return(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if( 'tok606_vazio' in self.tokens[self.i] ):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    elif ('tok500_' in self.tokens[self.i] ):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.identificador_param_deriva()
    elif('tok617_cadeia' in self.tokens[self.i] or 
          'tok614_real' in self.tokens[self.i] or
          'tok613_inteiro' in self.tokens[self.i] or
          'tok616_char' in self.tokens[self.i] or
          'tok615_booleano' in self.tokens[self.i]):
      self.tipo_primitivo()
    else:
      print("Erro sintatico - Esperado tipo de retorno da funcao - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado tipo de retorno da funcao - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok500_' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    
  # <decl_param> := <declaracao> <identificador_param_deriva> <deriva_param> | token_identificador token_identificador <deriva_param> 
  def decl_param(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if ('tok500_' in self.tokens[self.i] ):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      if ('tok500_' in self.tokens[self.i] ):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        self.deriva_param()
      else:
        print("Erro sintatico - Esperado identificador com o nome registro declarado como parâmetro - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperado identificador com o nome registro declarado como parâmetro - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not 'tok201_,' in self.tokens[self.i] or
         not 'tok203_)' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    elif('tok617_cadeia' in self.tokens[self.i] or 
      'tok614_real' in self.tokens[self.i] or
      'tok613_inteiro' in self.tokens[self.i] or
      'tok616_char' in self.tokens[self.i] or
      'tok615_booleano' in self.tokens[self.i]):
        self.declaracao()
        self.identificador_param_deriva()
        self.deriva_param()
    else:
      print("Erro sintatico - Esperado tipo primitivo ou um tipo registro na declaracao de parametros - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado tipo primitivo ou um tipo registro na declaracao de parametros - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok201_,' in self.tokens[self.i] or
         not 'tok203_)' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]

  # <identificador_param_deriva> := []<matriz_param> | Ɛ
  def identificador_param_deriva(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok201_,' in self.tokens[self.i] or
        'tok203_)' in self.tokens[self.i] or
        'tok500_' in self.tokens[self.i] ):
      return
    elif('tok206_[' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      if('tok207_]' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        self.matriz_param()
      else:
        print("Erro sintatico - Esperado símbolo ']' na declaracao do parâmetro vetor ou matriz, colchetes desbalanceados - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperado símbolo ']' na declaracao do parâmetro vetor ou matriz, colchetes desbalanceados - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not 'tok201_,' in self.tokens[self.i] or
            not 'tok203_)' in self.tokens[self.i] or
            not 'tok500_' in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - Esperado símbolo '[' na declaracao do parâmetro vetor ou matriz, colchetes desbalanceados - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado símbolo '[' na declaracao do parâmetro vetor ou matriz, colchetes desbalanceados - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok201_,' in self.tokens[self.i] or
            not 'tok203_)' in self.tokens[self.i] or
            not 'tok500_' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]

  # <matriz_param> := [] | Ɛ
  def matriz_param(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok201_,' in self.tokens[self.i] or
        'tok203_)' in self.tokens[self.i] or
        'tok500_' in self.tokens[self.i]):
      return
    elif('tok206_[' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      if('tok207_]' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Esperado símbolo ']' na declaracao do parâmetro vetor ou matriz, colchetes desbalanceados - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperado símbolo ']' na declaracao do parâmetro vetor ou matriz, colchetes desbalanceados - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not 'tok201_,' in self.tokens[self.i] or
            not 'tok203_)' in self.tokens[self.i] or
            not 'tok500_' in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]

    else:
      print("Erro sintatico - Esperado símbolo '[' na declaracao do parâmetro vetor ou matriz, colchetes desbalanceados - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado símbolo '[' na declaracao do parâmetro vetor ou matriz, colchetes desbalanceados - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok201_,' in self.tokens[self.i] or
            not 'tok203_)' in self.tokens[self.i] or
            not 'tok500_' in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]

  # <deriva_param> := ,<decl_param> | Ɛ
  def deriva_param(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok203_)' in self.tokens[self.i]):
      return
    elif('tok201_,' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.decl_param()
    else:
      print("Erro sintatico - Esperado símbolo ',' no parâmetro da funcao - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado símbolo ',' no parâmetro da funcao - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok201_,' in self.tokens[self.i] or
           not 'tok203_)' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
            
  # <deriva_cont_funcao> := <variaveis_declaracao> <decl_comandos> retorno <return_deriva>; | <decl_comandos> retorno <return_deriva>;
  def deriva_cont_funcao(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok601_variaveis' in self.tokens[self.i]):
      self.variaveis_declaracao()
      self.decl_comandos()
      if('tok605_retorno' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        self.return_deriva()
        if('tok200_;' in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        else:
          print("Erro sintatico - Esperado símbolo ';' ao final da declaração de retorno da função - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.arquivo_saida.write("Erro sintatico - Esperado símbolo ';' ao final da declaração de retorno da função - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          self.tem_erro_sintatico = True
          while(not 'tok205_}' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Esperada palavra reservada retorno para indicar que a função acabou e está retornando algo ou vazio - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperada palavra reservada retorno para indicar que a função acabou e está retornando algo ou vazio - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not 'tok205_}' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    elif( 'tok607_se' in self.tokens[self.i] or
        'tok612_escreva' in self.tokens[self.i] or
        'tok611_leia' in self.tokens[self.i] or
        'tok609_enquanto' in self.tokens[self.i] or
        'tok610_para' in self.tokens[self.i] or
        'tok500_' in self.tokens[self.i]):
          self.decl_comandos()
          if('tok605_retorno' in self.tokens[self.i]):
              self.i += 1
              self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
              self.return_deriva()
          else:
              print("Erro sintatico - Esperada palavra reservada retorno para indicar que a função acabou e está retornando algo ou vazio - linha: "+self.linha_atual+"\n")
              print('Token problemático: '+self.tokens[self.i])
              self.arquivo_saida.write("Erro sintatico - Esperada palavra reservada retorno para indicar que a função acabou e está retornando algo ou vazio - linha: "+self.linha_atual+"\n")
              self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
              self.tem_erro_sintatico = True
              while(not 'tok205_}' in self.tokens[self.i]):
                  self.i += 1
                  self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - Esperado declaracao de variveis ou declaracao de comandos - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado declaracao de variveis ou declaracao de comandos - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok205_}' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
            
  # <return_deriva> := vazio | token_identificador<identificador_imp_arm_deriva> | <valor_primitivo>
  def return_deriva(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if( 'tok606_vazio' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    elif('tok500_' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.identificador_imp_arm_deriva()
    elif('tok617_cadeia' in self.tokens[self.i] or 
      'tok614_real' in self.tokens[self.i] or
      'tok613_inteiro' in self.tokens[self.i] or
      'tok616_char' in self.tokens[self.i] or
      'tok615_booleano' in self.tokens[self.i]):
        self.valor_primitivo()
    else:
      print("Erro sintatico - Esperado o retorno da funcao - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado o retorno da funcao - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok200_;' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
  # <decl_comandos> := <comandos> <decl_comandos> | Ɛ
  def decl_comandos(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
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
    else: 
      print("Erro sintatico - Esperado uma atribuicao ou um comando - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado uma atribuicao ou um comando - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok605_retorno' in self.tokens[self.i] or
       not 'tok205_}' in self.tokens[self.i] or
       not 'tok607_se' in self.tokens[self.i] or
       not 'tok612_escreva' in self.tokens[self.i] or
       not 'tok611_leia' in self.tokens[self.i] or
       not 'tok609_enquanto' in self.tokens[self.i] or
       not 'tok610_para' in self.tokens[self.i] or
       not 'tok500_' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      
      
  # <comandos> := <se_declaracao> | <enquanto_declaracao> | <para_declaracao> | <escreva_declaracao> | <leia_declaracao> | <atribuicao> | Ɛ
  def comandos(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
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
    else:
      print("Erro sintatico - Esperado uma atribuicao ou um comando - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado uma atribuicao ou um comando - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i] or
            not 'tok205_}' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      
  #<atribuicao> := token_identificador <identificador_imp_arm_deriva>  = <atribuicao_deriva>;
  def atribuicao(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok500_' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.identificador_imp_arm_deriva()
      if('tok115_=' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        self.atribuicao_deriva()
        if('tok200_;' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        else:
          print("Erro sintatico - Esperado ';' - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.arquivo_saida.write("Erro sintatico - Esperado ';' - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          self.tem_erro_sintatico = True
          while(not 'tok607_se' in self.tokens[self.i] or
           not 'tok612_escreva' in self.tokens[self.i] or
           not 'tok611_leia' in self.tokens[self.i] or
           not 'tok609_enquanto' in self.tokens[self.i] or
           not 'tok610_para' in self.tokens[self.i] or
           not 'tok500_' in self.tokens[self.i] or
           not 'tok605_retorno' in self.tokens[self.i] or
           not 'tok205_}' in self.tokens[self.i]):
              self.i += 1
              self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Esperado '=' - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperado '=' - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not 'tok607_se' in self.tokens[self.i] or
           not 'tok612_escreva' in self.tokens[self.i] or
           not 'tok611_leia' in self.tokens[self.i] or
           not 'tok609_enquanto' in self.tokens[self.i] or
           not 'tok610_para' in self.tokens[self.i] or
           not 'tok500_' in self.tokens[self.i] or
           not 'tok605_retorno' in self.tokens[self.i] or
           not 'tok205_}' in self.tokens[self.i]):
              self.i += 1
              self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - Esperado uma variavel - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado uma variavel - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i] or
            not 'tok205_}' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
  #<atribuicao_deriva> := <exp_simples> | <chamada_funcao>
  def atribuicao_deriva(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok500_' in self.tokens[self.i]):
      self.chamada_funcao()
    elif('tok202_(' in self.tokens[self.i] or
         'tok101_+' in self.tokens[self.i] or
         'tok102_-' in self.tokens[self.i] or
         'tok500_' in self.tokens[self.i] or
         'tok300_' in self.tokens[self.i]):
      self.exp_simples()
    else:
      print("Erro sintatico - Esperando uma expressão aritmetica ou uma chamada de funcao - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperando uma expressão aritmetica ou uma chamada de funcao - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok200_;' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
  
  #<chamada_funcao> := token_identificador (<decl_param_chamada>)
  def chamada_funcao(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok500_' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      if('tok202_(' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        self.decl_param_chamada()
        if('tok203_)' in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        else:
          print("Erro sintatico - Esperada símbolo ')' para finalizar bloco de comando <chamada_funcao> - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.arquivo_saida.write("Erro sintatico - Esperada símbolo ')' para finalizar bloco de comando <chamada_funcao> - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          self.tem_erro_sintatico = True
          while(not 'tok200_;' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Esperada símbolo '(' para finalizar bloco de comando <chamada_funcao> - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperada símbolo '(' para finalizar bloco de comando <chamada_funcao> - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not 'tok200_;' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - Esperada símbolo 'tok500_' para finalizar bloco de comando <chamada_funcao> - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperada símbolo 'tok500_' para finalizar bloco de comando <chamada_funcao> - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok200_;' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]

  #<decl_param_chamada> := <decl_chamada> <chamada_param_deriva> | Ɛ
  def decl_param_chamada(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok203_)' in self.tokens[self.i]):
      return
    elif('tok500_' in self.tokens[self.i] or 'tok400_' in self.tokens[self.i] or 'tok700_' in self.tokens[self.i] or 'tok300_' in self.tokens[self.i] or 'tok301_' in self.tokens[self.i]):
      self.decl_chamada()
      self.chamada_param_deriva()
    else:
      print("Erro sintatico - Esperando uma expressão aritmetica ou uma chamada de funcao - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperando um numero, vetor, matriz ou registro - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok201_,' in self.tokens[self.i] or
            not 'tok203_)' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    
  #<decl_chamada> := token_identifcador<identificador_imp_arm_deriva> | <valor_primitivo>
  def decl_chamada(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok500_' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.identificador_imp_arm_deriva()
    elif('tok700_' in self.tokens[self.i] or 'tok400_' in self.tokens[self.i] or 'tok300_' in self.tokens[self.i] or 'tok301_' in self.tokens[self.i]):
      self.valor_primitivo()
    else:
      print("Erro sintatico - Esperado valores primitvos ou um registro ou vetor ou uma matriz ou uma variavel - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado valores primitvos ou um registro ou vetor ou uma matriz ou uma variavel - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok201_,' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]

  #<chamada_param_deriva> := , <decl_param_chamada> | Ɛ
  def chamada_param_deriva(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok203_)' in self.tokens[self.i]):
      return
    elif('tok201_,' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.decl_param_chamada()
    else:
      print("Erro sintatico - Esperado ',' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado ',' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok201_,' in self.tokens[self.i] or
            not 'tok203_)' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
     
# <identificador_imp_arm_deriva> := .token_identificador | [<indice>]<matriz_chamada> | Ɛ    
  def identificador_imp_arm_deriva(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
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
          return
    elif("tok100_." in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      if("tok500_" in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    elif("tok206_[" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.indice()
      if("tok207_]" in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          self.matriz_chamada()
      else:
        print("Erro sintatico - Esperado símbolo ']' - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Esperado símbolo ']'  - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not 'tok200_;' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
        print("Erro sintatico - Esperado símbolo '.' ou '[' - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Esperado símbolo '.' ou '[' - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not 'tok200_;' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    
  #<matriz_chamada> := [<indice>] | Ɛ
  def matriz_chamada(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok200_;" in self.tokens[self.i]):
      return
    elif("tok206_[" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.indice()
      if("tok207_]" in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Esperado símbolo ']' - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Esperado símbolo ']' - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not 'tok200_;' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - Esperado símbolo '[' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Esperado símbolo '[' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok200_;' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
            
  #<indice> := token_inteiro | Ɛ
  def indice(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok207_]' in self.tokens[self.i]):
      return
    if('tok300_' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - Esperado indice do vetor ou matriz - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Esperado indice um vetor ou matriz ou '[]' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok207_]' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      
  # <se_declaracao> := se (<exp_rel_bol>) {<decl_comandos>}<senao_decl>
  def se_declaracao(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok607_se" in self.tokens[self.i]):
      self.i += 1
      if("tok202_(" in self.tokens[self.i]):
        self.i += 1
        self.exp_rel_bol()
        if("tok203_)" in self.tokens[self.i]):
          self.i += 1
          if('tok204_{' in self.tokens[self.i]):
            self.i += 1
            self.decl_comandos()
            if('tok205_}' in self.tokens[self.i]):
              self.i += 1
              self.senao_decl()
            else:
              print("Erro sintatico - Esperada símbolo '}'  para finalizar bloco de comando do 'se' - linha: "+self.linha_atual+"\n")
              print('Token problemático: '+self.tokens[self.i])
              self.arquivo_saida.write("Erro sintatico - Esperada símbolo '}'  para finalizar bloco de comando do 'se' - linha: "+self.linha_atual+"\n")
              self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
              self.tem_erro_sintatico = True
              while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        
          else:
            print("Erro sintatico - Esperada símbolo '{'  para iniciar o bloco de comando do 'se' - linha: "+self.linha_atual+"\n")
            print('Token problemático: '+self.tokens[self.i])
            self.arquivo_saida.write("Erro sintatico - Esperada símbolo '{'  para iniciar o bloco de comando do 'se' - linha: "+self.linha_atual+"\n")
            self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
            self.tem_erro_sintatico = True
            while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        else:
          print("Erro sintatico - Esperada símbolo ')'  para finalizar a expressão do comando 'se', parêtensis desbalaceados - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.arquivo_saida.write("Erro sintatico - Esperada símbolo ')'  para finalizar a expressão do comando 'se', parêtensis desbalaceados - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          self.tem_erro_sintatico = True
          while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Esperada símbolo '(' após o comando se - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperada símbolo '(' após o comando se - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        
    else:
      print("Erro sintatico - Esperada comando 'se' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperada comando 'se' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        

  # <senao_decl> := senao {<decl_comandos>} | Ɛ
  def senao_decl(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
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
      self.i += 1
      if('tok204_{' in self.tokens[self.i]):
        self.i += 1
        self.decl_comandos()
        if('tok205_}' in self.tokens[self.i]):
          self.i += 1
        else:
          print("Erro sintatico - Esperada símbolo '}'  para finalizar para finalizar o bloco de comando do 'senao' - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.arquivo_saida.write("Erro sintatico - Esperada símbolo '}'  para finalizar para finalizar o bloco de comando do 'senao' - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          self.tem_erro_sintatico = True
          while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Esperada símbolo '{'  para iniciar o bloco de comando do 'senao' - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperada símbolo '{'  para iniciar o bloco de comando do 'senao' - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
        print("Erro sintatico - Esperado o bloco de comando do 'senao' - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperado o bloco de comando do 'senao' - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      
  # <enquanto_declaracao> := enquanto (<exp_rel_bol>) { <decl_comandos> }
  def enquanto_declaracao(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok609_enquanto" in self.tokens[self.i]):
      self.i += 1
      if("tok202_(" in self.tokens[self.i]):
        self.i += 1
        self.exp_rel_bol()
        if("tok203_)" in self.tokens[self.i]):
          self.i += 1
          if('tok204_{' in self.tokens[self.i]):
            self.i += 1
            self.decl_comandos()
            if('tok205_}' in self.tokens[self.i]):
              self.i += 1
            else:
              print("Erro sintatico - Esperada símbolo '}'  para finalizar bloco de comando do 'enquanto' - linha: "+self.linha_atual+"\n")
              print('Token problemático: '+self.tokens[self.i])
              self.tem_erro_sintatico = True
              self.arquivo_saida.write("Erro sintatico - Esperada símbolo '}'  para finalizar bloco de comando do 'enquanto' - linha: "+self.linha_atual+"\n")
              self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
              while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          else:
            print("Erro sintatico - Esperada símbolo '{'  para iniciar o bloco de comando do 'enquanto' - linha: "+self.linha_atual+"\n")
            print('Token problemático: '+self.tokens[self.i])
            self.tem_erro_sintatico = True
            self.arquivo_saida.write("Erro sintatico - Esperada símbolo '{'  para iniciar o bloco de comando do 'enquanto' - linha: "+self.linha_atual+"\n")
            self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
            while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        else:
          print("Erro sintatico - Esperada símbolo ')'  para finalizar a expressão do comando 'enquanto', parêtensis desbalaceados - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.tem_erro_sintatico = True
          self.arquivo_saida.write("Erro sintatico - Esperada símbolo ')'  para finalizar a expressão do comando 'enquanto', parêtensis desbalaceados - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Esperada símbolo '(' após o comando enquanto - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.tem_erro_sintatico = True
        self.arquivo_saida.write("Erro sintatico - Esperada símbolo '(' após o comando enquanto - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        
    else:
      print("Erro sintatico - Esperada comando 'enquanto' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperada comando 'enquanto' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]

  # <para_declaracao> := para (token_identificador = token_inteiro; token_identificador <op_relacional> token_inteiro; token_identificador <op_cont>) {<decl_comandos>}
  def para_declaracao(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok610_para" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      if("tok202_(" in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        if("tok500_" in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          if("tok115_=" in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
            if("tok300_" in self.tokens[self.i]):
              self.i += 1
              self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
              if("tok200_;" in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
                if("tok500_" in self.tokens[self.i]):
                  self.i += 1
                  self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
                  self.op_relacional()
                  if("tok300_" in self.tokens[self.i]):
                    self.i += 1
                    self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
                    if("tok200_;" in self.tokens[self.i]):
                      self.i += 1
                      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
                      if("tok500_" in self.tokens[self.i]):
                        self.i += 1
                        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
                        self.op_cont()
                        if("tok203_)" in self.tokens[self.i]):
                          self.i += 1
                          if("tok204_{" in self.tokens[self.i]):
                            self.i += 1
                            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
                            self.decl_comandos()
                            if("tok205_}" in self.tokens[self.i]):
                              self.i += 1
                              self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
                            else:
                              print("Erro sintatico - Esperada símbolo '}' para fechar bloco do comando 'para' - linha: "+self.linha_atual+"\n")
                              print('Token problemático: '+self.tokens[self.i])
                              self.tem_erro_sintatico = True
                              self.arquivo_saida.write("Erro sintatico - Esperada símbolo '}' para fechar bloco do comando 'para' - linha: "+self.linha_atual+"\n")
                              self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
                              while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                                  self.i += 1
                                  self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
                          else:
                              print("Erro sintatico - Esperada símbolo '{' para abrir bloco do comando 'para' - linha: "+self.linha_atual+"\n")
                              print('Token problemático: '+self.tokens[self.i])
                              self.tem_erro_sintatico = True
                              self.arquivo_saida.write("Erro sintatico - Esperada símbolo '{' para abrir bloco do comando 'para' - linha: "+self.linha_atual+"\n")
                              self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
                              while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                                  self.i += 1
                                  self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
                        else:
                          print("Erro sintatico - Espera-se símbolo ')' para fechar declarações do comando para - linha: "+self.linha_atual+"\n")
                          print('Token problemático: '+self.tokens[self.i])
                          self.tem_erro_sintatico = True
                          self.arquivo_saida.write("Erro sintatico - Espera-se símbolo ')' para fechar declarações do comando para - linha: "+self.linha_atual+"\n")
                          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
                          while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                                self.i += 1
                                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
                      else:
                        print("Erro sintatico - Espera-se identificador para incremento ou decremento ao final do comando para - linha: "+self.linha_atual+"\n")
                        print('Token problemático: '+self.tokens[self.i])
                        self.tem_erro_sintatico = True
                        self.arquivo_saida.write("Erro sintatico - Espera-se identificador para incremento ou decremento ao final do comando para - linha: "+self.linha_atual+"\n")
                        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
                        while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                              self.i += 1
                              self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
                    else:
                      print("Erro sintatico - Espera-se o símbolo ';' ao final da expressão relacional do meio do comando 'para' - linha: "+self.linha_atual+"\n")
                      print('Token problemático: '+self.tokens[self.i])
                      self.arquivo_saida.write("Erro sintatico - Espera-se o símbolo ';' ao final da expressão relacional do meio do comando 'para' - linha: "+self.linha_atual+"\n")
                      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
                      self.tem_erro_sintatico = True
                      while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                            self.i += 1
                            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
                  else:
                    print("Erro sintatico - Espera-se número inteiro como parte da expressão relacional do meio do comando 'para' - linha: "+self.linha_atual+"\n")
                    print('Token problemático: '+self.tokens[self.i])
                    self.arquivo_saida.write("Erro sintatico - Espera-se número inteiro como parte da expressão relacional do meio do comando 'para' - linha: "+self.linha_atual+"\n")
                    self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
                    self.tem_erro_sintatico = True
                    while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                            self.i += 1
                            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
                else:
                  print("Erro sintatico - Espera-se identificador para a expressão relacional do meio do comando 'para' - linha: "+self.linha_atual+"\n")
                  print('Token problemático: '+self.tokens[self.i])
                  self.arquivo_saida.write("Erro sintatico - Espera-se identificador para a expressão relacional do meio do comando 'para' - linha: "+self.linha_atual+"\n")
                  self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
                  self.tem_erro_sintatico = True
                  while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                            self.i += 1
                            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
              else:
                print("Erro sintatico - Espera-se o símbolo ';' após a inicialização do identificador contador do comando 'para' - linha: "+self.linha_atual+"\n")
                print('Token problemático: '+self.tokens[self.i])
                self.arquivo_saida.write("Erro sintatico - Espera-se o símbolo ';' após a inicialização do identificador contador do comando 'para' - linha: "+self.linha_atual+"\n")
                self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
                self.tem_erro_sintatico = True
                while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                      self.i += 1
                      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
            else:
              print("Erro sintatico - Espera-se o número inteiro com o valor da inicialização do identificador contador do comando 'para' - linha: "+self.linha_atual+"\n")
              print('Token problemático: '+self.tokens[self.i])
              self.arquivo_saida.write("Erro sintatico - Espera-se o número inteiro com o valor da inicialização do identificador contador do comando 'para' - linha: "+self.linha_atual+"\n")
              self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
              self.tem_erro_sintatico = True
              while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                      self.i += 1
                      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          else:
            print("Erro sintatico - Espera-se símbolo '=' para indicar inicialização do identificador contador do 'para' - linha: "+self.linha_atual+"\n")
            print('Token problemático: '+self.tokens[self.i])
            self.arquivo_saida.write("Erro sintatico - Espera-se símbolo '=' para indicar inicialização do identificador contador do 'para' - linha: "+self.linha_atual+"\n")
            self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
            self.tem_erro_sintatico = True
            while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                    self.i += 1
                    self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        else:
          print("Erro sintatico - Espera-se identificador contador para ser inicializado - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.arquivo_saida.write("Erro sintatico - Espera-se identificador contador para ser inicializado - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          self.tem_erro_sintatico = True
          while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Espera-se símbolo '(' após o início do comando 'para' - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Espera-se símbolo '(' após o início do comando 'para' - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - Espera-se palavra reservada 'para' quando se inicia o comando 'para' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Espera-se palavra reservada 'para' quando se inicia o comando 'para' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]


  # <leia_declaracao> := leia (<exp_leia>); 
  def leia_declaracao(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok611_leia" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      if("tok202_(" in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        self.exp_leia()
        if("tok203_)" in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          if("tok200_;" in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          else:
            print("Erro sintatico - Espera-se símbolo ';' ao final da chamada de funcao 'leia' - linha: "+self.linha_atual+"\n")
            print('Token problemático: '+self.tokens[self.i])
            self.arquivo_saida.write("Erro sintatico - Espera-se símbolo ';' ao final da chamada de funcao 'leia' - linha: "+self.linha_atual+"\n")
            self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
            self.tem_erro_sintatico = True
            while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        else:
          print("Erro sintatico - Espera-se símbolo ')' ao final da declaração de parâmetros da chamada de funcao 'leia' - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.arquivo_saida.write("Erro sintatico - Espera-se símbolo ')' ao final da declaração de parâmetros da chamada de funcao 'leia' - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          self.tem_erro_sintatico = True
          while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Espera-se símbolo '(' ao início da declaração de parâmetros da chamada de funcao 'leia' - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Espera-se símbolo '(' ao início da declaração de parâmetros da chamada de funcao 'leia' - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - Espera-se palavra reservada escreva para chamada de funcao 'leia' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Espera-se palavra reservada escreva para chamada de funcao 'leia' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
  # <exp_leia> := <exp_armazena><exp_leia_deriva><exp_leia> | Ɛ
  def exp_leia(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok203_)" in self.tokens[self.i]):
      return
    elif("tok500_" in self.tokens[self.i]):
      self.exp_armazena()
      self.exp_leia_deriva()
      self.exp_leia()
    else:
      print("Erro sintatico - Espera-se uma variavel - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Espera-se uma variavel - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok203_)" in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      
  # <exp_leia_deriva> := ,<exp_armazena> | Ɛ
  def exp_leia_deriva(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok203_)" in self.tokens[self.i]):
      return
    elif("tok201_," in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.exp_armazena()
    else:
      print("Erro sintatico - Espera-se ',' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Espera-se ',' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok203_)" in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
                
  # <exp_armazena> := token_identificador <identificador_imp_arm_deriva>
  def exp_armazena(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok500_" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.identificador_imp_arm_deriva()
    else:
      print("Erro sintatico - Espera-se identificador - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Espera-se identificador - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok203_)" in self.tokens[self.i] or
            not "tok201_," in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
  # <escreva_declaracao> := escreva (<exp_escreva>);
  def escreva_declaracao(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok612_escreva" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      if("tok202_(" in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        self.exp_escreva()
        if("tok203_)" in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          if("tok200_;" in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          else:
            print("Erro sintatico - Espera-se símbolo ';' ao final da chamada de funcao 'escreva' - linha: "+self.linha_atual+"\n")
            print('Token problemático: '+self.tokens[self.i])
            self.arquivo_saida.write("Erro sintatico - Espera-se símbolo ';' ao final da chamada de funcao 'escreva' - linha: "+self.linha_atual+"\n")
            self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
            self.tem_erro_sintatico = True
            while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        else:
          print("Erro sintatico - Espera-se símbolo ')' ao final da declaração de parâmetros da chamada de funcao 'escreva' - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.arquivo_saida.write("Erro sintatico - Espera-se símbolo ')' ao final da declaração de parâmetros da chamada de funcao 'escreva' - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          self.tem_erro_sintatico = True
          while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Espera-se símbolo '(' ao início da declaração de parâmetros da chamada de funcao 'escreva' - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Espera-se símbolo '(' ao início da declaração de parâmetros da chamada de funcao 'escreva' - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - Espera-se palavra reservada escreva para chamada de funcao 'escreva' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Espera-se palavra reservada escreva para chamada de funcao 'escreva' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not 'tok607_se' in self.tokens[self.i] or
         not 'tok612_escreva' in self.tokens[self.i] or
         not 'tok611_leia' in self.tokens[self.i] or
         not 'tok609_enquanto' in self.tokens[self.i] or
         not 'tok610_para' in self.tokens[self.i] or
         not 'tok500_' in self.tokens[self.i] or
         not 'tok605_retorno' in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
  # <exp_escreva> := <exp_imprime><exp_escreva_deriva><exp_escreva> | Ɛ
  def exp_escreva(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok203_)" in self.tokens[self.i]):
      return
    elif("tok700_" in self.tokens[self.i] or "tok400_" in self.tokens[self.i] or "tok500_" in self.tokens[self.i] or "(" in self.tokens[self.i]):
      self.exp_imprime()
      self.exp_escreva_deriva
      self.exp_escreva()
    else:
      print("Erro sintatico - Espera-se uma variavel ou uma cadeia ou char ou um numero - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Espera-se uma variavel ou uma cadeia ou char ou um numero - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok203_)" in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
  # <exp_escreva_deriva> := ,<exp_imprime> | Ɛ
  def exp_escreva_deriva(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok203_)" in self.tokens[self.i]):
      return
    elif("tok201_," in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.exp_imprime()
    else:
      print("Erro sintatico - Espera-se ',' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Espera-se ',' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok203_)" in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    
  # <exp_imprime> := token_cadeia | token_char | token_identificador <identificador_imp_arm_deriva> | (<exp_simples>)
  def exp_imprime(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok700_" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    elif("tok400_" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    elif("tok500_" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.identificador_imp_arm_deriva()
    elif("tok202_(" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.exp_simples()
      if("tok203_)" in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Esperado símbolo ')' para fechamento de expressões - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperado símbolo ')' para fechamento de expressões - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not "tok203_)" in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - Esperado símbolo '(' para abertura de expressões ou uma cadeia ou um char ou um vetor ou uma matriz ou um registro - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado símbolo '(' para abertura de expressões ou uma cadeia ou um char ou um vetor ou uma matriz ou um registro - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok203_)" in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]



  # <exp_aritmetica> := token_identificador = <exp_simples>;
  #ELIMINADA
  def exp_aritmetica(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok500_" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      if("tok115_=" in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        self.exp_simples()
        if("tok200_;" in self.tokens[self.i]):
          self.i += 1
        else:
          print("Erro sintatico - Esperado símbolo (;) ao final do expressão aritmética - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.arquivo_saida.write("Erro sintatico - Esperado símbolo (;) ao final do expressão aritmética - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          self.tem_erro_sintatico = True  
      else:  
        print("Erro sintatico - Esperado símbolo '=' para atribuição de valores à variáveis - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperado símbolo '=' para atribuição de valores à variáveis - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
    else:
      print("Erro sintatico - Esperado um identificador representante da varíavel que receberá a atribuição - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado um identificador representante da varíavel que receberá a atribuição - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      
  # <exp_rel_bol> := <exp_boll> <op_relacional> <exp_boll> <exp_rel_deriva>
  def exp_rel_bol(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    #import pdb; pdb.set_trace() # Break do debbug
    if("tok500_" in self.tokens[self.i] or
       "tok300_" in self.tokens[self.i] or
       "tok202_(" in self.tokens[self.i]):
      self.exp_boll()
      self.op_relacional()
      self.exp_boll()
      self.exp_rel_deriva()
    else:
      print("Erro sintatico - Esperado uma variavel ou um numero ou '(' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado uma variavel ou um numero ou '(' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok203_)" in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]


  #<exp_boll> := <termo><termo_deriva>
  def exp_boll(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    #import pdb; pdb.set_trace() # Break do debbug
    if("tok500_" in self.tokens[self.i] or
       "tok300_" in self.tokens[self.i] or
       "tok202_(" in self.tokens[self.i]):
        self.termo()
        self.termo_deriva()
    else:
      print("Erro sintatico - Esperado uma variavel ou um numero ou '(' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado uma variavel ou um numero ou '(' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok112_<=" in self.tokens[self.i] or
            not "tok110_>=" in self.tokens[self.i] or
            not "tok109_>" in self.tokens[self.i] or
            not "tok111_<" in self.tokens[self.i] or
            not "tok107_==" in self.tokens[self.i] or
            not "tok108_!=" in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]


  
  # <exp_simples> := <op_ss><termo><termo_deriva> | <termo><termo_deriva>
  def exp_simples(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok101_+" in self.tokens[self.i] or "tok102_-" in self.tokens[self.i]):
      self.op_ss()
      self.termo()
      self.termo_deriva()
    elif("tok500_" in self.tokens[self.i] or
       "tok300_" in self.tokens[self.i] or
       "tok202_(" in self.tokens[self.i]):
      self.termo()
      self.termo_deriva()
    else:
      print("Erro sintatico - Esperado uma variavel ou um numero ou '(' ou '+' ou '-' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Esperado uma variavel ou um numero ou '(' ou '+' ou '-' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok112_<=" in self.tokens[self.i] or
            not "tok110_>=" in self.tokens[self.i] or
            not "tok109_>" in self.tokens[self.i] or
            not "tok111_<" in self.tokens[self.i] or
            not "tok107_==" in self.tokens[self.i] or
            not "tok108_!=" in self.tokens[self.i] or
            not "tok203_)" in self.tokens[self.i] or
            not "tok200_;" in self.tokens[self.i] or
            not "tok113_&&" in self.tokens[self.i] or
            not "tok114_||" in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]

  # <op_relacional> := < | > | == | != | <= | >=
  def op_relacional(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok112_<=" in self.tokens[self.i] or "tok110_>=" in self.tokens[self.i] or "tok109_>" in self.tokens[self.i] or "tok111_<" in self.tokens[self.i] or "tok107_==" in self.tokens[self.i] or "tok108_!=" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - Operador relacional era esperado: < | > | == | != | <= | >= - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Operador relacional era esperado: < | > | == | != | <= | >= - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while( not "tok500_" in self.tokens[self.i] or
       not "tok300_" in self.tokens[self.i] or
       not "tok202_(" in self.tokens[self.i] or
             not "tok101_+" in self.tokens[self.i] or
             not "tok102_-" in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      
  # <exp_rel_deriva> := <op_bolleano> <exp_simples> <op_relacional> <exp_simples> <exp_rel_deriva> | Ɛ
  def exp_rel_deriva(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok203_)" in self.tokens[self.i]):
      return
    elif("tok113_&&" in self.tokens[self.i] or "tok114_||" in self.tokens[self.i]):
      self.op_bolleano()
      self.exp_simples()
      self.op_relacional()
      self.exp_simples()
      self.exp_rel_deriva()
    else:
      print("Erro sintatico - Esperado operadores '&&' ou '||' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado uma variavel ou um numero ou '(' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok203_)" in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]

  # <op_ss> := + | -
  def op_ss(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok101_+" in self.tokens[self.i] or "tok102_-" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - esperado um '+' ou '-' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - esperado um '+' ou '-' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while( not"tok500_" in self.tokens[self.i] or
       not "tok300_" in self.tokens[self.i] or
       not "tok202_(" in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          
  # <termo> := <fator><fator_deriva>
  def termo(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok500_' in self.tokens[self.i] or 'tok300_' in self.tokens[self.i] or 'tok202_(' in self.tokens[self.i]):
      self.fator()
      self.fator_deriva()
    else:
      print("Erro sintatico - Esperado um identificador, número inteiro ou símbolo '(' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado um identificador, número inteiro ou símbolo '(' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while( not "tok101_+" in self.tokens[self.i] or
             not "tok102_-" in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
          

  # <termo_deriva> := +<op_soma_deriva> | -<op_sub_deriva> | Ɛ
  def termo_deriva(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
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
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.op_soma_deriva()
    elif('tok102_-' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.op_sub_deriva()
    else:
      print("Erro sintatico - Esperado '+' ou '-' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado '+' ou '-' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok112_<=" in self.tokens[self.i] or
            not "tok110_>=" in self.tokens[self.i] or
            not "tok109_>" in self.tokens[self.i] or
            not "tok111_<" in self.tokens[self.i] or
            not "tok107_==" in self.tokens[self.i] or
            not "tok108_!=" in self.tokens[self.i] or
            not "tok203_)" in self.tokens[self.i] or
            not "tok200_;" in self.tokens[self.i]or
            not "tok113_&&" in self.tokens[self.i] or
            not "tok114_||" in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    
  # <op_bolleano> := && | || 
  def op_bolleano(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok113_&&" in self.tokens[self.i] or "tok114_||" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - expressao booleana necessita de operadores booleanos '&&' ou '||' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - expressao booleana necessita de operadores booleanos '&&' ou '||' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while( not "tok101_+" in self.tokens[self.i] or
             not "tok102_-" in self.tokens[self.i] or
             not"tok500_" in self.tokens[self.i] or
             not "tok300_" in self.tokens[self.i] or
             not "tok202_(" in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      
  # <fator> := token_identificador <identificador_imp_arm_deriva> | token_inteiro | (<exp_simples>) 
  def fator(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok500_' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.identificador_imp_arm_deriva()
    elif('tok300_' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    elif('tok202_(' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      self.exp_simples()
      if('tok203_)' in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Parêntesis desbalanceados - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Parêntesis desbalanceados - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
    else: 
      print("Erro sintatico - esperado um identificador, token inteiro, ou (expressão simples) - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - esperado um identificador, token inteiro, ou (expressão simples) - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok112_<=" in self.tokens[self.i] or
            not "tok110_>=" in self.tokens[self.i] or
            not "tok109_>" in self.tokens[self.i] or
            not "tok111_<" in self.tokens[self.i] or
            not "tok107_==" in self.tokens[self.i] or
            not "tok108_!=" in self.tokens[self.i] or
            not "tok101_+" in self.tokens[self.i] or
            not "tok102_-" in self.tokens[self.i] or
            not "tok103_*" in self.tokens[self.i] or
            not "tok104_/" in self.tokens[self.i] or
            not "tok105_++" in self.tokens[self.i] or
            not "tok106_--" in self.tokens[self.i] or
            not "tok113_&&" in self.tokens[self.i] or
            not "tok114_||" in self.tokens[self.i] or
            not "tok115_=" in self.tokens[self.i] or
            not "tok203_)" in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
  # <fator_deriva> := <op_md><fator><fator_deriva> | Ɛ
  def fator_deriva(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
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
    else:
      print("Erro sintatico - Esperado '*' ou '/' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado '*' ou '/' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok112_<=" in self.tokens[self.i] or
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
            not "tok203_)" in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
  # <op_soma_deriva> := <termo><termo_deriva> | +
  def op_soma_deriva(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok101_+' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    elif("tok500_" in self.tokens[self.i] or
       "tok300_" in self.tokens[self.i] or
       "tok202_(" in self.tokens[self.i]):
      self.termo()
      self.termo_deriva()
    else:
      print("Erro sintatico - Esperado '+' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado '+' ou '-' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok112_<=" in self.tokens[self.i] or
            not "tok110_>=" in self.tokens[self.i] or
            not "tok109_>" in self.tokens[self.i] or
            not "tok111_<" in self.tokens[self.i] or
            not "tok107_==" in self.tokens[self.i] or
            not "tok108_!=" in self.tokens[self.i] or
            not "tok203_)" in self.tokens[self.i] or
            not "tok200_;" in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    
  # <op_sub_deriva> := <termo><termo_deriva> | -
  def op_sub_deriva(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if('tok102_-' in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    elif("tok500_" in self.tokens[self.i] or
       "tok300_" in self.tokens[self.i] or
       "tok202_(" in self.tokens[self.i]):
      self.termo()
      self.termo_deriva()
    else:
      print("Erro sintatico - Esperado '-' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Esperado '+' ou '-' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok112_<=" in self.tokens[self.i] or
            not "tok110_>=" in self.tokens[self.i] or
            not "tok109_>" in self.tokens[self.i] or
            not "tok111_<" in self.tokens[self.i] or
            not "tok107_==" in self.tokens[self.i] or
            not "tok108_!=" in self.tokens[self.i] or
            not "tok203_)" in self.tokens[self.i] or
            not "tok200_;" in self.tokens[self.i]):
                self.i += 1
                self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    
  # <op_md> := * | /
  def op_md(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok103_*" in self.tokens[self.i] or "tok104_/" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - esperado operador '*' ou '/' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - esperado operador '*' ou '/' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok500_" in self.tokens[self.i] or
       not "tok300_" in self.tokens[self.i] or
       not "tok202_(" in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
  # <op_cont> := ++ | --
  def op_cont(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if("tok105_++" in self.tokens[self.i] or "tok106_--" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - esperado um '++' ou '--' - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - esperado um '++' ou '--' - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "tok203_)" in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
  # <algoritmo_declaracao> :=  algoritmo {<deriva_cont_principal> }
  def algoritmo_declaracao(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
    if ("tok600_algoritmo" in self.tokens[self.i]):
      self.i += 1
      self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      if("tok204_{" in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        self.deriva_cont_principal()
        if("tok205_}" in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
        else:
          print("Erro sintatico - Esperado '}' na declaracao de algoritmo - linha: "+self.linha_atual+"\n")
          print('Token problemático: '+self.tokens[self.i])
          self.arquivo_saida.write("Erro sintatico - Esperado '}' na declaracao de algoritmo - linha: "+self.linha_atual+"\n")
          self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
          self.tem_erro_sintatico = True
          while(not "$" in self.tokens[self.i]):
            self.i += 1
            self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
      else:
        print("Erro sintatico - Esperado '{' na declaracao de algoritmo - linha: "+self.linha_atual+"\n")
        print('Token problemático: '+self.tokens[self.i])
        self.arquivo_saida.write("Erro sintatico - Esperado '{' na declaracao de algoritmo - linha: "+self.linha_atual+"\n")
        self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
        self.tem_erro_sintatico = True
        while(not "$" in self.tokens[self.i]):
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    else:
      print("Erro sintatico - Declaração do bloco 'algoritmo' é obrigatória nessa linguagem - linha: "+self.linha_atual+"\n")
      print('Token problemático: '+self.tokens[self.i])
      self.arquivo_saida.write("Erro sintatico - Declaração do bloco 'algoritmo' é obrigatória nessa linguagem - linha: "+self.linha_atual+"\n")
      self.arquivo_saida.write('Token problemático: '+self.tokens[self.i]+'\n')
      self.tem_erro_sintatico = True
      while(not "$" in self.tokens[self.i]):
        self.i += 1
        self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
  # <deriva_cont_principal> := <variaveis_declaracao> <decl_comandos> | <decl_comandos> | Ɛ
  def deriva_cont_principal(self):
    if("Erro Lexico" in self.tokens[self.i]):
      self.i += 1
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
          self.i += 1
          self.linha_atual = self.tokens[self.i][ self.tokens[self.i].find('->')+2: -1]
    # ========================== FIM DO ANALISADOR SINTATICO
