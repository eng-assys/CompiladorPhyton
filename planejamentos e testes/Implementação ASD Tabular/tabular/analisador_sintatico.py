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

# Importando classe construtora e possuidora da tabela sintatica
from tab import GeraTabelaSintatica

# Classe que define a estrututa de dados de pilha que serah usada no algoritmo
class Pilha():
    def __init__(self):
        self.dados = []
 
    def empilha(self, elemento):
        self.dados.append(elemento)
    def get_pilha(self):
      return self.dados
    def desempilha(self):
        if not self.vazia():
            return self.dados.pop()
    def get_topo(self):
      return self.dados[len(self.dados) - 1]
    def vazia(self):
        return len(self.dados) == 0


# Declarando Classe do Analisador Sintatico
class AnalisadorSintatico():
  # ========================== DECLARACAO DE METODOS DA CLASSE
  # Metodo construtor da classe
  def __init__(self):
    self.arquivo_entrada = "resp-lex.txt"
    self.arquivo_saida = "resp-sint.txt"
    self.tabela = GeraTabelaSintatica() # Criando instancia do criador da tabela sintatica

  # Metodo para mudar arquivo de entrada
  def mudaEntrada(self, string):
    self.arquivo_entrada = string

  def getEntrada(self):
    return self.arquivo_entrada

  def getSaida(self):
    return self.arquivo_saida

  '''
    Define se uma string de entrada eh ou nao um nao-terminal
  '''
  def isNaoTerminal(self, entrada):
    return ('¬' in entrada)
  
  '''
    Define se uma string de entrada eh um terminal
  '''
  def isTerminal(self, entrada):
    return (entrada != 'Ɛ') and not self.isNaoTerminal(entrada)

  '''
    Realiza uma busca na hash da tabela sintatica, com a chave topo_pilha+atual_buffer.
    Caso a chave seja invalida retorna-se uma lista vazia para quem chamou a funcao.
    Caso a chave seja valida retorna-se uma lista contendo as producoes presentes na tabela
  '''
  def procura_tabela(self, topo_pilha, atual_buffer):
    print("Tabela M["+topo_pilha+","+atual_buffer+']')
    tabela_temp = self.tabela.get_tabela()
    
    # Nao estava reconhecendo na declaracao de variaveis os registros jah criados
    if(topo_pilha == '¬declaracao_var@' and atual_buffer == 'tok500_'):
      lista_producoes_tabela = "tok500_ tok500_ tok200_; ¬declaracao_var@"
      lista_producoes_tabela = lista_producoes_tabela.split(' ')
      return lista_producoes_tabela
    elif(topo_pilha == '¬comandos@' and atual_buffer == 'tok607_se'):
      lista_producoes_tabela = []
      lista_producoes_tabela.append("¬se_declaracao@")
      return lista_producoes_tabela

    try:
      lista_producoes_tabela = tabela_temp[topo_pilha+atual_buffer]
      lista_producoes_tabela = lista_producoes_tabela[lista_producoes_tabela.find('=')+2:]
      lista_producoes_tabela = lista_producoes_tabela.split(' ')
      return lista_producoes_tabela
    except KeyError:
      return []
  '''
    Alguns tipos de terminais sao representados na gramatica de forma generica, pois nao
    eh possivel saber de antemao seus valores no codigo do usuario, sao eles numero inteiro,
    numero real, caractere constante, identificadores e cadeia constante, que sao representados
    pelos seguintes codigos respectivamente: tok300_, tok301_, tok400_, tok500_ e tok700_

    O algoritmo de reconhecimento de sentenca exige que a comparacao desses terminais
    representados na gramatica e no codigo do usuario seja realizada, assim essa funcao intermedia
    essa comparacao. Por exemplo, uma cadeia constante do usuario, representada pelo token tok700_conteudo
    deverah ser considerada igual ao token generico da gramatica tok700_
  '''
  def compara_terminais(self, terminal_gram, terminal_user):
    print('Comparando terminais, t1: '+terminal_gram+' t2: '+terminal_user)
    print("Os terminais sao iguais: ", terminal_gram[:7] == terminal_user[:7])
    return terminal_gram[:7] == terminal_user[:7]



  # Metodo que executa o analisador sintatico
  # Considere X como o topo da pilha (topo_pilha) e a como o atual_buffer (simbolo corrente na leitura do buffer)
  def analisa(self):
    # Criando arvore de derivacao vazia
    arvore_derivacao = []
    # Criando a tabela sintatica que serve de consulta para a execucao do codigo
    # reconhecedor de sentenca
    self.tabela.gerar_tabela()
    # Criando a pilha de execucao do codigo
    pilha = Pilha()
    # Empilhando o simbolo que indica fim de pilha
    pilha.empilha("$")
    # Empilhando o simbolo inicial da gramatica
    pilha.empilha("¬start@")
    # Abre o arquivo de saida do programa
    arquivo_saida = open(self.arquivo_saida, 'w')
    # Verifica se o arquivo de entrada existe no diretorio em questao
    if not os.path.exists(self.arquivo_entrada):
      print("Arquivo de entrada inexistente")
      arquivo_saida.write("Arquivo de entrada inexistente")
      return
    # Abre o arquivo de entrada do programa
    arquivo = open(self.arquivo_entrada, 'r')
    # Criando a variavel que vai guardar o topo atual da pilha
    topo_pilha = pilha.get_topo()
    # Criando a variavel que vai guardar o simbolo atual do buffer de entrada, sem considerar o \n presente em seu final
    atual_buffer = arquivo.readline()[:-1]
    if("Erro Lexico " in atual_buffer):
      atual_buffer = arquivo.readline()[:-1]
    # Se X = a = $, entao o analisador termina a analise com sucesso
    while (not (topo_pilha == atual_buffer and topo_pilha == '$') and atual_buffer): 
      print('topo da pilha, inicio while:    '+topo_pilha)
      # Se X eh um terminal
      if( self.isTerminal(topo_pilha) ): #OK
        # Se X = a != $
        if ( self.compara_terminais(topo_pilha, atual_buffer) and topo_pilha != '$' ):
          # entao o analisador desempilha X
          pilha.desempilha()
          # A pilha agora tem um novo topo
          topo_pilha = pilha.get_topo()
          # e consome o simbolo corrente do buffer de entrada
          atual_buffer = arquivo.readline()[:-1]
          if("Erro Lexico " in atual_buffer):
            atual_buffer = arquivo.readline()[:-1]
        # Se X eh um terminal e eh diferente de 'a'
        elif ( topo_pilha != atual_buffer ): # Tratar quando ocorre esse erro
          print("Erro sintatico - O topo da pilha: ", topo_pilha, " é um terminal e diferente do simbolo corrente: ", atual_buffer)
          break
          pilha.desempilha()
          topo_pilha = pilha.get_topo()
      # Se X eh nao-terminal...
      # lado direito
      elif(self.isNaoTerminal(topo_pilha)):
        atual_buffer_aux = atual_buffer
        if(atual_buffer[3:6] == '300' or atual_buffer[3:6] == '301' or atual_buffer[3:6] == '400' or atual_buffer[3:6] == '500' or atual_buffer[3:6] == '700'):
          atual_buffer_aux = atual_buffer[:7] 

        if(topo_pilha == '¬decl_param@' and  atual_buffer == 'tok203_)' ):
          print("regra do tipo X->Ɛ, apenas desempilha X")
          pilha.desempilha()
          topo_pilha = pilha.get_topo()
        else:
          # ... entao o analisador procura na tabela sintatica a regra [X,a] ...
          lista_producao = self.procura_tabela(topo_pilha, atual_buffer_aux)
          # Se X eh nao-terminal e nao existe regra cuja derivacao produza a, entao ocorreu um erro
          if(len(lista_producao) == 0):
            print("Erro sintatico - regra não terminal: ", topo_pilha, " + terminal: ", atual_buffer, " invalida")
            break
          # Se a regra for do tipo X->Ɛ, apenas desempilha X
          elif('Ɛ' in lista_producao):
            print("regra do tipo X->Ɛ, apenas desempilha X")
            pilha.desempilha()
            topo_pilha = pilha.get_topo()
            print('pilha apos desempilhar: ', pilha.get_pilha(), "\n")
          # ... e empilha o seu lado direito na ordem em que a primeira producao vai para o topo da pilha
          else:
            pilha.desempilha()
            for prod in reversed(lista_producao):
              pilha.empilha(prod)
              print("Producao empilhada: "+prod)
            topo_pilha = pilha.get_topo()
            print('----------\n')
            print('pilha: ', pilha.get_pilha())
    # Se X = a = $, entao o analisador termina a analise com sucesso
    if (topo_pilha == atual_buffer and topo_pilha == '$'):
      print("Cadeia de entrada reconhecida")
      print("Arvore de derivacao gerada: ", arvore_derivacao)
    else:
      print('Cadeia de entrada nao-reconhecida')
    
    # Fim do arquivo de entrada
    arquivo.close()
    # Fim do arquivo de entrada
    arquivo_saida.close
    # ========================== FIM DO ANALISADOR LEXICO

sintatico = AnalisadorSintatico()
sintatico.analisa()