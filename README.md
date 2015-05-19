DOCUMENTAÇÃO DO PROJETO
=======================

Execução do código fonte
------------------------

Para executar o compilador completo é necessário utilizar o comando:

```bash
 python3 executa.py.
```

Fases de Desenvolvimento
------------------------

* Fase 1 - Analisador Léxico (Finalizada);

* Fase 2 - Analisador Sintático (em desenvolvimento);

* Fase 3 - Analisador Semântico (em planejamento).

Requisitos detalhados de cada fase de desenvolvimento
-----------------------------------------------------

* Analisador Léxico
  1. Implementação de um analisador léxico para a linguagem definida pela tabela a seguir (maiores detalhes sobre a linguagem foram baseados na linguagem de progração C):
  
| Palavra Token                        | Expressão regular correspondente     |
|--------------------------------------|--------------------------------------|
| Palavras reservadas                  | algoritmo, variaveis, constantes, registro, funcao, retorno, vazio, se, senao, enquanto, para, leia, escreva, inteiro, real, booleano, char, cadeia, verdadeiro, falso |
| Identificadores                      | ```Letra(Letra|Dígito|_)*```                          |
| Número                               | ```Dígito+(.Dígito+)?```                              |
| Letra                                | ```(a..z|A..Z)```                                     |
| Dígito                               | ```0..9```                                            |
| Símbolo                              | ```ASCII de 32 a 126```                               |
| Cadeia Constante                     | ```"(Letra|Dígito|Símbolo (exceto 34))"```            |
| Caractere Constante                  | ```'(Letra|Dígito|Símbolo (exceto 39))'```            |
| Operadores                           | ```. + - * / ++ -- == != > >= < <= && || =```         |
| Delimitadores                        | ```; , ( ) { } [ ]```                                 |
| Comentários de Linha                 | ```/* Isto é um comentário de bloco */```             |
| Comentários de Bloco                 | ```// Isto é um comentário de linha```                |

* Analisador Sintático
  1. Construção de uma gramática livre de contexto fatorada à esquerda, sem recursão à esquerda, na forma de Backus-Naur (BNF), de acordo com as especificações do anexo A a seguir:
 
  Anexo A - Características Gerais da Linguagem de Programação criada
  -------------------------------------------------------------------

   - Linguagem estruturada;
   * A declaração de constantes deverá vir em um bloco iniciado pela palavra reservada constantes. Constantes podem ser de qualquer tipo primitivo (inteiro, real, blooleano, char, cadeia). Cada constante deve ser declarada em uma linha dentro do bloco. Este bloco é obrigatório. Se não houver constantes, o bloco deverá estar vazio.
   
    Exemplo:
     ```cpp
      constantes
      {
       inteiro MAX = 10;
       inteiro MAX2 = 50;
       cadeia Texto = "mensagem";
      }
     ```
   * Todas as constantes devem ser globais;
   * A criação de um tipo registro dessa linguagem deve-se iniciar pela palavra reservada registro, seguida do nome do tipo do registro, seguida de um bloco contendo a declaração dos campos do registro (tipo e nome). Uma declaração em cada linha do bloco.
   * Todos os tipos registros, se existirem, devem ser globais e declarados no início do programa antes da declaração das constantes e variáveis globais.
   * Toda declaração de variáveis deverá vir em um bloco começando com a palavra reservada variáveis. Cada variável deve ser declarada em uma linha dentro do bloco, contendo o tipo e o nome da variável seguido de ponto e vírgula. Este bloco é obrigatório. Se não houver variáveis, o bloco deverá estar vazio.
   
    Exemplo:
     ```cpp
      variaveis
      {
       inteiro a;
       inteiro b;
       cadeia Mensagem;
      }
     ```
   * As variáveis podem ser dos tipos primitivos ou dos tipos registros.
   * A declaração de vetores e matrizes deve ser feita no bloco de declaração de variáveis. A linguagem permite somente a declaração e manipulação de vetores e matrizes dos tipos primitivos.
   * É permitida a inicialização de variáveis na declaração, mas não de vetores e matrizes.
   * As variáveis podem ser locais ou globais. Se forem globais devem vir devem vir declaradas após a declaração das constantes. Se forem locais, deve ser declaradas no início do bloco da função, sendo seu escopo, o corpo da função onde as variáveis forem declaradas.
   * Para acessar os campos de uma variável do tipo registro deve-se utilizar o nome da variável seguido deo operador ponto, seguido do nome do campo.
   * O corpo principal do programa é um bloco iniciado pela palavra reservada algoritmo. Quando um programa nessa linguagem é executado, é este bloco que é executado. Este bloco é a última parte de um programa nesta linguagem.
   * Um programa nesta linguagem pode possuir várias funções.
   * As funções podem ter parâmetros dos tipos primitivos e do tipo registro e podem retornar valores (usando o comando retorno).
   * Toda função deve iniciar com a palavra reservada funcao, seguida do tipo de retorno (dos tipos primitivos, do tipo registro ou vazio), seguida do identificador de nome da função, seguido pela lista de parâmetros formais e o corpo da função delimitado por { e }.
   * Delimitadores { e } marcam início e fim de blocos (comandos, declarações, funções), respectivamente.
   * São permitidas exṕressões relacionais, lógicas e aritméticas.
   * O operadores desta linguagem têm a precedência e associatividade de operadores idênticas à da linguagem C.
   * Comandos:
    * Comando se..senão:
     * Na condição do comando se só serão permitidas expressões relacionais ou lógica.
     * A parte senão será opcional.
    * Comando para:
     * Comando semelhante ao for das linguagens C e Java, sendo obrigatórias as três partes do comando.
    * Comando enquanto:
     * Comando semelhante ao while das linguagens C e Java
     * Na condição do comando enquanto só serão permitidas expressões relacionais ou lógicas.
    * Comando escreva:
     * O comando iniciará com a palavra escreva e o que deverá ser escrito entre parênteses, finalizando com ponto e vírgula.
     * Múltiplas impressões no mesmo comando deverão ser separadas por vírgulas.
     * O comando pode imprimir: constantes, cadeias contantes, variáveis, vetores, matrizes e expressões.
    * comando leia:
     * O comando iniciará com a palavra leia e o nome da variável, posição do vetor ou matriz entre parênteses, finalizando com ponto e vírgula.
     * Múltiplas leituras no mesmo comando deverão ser separadas por vírgulas.
   * Variáveis, vetores, matrizes e campos de registros podem ser usados em atribuições, expressões, retornos de funções e parâmetros em chamadas de funções.
   
   
   Gramática Livre de Contexto da Linguagem
   ----------------------------------------

   * Constantes
   * Registro
   * Variáveis
   * Função
   * Algoritmo
   * Expressões (lógicas, aritméticas e relacionais)
   * Precedência e associatividade de operadores
   * Comandos
    * Se/Senão
    * Para
    * Enquanto
    * escreva
    * leia

  1. Implementação de um analisador sintático para a linguagem definida pela gramática construída.

* Analisador Semântico
