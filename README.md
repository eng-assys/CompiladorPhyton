DOCUMENTAÇÃO DO PROJETO
=======================

Execução do código fonte
------------------------

Para executar (em linux) o compilador completo é necessário utilizar o comando:

```bash
 python3 executa_compilador.py
```

Arquivos de códigos-fonte presentes
-----------------------------------
* programa.txt - arquivo que contém o programa a ser analisado

* analisador_lexico.py - contém o arquivo do analisador léxico

* resp.lex.txt - arquivo que irá receber o resultado da análise léxica

* tab.py - arquivo que gera a tabela sintática para a análise sintática

* glc.txt - contém a gramática livre de contexto para a análise sintática

* log.txt - arquivo de log que guarda uma cópia da tabela gerada

* analisador_sintatico.py - contém o arquivo do analisador sintático

* pilha.py - arquivo que representa uma estrutura de dados de pilha

* resp-sint.txt - arquivo que receberá o resultado da análise sintática

* analisador_semantico.py - irá conter o arquivo do analisador semântico

* executa_compilador.py - executa o analisadores do compilador em sua ordem correta


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
  1. Construção de uma gramática livre de contexto fatorada à esquerda, sem recursão à esquerda, na forma de Backus-Naur (BNF), de acordo com as especificações do anexo A abaixo
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
   
   
   Gramática Livre de Contexto da Linguagem - Forma BNF
   ----------------------------------------------------
   
   * ```<start> := <registro_declaracao><constantes_declaracao><variaveis_declaracao><funcao_declaracao><algoritmo_declaracao>```

   * ```<registro_declaracao> := registro token_identificador { <declaracao_reg> } <registro_declaracao> | Ɛ ```

   * ```<declaracao_reg> := <declaracao>; <declaracao_reg> | Ɛ ```

   * ```<declaracao> := <tipo_primitivo> token_identificador ```                                                      

   * ```<tipo_primitivo> := cadeia | real | inteiro | char | booleano ```

   * ```<constantes_declaracao> := constantes { <declaracao_const>  }  ```

   * ```<declaracao_const> := <declaracao> = <valor_primitivo>;  <declaracao_const> | Ɛ  ```                   

   * ```<valor_primitivo> := token_cadeia | token_real | token_inteiro | token_char | verdadeiro | falso ```          

   * ```<variaveis_declaracao> := variaveis { <declaracao_var> } ```          

   * ```<declaracao_var> := <declaracao> <identificador_deriva>; <declaracao_var> | token_identificador token_identificador; <declaracao_var> | Ɛ```

   * ```<identificador_deriva> := [token_inteiro]<matriz> | <inicializacao> | Ɛ ```

   * ```<matriz> := [token_inteiro] | Ɛ ```
   
   * ```<inicializacao> := = <valor_primitivo> | Ɛ ```          

   * ```<funcao_declaracao> := funcao <tipo_return> token_identificador (<decl_param>)  { <deriva_cont_funcao>  } <funcao_declaracao> | Ɛ ```

   * ```<tipo_return> := <tipo_primitivo> | vazio | token_identificador // Para retorno de variaveis e de registros ```                     

   * ```<decl_param> := <declaracao> <identificador_param_deriva> <deriva_param> | token_identificador token_identificador <deriva_param> ```

   * ```<identificador_param_deriva> := []<matriz_param> | Ɛ```

   * ```<matriz_param> := [] | Ɛ```

   * ```<deriva_param> := ,<decl_param> | Ɛ```

   * ```<deriva_cont_funcao> := <variaveis_declaracao> <decl_comandos> retorno <return_deriva>; | <decl_comandos> retorno <return_deriva>;```

   * ```<return_deriva> := vazio | token_identificador<identificador_imp_arm_deriva> | <valor_primitivo>```

   * ```<decl_comandos> := <comandos> <decl_comandos> | Ɛ```

   * ```<comandos> := <se_declaracao> | <enquanto_declaracao> | <para_declaracao> | <escreva_declaracao> | <leia_declaracao> | <exp_aritmetica> | Ɛ```

   * ```<se_declaracao> := se (<exp_rel_bol>) {<decl_comandos>}<senao_decl>```

   * ```<senao_decl> := senao {<decl_comandos>} | Ɛ```

   * ```<enquanto_declaracao> := enquanto (<exp_rel_bol>) { <decl_comandos> }```

   * ```<para_declaracao> := para (token_identificador = token_inteiro; token_identificador <op_relacional> token_inteiro; token_identificador <op_cont>) {<decl_comandos>}```

   * ```<leia_declaracao> := leia (<exp_leia>);```

   * ```<exp_leia> := <exp_armazena><exp_leia_deriva><exp_leia> | Ɛ```

   * ```<exp_leia_deriva> := ,<exp_armazena> | Ɛ```

   * ```<exp_armazena> := token_identificador <identificador_imp_arm_deriva>```

   * ```<escreva_declaracao> := escreva (<exp_escreva>);```

   * ```<exp_escreva> := <exp_imprime><exp_escreva_deriva><exp_escreva> | Ɛ```

   * ```<exp_escreva_deriva> := ,<exp_imprime> | Ɛ```

   * ```<exp_imprime> := token_cadeia | token_char | token_identificador <identificador_imp_arm_deriva> | (<exp_simples>)```

   * ```<identificador_imp_arm_deriva> := .token_identificador | [token_inteiro]<matriz> | Ɛ ```

   * ```<exp_aritmetica> := token_identificador = <exp_simples>```

   * ```<exp_rel_bol> := <exp_simples> <op_relacional> <exp_simples> <exp_rel_deriva>```

   * ```<exp_simples> := <op_ss><termo><termo_deriva> | <termo><termo_deriva>```

   * ```<op_relacional> := < | > | == | != | <= | >=```

   * ```<exp_rel_deriva> := <op_bolleano> <exp_simples> <op_relacional> <exp_simples> <exp_rel_deriva> | Ɛ```

   * ```<op_ss> := + | -```

   * ```<termo> := <fator><fator_deriva>```

   * ```<termo_deriva> := +<op_soma_deriva> | -<op_sub_deriva> | Ɛ```

   * ```<op_bolleano> := && | || | !```

   * ```<fator> := token_identificador <identificador_imp_arm_deriva> | token_inteiro | (<exp_simples>) ```

   * ```<fator_deriva> := <op_md><fator><fator_deriva> | Ɛ```

   * ```<op_soma_deriva> := <termo><termo_deriva> | +```

   * ```<op_sub_deriva> := <termo><termo_deriva> | -```

   * ```<op_md> := * | /```

   * ```<op_cont> := ++ | --```

   * ```<algoritmo_declaracao> :=  algoritmo {<deriva_cont_principal> }```

   * ```<deriva_cont_principal> := <declaracao_var> <decl_comandos> | <decl_comandos> | Ɛ```

