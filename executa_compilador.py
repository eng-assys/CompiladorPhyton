# Lucas Vinicius e Andressa Moura
# Arquivo que executa as classes disponiveis do compilador python
# de uma soh vez

# Importando arquivos contendo analisadores
from analisador_lexico import AnalisadorLexico
from analisador_sintatico import AnalisadorSintatico
from analisador_semantico import AnalisadorSemantico

# Realizando etapa de analise lexica
lexico = AnalisadorLexico()
lexico.analisa()
# Realizando etapa de analise sintatica
sintatico = AnalisadorSintatico()
sintatico.start()
# Realizando etapa de analise semantica
# semantico = AnalisadorSemantico()
# semantico.analisa()
