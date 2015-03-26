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
# tok2 - Delimitador
# tok3 - Numero
# tok4 - Caractere Constante
# tok5 - Identificador
# tok6 - Palavra reservada
# tok7 - Cadeia constante
# ========================== ERROS LEXICOS
# Simbolo nao pertencente ao conjunto de simbolos terminais da linguagem
# Identificador Mal formado
# Tamanho do identificador
# Numero mal formado
# Fim de arquivo inesperado (comentario de bloco nao fechado)
# Caractere ou string mal formados
# ==============================================================================
# Bibliotecas para entrada e saida de arquivos
import sys
import os.path

# Bliblioteca padrao de string
import string

# ========================== DECLARACAO DE METODOS

# Metodo que verifica se a entrada eh um delimitador
# O metodo find() retorna a posicao do caractere na string de 
# entrada caso o mesmo seja encontrado
def ehDelimitador(caracter):
  # String com os delimitadores componentes da linguagem
  delimitadores = ",;(){}[]"
  if caracter in delimitadores:
    return True
  return False

# Metodo que verifica se a entrada eh uma letra
def ehLetra (caracter):
  # String com as letras componentes da linguagem (a..z|A..Z)
  letra = string.ascii_letters
  if caracter in letra:
    return True
  return False

# Metodo que verifica se a entrada eh um digito
def ehDigito (caracter):
  # String com os digitos componentes da linguagem
  digito = '0123456789'
  if caracter in digito:
    return True
  return False

# Metodo que verifica se a entrada eh um simbolo asc_ii
def ehSimbolo(caracter):
  # Strings com os simbolos da tabela ASCII (32 a 126)
  simbolos = ''' !#$%&()'*+.-,/0123456789:;<=>?@ABCDEFGHJKLMNOPQRSTUVXWYZ[]"\^_`abcdefghijklmnopqrstuvxwyz{|}~'''
  if(caracter in simbolos):
    return True
  return False

# Metodo que verifica se a entrada eh um operador
def ehOperador(entrada):
  # Listas com os operadores componentes da linguagem
  operadores = '. + ++ - -- * / = == != > >= <= < && ||'.split()
  if entrada in operadores:
    return True
  return False
  
# Metodo que verifica se a entrada eh uma palavra reservada
def ehReservada(entrada):
  # Criando Listas para abrigar palavras que serao indexadas por uma mesma letra no dicionario a seguir
  reservadas = '''algoritmo booleano char constantes cadeia escreva enquanto funcao falso inteiro leia para registro real retorno variaveis se senao verdadeiro vazio'''.split()
  if entrada in reservadas:
    return True
  return False

# Metodo que verifica se a entrada eh um caracter inválido
def ehCaracterInvalido(caracter):
  caracteres_invalidos = '''#$%():?@^_`|~¹²³£¢¬ªº´'''
  if(caracter in caracteres_invalidos):
    return True
  return False

# ========================== INICIO DO PROGRAMA
# Abre o arquivo de saida do programa
arquivo_saida = open('resp-lex.lo', 'w')

# Verifica se o arquivo de entrada existe no diretorio em questao
if not os.path.exists('programa.li'):
  print('Arquivo de entrada inexistente')
  arquivo_saida.write("Arquivo de entrada inexistente")
  sys.exit()

