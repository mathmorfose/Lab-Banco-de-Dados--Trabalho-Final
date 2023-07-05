from bd import BancoDados as Bd
from utils import limpa_tela


class Admin:
    def __init__(self, pilotos_quantidade, escuderias_quantidade, corridas_quantidade, temporadas_quantidade):
        self.pilotos_quantidade = pilotos_quantidade
        self.escuderias_quantidade = escuderias_quantidade
        self.corridas_quantidade = corridas_quantidade
        self.temporadas_quantidade = temporadas_quantidade

    def tela_admin(self):
        while True:
            limpa_tela()
            print(f"Você está logado como: Administrador                  \n\n \
        Pilotos cadastrados: {self.pilotos_quantidade}      \n \
        Escuderias cadastradas: {self.escuderias_quantidade}\n \
        Corridas cadastradas: {self.corridas_quantidade}    \n \
        Temporadas cadastradas: {self.temporadas_quantidade}\n\n \
            Escolha uma opção:                                            \n\n \
                1- Cadastrar Escuderia.                                   \n\n \
                2- Cadastrar Pilotos.                                     \n\n \
                3- Visualizar relatórios.                                 \n\n \
                0- Sair.                                                  \n\n \
            ")
            opcao = input("         Digite o número da opção: ")

            if opcao == '1':
                self.cadastrar_escuderia()
            elif opcao == '2':
                self.cadastrar_piloto()
            elif opcao == '3':
                self.tela_relatorios()
            elif opcao == '0':
                break

    def cadastrar_escuderia(self):
        while True:
            limpa_tela()
            print("---------------- Cadastro de Escuderia ---------------- \n\n \
   Digite o valor de cada dado e pressione [ENTER]                            \n")

            constructor_ref = input("   ConstructorRef: ")
            name = input("   Name: ")
            nationality = input("   Nationality: ")
            url = input("   URL: ")
            print("\n      Escolha uma opção:                              \n\n \
            1- Confirmar cadastro.                                          \n\n \
            2- Digitar novamente os dados da Escuderia.                     \n\n \
            0- Cancelar cadastro e voltar para tela de Overview.            \n\n")

            opcao = input("      Digite o número da opção: ")

            if opcao == '1':
                if Bd.insert_construct(constructor_ref, name, nationality, url):
                    print("\nEscuderia cadastrada com sucesso. Pressione [ENTER] para continuar.")
                    input()
                    self.escuderias_quantidade += 1
                    break
                else:
                    print("Pressione [ENTER] para tentar novamente.")
                    input()
                    continue

            elif opcao == '2':
                continue
            elif opcao == '0':
                break
            else:
                print("\nOpção inválida! Reiniciando cadastro")
                print("Pressione [ENTER] para continuar")
                input()

    def cadastrar_piloto(self):
        while True:
            limpa_tela()
            print("----------------- Cadastro de Piloto -----------------  \n\n \
   Digite o valor de cada dado e pressione [ENTER]                            \n")

            driver_ref = input("   Driverref: ")
            number = input("   Number: ")
            code = input("   Code: ")
            forename = input("   Forename: ")
            surname = input("   Surname: ")
            birth_date = input("   Date of Birth: ")
            nationality = input("   Nationality: ")
            print("\n      Escolha uma opção:                              \n\n \
            1- Confirmar cadastro.                                          \n\n \
            2- Digitar novamente os dados do Piloto.                        \n\n \
            0- Cancelar cadastro e voltar para tela de Overview.            \n\n")

            opcao = input("      Digite o número da opção: ")

            if opcao == '1':
                if Bd.insert_driver(driver_ref, number, code, forename, surname, birth_date, nationality):
                    print("\nPiloto cadastrado com sucesso. Pressione [ENTER] para continuar.")
                    input()
                    self.pilotos_quantidade += 1
                    break
                else:
                    print("Pressione [ENTER] para tentar novamente.")
                    input()
                    continue
            elif opcao == '2':
                continue
            elif opcao == '0':
                break
            else:
                print("\nOpção inválida! Reiniciando cadastro")
                print("Pressione [ENTER] para continuar")
                input()

    def tela_contagem_resultados_status(self):
        limpa_tela()
        todos_status = Bd.get_contagem_resultados_status()
        print("{:-^60}".format(" Contagem de Resultados por Status em ordem decrescente "), end="\n\n\n")
        print("{:^18} | {:^9}".format("STATUS", "CONTAGEM"))
        print("—"*32)
        for status in todos_status:
            print("{:^18} | {:>8}".format(status['status'], status['quantidade_resultados']))

        print("\nPressione [ENTER] para voltar à tela de relatórios.")
        input()

    def tela_aeroportos_proximos_cidade(self):
        while True:
            limpa_tela()
            print("{:-^54}".format(" Consultar aeroportos próximos à cidade "), end="\n\n\n")
            print("    - Digite a cidade e pressione [ENTER]")
            print("    - Deixe o campo em branco para sair\n")

            cidade = input("    Cidade: ")
            if len(cidade) <= 0:
                return

            aeroportos = Bd.get_aeroportos_proximos_cidade(cidade)
            if len(aeroportos) <= 0:
                print(f"\nNenhum aeroporto encontrado próximo à cidade de '{cidade}'")
                print("Pressione [ENTER] para pesquisar novamente.")
                input()
            else:
                break

        limpa_tela()
        print(f"Aeroportos próximos à cidade de '{cidade}' \n")
        print("{:^22} | {:^9} | {:^40} | {:^22} | {:^6} | {:^14} | {:^7} ".format("CIDADE", "IATA CODE", "AEROPORTO", "CIDADE AEROPORTO", "REGIÃO", "DISTÂNCIA (KM)", "TAMANHO"))
        print("—"*139)

        for a in aeroportos:
            f_cidade = a["cidade"][:19] + '...' if len(a["cidade"]) > 22 else a["cidade"]
            f_iatacode = "---" if not a["iatacode"] else a["iatacode"]
            f_aeroporto = a["aeroporto"][:37] + '...' if len(a["aeroporto"]) > 40 else a["aeroporto"]
            f_cidade_aeroporto = a["cidade_aeroporto"][:19] + '...' if len(a["cidade_aeroporto"]) > 22 else a["cidade_aeroporto"]
            f_estado = a["estado"][2:].strip().replace("-", "")
            f_type = "médio" if (a["type"] == 'medium_airport ') else "grande"
            print("{:^22} | {:^9} | {:^40} | {:^22} | {:^6} | {:>14} | {:<7} ".format(f_cidade, f_iatacode, f_aeroporto, f_cidade_aeroporto, f_estado, a["distancia"], f_type))

        print("\nPressione [ENTER] para voltar à tela de relatórios.")
        input()

    def tela_relatorios(self):
        while True:
            limpa_tela()
            print("------------------ Gerar Relatórios ------------------  \n\n \
   Escolha o tipo de relatório e pressione [ENTER].                           \n")

            print("            1- Contagem de Resultados por Status.                   \n\n\
            2- Aeroportos Próximos a uma Cidade por Nome.                   \n\n\
            0- Voltar para tela de Overview.            \n\n")

            opcao = input("      Digite o número da opção: ")

            if opcao == '1':
                self.tela_contagem_resultados_status()
            elif opcao == '2':
                self.tela_aeroportos_proximos_cidade()
            elif opcao == '0':
                break
