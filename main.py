import time
import sys
from admin import Admin
from escuderia import Escuderia
from piloto import Piloto
from bd import BANCO_DADOS as bd
from utils import limpa_tela, formatar_query


def criar_admin():
    pilotos_qnt = bd.select("SELECT COUNT(*) as contagem FROM driver")[0]["contagem"]
    escuderia_qnt = bd.select("SELECT COUNT(*) as contagem FROM constructors")[0]["contagem"]
    corridas_qnt = bd.select("SELECT COUNT(*) as contagem FROM races")[0]["contagem"]
    temporadas_qnt = bd.select("SELECT COUNT(*) as contagem FROM seasons")[0]["contagem"]
    return Admin(pilotos_qnt, escuderia_qnt, corridas_qnt, temporadas_qnt)


def criar_escuderia(constructorid):
    sql = "SELECT name FROM constructors WHERE constructorid = {}"
    values = (constructorid, )
    rows = bd.select(
        formatar_query(sql, values)
    )
    nome_escuderia = rows[0]["name"]

    vitorias_quantidade, pilotos_quantidade, primeiro_ano, ultimo_ano = bd.overview_escuderia(constructorid)

    return Escuderia(constructorid, nome_escuderia, vitorias_quantidade, pilotos_quantidade, primeiro_ano, ultimo_ano)


def criar_piloto(driverid):
    sql = "SELECT forename || ' ' || surname as nome_completo FROM driver WHERE driverid = {}"
    values = (driverid, )
    rows = bd.select(
        formatar_query(sql, values)
    )
    nome_piloto = rows[0]["nome_completo"]

    vitorias_quantidade, primeiro_ano, ultimo_ano = bd.overview_piloto(driverid)

    return Piloto(driverid, nome_piloto, vitorias_quantidade, primeiro_ano, ultimo_ano)


def registrar_login(user_id):
    if not bd.insert_log_table(user_id):
        print('\nHouve um erro registrando seu login!')


def fazer_login(username, password):
    values = (username, password)

    sql = "  SELECT * \
                FROM users \
                WHERE login = {} and password = MD5({})"
    user = bd.select(formatar_query(sql, values))

    if not user:
        return False

    user = user[0]
    if user['tipo'] == 'Administrador':
        admin = criar_admin()
        registrar_login(user['userid'])
        admin.tela_admin()
    elif user['tipo'] == "Escuderia":
        escuderia = criar_escuderia(int(user['idoriginal']))
        registrar_login(user['userid'])
        escuderia.tela_escuderia()
    else:
        piloto = criar_piloto(int(user['idoriginal']))
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
    print("\n\tObrigado por utilizar o sistema! Volte sempre!\n\
    ----------------------- Encerrando ----------------------- \n")


while True:
    limpa_tela()
    print("---------------------- TELA DE LOGIN ----------------------")
    print("""
               ___                   __       ___
              / _/__  ______ _ __ __/ /__ _  <  /
             / _/ _ \/ __/  ' \ // / / _ `/  / / 
            /_/ \___/_/ /_/_/_\_,_/_/\_,_/  /_/    

    """)
    print("Digite o usuario e pressione [ENTER], repita para a senha.            \n")

    username = input("Usuário: ")
    password = input("Senha: ")

    print("\n                       Autenticando", end="")

    # carregando()

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
