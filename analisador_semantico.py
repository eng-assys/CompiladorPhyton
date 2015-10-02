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
    def __init__():
        self.tabela_semantica = {}
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
        self.variaveisGlobais_tab = {}
        self.funcao_tab = {}
        self.algoritmo_tab = {}

        '''
            Construindo estrutura de tabela semantica de simbolos
        '''
        self.tabela_semantica["registro"] = self.registro_tab
        self.tabela_semantica["constantes"] = self.constantes_tab
        self.tabela_semantica["variaveisGlobais"] = self.variaveisGlobais_tab
        self.tabela_semantica["funcao"] = self.funcao_tab
        self.tabela_semantica["algoritmo"] = self.algoritmo_tab

    def analisa():
