import random

class Tabela_Sintatica(object):

  def __init__(self) :
    self.tabela_sintatica = []

  def cria_tabela_sintatica(self):
    lin = 55
    col = 46
    for i in range(lin):
      linha=[]
      for j in range(col):
        linha = linha + [random.randint(1,10)]
      self.tabela_sintatica = self.tabela_sintatica + [linha]
    return self.tabela_sintatica

  def preenche_tabela_sintatica(self):
    self.tabela_sintatica[0][1] = "tok500"
    self.tabela_sintatica[0][2] = "tok300"
    self.tabela_sintatica[0][3] = "tok300"
    self.tabela_sintatica[0][4] = "tok400"
    self.tabela_sintatica[0][5] = "tok700"
    self.tabela_sintatica[0][6] = "verdadeiro"
    self.tabela_sintatica[0][7] = "falso"
    self.tabela_sintatica[0][8] = "registro"
    self.tabela_sintatica[0][9] = "constantes"
    self.tabela_sintatica[0][10] = "variaveis"
    self.tabela_sintatica[0][11] = "funcao"
    self.tabela_sintatica[0][12] = "algoritmo"
    self.tabela_sintatica[0][13] = "cadeia"
    self.tabela_sintatica[0][14] = "real"
    self.tabela_sintatica[0][15] = "char"
    self.tabela_sintatica[0][16] = "booleano"
    self.tabela_sintatica[0][17] = "inteiro"
    self.tabela_sintatica[0][18] = "vazio"
    self.tabela_sintatica[0][19] = "retorno"
    self.tabela_sintatica[0][20] = "("
    self.tabela_sintatica[0][21] = ")"
    self.tabela_sintatica[0][22] = "{"
    self.tabela_sintatica[0][23] = "}"
    self.tabela_sintatica[0][24] = "["
    self.tabela_sintatica[0][25] = "]"
    self.tabela_sintatica[0][26] = "+"
    self.tabela_sintatica[0][27] = "-"
    self.tabela_sintatica[0][28] = "*"
    self.tabela_sintatica[0][29] = "/"
    self.tabela_sintatica[0][30] = "="
    self.tabela_sintatica[0][31] = "!"
    self.tabela_sintatica[0][32] = "<"
    self.tabela_sintatica[0][33] = ">"
    self.tabela_sintatica[0][34] = "."
    self.tabela_sintatica[0][35] = ";"
    self.tabela_sintatica[0][36] = "|"
    self.tabela_sintatica[0][37] = "&"
    self.tabela_sintatica[0][38] = ","
    self.tabela_sintatica[0][39] = "$"
    self.tabela_sintatica[0][40] = "se"
    self.tabela_sintatica[0][41] = "senao"
    self.tabela_sintatica[0][42] = "para"
    self.tabela_sintatica[0][43] = "enquanto"
    self.tabela_sintatica[0][44] = "leia"
    self.tabela_sintatica[0][45] = "escreva"
    
    self.tabela_sintatica[1][0] = "<start>"
    self.tabela_sintatica[2][0] = "<registro_declaracao>"
    self.tabela_sintatica[3][0] = "<constantes_declaracao>"
    self.tabela_sintatica[4][0] = "<variaveis_declaracao>"
    self.tabela_sintatica[5][0] = "<funcao_declaracao>"
    self.tabela_sintatica[6][0] = "<algoritmo_declaracao>"
    self.tabela_sintatica[7][0] = "<declaracao_reg>"
    self.tabela_sintatica[8][0] = "<declaracao_const>"
    self.tabela_sintatica[9][0] = "<declaracao_var>"
    self.tabela_sintatica[10][0] = "<declaracao>"
    self.tabela_sintatica[11][0] = "<tipo_primitivo>"
    self.tabela_sintatica[12][0] = "<valor_primitivo>"
    self.tabela_sintatica[13][0] = "<decl_var_deriva>"
    self.tabela_sintatica[14][0] = "<inicializacao>"
    self.tabela_sintatica[15][0] = "<funcao_deriva>"
    self.tabela_sintatica[16][0] = "<param_deriva>"
    self.tabela_sintatica[17][0] = "<funcao_deriva_fat>"
    self.tabela_sintatica[18][0] = "<deriva_cont_funcao>"
    self.tabela_sintatica[19][0] = "<tipo_return>"
    self.tabela_sintatica[20][0] = "<tipo_param>"
    self.tabela_sintatica[21][0] = "<return_deriva>"
    self.tabela_sintatica[22][0] = "<comandos>"
    self.tabela_sintatica[23][0] = "<se_declaracao>"
    self.tabela_sintatica[24][0] = "<senao_decl>"
    self.tabela_sintatica[25][0] = "<enquanto_declaracao>"
    self.tabela_sintatica[26][0] = "<para_declaracao>"
    self.tabela_sintatica[27][0] = "<escreva_declaracao>"
    self.tabela_sintatica[28][0] = "<exp_escreva>"
    self.tabela_sintatica[29][0] = "<exp_escreva_deriva>"
    self.tabela_sintatica[30][0] = "<exp_imprime>"
    self.tabela_sintatica[31][0] = "<identificador_deriva>"
    self.tabela_sintatica[32][0] = "<matriz>"
    self.tabela_sintatica[33][0] = "<leia_declaracao>"
    self.tabela_sintatica[34][0] = "<exp_leia>"
    self.tabela_sintatica[35][0] = "<exp_leia_deriva>"
    self.tabela_sintatica[36][0] = "<exp_armazena>"
    self.tabela_sintatica[37][0] = "<exp_rel_bol>"
    self.tabela_sintatica[38][0] = "<exp_rel_deriva>"
    self.tabela_sintatica[39][0] = "<op_relacional>"
    self.tabela_sintatica[40][0] = "<op_booleano>"
    self.tabela_sintatica[41][0] = "<exp_aritmetica>"
    self.tabela_sintatica[42][0] = "<exp_simples>"
    self.tabela_sintatica[43][0] = "<termo_deriva>"
    self.tabela_sintatica[44][0] = "<op_ss>"
    self.tabela_sintatica[45][0] = "<op_cont>"
    self.tabela_sintatica[46][0] = "<op_soma_deriva>"
    self.tabela_sintatica[47][0] = "<op_sub_deriva>"
    self.tabela_sintatica[48][0] = "<termo>"
    self.tabela_sintatica[49][0] = "<fator_deriva>"
    self.tabela_sintatica[50][0] = "<op_md>"
    self.tabela_sintatica[51][0] = "<fator>"
    self.tabela_sintatica[52][0] = "<op_rel_deriva>"
    self.tabela_sintatica[53][0] = "<identificador_param_deriva>"
    self.tabela_sintatica[54][0] = "<matriz_param>"
    
    self.tabela_sintatica[28][1] = ["<exp_escreva>", "<exp_escreva_deriva>", "<exp_imprime>"]
    self.tabela_sintatica[29][1] = ["$"]
    self.tabela_sintatica[30][1] = ["<identificador_deriva>", "tok500"]
    self.tabela_sintatica[31][1] = ["$"]
    self.tabela_sintatica[34][1] = ["<exp_leia>", "<exp_leia_deriva>", "<exp_armazena>"]
    self.tabela_sintatica[35][1] = ["$"]
    self.tabela_sintatica[36][1] = ["<identificador_deriva>", "tok500"]
    self.tabela_sintatica[37][1] = ["<exp_rel_deriva>", "<exp_simples>", "<op_relacional>", "<exp_simples>"]
    self.tabela_sintatica[38][1] = ["$"]
    self.tabela_sintatica[41][1] = ["<exp_simples>", "=", "token_identificador"]
    self.tabela_sintatica[42][1] = ["<termo_deriva><termo>"]
    self.tabela_sintatica[43][1] = ["<termo_deriva>"]
    self.tabela_sintatica[46][1] = ["<termo_deriva>", "<termo>"]
    self.tabela_sintatica[47][1] = ["<termo_deriva>", "<termo>"]
    self.tabela_sintatica[48][1] = ["<fator_deriva>", "<fator>"]
    self.tabela_sintatica[51][1] = ["<identificador_deriva>", "tok500"]
    
    self.tabela_sintatica[12][2] = ["tok_300"]
    self.tabela_sintatica[21][2] = ["; ", "<valor_primitivo>"]
    self.tabela_sintatica[29][2] = ["$"]
    self.tabela_sintatica[30][2] = ["tok300"]
    self.tabela_sintatica[37][2] = ["<exp_rel_deriva>", "<exp_simples>", "<op_relacional>", "<exp_simples>"]
    self.tabela_sintatica[38][2] = ["$"]
    self.tabela_sintatica[42][2] = ["<termo_deriva><termo>"]
    self.tabela_sintatica[46][2] = ["<termo_deriva>", "<termo>"]
    self.tabela_sintatica[47][2] = ["<termo_deriva>", "<termo>"]
    self.tabela_sintatica[48][2] = ["<fator_deriva>", "<fator>"]
    
    self.tabela_sintatica[12][3] = ["tok300"]
    self.tabela_sintatica[21][3] = ["<valor_primitivo>;"]
    self.tabela_sintatica[29][3] = ["$"]
    self.tabela_sintatica[30][3] = ["tok300"]
    
    self.tabela_sintatica[12][4] = ["tok400"]
    self.tabela_sintatica[21][4] = ["; ", "<valor_primitivo>"]
    self.tabela_sintatica[28][4] = ["<exp_escreva>", "<exp_escreva_deriva>", "<exp_imprime>"]
    self.tabela_sintatica[30][4] = ["tok500"]

    self.tabela_sintatica[12][5] = ["tok700"]
    self.tabela_sintatica[21][5] = ["; ", "<valor_primitivo>"]
    self.tabela_sintatica[28][5] = ["<exp_escreva>", "<exp_escreva_deriva>", "<exp_imprime>"]
    self.tabela_sintatica[29][5] = ["$"]
    self.tabela_sintatica[30][5] = ["tok700"]

    self.tabela_sintatica[12][6] = ["verdadeiro"]
    self.tabela_sintatica[21][6] = ["; ", "<valor_primitivo>"]

    self.tabela_sintatica[12][7] = ["falso"]
    self.tabela_sintatica[21][7] = ["; ", "<valor_primitivo>"]
    
    self.tabela_sintatica[1][8] = ["<algoritmo_declaracao>", "<funcao_declaracao>", "<variaveis_declaracao>", "<constantes_declaracao>", "<registro_declaracao>"]
    self.tabela_sintatica[2][8] = ["}", "<declaracao_reg>", "{", "tok500", "registro"]
    self.tabela_sintatica[9][8] = ["<declaracao_var>", ";", "<identificador_deriva>", "tok500", "registro"]
    self.tabela_sintatica[15][8] = ["<funcao_deriva_fat>", "}", "<deriva_cont_funcao>", "{", ")", "<param_deriva>", "(", "tok500", "<tipo_return>"]
    self.tabela_sintatica[16][8] = ["<param_deriva>", "<identificador_param_deriva>", "tok500", "<tipo_param>"]
    self.tabela_sintatica[17][8] = ["<funcao_deriva>"]
    self.tabela_sintatica[18][8] = ["<return_deriva>", "retorno", "<comandos>", "<declaracao_var>"]
    self.tabela_sintatica[20][8] = ["registro"]
    
    self.tabela_sintatica[1][9] = ["<algoritmo_declaracao>", "<funcao_declaracao>", "<variaveis_declaracao>", "<constantes_declaracao>", "<registro_declaracao>"]
    self.tabela_sintatica[3][9] = ["}", "<declaracao_const>", "{", "constantes"]
    

    self.tabela_sintatica[4][10] = ["}", "<declaracao_var>", "{", "variaveis"]

    self.tabela_sintatica[5][11] = ["<funcao_deriva>", "funcao"]
    self.tabela_sintatica[17][11] = ["<funcao_deriva>", "funcao"]

    self.tabela_sintatica[5][12] = ["$"]
    self.tabela_sintatica[6][12] = ["}", "<deriva_cont_funcao>", "{", "algoritmo"]
    self.tabela_sintatica[15][12] = ["$"]
    self.tabela_sintatica[17][12] = ["$"]

    self.tabela_sintatica[7][13] = ["<declaracao_reg>", ";", "tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[8][13] = ["<declaracao_const>", ";", "<valor_primitivo>", "=", "tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[9][13] = ["<decl_var_deriva>", "<identificador_deriva>", "tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[10][13] = ["tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[11][13] = ["cadeia"]
    self.tabela_sintatica[15][13] = ["<funcao_deriva_fat>", "}", "<deriva_cont_funcao>", "{", ")", "<param_deriva>", "(", "tok500", "<tipo_return>"]
    self.tabela_sintatica[16][13] = ["<param_deriva>", "<identificador_param_deriva>", "tok500", "<tipo_param>"]
    self.tabela_sintatica[17][13] = ["<funcao_deriva>"]
    self.tabela_sintatica[18][13] = ["<return_deriva>", "retorno", "<comandos>", "<declaracao_var>"]
    self.tabela_sintatica[19][13] = ["<tipo_primitivo>"]
    self.tabela_sintatica[20][13] = ["<tipo_primitivo>"]

    self.tabela_sintatica[7][14] = ["<declaracao_reg>", ";", "tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[8][14] = ["<declaracao_const>", ";", "<valor_primitivo>", "=", "tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[9][14] = ["<decl_var_deriva>", "<identificador_deriva>", "tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[10][14] = ["tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[11][14] = ["real"]
    self.tabela_sintatica[15][14] = ["<funcao_deriva_fat>", "}", "<deriva_cont_funcao>", "{", ")", "<param_deriva>", "(", "tok500", "<tipo_return>"]
    self.tabela_sintatica[16][14] = ["<param_deriva>", "<identificador_param_deriva>", "tok500", "<tipo_param>"]
    self.tabela_sintatica[17][14] = ["<funcao_deriva>"]
    self.tabela_sintatica[18][14] = ["<return_deriva>", "retorno", "<comandos>", "<declaracao_var>"]
    self.tabela_sintatica[19][14] = ["<tipo_primitivo>"]
    self.tabela_sintatica[20][14] = ["<tipo_primitivo>"]

    self.tabela_sintatica[7][15] = ["<declaracao_reg>", ";", "tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[8][15] = ["<declaracao_const>", ";", "<valor_primitivo>", "=","tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[9][15] = ["<decl_var_deriva>", "<identificador_deriva>", "tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[10][15] = ["tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[11][15] = ["char"]
    self.tabela_sintatica[15][15] = ["<funcao_deriva_fat>", "}", "<deriva_cont_funcao>", "{", ")", "<param_deriva>", "(", "tok500", "<tipo_return>"]
    self.tabela_sintatica[16][15] = ["<param_deriva>", "<identificador_param_deriva>", "tok500", "<tipo_param>"]
    self.tabela_sintatica[17][15] = ["<funcao_deriva>"]
    self.tabela_sintatica[18][15] = ["<return_deriva>", "retorno", "<comandos>", "<declaracao_var>"]
    self.tabela_sintatica[19][15] = ["<tipo_primitivo>"]
    self.tabela_sintatica[20][15] = ["<tipo_primitivo>"]

    self.tabela_sintatica[7][16] = ["<declaracao_reg>", ";", "tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[8][16] = ["<declaracao_const>", ";", "<valor_primitivo>", "=", "tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[9][16] = ["<decl_var_deriva>", "<identificador_deriva>", "tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[10][16] = ["tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[11][16] = ["booleano"]
    self.tabela_sintatica[15][16] = ["<funcao_deriva_fat>", "}", "<deriva_cont_funcao>", "{", ")", "<param_deriva>", "(", "tok500", "<tipo_return>"]
    self.tabela_sintatica[16][16] = ["<param_deriva>", "<identificador_param_deriva>", "tok500", "<tipo_param>"]
    self.tabela_sintatica[17][16] = ["<funcao_deriva>"]
    self.tabela_sintatica[18][16] = ["<return_deriva>", "retorno", "<comandos>", "<declaracao_var>"]
    self.tabela_sintatica[19][16] = ["<tipo_primitivo>"]
    self.tabela_sintatica[20][16] = ["<tipo_primitivo>"]

    self.tabela_sintatica[7][17] = ["<declaracao_reg>", ";", "tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[8][17] = ["<declaracao_const>", ";", "<valor_primitivo>", "=", "tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[9][17] = ["<decl_var_deriva>", "<identificador_deriva>", "tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[10][17] = ["tok500", "<tipo_primitivo>"]
    self.tabela_sintatica[11][17] = ["inteiro"]
    self.tabela_sintatica[15][17] = ["<funcao_deriva_fat>", "}", "<deriva_cont_funcao>", "{", ")", "<param_deriva>", "(", "tok500", "<tipo_return>"]
    self.tabela_sintatica[16][17] = ["<param_deriva>", "<identificador_param_deriva>", "tok500", "<tipo_param>"]
    self.tabela_sintatica[17][17] = ["<funcao_deriva>"]
    self.tabela_sintatica[18][17] = ["<return_deriva>", "retorno", "<comandos>", "<declaracao_var>"]
    self.tabela_sintatica[19][17] = ["<tipo_primitivo>"]
    self.tabela_sintatica[20][17] = ["<tipo_primitivo>"]

    self.tabela_sintatica[15][18] = ["<funcao_deriva_fat>", "}", "<deriva_cont_funcao>", "{", ")", "<param_deriva>", "(", "tok500", "<tipo_return>"]
    self.tabela_sintatica[16][18] = ["<param_deriva>", "<identificador_param_deriva>", "tok500", "<tipo_param>"]
    self.tabela_sintatica[17][18] = ["<funcao_deriva>"]
    self.tabela_sintatica[19][18] = ["vazio"]
    self.tabela_sintatica[21][18] = [";", "vazio"]

    self.tabela_sintatica[22][19] = ["$"]
    self.tabela_sintatica[24][19] = ["$"]

    self.tabela_sintatica[16][20] = ["<param_deriva>", "tok500", "<tipo_param>"]
    self.tabela_sintatica[28][20] = ["<exp_escreva>", "<exp_escreva_deriva>", "<exp_imprime>"]
    self.tabela_sintatica[29][20] = ["$"]
    self.tabela_sintatica[30][20] = [")", "<exp_simples>", "("]
    self.tabela_sintatica[37][20] = ["<exp_rel_deriva>", "<exp_simples>", "<op_relacional>", "<exp_simples>"]
    self.tabela_sintatica[42][20] = ["<termo_deriva><termo>"]
    self.tabela_sintatica[46][20] = ["<termo_deriva><termo>"]
    self.tabela_sintatica[47][20] = ["<termo_deriva><termo>"]
    self.tabela_sintatica[48][20] = ["<fator_deriva>", "<fator>"]
    self.tabela_sintatica[51][20] = [")", "<exp_simples>", "("]
    self.tabela_sintatica[52][20] = ["$"]
    self.tabela_sintatica[54][20] = ["$"]

    self.tabela_sintatica[16][21] = ["$"]
    self.tabela_sintatica[28][21] = ["$"]
    self.tabela_sintatica[29][21] = ["$"]
    self.tabela_sintatica[32][21] = ["$"]
    self.tabela_sintatica[34][21] = ["$"]
    self.tabela_sintatica[43][21] = ["$"]
    self.tabela_sintatica[49][21] = ["$"]
    self.tabela_sintatica[53][21] = ["$"]

    self.tabela_sintatica[16][22] = ["$"]
    self.tabela_sintatica[38][22] = ["$"]
    self.tabela_sintatica[43][22] = ["$"]
    self.tabela_sintatica[49][22] = ["$"]

    self.tabela_sintatica[7][23] = ["$"]
    self.tabela_sintatica[8][23] = ["$"]
    self.tabela_sintatica[9][23] = ["$"]
    self.tabela_sintatica[18][23] = ["$"]
    self.tabela_sintatica[22][23] = ["$"]
    self.tabela_sintatica[24][23] = ["$"]

    self.tabela_sintatica[31][24] = ["<matriz>", "]", "tok300", "["]
    self.tabela_sintatica[32][24] = ["]", "tok300", "["]
    self.tabela_sintatica[53][24] = ["<matriz_deriva>", "]", "["]
    self.tabela_sintatica[54][24] = ["]", "["]

    self.tabela_sintatica[28][26] = ["<exp_escreva>", "<exp_escreva_deriva>", "<exp_imprime>"]
    self.tabela_sintatica[45][26] = ["+", "+"]
    self.tabela_sintatica[29][26] = ["$"]
    self.tabela_sintatica[37][26] = ["<exp_rel_deriva>", "<exp_simples>", "<op_relacional>", "<exp_simples>"]
    self.tabela_sintatica[42][26] = ["<termo_deriva>", "<termo>", "<op_ss>"]
    self.tabela_sintatica[43][26] = ["<op_soma_deriva>", "+"]
    self.tabela_sintatica[49][26] = ["$"]
    self.tabela_sintatica[52][26] = ["$"]

    self.tabela_sintatica[28][27] = ["<exp_escreva>", "<exp_escreva_deriva>", "<exp_imprime>"]
    self.tabela_sintatica[29][27] = ["$"]
    self.tabela_sintatica[49][27] = ["$"]
    self.tabela_sintatica[37][27] = ["<exp_rel_deriva>", "<exp_simples>", "<op_relacional>", "<exp_simples>"]
    self.tabela_sintatica[42][27] = ["<termo_deriva>", "<termo>", "<op_ss>"]
    self.tabela_sintatica[43][27] = ["<op_sub_deriva>", "-"]
    self.tabela_sintatica[45][27] = ["-", "-"]
    self.tabela_sintatica[52][27] = ["$"]

    self.tabela_sintatica[49][28] = ["<fator_deriva>", "<fator>", "<op_md>"]
    self.tabela_sintatica[50][28] = ["*"]

    self.tabela_sintatica[49][29] = ["<fator_deriva>", "<fator>", "<op_md>"]
    self.tabela_sintatica[50][29] = ["/"]

    self.tabela_sintatica[13][30] = ["<declaracao_var>", ";", "<inicializacao>"]
    self.tabela_sintatica[14][30] = ["<valor_primitivo>", "="]
    self.tabela_sintatica[39][30] = ["=", "="]
    self.tabela_sintatica[31][30] = ["$"]
    self.tabela_sintatica[43][30] = ["$"]
    self.tabela_sintatica[49][30] = ["$"]

    self.tabela_sintatica[39][31] = ["=", "!"]
    self.tabela_sintatica[43][31] = ["$"]
    self.tabela_sintatica[49][31] = ["$"]

    self.tabela_sintatica[39][32] = ["=", "<"]
    self.tabela_sintatica[43][32] = ["$"]
    self.tabela_sintatica[49][32] = ["$"]
    
    
    self.tabela_sintatica[39][33] = ["=", ">"]
    self.tabela_sintatica[43][33] = ["$"]
    self.tabela_sintatica[49][33] = ["$"]

    self.tabela_sintatica[31][34] = ["<valor_primitivo>", "=", "tok500", "."]
    self.tabela_sintatica[53][34] = ["tok500", "."]

    self.tabela_sintatica[7][35] = ["$"]
    self.tabela_sintatica[14][35] = ["$"]
    self.tabela_sintatica[13][35] = ["<declaracao_var>", ";", "<inicializacao>"]
    self.tabela_sintatica[31][35] = ["$"]
    self.tabela_sintatica[32][35] = ["$"]

    self.tabela_sintatica[40][36] = ["|", "|"]
    self.tabela_sintatica[43][36] = ["$"]
    self.tabela_sintatica[49][36] = ["$"]
    self.tabela_sintatica[52][36] = ["<exp_rel_deriva>", "<exp_simples>", "<op_relacional>", "<exp_simples>", "<op_booleano>"]

    self.tabela_sintatica[40][37] = ["&", "&"]
    self.tabela_sintatica[43][37] = ["$"]
    self.tabela_sintatica[49][37] = ["$"]
    self.tabela_sintatica[52][37] = ["<exp_rel_deriva>", "<exp_simples>", "<op_relacional>", "<exp_simples>", "<op_booleano>"]

    self.tabela_sintatica[13][38] = ["<declaracao_var>", ";", "<inicializacao>"]
    self.tabela_sintatica[16][38] = ["<param_deriva>", ","]
    self.tabela_sintatica[29][38] = ["<exp_imprime>", ","]
    self.tabela_sintatica[31][38] = ["$"]
    self.tabela_sintatica[32][38] = ["$"]
    self.tabela_sintatica[53][38] = ["$"]
    self.tabela_sintatica[54][38] = ["$"]

    self.tabela_sintatica[9][23] = ["$"]
    
    self.tabela_sintatica[9][40] = ["$"]
    self.tabela_sintatica[22][40] = ["<se_declaracao>"]
    self.tabela_sintatica[18][40] = ["<return_deriva>", "retorno", "<comandos>"]
    self.tabela_sintatica[23][40] = ["<senao_decl>", "}", "<comandos>", "{", "<exp_rel_bol>", "se"]
    
    self.tabela_sintatica[9][41] = ["$"]
    self.tabela_sintatica[23][41] = ["}", "<comandos>", "{", "senao"]
    
    self.tabela_sintatica[9][42] = ["$"]
    self.tabela_sintatica[18][42] = ["<return_deriva>", "retorno", "<comandos>"]
    self.tabela_sintatica[22][42] = ["<para_declaracao>"]
    self.tabela_sintatica[26][42] = ["}", "<comandos>", "{", ")", ";", "<op_cont>", "tok500", ";", "tok300", "<op_relacional>", "tok500", ";", "tok300", "=", "tok500","(", "para"]
    
    self.tabela_sintatica[9][43] = ["$"]
    self.tabela_sintatica[18][43] = ["<return_deriva>", "retorno", "<comandos>"]
    self.tabela_sintatica[22][43] = ["<enquanto_declaracao>"]
    self.tabela_sintatica[25][43] = ["}", "<comandos>", "{", "<exp_rel_bol>", "enquanto"]
    
    
    self.tabela_sintatica[9][44] = ["$"]
    self.tabela_sintatica[18][44] = ["<return_deriva>", "retorno", "<comandos>"]
    self.tabela_sintatica[22][40] = ["<leia_declaracao>"]
    self.tabela_sintatica[33][44] = ["}", "<comandos>", "{", "leia"]
     

    self.tabela_sintatica[9][45] = ["$"]
    self.tabela_sintatica[18][45] = ["<return_deriva>", "retorno", "<comandos>"]
    self.tabela_sintatica[22][45] = ["<escreva_declaracao>"]
    self.tabela_sintatica[27][45] = [";", ")", "<exp_escreva>", "(", "escreva"]
    
      
    
  def consultar_tabela_sintatica(self, prod_topo_pilha, token_atual):
    lin = 0
    col = 0
    for i in range(len(self.tabela_sintatica)):
      if (self.tabela_sintatica[i][0] == prod_topo_pilha):
        lin = i;
    for j in range(len(self.tabela_sintatica[0])):
      if (self.tabela_sintatica[0][j] == token_atual):
        col = j;
    return self.tabela_sintatica[lin][col]

  
  def imprime_tabela_sintatica(self):
    print 'Tabela Sintatica'
    for i in range(len(self.tabela_sintatica)):
      for j in range(len(self.tabela_sintatica[0])):
        print self.tabela_sintatica[i][j],'\t',
      print
    print '_' * 10

  def imprime_linha(self):
    return self.tabela_sintatica[1][8]
