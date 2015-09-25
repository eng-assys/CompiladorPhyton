######           Analisador Lexico    ######
# Autor 1: Lucas Vinicius dos Santos Assis
# Autora 2: Andressa Moura
# EXA 869 - MI - Processadores de Linguagem de Programacao
# ==============================================================================
# Implementacao do analisador lexico de um compilador
# Cada codigo citado a seguir representa um tipo de token
# Essa codificacao eh usada no arquivo de saida que contem os 
# resultados de operacao do analisador lexico
# tok1 - Operador
#   tok100 - .
#   tok101 - +
#   tok102 - -
#   tok103 - *
#   tok104 - /
#   tok105 - ++
#   tok106 - --
#   tok107 - ==
#   tok108 - !=
#   tok109 - >
#   tok110 - >=
#   tok111 - <
#   tok112 - <=
#   tok113 - &&
#   tok114 - ||
#   tok115 - =

# tok2 - Delimitador
#   tok200 - ;
#   tok201 - ,
#   tok202 - (
#   tok203 - )
#   tok204 - {
#   tok205 - }
#   tok206 - [
#   tok207 - ]

# tok3 - Numero
# tok300 - Numero Inteiro
# tok301 - Numero Real

# tok400 - Caractere Constante

# tok500 - Identificador

# tok6 - Palavra reservada
#   tok600 - algoritmo
#   tok601 - variaveis
#   tok602 - constantes
#   tok603 - registro
#   tok604 - funcao
#   tok605 - retorno
#   tok606 - vazio
#   tok607 - se
#   tok608 - senao
#   tok609 - enquanto
#   tok610 - para
#   tok611 - leia
#   tok612 - escreva
#   tok613 - inteiro
#   tok614 - real
#   tok615 - booleano
#   tok616 - char
#   tok617 - cadeia
#   tok618 - verdadeiro
#   tok619 - falso

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


