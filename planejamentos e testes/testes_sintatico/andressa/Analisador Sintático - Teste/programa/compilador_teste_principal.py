######           Analisador Sintatico    ######
# Autor 1: Lucas Vinicius dos Santos Assis
# Autora 1: Andressa Moura de Souza
# EXA 869 - MI - Processadores de Linguagem de Programacao
# ==============================================================================
# Implementacao do analisador sintatico de um compilador
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
#   tok201 - Delimitador Virgula,3e4y
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
import analisador_lexico
import analisador_sintatico

al = analisador_lexico.AnalisadorLexico()
ass= analisador_sintatico.AnalisadorSintatico()
al.analisa()
ass.analisa()
  
