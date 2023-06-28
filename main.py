import time
import sys
from admin import Admin
from escuderia import Escuderia
from piloto import Piloto
from bd import BANCO_DADOS as bd
from utils import limpa_tela, limpa_input

def criar_admin():
    pilotos_qnt = bd.select("SELECT COUNT(*) as contagem FROM driver")[0]["contagem"]
    escuderia_qnt = bd.select("SELECT COUNT(*) as contagem FROM constructors")[0]["contagem"]
    corridas_qnt = bd.select("SELECT COUNT(*) as contagem FROM races")[0]["contagem"]
    temporadas_qnt = bd.select("SELECT COUNT(*) as contagem FROM seasons")[0]["contagem"]
    return Admin(pilotos_qnt, escuderia_qnt, corridas_qnt, temporadas_qnt)

def criar_escuderia(username):
    escuderia = bd.select(f"SELECT constructorid, name FROM constructors WHERE constructorref = '{username[:-2]}'")[0]

    vitorias_quantidade, pilotos_quantidade, primeiro_ano, ultimo_ano = bd.overview_escuderia(escuderia["constructorid"])

    return Escuderia(escuderia["constructorid"], escuderia["name"], vitorias_quantidade, pilotos_quantidade, primeiro_ano, ultimo_ano)

def criar_piloto(username):
    piloto = bd.select(f"SELECT driverid, forename || ' ' || surname as nome_completo FROM driver WHERE driverref = '{username[:-2]}'")[0]

    vitorias_quantidade, primeiro_ano, ultimo_ano = bd.overview_piloto(piloto["driverid"])

    return Piloto(piloto["driverid"], piloto["nome_completo"], vitorias_quantidade, primeiro_ano, ultimo_ano)

def registrar_login(user_id):
    if not bd.insert_log_table(user_id):
        print('\nHouve um erro registrando seu login!')

def fazer_login(username, password):
    username = limpa_input(username)
    password = limpa_input(password)

    query = f"  SELECT * \
                FROM users \
                WHERE login = '{username}' and password = MD5('{password}')"
    user = bd.select(query)

    if not user:
        return False

    user = user[0]
    if user['tipo'] == 'Administrador':
        admin = criar_admin()
        registrar_login(user['userid'])
        admin.tela_admin()
    elif user['tipo'] == "Escuderia":
        escuderia = criar_escuderia(username)
        registrar_login(user['userid'])
        escuderia.tela_escuderia()
    else:
        piloto = criar_piloto(username)
        registrar_login(user['userid'])
        piloto.tela_piloto()

    return True
      
def carregando():
    for _ in range(3):
        sys.stdout.flush()
        time.sleep(0.5)
        print(".", end="")
    sys.stdout.flush()
    time.sleep(0.5)
    print(".")

def msg_sair():
    print(f"\n\tObrigado por utilizar o sistema! Volte sempre!\n\
    ----------------------- Encerrando ----------------------- \n")

while True:
    limpa_tela()
    print(f"---------------------- TELA DE LOGIN ---------------------- \n\
                                                                        \n\
    Digite o usuario e pressione [ENTER], repita para a senha.            \n")

    username = input("Usuário: ")
    password = input("Senha: ")

    print("\n                       Autenticando", end="")

    #carregando()

    if fazer_login(username, password):
        msg_sair()
        break
    else:
        print("\nNome de usuário ou senha incorretos!\n")
        print("- Pressione [ENTER] para tentar novamente")
        print("- Digite 'sair' para encerrar")
        resposta = input()
        if resposta == 'sair':
            msg_sair()
            break
