from bd import BANCO_DADOS as bd
from utils import limpa_tela

class Piloto:
    def __init__(self, id, nome, vitorias_quantidade, primeiro_ano, ultimo_ano):
        self.nome = nome
        self.id = id
        self.vitorias_quantidade = vitorias_quantidade
        self.primeiro_ano = primeiro_ano
        self.ultimo_ano = ultimo_ano

    def tela_piloto(self):
        while True:
            limpa_tela()
            print(f"Você está logado como: {self.nome}                      \n\n \
        Quantidade de vitórias: {self.vitorias_quantidade}                  \n \
        Primeiro ano que há dados: {self.primeiro_ano}                      \n \
        Último ano que há dados: {self.ultimo_ano}                          \n\n \
            Escolha uma opção:                                              \n\n \
                1- Listar vitórias.                                   \n\n \
                2- Listar quantidade de resultados para cada status                                   \n\n \
                0- Sair.                                   \n\n \
            ")
            opcao = input("         Digite o número da opção: ")

            if opcao == '1':
                self.tela_get_all_vitorias_piloto()
            elif opcao == '2':
                self.tela_get_contagem_status_do_piloto()
            elif opcao == '0':
                break

            else:
                print("opção inválida")

    def tela_get_all_vitorias_piloto(self):
        limpa_tela()
        print("{:-^54}".format(" Listar vitórias"), end="\n\n\n")

        vitorias = bd.get_all_vitorias_piloto(self.id)

        print(f"Vitórias do piloto {self.nome} \n")

        for vitoria in vitorias:
            if (vitoria['name'] is None and vitoria['year'] is None):
                print("\n\n{:^35}".format("TOTAL DE VITÓRIAS"))
                print("–"*35)
                print("{:^35}".format(vitoria['vitorias']))

            elif (vitoria['name'] is None):
                texto = "VITÓRIA" if vitoria['vitorias'] == 1 else "VITÓRIAS"
                print("\n\n{:^35}".format(f"{vitoria['year']} – {vitoria['vitorias']} {texto} "))
                print("–"*35)

            else:
                print("{:^35}".format(vitoria['name']))

        print("\nPressione [ENTER] para voltar à tela de relatórios.")
        input()

    def tela_get_contagem_status_do_piloto(self):
        limpa_tela()
        print("{:-^54}".format(" Listar quantidade de resultados para cada status "), end="\n\n\n")

        resultados = bd.get_contagem_status_do_piloto(self.id)

        print(f"Quantidade resultados do piloto {self.nome} por status \n")
        print("{:^18} | {:^10}".format("STATUS", "QUANTIDADE"))
        print("–"*31)
        for resultado in resultados:
            print("{:^18} | {:>10}".format(resultado['status'], resultado['quantidade_resultados']))

        print("\nPressione [ENTER] para voltar à tela de relatórios.")
        input()
