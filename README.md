Primeiro commit de testes
//FASE DO ANALISADOR LÉXICO

+++ // Eh para dizer que tem caractere demais, algo assim
--- // Erro de mais um operador junto
.+ // Mesmo erro anterior
>== //Mesmo erro anterior

Esses erros citados acima, acho que temos que deixar para tratar depois (não na fase léxica) nas fases seguintes da compilação, por exemplo o de cima devemos identificar como: 'token >' e 'token ==' ao invés de identificar erro de operador mal formado.

Tem certas coisas que identificamos como erro léxico que na verdade são erros de sintaxe, por exemplo: é correto dizer que ana$ana é um identificador mal formado (erro léxico), mas _ ana temos que identificar como caractere inválido underline seguido do identificador ana. Estou revisando isso e deixando atualizado para você ler depois.

Consertei os problemas com: identificadores(certos e com erros), operadores (certos e com erros) e palavras reservadas