# Abre o arquivo de entrada do programa
arquivo = open('programa.li', 'r')

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
      if (ehDelimitador(caracter_atual)):
        arquivo_saida.write('tok2 '+caracter_atual+'\n')
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
      elif (ehOperador(caracter_atual)):
        if(ehOperador(caracter_atual+caractere_seguinte) and caractere_seguinte != None):
          arquivo_saida.write('tok1 '+caracter_atual+caractere_seguinte+'\n')
          i += 1
        else:
          arquivo_saida.write('tok1 %s\n' %caracter_atual)

      # ===================================================================================
      # Verificando se o elemento em questao eh caractere constante - OK
      # string.punctuation[6] retorna o simbolo - ' - que representa o inicio do caractere constante
      elif (caracter_atual == string.punctuation[6]):
        i += 1
        caracter_atual = linha_programa[i]
        caractere_seguinte = None
        if ((i+1) < tamanho_linha):
          caractere_seguinte = linha_programa[i+1]

        if (ehSimbolo(caracter_atual) and caractere_seguinte == string.punctuation[6]):
          arquivo_saida.write('tok4 '+caracter_atual+'\n')
          i += 1
        elif ((caracter_atual == string.punctuation[6]) and (caractere_seguinte != caracter_atual)):
          arquivo_saida.write('Erro Lexico - Caracter Constante vazio - Linha: %d\n' %numero_linha)
        elif (ehSimbolo(caracter_atual) and caractere_seguinte != string.punctuation[6]):
          arquivo_saida.write('Erro Lexico - Caracter Constante mal formado - Linha: %d\n' %numero_linha)

      # ===================================================================================
      # Verificando se o elemento em questao eh cadeia constante - OK
      # string.punctuation[1] retorna o simbolo - " - que representa o inicio da cadeia constante
      elif (caracter_atual == string.punctuation[1]):
        i += 1
        caracter_atual = linha_programa[i]
        if (caracter_atual == string.punctuation[1]):
          arquivo_saida.write('tok7 empty\n')
          break

        string_temp = caracter_atual
        while ehSimbolo(caracter_atual) and caracter_atual != string.punctuation[1] and (i+1 < tamanho_linha):
          i += 1
          caracter_atual = linha_programa[i]
          if caracter_atual != string.punctuation[1]:
            string_temp += caracter_atual
        if caracter_atual != string.punctuation[1]:
          arquivo_saida.write('Erro Lexico - Cadeia Constante mal formada - Linha: %d\n' %numero_linha)
          break
        arquivo_saida.write('tok7 '+string_temp+'\n')

      # ===================================================================================
      # Verificando se o elemento em questao eh um numero - OK
      elif (ehDigito(caracter_atual)):
        string_temp = caracter_atual
        i += 1
        j = 0 # Vai contar se o numero tem pelo menos 1 digito depois do '.'
        caracter_atual = linha_programa[i]
        while (ehDigito(caracter_atual) and (i+1 < tamanho_linha)):
          string_temp += caracter_atual
          i += 1
          caracter_atual = linha_programa[i]

        if (caracter_atual == '.'):
          if ((i+1) < tamanho_linha):
            string_temp += caracter_atual
            i += 1
            caracter_atual = linha_programa[i]
            while ehDigito(caracter_atual) and i+1 < tamanho_linha:
              j += 1
              string_temp += caracter_atual
              i += 1
              caracter_atual = linha_programa[i]
          else:
            arquivo_saida.write('Erro Lexico - Numero mal formado - Linha: %d\n' %numero_linha)

          if (j > 0):
            arquivo_saida.write('tok3 '+string_temp+'\n')
            break
          else: 
            arquivo_saida.write('Erro Lexico - Numero mal formado - Linha: %d\n' %numero_linha)
            break
            
        arquivo_saida.write('tok3 '+string_temp+'\n')
        i -= 1
      # ===================================================================================
      # Verificando identificadores ou palavras reservadas - OK
      elif (ehLetra(caracter_atual)):
        # Apos verificar que o primeiro caractere da palavra era uma letra, vou percorrendo o identificador
        # ateh encontrar um caractere que nao possa ser de identificadores ou ateh o final da linha
        string_temp = caracter_atual
        i += 1
        algum_erro = False
        while i < tamanho_linha:
          caracter_atual = linha_programa[i]
          if (ehLetra(caracter_atual) or ehDigito(caracter_atual) or caracter_atual == '_'):
            string_temp += caracter_atual
          elif (ehDelimitador(caracter_atual) or caracter_atual == ' '):
            i -= 1 # Preciso voltar um elemento da linha para que o delimitador seja reconhecido no momento certo
            break
          elif (ehSimbolo(caracter_atual)):
            arquivo_saida.write('Erro Lexico - Identificador mal formado - linha: %d\n' %numero_linha)
            algum_erro = True
            break
          i += 1 # Passando o arquivo ateh chegar ao final do identificador/palavra reservada

        if (algum_erro):
          while (i+1 < tamanho_linha) and (not(ehDelimitador(caracter_atual) or caracter_atual == ' ')):
            i += 1
            caracter_atual = linha_programa[i]
            if (ehDelimitador(caracter_atual)):
              i -= 1
        else: # Se nao houver erros basta verificar se o elemento eh palavra reservada tambem
          if (ehReservada(string_temp)):
            arquivo_saida.write('tok6 '+string_temp+'\n')
          else:
            arquivo_saida.write('tok5 '+string_temp+'\n')
      
      # ===================================================================================
      # Verificando Erros Léxicos - Caracter Invalido
      elif(ehCaracterInvalido(caracter_atual)):
        arquivo_saida.write('Erro Lexico - Caracter Invalido ' + caracter_atual + ' - linha: %d\n' %numero_linha)
        print(caracter_atual)
      # ===================================================================================
      
      i += 1 # Incrementando a leitura dos caracteres da linha lida no momento

   linha_programa = arquivo.readline() # Le a proxima linha
   numero_linha += 1

# Fim do arquivo de entrada
arquivo.close()
# Fim do arquivo de entrada
arquivo_saida.close
# ========================== FIM DO PROGRAMA
