# Incluindo caracteres especiais no programa
# -*- coding: utf-8 -*-

# Bibliotecas para entrada e saida de arquivos
import sys
import os.path

# Biblioteca padrao de string
import string

class GeraTabelaSintatica():
	def __init__(self):
		self.funcoes_primeiros = {} # Dicionario que guardara as funcoes primeiro da gramatica
		self.funcoes_seguintes = {} # Dicionario que guardara as funcoes seguintes da gramatica
		self.tabela_sintatica = {}  # Dicionario que guardara as a tabela sintatica da gramatica
		self.nome_gramatica = 'glc.txt' # Nome do arquivo para pegar a gramatica
		self.nome_log = 'log-tab.txt'		# Nome do arquivo para gravar o log da execucao da classe
		self.gramatica_lida = []		# Lista de strings que guadara a gramatica lida na memoria principal

	def get_tabela(self):
		return self.tabela_sintatica

	# Funcoes principais do codigo. Cada uma chama seus submetodos que juntos ajudam a criar a tabela sintatica
	'''
		Abre o arquivo contendo a gramatica, coloca seu conteudo na memoria principal
		e chama cada uma das funcoes (etapas) para construcao da tabela sintatica
	'''
	def gerar_tabela(self):
		arquivo = open(self.nome_gramatica, 'r')
		# Coloco cada linha da gramatica em uma celula separada da lista self.gramatica_lida
		self.gramatica_lida = arquivo.readlines()
		self.cria_funcoes_primeiro()
		self.cria_funcoes_seguinte()
		self.cria_tabela_sintatica()
		arquivo.close()

	'''
		Criando dicionários contendo as funcoes primeiros da gramática
	'''
	def cria_funcoes_primeiro(self):
		# Abrindo arquivo de log do programa
		log = open(self.nome_log, 'w')

		# Colocando como chave do dicionario de primeiros todos os nao terminais da gramatica
		for linha_gramatica in self.gramatica_lida:
			# Captura nao terminal (delimitado por '¬ @') que estah presente logo no inicio da linha
			nao_terminal = linha_gramatica [:linha_gramatica.find('@')+1]
			pilha_n_t = []
			# Lista que ira conter os primeiros desse nao-terminal apos a execucao de STF
			self.funcoes_primeiros[nao_terminal] = self.STF(nao_terminal, pilha_n_t)
			#print("===================\nFuncao primeiro de: " + nao_terminal)
			#print(self.funcoes_primeiros[nao_terminal])
		log.close()

	# Sub metodo usado pelo algoritmo de funcoes primeiro
	'''
		Dado um nao-terminal valido, a funcao ira procurar sua posicao dentro da gramatica e
		retornara uma lista contendo todas as suas producoes. Caso a busca nao tenha sucesso
		ou retornarah uma lista vazia
	'''
	def get_lista_producoes(self, n_terminal):
		contador = 0
		tam_gram = len(self.gramatica_lida)
		while contador < tam_gram:
			linha_gram = self.gramatica_lida[contador][:-1] # Evita pegar o \n contido no final da linha
			if(linha_gram[0:linha_gram.find('@')+1] == n_terminal):
				return linha_gram[linha_gram.find(':=')+3:].split('$')
			contador += 1
		return []

	# Sub metodo usado pelo algoritmo de funcoes primeiro
	'''
		Implementacao do algoritmo stf que encontra os primeiros de cada uma das producoes para
		um nao-terminal da gramatica considerada
	'''
	def STF(self, nao_terminal, pilha_n_t):
		# Cada producao do nao terminal trabalhado sera um elemento da lista a seguir (lista_producoes)
		lista_producoes = self.get_lista_producoes(nao_terminal)
		# Vai conter os primeiros do nao-terminal atual
		lista_primeiros = []
		# Verifico se nao estou tirando o primeiro do mesmo nao-terminal que iniciei STF
		# evitando assim loops infinitos
		if nao_terminal in pilha_n_t:
			return lista_primeiros

		pilha_n_t.append(nao_terminal)
		# passo por cada uma das producoes presentes na lista de producao do nao-terminal dado
		for prod in lista_producoes:
			elementos_producao = prod.split(' ')
			if('Ɛ' in elementos_producao or not self.isNaoTerminal(elementos_producao[0])):
				lista_primeiros.append(elementos_producao[0])
			else:
				i = 0
				tam = len(elementos_producao)
				p = []
				p += self.STF(elementos_producao[i], pilha_n_t)
				if ('Ɛ' not in p):
					lista_primeiros += p
				else:
					while i < tam and 'Ɛ' in p:
						p.remove('Ɛ')
						lista_primeiros += p
						i += 1
						if (i == tam):
							lista_primeiros.append('Ɛ')
							break
						#print('n-term:', nao_terminal ,' elemnto prod: ', i, ' - ', elementos_producao[i])
						p = self.STF(elementos_producao[i], pilha_n_t)
						#print('p: ', p)
						if ('Ɛ' not in p):
							lista_primeiros += p
		return lista_primeiros

	'''
		Criando o dicionario de funcoes seguintes da gramatica
	'''
	def cria_funcoes_seguinte(self):
		log = open(self.nome_log, 'a')
		# Colocando como chave do dicionario de primeiros todos os nao terminais da gramatica
		for linha_gramatica in self.gramatica_lida:
			# Captura nao terminal (delimitado por '¬ @') que estah presente logo no inicio da linha
			nao_terminal = linha_gramatica [:linha_gramatica.find('@')+1]
			pilha_n_t = []
			self.funcoes_seguintes[nao_terminal] = self.seguintes(nao_terminal, pilha_n_t)
			# Evita elementos repetidos na lista, transformo em set (conjunto), pois elementos
			# em conjunto nao podem ser repetidos
			self.funcoes_seguintes[nao_terminal] = list(set(self.funcoes_seguintes[nao_terminal]))
			#print("seguinte de: ", nao_terminal)
			#print(self.funcoes_seguintes[nao_terminal], '\n')
		log.close()

	# Sub metodo usado pelo algoritmo de funcoes seguinte
	'''
		Trabalha em conjunto com a funcao "seguintes". Ao receber um nao-terminal, procura em
		todas as linhas da gramatica e retorna uma lista contendo as linhas que tinham o nao-
		terminal procurado como parte de seu conteudo
	'''
	def get_linha_nao_terminal(self, nao_terminal):
		linhas_match_n_terminal = []
		# Percorro todas as linhas da gramatica na tentativa de encontrar as que possuem
		# ocorrencias do nao-terminal dado
		for linha in self.gramatica_lida:
			# Evita pegar o nao terminal no inicio da linha e o \n contido no final da linha
			todas_producoes = linha[linha.find('=')+2:-1]
			# Coloco cada uma das producoes da linha da gramatica tirada anteriormente em uma lista
			lista_producoes = todas_producoes.split('$')
			i = 0
			tam_l_producoes = len(lista_producoes)
			while i < tam_l_producoes:
				simbolos_producao = lista_producoes[i].split(" ")
				# print("simbolos prod: ", simbolos_producao)
				j = 0
				tam_s_producao = len(simbolos_producao)
				while j < tam_s_producao:
					if(simbolos_producao[j] == nao_terminal):
						linhas_match_n_terminal.append(linha[:-1])
					j += 1
				i += 1

		return linhas_match_n_terminal

	# Algoritmo de funcoes seguinte
	'''
		Executa o algoritmo de funcoes seguintes, retorna a lista de seguintes do elemento
		em questao
	'''
	def seguintes(self, nao_terminal, pilha_n_t):
		# Crio a lista que vai guardar as funcoes seguintes do nao-terminal de entrada
		funcao_seguinte = []
		# Adicionando ao seguinte do simmbolo inicial da gramatica o marcador de fim de cadeia
		if(nao_terminal == '¬start@'):
			funcao_seguinte.append('$')
		# Verifico se nao estou tirando o primeiro do mesmo nao-terminal que iniciei STF
		# evitando assim loops infinitos
		if nao_terminal in pilha_n_t:
			return funcao_seguinte
		pilha_n_t.append(nao_terminal)

		# Linha da gramatica que possui uma ocorrencia do nao-terminal dado
		linha_contendo_nao_terminal = self.get_linha_nao_terminal(nao_terminal)
		
		for linha in linha_contendo_nao_terminal:
			linha_sem_inicio = linha[linha.find('=')+2:]
			lista_producoes = linha_sem_inicio.split('$')
			
			for producao in lista_producoes:
				simbolos = producao.split(' ')
				# Percorro a lista de simbolos ateh achar o nao-terminal de entrada da funcao 'seguintes'
				i = 0
				tam = len(simbolos)
				while i < tam:
					# print('simbolo: ',simbolos[i], 'terminal: ', nao_terminal)
					# Quando acho o simbolo que eh igual ao nao-terminal de entrada
					if(simbolos[i] == nao_terminal):
						# Se nao ha nenhum simbolo apos o simbolo corrente, o seguinte do nao-terminal
						# de entrada eh o seguinte do nao-terminal do inicio da linha em questao
						if((i+1) == tam):
							if(linha[:linha.find('@')+1] != nao_terminal):
								funcao_seguinte += self.seguintes(linha[:linha.find('@')+1], pilha_n_t)
						# Senao verifico a natureza do proximo simbolo da linha para tirar o seu primeiro
						else:
							# Vou para o proximo simbolo da linha
							i += 1
							# Se jah for um terminal soh adiciono seu conteudo ao seguinte do nao-terminal
							# da entrada
							if( self.isTerminal(simbolos[i]) ):# and (not simbolos[i] == 'Ɛ') ):
								funcao_seguinte.append(simbolos[i])
								break
							else:
								seg_aux = self.funcoes_primeiros[simbolos[i]]
								if('Ɛ' in seg_aux):
									while 'Ɛ' in seg_aux and i < tam:
										while 'Ɛ' in seg_aux:
											seg_aux.remove('Ɛ')
										funcao_seguinte += seg_aux
										i += 1
										if( (i == tam) and (linha[:linha.find('@')+1] != nao_terminal)):
											funcao_seguinte += self.seguintes(linha[:linha.find('@')+1], pilha_n_t)
											break
										if( self.isTerminal(simbolos[i]) ):# and (not simbolos[i] == 'Ɛ') ):
											funcao_seguinte.append(simbolos[i])
											break
										else:
											seg_aux = self.funcoes_primeiros[simbolos[i]]
								else:
									funcao_seguinte += seg_aux
					i += 1
		return funcao_seguinte

	'''
		Cria a tabela sintatica apos a execucao dos algoritmos para criacao das funcoes
		primeiro e seguinte de cada um dos nao terminais da gramatica
	'''
	def cria_tabela_sintatica(self):
		log = open(self.nome_log, 'a')
		 # Para cada linha da gramatica
		for linha in self.gramatica_lida:
			# Tirando o \n do final da linha
			linha = linha[:-1]
			# Pegando o nao-terminal do inicio da linha
			linha_inicio = linha[:linha.find('@')+1]
			# Pegando o resto da linha tirando o nao-terminal do inicio
			linha_sem_inicio = linha[linha.find('=')+2:]
			# Dividindo as producoes presentes na linha
			lista_producoes = linha_sem_inicio.split('$')
			# Para cada producao da linha
			for producao in lista_producoes:
				# Para cada simbolo da producao
				parte_producao = producao.split(' ')
				# Se o primeiro simbolo eh um terminal, ele jah eh o primeiro da producao
				if(self.isTerminal(parte_producao[0])):
					# Adiciono a chave (nao_treminal do inicio da linha + primeiro_da_producao) = recebendo a producao correspondente
					self.tabela_sintatica[linha_inicio+parte_producao[0]] = linha[:linha.find('=')+2] + producao
				# Se o primeiro simbolo eh um nao-terminal, preciso tirar o primeiro de toda a producao
				elif(self.isNaoTerminal(parte_producao[0])):
					primeiro_n_t = []
					# Para cada parte da producao
					for parte in parte_producao:
						if( self.isTerminal(parte) ):
							primeiro_n_t.append(parte)
							break
						primeiro_n_t += self.funcoes_primeiros[parte]
						if('Ɛ' in primeiro_n_t):
							primeiro_n_t.remove('Ɛ')
						else:
							break
					# Para cada terminal p em primeiro_n_t inclua a sua producao corresponente na tabela sintatica de chave linha_inicio+p
					for p in primeiro_n_t:
						self.tabela_sintatica[linha_inicio+p] = linha[:linha.find('=')+2] + producao
											
				elif(producao == 'Ɛ'):
					seguinte_n_t = self.funcoes_seguintes[linha_inicio]
					if('$' in seguinte_n_t):
						self.tabela_sintatica[linha_inicio+'$'] = linha[:linha.find('=')+2] + producao
					for s in seguinte_n_t:
						self.tabela_sintatica[linha_inicio+s] = linha[:linha.find('=')+2] + producao
		
		# Imprimindo tabela sintatica para conferencias e testes
		for key, value in self.tabela_sintatica.items():
			print('Chave: ',key, 'valor: ', value)
			log.write('Chave: ')
			log.write(key)
			log.write(' valor: ')
			log.write(value)
			log.write('\n')
		print('---------')
		log.close()

	# Sub metodo usado por diversas etapas do algoritmo
	'''
		Define se uma string de entrada eh ou nao um nao-terminal
	'''
	def isNaoTerminal(self, entrada):
		return ('¬' in entrada)
	# Sub metodo usado por diversas etapas do algoritmo
	'''
		Define se uma string de entrada eh um terminal
	'''
	def isTerminal(self, entrada):
		return (entrada != 'Ɛ') and not self.isNaoTerminal(entrada)

# Executa o codigo do programa, como na main() do c, por exemplo
# Usando para testes na classe
#tabela = GeraTabelaSintatica()
#tabela.gerar_tabela()
