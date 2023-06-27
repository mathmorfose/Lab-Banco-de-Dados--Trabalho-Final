from os import system, name

def limpaTela():
    if name == 'nt':
        # sistemas Windows
        system('cls')
    else:
        # sistemas mac e linux
        system('clear')
