# Incluindo caracteres especiais no programa
# -*- coding: utf-8 -*-

# Bibliotecas para entrada e saida de arquivos
import sys
import os.path

# Biblioteca padrao de string
import string

class GeraTabelaSintatica():
	def __init__(self):
		self.funcoes_primeiros = {}
		self.funcoes_seguintes = {}
		self.tabela_sintatica = {}
		self.nome_gramatica = 'glc.txt'
		self.nome_log = 'log.txt'
	'''
		Criando dicionários contendo os primeiros da gramática
	'''
	def cria_funcoes_primeiro(self):
		arquivo = open(self.nome_gramatica, 'r')
		log = open(self.nome_log, 'w')
		print ("--- Criando funções primeiro ---")
		log.write("--- Criando funções primeiro ---\n")
		linha_gramatica = arquivo.readline()
		linha_programa = 0;
		while linha_gramatica:
			linha_programa += 1
			i = 0
			fim = linha_gramatica.find('>')
			chave = linha_gramatica[1:fim] 
			print(chave+"->")
			log.write(chave+"->")
			ini = linha_gramatica.find(":=")+2 # Somo 2, pois quero ignorar a atribuicao na forma bnf ':='
			fim = len(linha_gramatica) - 1 # Diminuo em 1, pois nao quero pegar os \n presentes no fim da cadeia derivados do arquivo
			producoes = linha_gramatica[ini+1:fim].split("$") # O divisor das producoes eh '$', nao presente na gramatica
			while i in range(0, len(producoes)-1):
				prod = producoes[i]
			print(producoes)
			# Achando producoes que comecem com terminais


			linha_gramatica = arquivo.readline()

		arquivo.close()
		log.close()

	def cria_funcoes_seguinte(self):
		arquivo = open(self.nome_gramatica, 'r')
		log = open(self.nome_log, 'a')
		print ("--- Criando funções seguinte ---")
		log.write("--- Criando funções seguinte ---\n")
		arquivo.close()
		log.close()

	def cria_tabela_sintatica(self, primeiro, seguinte):
		log = open(self.nome_log, 'a')
		print ("--- Criando tabela sintática ---")
		log.write("--- Criando tabela sintática ---\n")
		log.close()

	def gerar_tabela(self):
		self.cria_funcoes_primeiro()
		self.cria_funcoes_seguinte()
		self.cria_tabela_sintatica(self.funcoes_primeiros, self.funcoes_seguintes)



tabela = GeraTabelaSintatica()
tabela.gerar_tabela()
