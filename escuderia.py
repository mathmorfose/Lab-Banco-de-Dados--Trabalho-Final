from bd import BancoDados as Bd
from utils import limpa_tela


class Escuderia:
    def __init__(self, id, nome, vitorias_quantidade, pilotos_quantidade, primeiro_ano, ultimo_ano):
        self.nome = nome
        self.id = id
        self.vitorias_quantidade = vitorias_quantidade
        self.pilotos_quantidade = pilotos_quantidade
        self.primeiro_ano = primeiro_ano
        self.ultimo_ano = ultimo_ano

    def tela_escuderia(self):
        while True:
            limpa_tela()
            print(f"Você está logado como: {self.nome}                      \n\n \
        Quantidade de vitórias: {self.vitorias_quantidade}                  \n \
        Quantidade de pilotos diferentes que já correram pela escuderia: {self.pilotos_quantidade}     \n \
        Primeiro ano que há dados: {self.primeiro_ano}                      \n \
        Último ano que há dados: {self.ultimo_ano}                          \n\n \
            Escolha uma opção:                                              \n\n \
                1- Consultar piloto pelo Forename.                          \n\n \
                2- Listar pilotos e a quantidade de vitórias                                  \n\n \
                3- Listar quantidade de resultados para cada status                            \n\n \
                0- Sair                            \n\n \
            ")
            opcao = input("         Digite o número da opção: ")

            if opcao == '1':
                self.consultar_piloto()
            elif opcao == '2':
                self.tela_get_numero_vitorias_pilotos_da_escuderia()
            elif opcao == '3':
                self.tela_get_contagem_status_da_escuderia()
            elif opcao == '0':
                break

    def consultar_piloto(self):
        while True:
            limpa_tela()
            print("{:-^54}".format("Consultar se piloto já correu pela escuderia"), end="\n\n")
            print("    - Digite o primeiro nome do piloto e pressione [ENTER]")
            print("    - Deixe o campo em branco para sair\n")

            forename = input("   Forename: ")
            if len(forename) <= 0:
                return

            pilotos = Bd.consultar_pilotos_por_forename(forename, self.id)

            if len(pilotos) <= 0:
                print(f"\nNenhum piloto encontrado com o primeiro nome '{forename}' que tenha corrido pela escuderia logada.")
                print("Pressione [ENTER] para pesquisar novamente.")
                input()
            else:
                break

        limpa_tela()
        print(f"\nPilotos encontrados da escuderia {self.nome} com o primeiro nome {forename}:\n")
        for piloto in pilotos:
            forename, surname, date_of_birth, nationality = piloto
            print("Nome completo:", forename, surname)
            print("Data de Nascimento(AAAA/MM/DD):", date_of_birth)
            print("Nacionalidade:", nationality)
            print("----------------------")

        print("\nPressione [ENTER] para voltar à tela de relatórios.")
        input()

    def tela_get_numero_vitorias_pilotos_da_escuderia(self):
        limpa_tela()
        print("{:-^54}".format(" Listar pilotos e a quantidade de vitórias "), end="\n\n\n")

        pilotos = Bd.get_numero_vitorias_pilotos_da_escuderia(self.id)

        print(f"Pilotos da {self.nome} e suas vitórias pela escuderia \n")
        print("{:^35} | {:^8}".format("PILOTO", "VITÓRIAS"))
        print("–"*46)
        for piloto in pilotos:
            print("{:^35} | {:>8}".format(piloto['nome_completo'], piloto['quantidade']))

        print("\nPressione [ENTER] para voltar à tela de relatórios.")
        input()

    def tela_get_contagem_status_da_escuderia(self):
        limpa_tela()
        print("{:-^54}".format(" Listar quantidade de resultados para cada status "), end="\n\n\n")

        resultados = Bd.get_contagem_status_da_escuderia(self.id)

        print(f"Quantidade de resultados da escuderia {self.nome} por status \n")
        print("{:^18} | {:^10}".format("STATUS", "QUANTIDADE"))
        print("–"*31)
        for resultado in resultados:
            print("{:^18} | {:>10}".format(resultado['status'], resultado['quantidade_resultados']))

        print("\nPressione [ENTER] para voltar à tela de relatórios.")
        input()