* Analisador Semântico
 1. Construir um analisador semântico paraa  linguagem de programação até então elaborada, de acordo com as especificações do anexo B.
 Anexo B - Características semânticas da linguagem

| Tipo |
--------
| Atribuição deve ser do mesmo tipo que foi declarado |
| Operações aritméticas, lógicas e relacionais devem ser feitas entre operadores de mesmos tipos |
| Chamadas de funções devem ser feitas com o número e ordem de parâmetros corretos |
| Retorno de funções deve ser do mesmo tipo declarado |
| Operações + - / * são compatíveis apenas com operandos inteiro e real |
| Operações && || só podem ser feita entre booleanos |
| Operações ++ -- sucedem apenas tipos inteiros e reais |
| Operações relacionais com operadores == != podem ser feitas com inteiro, real, char ou cadeia, desde que ambos operandos sejam do mesmo tipo |
| Operações > < >= <= só podem ser feitas com operandos inteiro e real; e ambos os operandos devem ser do mesmo tipo |
| Posição de vetores e matrizes devem ser do tipo inteiro |
| Variáveis |
-------------
| As variáveis devem ser declaradas como locais ou globais |
| Constantes |
--------------
| As constantes devem ser declaradas como globais |
| Constantes não podem receber atribuições fora do bloco constantes{} |
| Escopo |
----------
| Diferentes escopos para sub-programas |
| Pode existir variável de mesmo nome global e local |
| Não pode haver duplicidade de variáveis e constantes em um mesmo escopo |
| Não pode haver duplicidade de funções |
| Comandos |
------------
| O comando escreva aceita caracteres constantes, cadeias constantes, variáveis, vetores, matrizes e expressões |
