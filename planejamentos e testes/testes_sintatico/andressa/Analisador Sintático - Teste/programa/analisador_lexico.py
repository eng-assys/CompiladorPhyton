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
#   tok201 - Delimitador Virgula
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


# Declarando Classe do analisador Lexico
class AnalisadorLexico(object):
  # ========================== DECLARACAO DE METODOS DA CLASSE
  # Metodo construtor da classe
  def __init__(self):
    self.arquivo_entrada = "programa.li"
    self.arquivo_saida = "resp-lex.lo"

  # Metodo para mudar arquivo de entrada
  def mudaEntrada(self, string):
    self.arquivo_entrada = string

  def getEntrada(self):
    return self.arquivo_entrada

  def getSaida(self):
    return self.arquivo_saida

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
    simbolos = ''' !#$%&()'*+.-,/0123456789:;<=>?@ABCDEFGHJKLMNOPQRSTUVXWYZ[]"\^_`abcdefghijklmnopqrstuvxwyz{|}~'''
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
    arquivo_saida = open('resp-lex.lo', 'w')
    # Verifica se o arquivo de entrada existe no diretorio em questao
    if not os.path.exists(self.arquivo_entrada):
      arquivo_saida.write("Arquivo de entrada inexistente")
      return

    # Abre o arquivo de entrada do programa
    arquivo = open(self.arquivo_entrada, 'r')

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
          arquivo_saida.write(self.qualTokenDelimitador(caracter_atual)+' '+caracter_atual+'\n')
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
          arquivo_saida.write(self.qualTokenOperador(caracter_atual+caractere_seguinte)+' '+caracter_atual+caractere_seguinte+'\n')
          i += 1
        elif self.ehOperador(caracter_atual):
          arquivo_saida.write(self.qualTokenOperador(caracter_atual)+' '+caracter_atual+'\n')

        # ===================================================================================
        # Verificando se o elemento em questao eh caractere constante - OK
        # string.punctuation[6] retorna o simbolo - ' - que representa o inicio do caractere constante
        elif (caracter_atual == string.punctuation[6]):

          if (linha_programa[i+1] == '\n') or (not (string.punctuation[6] in linha_programa[i+1:])):
            arquivo_saida.write('Erro Lexico - Caractere nao fechado - Linha: %d\n' %numero_linha)
            i = tamanho_linha
          elif self.ehSimbolo(linha_programa[i+1]) and linha_programa[i+1] != string.punctuation[6] and linha_programa[i+2] == string.punctuation[6]:
            arquivo_saida.write('tok400 '+linha_programa[i+1]+'\n')
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
          if linha_programa[i] == '\n' or linha_programa[i] == ' ' or linha_programa[i] == '\t' or linha_programa[i] == '\r' or not(string.punctuation[1] in linha_programa[i:]):
            arquivo_saida.write('Erro Lexico - String nao fechada - Linha: %d\n' %numero_linha)
            i = tamanho_linha
            break

          fim_cadeia = i+linha_programa[i:].find(string.punctuation[1]) # Se a cadeia tiver corretamente formada o seu fim serah indicado por "
                                                                          # ou seja, quando acho esse fim, acho a posicao do ultimo elemento da string
          # No codigo do while abaixo verifico se a string tem mais alguma ocorrencia de "
          # se tiver eh necessario indicar erro de caractere invalido ".
          j = fim_cadeia
          while j+1 < tamanho_linha:
            j += 1
            if(linha_programa[j] == string.punctuation[1]):
              arquivo_saida.write('Erro Lexico - String contem caractere invalido: '+string.punctuation[1]+"\n")
              i = tamanho_linha
          if i < tamanho_linha:
            string_temp = linha_programa[i:fim_cadeia] # Pegando a string que sera o token de cadeia constante
            i = fim_cadeia # Indicando aonde na linha o programa principal deve continuar

            for x in string_temp:# Verificando se nao tenho nenhum caractere invalido dentro da string
              if not self.ehSimbolo(x):
                arquivo_saida.write('Erro Lexico - Caractere invalido na string: '+x+' - Linha: %d\n' %numero_linha)
                ehValido = False
                break
            if ehValido:
              arquivo_saida.write('tok700 '+string_temp+'\n')
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
            else:
              arquivo_saida.write('Erro Lexico - Numero mal formado - Linha: %d\n' %numero_linha)

            if (j > 0):
              arquivo_saida.write('tok300 '+string_temp+'\n')
              break
            else: 
              arquivo_saida.write('Erro Lexico - Numero mal formado - Linha: %d\n' %numero_linha)
              break
                
          arquivo_saida.write('tok300 '+string_temp+'\n')
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
              arquivo_saida.write(self.qualTokenReservada(string_temp)+' '+string_temp+'\n')
            else:
              arquivo_saida.write('tok500 '+string_temp+'\n')
          
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

    # Fim do arquivo de entrada
    arquivo.close()
    # Fim do arquivo de entrada
    arquivo_saida.close
    # ========================== FIM DO ANALISADOR LEXICO

# Executando o programa

#analisador_lexico = AnalisadorLexico()
#analisador_lexico.analisa()
