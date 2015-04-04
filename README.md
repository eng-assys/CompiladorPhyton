Primeiro commit de testes
//FASE DO ANALISADOR LÉXICO

+++ // Eh para dizer que tem caractere demais, algo assim
--- // Erro de mais um operador junto
.+ // Mesmo erro anterior
>== //Mesmo erro anterior

Esses erros citados acima, acho que temos que deixar para tratar depois (não na fase léxica) nas fases seguintes da compilação, por exemplo o de cima devemos identificar como: 'token >' e 'token ==' ao invés de identificar erro.
