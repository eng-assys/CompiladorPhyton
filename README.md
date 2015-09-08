DOCUMENTAÇÃO DO PROJETO
=======================

Execução do código fonte
------------------------

Para executar (em linux) o compilador completo é necessário utilizar o comando:

```bash
 python3 executa_compilador
```

Arquivos de códigos-fonte presentes
-----------------------------------
programa.txt - arquivo que contém o programa a ser analisado
analisador_lexico.py - contém o arquivo do analisador léxico
resp.lex.txt - arquivo que irá receber o resultado da análise léxica
tab.py - arquivo que gera a tabela sintática para a análise sintática
glc.txt - contém a gramática livre de contexto para a análise sintática
log.txt - arquivo de log para a geração da tabela sintática
analisador_sintatico.py - contém o arquivo do analisador sintático
pilha.py - arquivo que representa uma estrutura de dados de pilha
resp-sint.txt - arquivo que receberá o resultado da análise sintática
analisador_semantico.py - irá conter o arquivo do analisador semântico
executa_compilador.py - executa o analisadores do compilador em sua ordem correta


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
  1. Construção de uma gramática livre de contexto fatorada à esquerda, sem recursão à esquerda, na forma de Backus-Naur (BNF), de acordo com as especificações do anexo A abaixo.
  2. Implementação de um analisador sintático para a linguagem definida pela gramática construída.
 
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
	P(1) <start> := <registro_declaracao><constantes_declaracao><variaveis_declaracao><funcao_declaracao><algoritmo_declaracao>

P(2) <registro_declaracao> := registro token_identificador { <declaracao_reg> } <registro_declaracao>
P(3)                      | Ɛ

P(4) <declaracao_reg> := <declaracao>; <declaracao_reg> 
P(5)                | Ɛ

P(6) <declaracao> := <tipo_primitivo> token_identificador

P(7) <tipo_primitivo> := cadeia 
P(8)            | real 
P(9)            | inteiro 
P(10)            | char 
P(11)            | booleano

P(12) <constantes_declaracao> := constantes { <declaracao_const>  }

P(13) <declaracao_const> := <declaracao> = <valor_primitivo>;  <declaracao_const> 
P(14)                | Ɛ

P(15) <valor_primitivo> := token_cadeia 
P(16)        | token_real 
P(17)        | token_inteiro 
P(18)        | token_char 
P(19)        | verdadeiro 
P(20)        | falso

P(21) <variaveis_declaracao> := variaveis { <declaracao_var> }

P(22) <declaracao_var> := <declaracao> <identificador_deriva>; <declaracao_var>
P(23)                | token_identificador token_identificador; <declaracao_var> 
P(24)                | Ɛ

P(25) <identificador_deriva> := [token_inteiro]<matriz>
P(26)                | <inicializacao>
P(27)                | Ɛ 

P(28) <matriz> := [token_inteiro]
P(29)              | Ɛ

P(30) <inicializacao> := = <valor_primitivo> 
P(31)                  | Ɛ

P(32) <funcao_declaracao> := funcao <tipo_return> token_identificador (<decl_param>)  { <deriva_cont_funcao>  } <funcao_declaracao> 
P(33)                      | Ɛ

P(34) <decl_param> := <declaracao> <identificador_param_deriva> <deriva_param>
P(35)            | registro token_identificador <deriva_param>

P(36) <deriva_param> := ,<decl_param>
P(37)            | Ɛ

P(38) <identificador_param_deriva> := []<matriz_param>
P(39)                | Ɛ

P(40) <matriz_param> := []
P(41)            | Ɛ

P(42) <deriva_cont_funcao> := <variaveis_declaracao> <decl_comandos> retorno <return_deriva>; 
P(43)                      | <decl_comandos> retorno <return_deriva>;


P(44) <decl_comandos> := <comandos> <decl_comandos>
P(45)                | Ɛ

