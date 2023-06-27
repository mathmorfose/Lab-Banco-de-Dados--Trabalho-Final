import os
from bd import BANCO_DADOS as bd
from utils import limpaTela

class Admin:
    def __init__(self, pilotos_quantidade, escuderias_quantidade, corridas_quantidade, temporadas_quantidade):
        self.pilotos_quantidade = pilotos_quantidade
        self.escuderias_quantidade = escuderias_quantidade
        self.corridas_quantidade = corridas_quantidade
        self.temporadas_quantidade = temporadas_quantidade
    
    def tela_admin(self):
        limpaTela()
        print(f"Você está logado como: Administrador                  \n\n \
    Quantidade de pilotos cadastrados: {self.pilotos_quantidade}      \n \
    Quantidade de escuderias cadastradas: {self.escuderias_quantidade}\n \
    Quantidade de corridas cadastradas: {self.corridas_quantidade}    \n \
    Quantidade de temporadas cadastradas: {self.temporadas_quantidade}\n\n \
        Escolha uma opção:                                            \n\n \
            1- Cadastrar Escuderia.                                   \n\n \
            2- Cadastrar Pilotos.                                     \n\n \
        ")
        opcao = input("         Digite o numero da opção: ")

        if opcao == '1':
            self.cadastrar_escuderia()
        elif opcao == '2':
            self.cadastrar_piloto()

        else:
            print("opção inválida")

    def cadastrar_escuderia(self):
        while True:
            limpaTela()
            print(f"Cadastro de Escuderia                                   \n\n \
   Digite o valor de cada dado e pressione enter                            \n")

            constructor_ref = input("   ConstructorRef: ")
            name = input("   Name: ")
            nationality = input("   Nationality: ")
            url = input("   URL: ")
            print(f"\n      Escolha uma opção:                              \n\n \
            1- Confirmar cadastro.                                          \n\n \
            2- Digitar novamente os dados da Escuderia.                     \n\n \
            3- Cancelar cadastro e voltar para tela de Overview.            \n\n")

            opcao = input("      Digite o numero da opção: ")

            if opcao == '1':
                if bd.insert_construct(constructor_ref, name, nationality, url):
                    print("\nEscuderia cadastrada com sucesso. Pressione enter para continuar.")
                    input()
                    self.escuderias_quantidade += 1
                    self.tela_admin()
                    break
                else:
                    print("Pressione enter para tentar novamente.")
                    input()
                    continue
                
            elif opcao == '2':
                continue
            elif opcao == '3':
                self.tela_admin()

            else:
                print("Opção inválida. Pressione enter para tentar novamente.")

    
    def cadastrar_piloto(self):
        while True:
            limpaTela()
            print(f"Cadastro de Piloto                                      \n\n \
   Digite o valor de cada dado e pressione enter                            \n")

            driver_ref = input("   Driverref: ")
            number = input("   Number: ")
            code = input("   Code: ")
            forename = input("   Forename: ")
            surname = input("   Surname: ")
            birth_date = input("   Date of Birth: ")
            nationality = input("   Nationality: ")
            print(f"\n      Escolha uma opção:                              \n\n \
            1- Confirmar cadastro.                                          \n\n \
            2- Digitar novamente os dados do Piloto.                        \n\n \
            3- Cancelar cadastro e voltar para tela de Overview.            \n\n")

            opcao = input("      Digite o numero da opção: ")

            if opcao == '1':
                if bd.insert_driver(driver_ref, number, code, forename, surname, birth_date, nationality):
                    print("\nPiloto cadastrado com sucesso. Pressione enter para continuar.")
                    input()
                    self.pilotos_quantidade += 1
                    self.tela_admin()
                    break
                else:
                    print("Pressione enter para tentar novamente.")
                    input()
                    continue
            elif opcao == '2':
                continue
            elif opcao == '3':
                self.tela_admin()

            else:
                print("Opção inválida. Pressione enter para tentar novamente.")
        