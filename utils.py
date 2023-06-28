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
def limpa_input(text):
    caracteres_banidos = ["'", "%", ";"]
    for caracter in caracteres_banidos:
        text = text.replace(caracter, "")
    
    return text