# Declarando Classe do analisador Lexico
class AnalisadorLexico():
  # ========================== DECLARACAO DE METODOS DA CLASSE
  # Metodo construtor da classe
  def __init__(self):
    self.arquivo_e = "programa.txt"
    self.arquivo_s = "resp-lex.txt"

  # Metodo para mudar arquivo de entrada
  def mudaEntrada(self, string):
    self.arquivo_e = string

  def getEntrada(self):
    return self.arquivo_e

  def getSaida(self):
    return self.arquivo_s

  # Metodo que verifica se a entrada eh um delimitador
  # O metodo find() retorna a posicao do caractere na string de 
  # entrada caso o mesmo seja encontrado
  def ehDelimitador(self, caracter):
    # String com os delimitadores componentes da linguagem
    delimitadores = ";,(){}[]"
    if caracter in delimitadores:
      return True
    return False

  # Metodo que especifica qual dos tokens delimitadores eh a entrada
  def qualTokenDelimitador(self, entrada):
    # String com os operadores componentes da linguagem
    delimitadores = ";,(){}[]"
    posicao = delimitadores.find(entrada)
    return "tok20"+str(posicao)

  # Metodo que verifica se a entrada eh uma letra
  def ehLetra (self, caracter):
    # String com as letras componentes da linguagem (a..z|A..Z)
    letra = string.ascii_letters
    if caracter in letra:
      return True
    return False

  # Metodo que verifica se a entrada eh um digito
  def ehDigito (self, caracter):
    # String com os digitos componentes da linguagem
    digito = '0123456789'
    if caracter in digito:
      return True
    return False

  # Metodo que verifica se a entrada eh um simbolo asc_ii
  def ehSimbolo(self, caracter):
    # Strings com os simbolos da tabela ASCII (32 a 126)
    simbolos = ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHJKLMNOPQRSTUVXWYZ[\]^_`abcdefghijklmnopqrstuvxwyz{|}~'''
    if(caracter in simbolos):
      return True
    return False

  # Metodo que verifica se a entrada eh um operador
  def ehOperador(self, entrada):
    # Listas com os operadores componentes da linguagem
    operadores = '. + - * / ++ -- == != > >= < <= && || ='.split()
    if entrada in operadores:
      return True
    return False
  
  # Metodo que especifica qual dos tokens operadores eh a entrada
  def qualTokenOperador(self, entrada):
    # Listas com os operadores componentes da linguagem
    operadores = '. + - * / ++ -- == != > >= < <= && || ='.split()
    posicao = 0
    for x in operadores:
      if x == entrada:
        break
      posicao += 1
    if(posicao > 9):
      return "tok1"+str(posicao)
    else:
      return "tok10"+str(posicao)

  # Metodo que verifica se a entrada eh uma palavra reservada
  def ehReservada(self, entrada):
    # Criando Listas para abrigar palavras que serao indexadas por uma mesma letra no dicionario a seguir
    reservadas = "algoritmo variaveis constantes registro funcao retorno vazio se senao enquanto para leia escreva inteiro real booleano char cadeia verdadeiro falso".split()
    if entrada in reservadas:
      return True
    return False

  # Metodo que especifica qual dos tokens palavras reservadas eh a entrada
  def qualTokenReservada(self, entrada):
    # Listas com os operadores componentes da linguagem
    reservadas = '''algoritmo variaveis constantes registro funcao retorno vazio se senao enquanto para leia escreva inteiro real booleano char cadeia verdadeiro falso'''.split()
    posicao = 0
    for x in reservadas:
      if x == entrada:
        break
      posicao += 1
    if(posicao > 9):
      return "tok6"+str(posicao)
    else:
      return "tok60"+str(posicao)

  # Metodo que executa o analsador lexico
  def analisa(self):
    # Abre o arquivo de saida do programa
    arquivo_saida = open(self.arquivo_s, 'w')
    # Verifica se o arquivo de entrada existe no diretorio em questao
    if not os.path.exists(self.arquivo_e):
      arquivo_saida.write("Arquivo de entrada inexistente")
      return

    # Abre o arquivo de entrada do programa
    arquivo = open(self.arquivo_e, 'r')

    # Le a primeira linha
    linha_programa = arquivo.readline()

    # Variavel que indica a linha do caracter_atual
    numero_linha = 1
    
    # Percorre o programa linha por linha
    while linha_programa:
      i = 0
      tamanho_linha = len(linha_programa)
      while i < tamanho_linha: #Percorre os caracteres da linha
        caracter_atual = linha_programa[i] 
        caractere_seguinte = None
        # Soh posso pegar o caractere_seguinte se ele existe na linha
        if ((i+1) < tamanho_linha):
          caractere_seguinte = linha_programa[i+1] 
        # ===================================================================================
        # Verifica se o caracter eh um delimitador - OK
        if (self.ehDelimitador(caracter_atual)):
          arquivo_saida.write(self.qualTokenDelimitador(caracter_atual)+'_'+caracter_atual+'->'+str(numero_linha)+'\n')
        # ===================================================================================
        # Consumindo comentarios de linha - OK
        elif (caracter_atual == '/' and caractere_seguinte == '/'):
          # Fazendo o programa pular para a proxima linha
          i = tamanho_linha
        # ===================================================================================
        # Consumindo comentarios de bloco - OK
        elif (caracter_atual == '/' and caractere_seguinte == '*'):
          cont = True # Variavel que impedirah o loop a seguir de continuar caso
                      # seja falsa, isso acontece com erro fim inesperado de arquivo
          linha_comeco = numero_linha # Guardo a linha que o bloco comecou, para caso 
                                      # o erro de bloco nao fechado ocorrer o programa
                                      # poderah indicar o comeco do erro
          while cont and not (caracter_atual == '*' and caractere_seguinte == '/'):
            # Soh posso pegar o caractere atual e o proximo se ele existe na linha
            if ((i+2) < tamanho_linha):
              i += 1
              caracter_atual = linha_programa[i]
              caractere_seguinte = linha_programa[i+1]                   
            else:
              linha_programa = arquivo.readline() # Le a proxima linha
              tamanho_linha = len(linha_programa)
              numero_linha += 1
              i = -1
              if (not linha_programa):
                arquivo_saida.write ("Erro Lexico - Comentario de bloco nao fechado - linha: %d\n" %linha_comeco)
                cont = False
          i += 1 # Faco isso para que nao considere o '/' do final do bloco (na composicao */) no proximo loop
        # ===================================================================================
        # Verificando se o elemento eh um operador
        elif caractere_seguinte != None and self.ehOperador(caracter_atual+caractere_seguinte):
          arquivo_saida.write(self.qualTokenOperador(caracter_atual+caractere_seguinte)+'_'+caracter_atual+caractere_seguinte+'->'+str(numero_linha)+'\n')
          i += 1
        elif self.ehOperador(caracter_atual):
          arquivo_saida.write(self.qualTokenOperador(caracter_atual)+'_'+caracter_atual+'->'+str(numero_linha)+'\n')

        # ===================================================================================
        # Verificando se o elemento em questao eh caractere constante - OK
        # string.punctuation[6] retorna o simbolo - ' - que representa o inicio do caractere constante
        elif (caracter_atual == string.punctuation[6]):

          if (linha_programa[i+1] == '\n') or (not (string.punctuation[6] in linha_programa[i+1:])):
            arquivo_saida.write('Erro Lexico - Caractere nao fechado - Linha: %d\n' %numero_linha)
            i = tamanho_linha
          elif self.ehSimbolo(linha_programa[i+1]) and linha_programa[i+1] != string.punctuation[6] and linha_programa[i+2] == string.punctuation[6]:
            arquivo_saida.write('tok400_'+linha_programa[i+1]+'->'+str(numero_linha)+'\n')
            i+=2
          elif linha_programa[i+1] == string.punctuation[6] and linha_programa[i+2] == string.punctuation[6]:
            arquivo_saida.write('Erro Lexico - Caractere nao pode ser aspas simples - Linha: %d\n' %numero_linha)
            i+=2
          elif linha_programa[i+1] == string.punctuation[6]:
            arquivo_saida.write('Erro Lexico - Caractere nao pode ser vazio - Linha: %d\n' %numero_linha)
            i+=1
          else:
            arquivo_saida.write('Erro Lexico - Tamanho ou simbolo do Caractere invalido - Linha: %d\n' %numero_linha)
            i=linha_programa[i+1:].find(string.punctuation[6])+1

        # ===================================================================================
        # Verificando se o elemento em questao eh cadeia constante - OK
        # string.punctuation[1] retorna o simbolo - " - que representa o inicio da cadeia constante
        elif (caracter_atual == string.punctuation[1]):
          i+=1 # Para passar a primeira ocorrencia do caractere "
          ehValido = True

          # Se a linha soh contem uma ocorrencia de ", significa que a string nao foi fechada
          if (linha_programa[i:].find(string.punctuation[1]) == -1):
            arquivo_saida.write('Erro Lexico - String nao fechada - Linha: %d\n' %numero_linha)
            i = tamanho_linha
          else:
            fim_cadeia = i+linha_programa[i:].find(string.punctuation[1])
            nova_cadeia = linha_programa[i:fim_cadeia]
            i = fim_cadeia
            for x in nova_cadeia:
              if(not self.ehSimbolo(x)):
                ehValido = False
                arquivo_saida.write('Erro Lexico - String com simbolo invalido (Nao ascii) - Linha: %d\n' %numero_linha)
                break
            if(ehValido):
              arquivo_saida.write('tok700_'+nova_cadeia+'->'+str(numero_linha)+'\n')
        # ===================================================================================
        # Verificando se o elemento em questao eh um numero - OK
        elif (self.ehDigito(caracter_atual)):
          string_temp = caracter_atual
          i += 1
          j = 0 # Vai contar se o numero tem pelo menos 1 digito depois do '.'
          caracter_atual = linha_programa[i]
          while (self.ehDigito(caracter_atual) and (i+1 < tamanho_linha)):
            string_temp += caracter_atual
            i += 1
            caracter_atual = linha_programa[i]

          if (caracter_atual == '.'):
            if ((i+1) < tamanho_linha):
              string_temp += caracter_atual
              i += 1
              caracter_atual = linha_programa[i]
              while self.ehDigito(caracter_atual) and i+1 < tamanho_linha:
                j += 1
                string_temp += caracter_atual
                i += 1
                caracter_atual = linha_programa[i]

              if(caracter_atual == '.'):
                j = 0
                # Tratamento de erro, modalidade do desespero
                while (i+1 < tamanho_linha):
                  i += 1
                  caracter_atual = linha_programa[i]
                  if self.ehDelimitador(caracter_atual) or caracter_atual == ' ':
                    i -= 1 # Preciso voltar um elemento da linha para que o delimitador seja reconhecido no momento certo
                    break
            else:
              arquivo_saida.write('Erro Lexico - Numero mal formado - Linha: %d\n' %numero_linha)

            if (j > 0):
              arquivo_saida.write('tok301_'+string_temp+'->'+str(numero_linha)+'\n')
            else: 
              arquivo_saida.write('Erro Lexico - Numero mal formado - Linha: %d\n' %numero_linha)
          else:
            arquivo_saida.write('tok300_'+string_temp+'->'+str(numero_linha)+'\n')
            if(not self.ehDigito(caracter_atual)):
              i -= 1
        # ===================================================================================
        # Verificando identificadores ou palavras reservadas - OK
        elif (self.ehLetra(caracter_atual)):
          # Apos verificar que o primeiro caractere da palavra era uma letra, vou percorrendo o identificador
          # ateh encontrar um caractere que nao possa ser de identificadores ou ateh o final da linha
          string_temp = caracter_atual
          i += 1
          algum_erro = False
          while i < tamanho_linha:
            caractere_seguinte = None
            caracter_atual = linha_programa[i]
            if(i+1 < tamanho_linha):
              caractere_seguinte = linha_programa[i+1]
            if (self.ehLetra(caracter_atual) or self.ehDigito(caracter_atual) or caracter_atual == '_'):
              string_temp += caracter_atual
            elif (self.ehDelimitador(caracter_atual) or caracter_atual == ' ' or caracter_atual == '\t' or caracter_atual == '\r'):
              i -= 1 # Preciso voltar um elemento da linha para que o delimitador seja reconhecido no momento certo
              break
            elif(caractere_seguinte != None and self.ehOperador(caracter_atual+caractere_seguinte)) or self.ehOperador(caracter_atual):
              i-=1
              break
            elif caracter_atual != '\n':
              arquivo_saida.write("Erro Lexico - Identificador com caracter invalido: "+caracter_atual+" - linha: %d\n" %numero_linha)
              algum_erro = True
              break
            i += 1 # Passando o arquivo ateh chegar ao final do identificador/palavra reservada
            

          if (algum_erro):
            while (i+1 < tamanho_linha):
              i += 1
              caracter_atual = linha_programa[i]
              if self.ehDelimitador(caracter_atual) or caracter_atual == ' ' or caracter_atual == '\t' or caracter_atual == '\r' or caracter_atual == '/':
                i -= 1 # Preciso voltar um elemento da linha para que o delimitador seja reconhecido no momento certo
                break
          else: # Se nao houver erros basta verificar se o elemento eh palavra reservada tambem
            if (self.ehReservada(string_temp)):
              arquivo_saida.write(self.qualTokenReservada(string_temp)+'_'+string_temp+'->'+str(numero_linha)+'\n')
            else:
              arquivo_saida.write('tok500_'+string_temp+'->'+str(numero_linha)+'\n')
          
        # ===================================================================================
        # Verificando Erros Lexicos - Caracter Invalido
        # Note que os caracteres especiais \n, \t, \r e espaco sao desconsiderados como caracteres invalidos
        # por aparecerem constantemente no codigo em questao
        elif caracter_atual != '\n' and caracter_atual != ' ' and caracter_atual != '\t' and caracter_atual != '\r':
          arquivo_saida.write('Erro Lexico - Caracter Invalido: ' + caracter_atual + ' - linha: %d\n' %numero_linha)
        # ===================================================================================
        i += 1 # Incrementando a leitura dos caracteres da linha lida no momento

      linha_programa = arquivo.readline() # Le a proxima linha
      numero_linha += 1
    # Fim do programa
    arquivo_saida.write('$')
    # Fim do arquivo de entrada
    arquivo.close()
    # Fim do arquivo de entrada
    arquivo_saida.close
    # ========================== FIM DO ANALISADOR LEXICO

# Executando o programa

analisador_lexico = AnalisadorLexico()
analisador_lexico.analisa()
