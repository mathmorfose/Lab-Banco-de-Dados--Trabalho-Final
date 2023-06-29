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
    valores_filtrados = ()
    for valor in valores:
        for caracter in caracteres_banidos:
            valor = valor.replace(caracter, "")
        valores_filtrados += (valor, )
    
    if len(valores_filtrados) == 1:
        return valores_filtrados[0]

    return valores_filtrados