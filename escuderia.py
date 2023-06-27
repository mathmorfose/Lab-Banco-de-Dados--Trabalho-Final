import os
from bd import BANCO_DADOS as bd
from utils import limpaTela

class Escuderia:
    def __init__(self, nome, vitorias_quantidade, pilotos_quantidade, primeiro_ano, ultimo_ano):
        self.nome = nome
        self.vitorias_quantidade = vitorias_quantidade
        self.pilotos_quantidade = pilotos_quantidade
        self.primeiro_ano = primeiro_ano
        self.ultimo_ano = ultimo_ano
    
    def tela_escuderia(self):
        limpaTela()
        print(f"Você está logado como: {self.nome}                      \n\n \
    Quantidade de vitórias: {self.vitorias_quantidade}                  \n \
    Quantidade de pilotos diferentes que já correram pela escuderia: {self.pilotos_quantidade}     \n \
    Primeiro ano que há dados: {self.primeiro_ano}                      \n \
    Último ano que há dados: {self.ultimo_ano}                          \n\n \
        Escolha uma opção:                                              \n\n \
            1- Consultar piloto pelo Forename.                          \n\n \
            2- Visualizar relatórios.                                   \n\n \
        ")
        opcao = input("         Digite o numero da opção: ")

        if opcao == '1':
            self.consultar_piloto()
        elif opcao == '2':
            print("FAZER RELATORIO")

        else:
            print("opção inválida")

    def consultar_piloto(self):
        while True:
            limpaTela()
            print(f"Consultar se piloto já correu pela escuderia            \n\n \
   Digite o forename do piloto e pressione enter                            \n")

            forename = input("   Forename: ")
            print(f"\n      Escolha uma opção:                              \n\n \
            1- Confirmar forename.                                          \n\n \
            2- Digitar novamente o forename.        .                       \n\n \
            3- Cancelar cadastro e voltar para tela de Overview.            \n\n")

            opcao = input("      Digite o numero da opção: ")

            if opcao == '1':
                #FAZER SELECT
                query = f"SELECT * FROM driver WHERE forename = '{forename}'"
                piloto = bd.select(query)
                if piloto:
                    print(piloto)
                    print("\nEscuderia cadastrada com sucesso. Pressione enter para continuar.")
                    input()
                    self.tela_escuderia()
                    break
                else:
                    print("O piloto não correu pela sua Escuderia. Pressione enter para tentar novamente.")
                    input()
                    continue
                
            elif opcao == '2':
                continue
            elif opcao == '3':
                self.tela_escuderia()

            else:
                print("Opção inválida. Pressione enter para tentar novamente.")
