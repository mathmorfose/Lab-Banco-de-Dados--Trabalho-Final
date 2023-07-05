from bd import BANCO_DADOS as bd
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
            else:
                print("opção inválida")

    def consultar_piloto(self):
        while True:
            limpa_tela()
            print("Consultar se piloto já correu pela escuderia            \n\n \
   Digite o forename do piloto e pressione [ENTER]                            \n")

            forename = input("   Forename: ")
            print("\n      Escolha uma opção:                              \n\n \
            1- Confirmar forename.                                          \n\n \
            2- Digitar novamente o forename.                               \n\n")

            opcao = input("      Digite o número da opção: ")

            if opcao == '1':
                bd.consultar_pilotos_por_forename(forename, self.id)
                print("Pressione [ENTER] para continuar.")
                input()
                break

            elif opcao == '2':
                continue

            else:
                print("Opção inválida. Pressione [ENTER] para tentar novamente.")

    def tela_get_numero_vitorias_pilotos_da_escuderia(self):
        limpa_tela()
        print("{:-^54}".format(" Listar pilotos e a quantidade de vitórias "), end="\n\n\n")

        pilotos = bd.get_numero_vitorias_pilotos_da_escuderia(self.id)

        print(f"Pilotos da escuderia {self.nome} e suas vitórias \n")
        print("{:^35} | {:^8}".format("PILOTO", "VITÓRIAS"))
        print("–"*46)
        for piloto in pilotos:
            print("{:^35} | {:>8}".format(piloto['nome_completo'], piloto['quantidade']))

        print("\nPressione [ENTER] para voltar à tela de relatórios.")
        input()

    def tela_get_contagem_status_da_escuderia(self):
        limpa_tela()
        print("{:-^54}".format(" Listar quantidade de resultados para cada status "), end="\n\n\n")

        resultados = bd.get_contagem_status_da_escuderia(self.id)

        print(f"Quantidade resultados da escuderia {self.nome} por status \n")
        print("{:^18} | {:^10}".format("STATUS", "QUANTIDADE"))
        print("–"*31)
        for resultado in resultados:
            print("{:^18} | {:>10}".format(resultado['status'], resultado['quantidade_resultados']))

        print("\nPressione [ENTER] para voltar à tela de relatórios.")
        input()
