DOCUMENTAÇÃO DO PROJETO
=======================

Execução do código fonte
------------------------

Para executar o compilador completo é necessário utilizar o arquivo executa.py.

Fases de Desenvolvimento
------------------------

* Fase 1 - Analisador Léxico (Finalizada);

* Fase 2 - Analisador Sintático (em desenvolvimento);

* Fase 3 - Analisador Semântico (Em planejamento).

Requisitos detalhados de cada fase de desenvolvimento
-----------------------------------------------------

* Analisador Léxico
  * Implementação de um analisador léxico para a linguagem definida pela tabela a seguir (maiores detalhes sobre a linguagem foram baseador la linguagem de progração C):
  
| Palavra Token                        | Expressão regular correspondente     |
|--------------------------------------|--------------------------------------|
| Palavras reservadas                                  | *API*                                |
| Identificadores                             | características                      |
| Número                           | características                      |
| Letra                          | ambiente                             |
| Dígito                         | *just-in-time*                       |
| Símbolo                    | *multiple dispatch*                  |
| Cadeia Constante                          | desempenho                           |
| Caractere Constante                          | experimentação                       |
| Operadores                              | *wrapper*                            |
| Delimitadores                               | *string*                             |
| Comentários de Linha                               | tipagem                              |
| Comentários de Bloco                                | enupla (ou tupla?)                   |
|                             | loops for                            |
|                            | tabela de espalhamento (ou manter hash table?)  |  

* Analisador Sintático
  * Construção de uma gramática livre de contexto fatorada à esquerda, na forma de Backus-Naur (BNF), de acordo com as especificações do anexo a seguir:
  * Implementação de um analisador sintático para a linguagem definida pela gramática construída.

* Analisador Semântico

  * Em planejamento 
