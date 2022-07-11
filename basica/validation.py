def campo_tem_algum_numero(valor_campo, nome_campo, lista_de_erros):
    """Verifica se o campo tem algum número"""
    if any(char.isdigit() for char in valor_campo):
        lista_de_erros[nome_campo] = 'Não inclua números neste campo.'

def campo_tem_alguma_letra(valor_campo, nome_campo,lista_de_erros):
    """Verifica se o campo tem alguma letra"""
    if valor_campo == "":
        pass
    else:
        if any(char.isdigit() for char in valor_campo):
            pass
        else:
            lista_de_erros[nome_campo] = 'Inclua apenas números neste campo. Sem caractéres como: . / + - @1'

def cpf_cnpj_numeros(valor_campo, nome_campo,lista_de_erros):
    """Verifica se o usuário digitou 11 dígitos para o CPF ou 14 dígitos para o CNPJ"""
    if valor_campo is not None:
        if (len(valor_campo) == 11 or len(valor_campo) == 14 or len(valor_campo) == 0):
            pass
        else:
            lista_de_erros[nome_campo] = 'CPF ou CNPJ inválido. Por favor, só inclua números. Sem caractéres como: . / + - @'
    

def telefone_numero(valor_campo, nome_campo,lista_de_erros):
    """Verifica se o usuário digitou pelo menos 9 números par ao telefone"""
    if valor_campo is not None:
        if len(valor_campo) < 8:
            lista_de_erros[nome_campo] = 'Por favor, inclua o DDD ou DDI no campo de telefone.' 

