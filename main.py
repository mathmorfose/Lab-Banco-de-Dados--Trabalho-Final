import time
import sys
import os
from admin import Admin
from escuderia import Escuderia
from bd import BANCO_DADOS as bd
from utils import limpaTela

def criar_admin():
    pilotos_qnt = bd.select("SELECT COUNT(*) FROM driver")[0][0]
    escuderia_qnt = bd.select("SELECT COUNT(*) FROM constructors")[0][0]
    corridas_qnt = bd.select("SELECT COUNT(*) FROM races")[0][0]
    temporadas_qnt = bd.select("SELECT COUNT(*) FROM seasons")[0][0]
    return Admin(pilotos_qnt, escuderia_qnt, corridas_qnt, temporadas_qnt)

def criar_escuderia(username):
    nome = bd.select(f"SELECT name FROM constructors WHERE constructorref = '{username[:-2]}'")[0][0]

    ##Fazer as queries
    vitorias_quantidade = 1
    pilotos_quantidade = 2
    primeiro_ano = 3
    ultimo_ano = 4
    return Escuderia(nome, vitorias_quantidade, pilotos_quantidade, primeiro_ano, ultimo_ano)

def registrar_login(user_id):
    if(bd.insert_log_table(user_id, 'CURRENT_DATE', 'CURRENT_TIME')):
        print("login registrado")
    else:
        print("registrou n")

def fazer_login(username, password):
    
    if username == 'admin' and password == 'admin':
        admin = criar_admin()
        admin.tela_admin()
        return True
    else: 
        if verificar_tipo_usuario(username, password):
            return True
        
    return False

def verificar_tipo_usuario(username, password):
    query = f"  SELECT * \
                FROM users \
                WHERE login = '{username}' and password = MD5('{password}')"
    user = bd.select(query)

    if user:
        # Trocar recebimento do bd como dicionario para ficar mais intuitivo, isso implica em alterar como esta outras chamadas ao bd tambem
        #user['Tipo'] = Escuderia
        if user[0][3] == "Escuderia":
            escuderia = criar_escuderia(username)
            registrar_login(user[0][0])
            escuderia.tela_escuderia()
            return True
        else:
            #piloto = criar_piloto(username)
            #piloto.tela_piloto()
            #registrar_login(username)
            print("piloto criado")
            return True
    
    return False

        
def carregando():
    for _ in range(3):
        sys.stdout.flush()
        time.sleep(0.5)
        print(".", end="")
    sys.stdout.flush()
    time.sleep(0.5)
    print(".")

def fazer_autenticacao(username, password):

    if(fazer_login(username, password)):
        return True
    return False
        

while True:
    limpaTela()
    print(f"---------------------- TELA DE LOGIN ---------------------- \n\
                                                                        \n\
    Digite o usuario e pressione enter, repita para a senha.            \n")

    username = input("Usuário: ")
    password = input("Senha: ")

    print("\n                       Autenticando", end="")

    #carregando()

    if fazer_autenticacao(username, password):
        break
    else:
        print("\nNome de usuário ou senha incorretos. Pressione Enter para tentar novamente.")
        input()
