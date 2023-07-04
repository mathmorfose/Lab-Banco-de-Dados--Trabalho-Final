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
                1- Visualizar relatórios.                                   \n\n \
                0- Sair.                                   \n\n \
            ")
            opcao = input("         Digite o número da opção: ")

            if opcao == '1':
                print("FAZER RELATORIO")
            elif opcao == '0':
                break

            else:
                print("opção inválida")
