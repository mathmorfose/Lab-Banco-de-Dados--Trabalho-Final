from os import system, name


# realiza o 'clear' da tela
# independente do sistema operacional
def limpa_tela():
    if name == 'nt':
        # sistemas Windows
        system('cls')
    else:
        # sistemas mac e linux
        system('clear')


# remove alguns caracteres especiais do texto
def limpa_inputs(*valores):
    caracteres_banidos = ["'", "%", ";"]
    valores_filtrados = []
    for valor in valores:
        if type(valor) is str:
            for caracter in caracteres_banidos:
                valor = valor.replace(caracter, "")
        valores_filtrados.append(valor)

    if len(valores_filtrados) == 1:
        return valores_filtrados[0]

    return tuple(valores_filtrados)


# formata a query SQL com os valores passados
def formatar_query(sql, valores):
    if len(valores) == 1:
        valores = (limpa_inputs(*valores), )
    else:
        valores = limpa_inputs(*valores)

    valores_formatados = []
    for valor in valores:
        if type(valor) is not str:
            valores_formatados.append("{}".format(valor))
        elif len(valor) <= 0:
            valores_formatados.append("null")
        else:
            valores_formatados.append("'{}'".format(valor))

    return sql.format(*valores_formatados)
