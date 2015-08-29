# 1 Preciso achar todas as funcoes primeiros de todos os nao-terminais de nossa gramatica
# 2 Preciso achar todas as funcoes seguintes de todos os nao-terminais de nossa gramatica
# Aplicar o algoritmo de criacao da tabela sintatica baseando-se nos resultados das funcoes primeiras e seguintes
# Organizar a tabela em um discionario - a chave de entrada eh a combinacao de um nao terminal e um terminal
# O conteudo dos elementos dos discionario serao as producoes relacionadas
# toda string eh unicode em python 3

class cria_tabela_sintatica:

	def __init__(self):
		self.funcoes_primeiros = {}
		self.funcoes_seguintes = {}
		self.tabela_sintatica = {}
		self.arquivo_gramatica = 'GramaticaLivreContexto.txt'

	''' Funcao que acha todas as funcoes primeiros de todos os nao-terminais da gramatica inserida.

	 	Pode-se calcular Primeiro(X) para todos os símbolos gramaticais X, aplicando repetidamente
	 	as regras abaixo até que nenhum terminal ou possa ser adicionado a qualquer conjunto Primeiro.

		1. Se X eh um terminal, entao Primeiro(X) = {X}
		2. Se X eh um nao-terminal e X -> aALFA (a sendo um terminal) eh uma producao, entao 
		acrescenta-se a ao conjunto Primeiro(X)
		3. Se X eh um nao-terminal e X-> vazio eh uma producao, entao acrescenta-se vazio ao conjunto
		Primeiro(X)
		4. Se X ->Y1Y2Y3...Yk eh uma producao para algum K>=1, entao acrescente a a Primeiro(X) se, para
		algum i

	'''
	def cria_funcoes_primeiros(self):


	# Acha todas as funcoes seguintes de todos os nao-terminais da gramatica inserida
	def cria_funcoes_seguintes(self):


	''' Uma tabela sintatica M para uma gramatica G pode ser construida por intermedio do algoritmo a seguir:
	 1. Para cada produção X→α da gramática , execute os passos 2 , 3 e 4 ;
	 2. Para cada terminal a em Primeiro(α), adicione X→α a M[X,a];
	 3. Se λ ∈ Primeiro(α), então adicione X→α a M [X,b] para cada terminal
	 b ∈ Seguinte(X);
	 4. Se λ ∈ Primeiro(α) e $ ∈ Seguinte(X), então adicione X→α a M [X ,$];
	 5. Faça cada entrada indefinida de M ser erro.
	'''
	def cria_tabela_sintatica(self):