P(46) <tipo_return> := <tipo_primitivo> 
P(47)            | registro
P(48)            | vazio

P(49) <return_deriva> := vazio
P(50)            | token_identificador <identificador_param_deriva>
P(51)            | <valor_primitivo>

P(52) <algoritmo_declaracao> :=  algoritmo {<deriva_cont_principal> }

P(53) <deriva_cont_principal> := <declaracao_var> <decl_comandos>
P(54)                | <decl_comandos>
P(55)                | Ɛ

P(56) <comandos> := <se_declaracao> 
P(57)            | <enquanto_declaracao> 
P(58)            | <para_declaracao> 
P(59)            | <escreva_declaracao> 
P(60)            | <leia_declaracao> 
P(61)            | <exp_aritmetica>
P(61)            | Ɛ

P(62) <se_declaracao> := se (<exp_rel_bol>) {<decl_comandos>}<senao_decl>

P(63) <senao_decl> := senão {<decl_comandos>} 
P(64)            | Ɛ
    
P(65) <enquanto_declaracao> := enquanto (<exp_rel_bol>) { <decl_comandos> }

P(66) <para_declaracao> := para (token_identificador = token_inteiro; token_identificador <op_relacional> token_inteiro; token_identificador <op_cont>) {<decl_comandos>}

P(67) <escreva_declaracao> := escreva (<exp_escreva>);

P(68) <exp_escreva> := <exp_imprime><exp_escreva_deriva><exp_escreva> 
P(69)            | Ɛ

P(70) <exp_escreva_deriva> := ,<exp_imprime> 
P(71)                | Ɛ

P(72) <exp_imprime> := token_cadeia 
P(73)            | token_char 
P(74)            | token_identificador <identificador_imp_arm_deriva> 
P(75)            | (<exp_simples>)

P(76) <identificador_imp_arm_deriva> := .token_identificador
P(77)                        | [token_inteiro]<matriz>
P(78)                        | Ɛ

P(79) <leia_declaracao> := leia (<exp_leia>);

P(80) <exp_leia> := <exp_armazena><exp_leia_deriva><exp_leia> 
P(81)        | Ɛ

P(82) <exp_leia_deriva> := ,<exp_armazena> 
P(83)            | Ɛ

P(84) <exp_armazena> := token_identificador <identificador_imp_arm_deriva>
    
P(85) <exp_rel_bol> := <exp_simples> <op_relacional> <exp_simples> <exp_rel_deriva>

P(86) <exp_rel_deriva> := <op_bolleano> <exp_simples> <op_relacional> <exp_simples> <exp_rel_deriva> 
P(87)            | Ɛ

P(88) <op_relacional> := <<op_rel_deriva> 
P(89)            | > <op_rel_deriva>
P(90)            | == 
P(91)            | !=

P(92) <op_rel_deriva> := = 
P(93):             | Ɛ

P(94) <op_bolleano> := && 
P(95)            | ||
    
P(96) <exp_aritmetica> := token_identificador = <exp_simples>

P(97) <exp_simples> := <op_ss><termo><termo_deriva> 
P(98)            | <termo><termo_deriva>

P(99) <termo_deriva> := +<op_soma_deriva>
P(100)            | -<op_sub_deriva> 
P(101)            | Ɛ

P(102) <op_soma_deriva> := <termo><termo_deriva> 
P(103)            | +

P(104) <op_sub_deriva> := <termo><termo_deriva> 
P(105)            | -

P(106) <op_ss> := + 
P(107)        | -

P(108) <op_cont> := ++ 
P(109)        | --

P(110) <termo> := <fator><fator_deriva>
    
P(111) <fator_deriva> := <op_md><fator><fator_deriva> 
P(112)            | Ɛ

P(113) <op_md> := * 
P(114)        | /

P(115) <fator> := token_identificador <identificador_imp_arm_deriva> 
P(116)        | token_inteiro 
P(117)        | (<exp_simples>) 


* Analisador Semântico
