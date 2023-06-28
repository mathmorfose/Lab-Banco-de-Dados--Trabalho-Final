import time
import sys
from admin import Admin
from escuderia import Escuderia
from bd import BANCO_DADOS as bd
from utils import limpaTela, limpaInput

def criar_admin():
    pilotos_qnt = bd.select("SELECT COUNT(*) FROM driver")[0][0]
    escuderia_qnt = bd.select("SELECT COUNT(*) FROM constructors")[0][0]
    corridas_qnt = bd.select("SELECT COUNT(*) FROM races")[0][0]
    temporadas_qnt = bd.select("SELECT COUNT(*) FROM seasons")[0][0]
    return Admin(pilotos_qnt, escuderia_qnt, corridas_qnt, temporadas_qnt)

def criar_escuderia(username):
    escuderia = bd.select(f"SELECT constructorid, name FROM constructors WHERE constructorref = '{username[:-2]}'")[0]
    id = escuderia[0]
    nome = escuderia[1]

    ##Fazer as queries
    vitorias_quantidade, pilotos_quantidade, primeiro_ano, ultimo_ano = bd.overViewEscuderia(id)
    return Escuderia(id, nome, vitorias_quantidade, pilotos_quantidade, primeiro_ano, ultimo_ano)

def registrar_login(user_id):
    if(bd.insert_log_table(user_id, 'CURRENT_DATE', 'CURRENT_TIME')):
        print("login registrado")
    else:
        print("registrou n")

def fazer_login(username, password):
    query = f"  SELECT * \
                FROM users \
                WHERE login = '{username}' and password = MD5('{password}')"
    user = bd.select(query)

    if user:
        # Trocar recebimento do bd como dicionario para ficar mais intuitivo, isso implica em alterar como esta outras chamadas ao bd tambem
        #user['Tipo'] = Escuderia
        tipo = user[0][3]
        if tipo == 'Administrador':
            admin = criar_admin()
            admin.tela_admin()
            return True
        elif tipo == "Escuderia":
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


while True:
    limpaTela()
    print(f"---------------------- TELA DE LOGIN ---------------------- \n\
                                                                        \n\
    Digite o usuario e pressione enter, repita para a senha.            \n")

    username = limpaInput(input("Usuário: "))
    password = limpaInput(input("Senha: "))

    print("\n                       Autenticando", end="")

    #carregando()

    if fazer_login(username, password):
        break
    else:
        print("\nNome de usuário ou senha incorretos!\n")
        print("- Pressione [ENTER] para tentar novamente")
        print("- Digite 'sair' para encerrar")
        resposta = input()
        if resposta == 'sair':
            break
