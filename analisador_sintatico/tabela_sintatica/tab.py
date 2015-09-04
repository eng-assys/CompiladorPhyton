# Incluindo caracteres especiais no programa
# -*- coding: utf-8 -*-

# Bibliotecas para entrada e saida de arquivos
import sys
import os.path

# Biblioteca padrao de string
import string

# Permite usar expressoes regulares
import re



class GeraTabelaSintatica():
	def __init__(self):
		self.funcoes_primeiros = {} # Dicionario que guardara as funcoes primeiro da gramatica
		self.funcoes_seguintes = {} # Dicionario que guardara as funcoes seguintes da gramatica
		self.tabela_sintatica = {}  # Dicionario que guardara as a tabela sintatica da gramatica
		self.nome_gramatica = 'glc.txt' # Nome do arquivo para pegar a gramatica
		self.nome_log = 'log.txt'		# Nome do arquivo para gravar o log da execucao da classe
		self.gramatica_lida = []		# Lista de strings que guadara a gramatica lida na memoria principal


	'''
		Define se uma string de entrada eh ou nao um nao-terminal
	'''
	def isNaoTerminal(self, entrada):
		return True if (entrada.find('@') != -1) else False 

	'''
		Dado um nao-terminal valido, a funcao ira procurar sua posicao dentro da gramatica e
		retornara uma lista contendo todas as suas producoes. Caso a busca nao tenha sucesso
		ou o nao-terminal for inválido retornarah uma lista vazia
	'''
	def get_lista_producoes(self, n_terminal):
		contador = 0
		if(n_terminal.find('@') != -1):
			n_terminal = n_terminal[1:n_terminal.find('@')]

		while contador < len(self.gramatica_lida):
			linha_gram = self.gramatica_lida[contador][:-1]
			if(linha_gram[1:linha_gram.find('@')] == n_terminal):
				# print(linha_gram[linha_gram.find(':=')+3:].split('$'))
				return linha_gram[linha_gram.find(':=')+3:].split('$')
			contador += 1
		return []

	'''
		Criando dicionários contendo as funcoes primeiros da gramática
	'''
	def cria_funcoes_primeiro(self):
		log = open(self.nome_log, 'w')

		# Colocando como chave do dicionario de primeiros todos os nao terminais da gramatica
		for linha_gramatica in self.gramatica_lida:
			# Captura nao terminal (delimitado por '¬ @') que estah presente logo no inicio da linha
			nao_terminal = linha_gramatica [1:linha_gramatica.find('@')]
			pilha_n_t = []
			# Lista que ira conter os primeiros desse nao-terminal apos a execucao de STF
			self.funcoes_primeiros[nao_terminal] = self.STF(nao_terminal, pilha_n_t)
			print("===================\nFuncao primeiro de: " + nao_terminal)
			print(self.funcoes_primeiros[nao_terminal])
			
		log.close()

	'''
		Implementacao do algoritmo stf que encontra os primeiros de cada uma das producoes de
		um nao-terminal da gramatica considerada
	'''
	def STF(self, nao_terminal, pilha_n_t):
		# Cada producao do nao terminal trabalhado sera um elemento da lista a seguir (lista_producoes)
		lista_producoes = self.get_lista_producoes(nao_terminal)
		# Vai conter os primeiros do nao-terminal atual
		lista_primeiros = []
		if(nao_terminal.find('@') != -1):
			nao_terminal = nao_terminal[1:nao_terminal.find('@')]
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
						print('n-term:', nao_terminal ,' elemnto prod: ', i, ' - ', elementos_producao[i])
						p = self.STF(elementos_producao[i], pilha_n_t)
						print('p: ', p)
						if ('Ɛ' not in p):
							lista_primeiros += p
		return lista_primeiros

	'''
		Criando o dicionario de funcoes seguintes da gramatica
	'''
	def cria_funcoes_seguinte(self):
		log = open(self.nome_log, 'a')
		print ("--- Criando funções seguinte ---")
		log.write("--- Criando funções seguinte ---\n")
		# Colocando como chave do dicionario de primeiros todos os nao terminais da gramatica
		for linha_gramatica in self.gramatica_lida:
			# Captura nao terminal (delimitado por '¬ @') que estah presente logo no inicio da linha
			nao_terminal = linha_gramatica [1:linha_gramatica.find('@')]


		log.close()

	'''
		Criando a tabela sintatica
	'''
	def cria_tabela_sintatica(self):
		log = open(self.nome_log, 'a')
		print ("--- Criando tabela sintática ---")
		log.write("--- Criando tabela sintática ---\n")
		log.close()

	'''
		Abre o arquivo contendo a gramatica, coloca seu conteudo na memoria principal
		e chama cada uma das funcoes (etapas) para construcao da tabela sintatica
	'''
	def gerar_tabela(self):
		arquivo = open(self.nome_gramatica, 'r')
		self.gramatica_lida = arquivo.readlines()
		self.cria_funcoes_primeiro()
		self.cria_funcoes_seguinte()
		self.cria_tabela_sintatica()
		arquivo.close()



tabela = GeraTabelaSintatica()
tabela.gerar_tabela()
