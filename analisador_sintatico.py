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

# Importando estrutura de dados pilha
from pilha import Pilha

# Importando classe construtora e possuidora da tabela sintatica
from tab import GeraTabelaSintatica



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
    tabela_temp = self.tabela.get_tabela()

    try:
      lista_producoes_tabela = tabela_temp[topo_pilha+atual_buffer]
      lista_producoes_tabela = lista_producoes_tabela[lista_producoes_tabela.find('=')+2:]
      lista_producoes_tabela = lista_producoes_tabela.split(' ')
      return lista_producoes_tabela
    except KeyError:
      return []

  # Metodo que executa o analisador sintatico
  # Considere X como o topo da pilha (topo_pilha) e a como o atual_buffer (simbolo corrente na leitura do buffer)
  def analisa(self):
    # Criando arvore de derivacao vazia
    arvore_derivacao = []
    # Criando a tabela sintatica que serve de consulta para a execucao do codigo
    # reconhecedor de sentenca
    self.tabela.gerar_tabela()
    # Criando a pilha de execucao do codigo
    p = Pilha()
    # Empilhando o simbolo que indica fim de pilha
    p.empilha("$")
    # Empilhando o simbolo inicial da gramatica
    p.empilha("<start>")
    # Abre o arquivo de saida do programa
    arquivo_saida = open(self.arquivo_saida, 'w')
    # Verifica se o arquivo de entrada existe no diretorio em questao
    if not os.path.exists(self.arquivo_entrada):
      print("Arquivo de entrada inexistente")
      arquivo_saida.write("Arquivo de entrada inexistente")
      return
    # Abre o arquivo de entrada do programa
    arquivo = open(self.arquivo_entrada, 'r')
    # Marca a linha atual de leitura
    linha_token = 1
    # Criando a variavel que vai guardar o topo atual da pilha
    topo_pilha = p.get_pilha()[-1]
    # Criando a variavel que vai guardar o simbolo atual do buffer de entrada
    atual_buffer = arquivo.readline()
    # Se X = a = $, entao o analisador termina a analise com sucesso
    while (not (topo_pilha == atual_buffer and topo_pilha == '$') ): 
      # Se X eh um terminal
      if( self.isTerminal(topo_pilha) ):
        # Se X = a != $, entao o analisador desempilha X e consome o simbolo corrente do buffer de entrada
        if (topo_pilha == atual_buffer and topo_pilha != '$'):
          p.desempilha()
          topo_pilha = p.get_pilha()[-1]
          # Atualizando a linha do arquivo do lexico lida
          linha_token += 1 
          # pegando novo token na linha
          atual_buffer = arquivo.readline()
        # Se X eh um terminal e eh diferente de a
        elif ( topo_pilha != atual_buffer ):
          print("Erro sintatico - O topo da pilha: ", topo_pilha, " é um terminal e diferente do simbolo corrente: ", atual_buffer)
      # Se X eh nao-terminal, entao o analisador procura na tabela sintatica a regra [X,a] e empilha o seu
      # lado direito
      elif(self.isNaoTerminal(topo_pilha)):
        lista_producao = self.procura_tabela(topo_pilha, atual_buffer)
        # Se X eh nao-terminal e nao existe regra cuja derivacao produza a, entao ocorreu um erro
        if(len(lista_producao) == 0):
          print("Erro sintatico - regra não terminal: ", topo_pilha, " + terminal: ", atual_buffer, " invalida")
        # Se a regra for do tipo X->Ɛ, apenas desempilha X
        elif('Ɛ' in lista_producao):
          p.desempilha()
          topo_pilha = p.get_pilha()[-1]
        # Empilhando o lado direito da regra da tabela sintatica presente em lista_producao
        else:
          for prod in lista_producao:
            p.empilha(prod)
            print(prod)
          print('----------\n')

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