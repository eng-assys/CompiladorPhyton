Primeiro commit de testes
//FASE DO ANALISADOR LÉXICO

+++ // Eh para dizer que tem caractere demais, algo assim
--- // Erro de mais um operador junto
.+ // Mesmo erro anterior
>== //Mesmo erro anterior

Esses erros citados acima, acho que temos que deixar para tratar depois (não na fase léxica) nas fases seguintes da compilação, por exemplo o de cima devemos identificar como: 'token >' e 'token ==' ao invés de identificar erro de operador mal formado.

Tem certas coisas que identificamos como erro léxico que na verdade são erros de sintaxe, por exemplo: é correto dizer que ana$ana é um identificador mal formado (erro léxico), mas _ ana temos que identificar como caractere inválido underline seguido do identificador ana. Estou revisando isso e deixando atualizado para você ler depois.

Consertei os problemas com: identificadores(certos e com erros), operadores (certos e com erros) e palavras reservadas

Acabei de colocar os tipos de tokens especificos, por exemplo, operadores não é mais identificado genericamente como tok1, temos uma identificação para cada tipo de operador tok100 para operador ponto, tok101 para operador mais e assim por diante

Finalizado sem a interface gráfica

Atualização do programa de testes e erro de string vazia consertado... Agora só falta a interface gráfica mesmo... Espero :'(
