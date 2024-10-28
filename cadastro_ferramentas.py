import pandas as pd
import os


class Disponibilidades:
    def __init__(self, ferramentas):
        self.ferramentas = ferramentas

    def existe_ferramenta(self, nome):
        if nome in self.ferramentas:
            return True
        else:
            print("Ferramenta não encontrada")
            return False

    def listar_ferramentas(self):
        for ferramenta in self.ferramentas.values():
            print(ferramenta)

    def nova_reserva(self, ferramenta, hora):
        if ferramenta in self.ferramentas:
            self.ferramentas[ferramenta]._nova_reserva(hora)
            return True
        return False

    def cancelar_reserva(self, ferramenta, hora):
        if ferramenta in self.ferramentas:
            self.ferramentas[ferramenta]._cancelar_reserva(hora)
            return True
        return False

    def checar_disponibilidade(self, ferramenta, hora):
        if ferramenta in self.ferramentas:
            return self.ferramentas[ferramenta]._checar_disponibilidade(hora)
        return False
        
    def novo_dia(self):
        for ferramenta in self.ferramentas.values():
            for i in range(0, 24):
                ferramenta._cancelar_reserva(i)
    
    def salvar_ferramentas(self):
        with open("ferramentas.txt", "w") as file:
            for ferramenta in self.ferramentas.values():
                horarios_str = ",".join(f"{hora}:{status}" for hora, status in ferramenta.horarios.items())
                file.write(f"{ferramenta.nome},{ferramenta.categoria},{ferramenta.codigo_sap},{horarios_str}\n")

    def carregar_ferramentas(self):
        with open("ferramentas.txt", "r") as file:
            for line in file:
                nome, categoria, codigo_sap, horarios_str = line.strip().split(",", 3)
                horarios = {int(hora): int(status) for hora, status in (item.split(":") for item in horarios_str.split(","))}
                ferramenta = Ferramenta(nome, categoria, codigo_sap, horarios)
                self.ferramentas[nome] = ferramenta

class Ferramenta:

    def __init__(self, nome, categoria, codigo_sap, horarios=[]):
        if horarios == []:
            horarios = {i: 0 for i in range(0, 24)}

        self.nome = nome
        self.horarios = horarios
        self.categoria = categoria
        self.codigo_sap = codigo_sap

    def _nova_reserva(self, hora):
        self.horarios[hora] = 1

    def _cancelar_reserva(self, hora):
        self.horarios[hora] = 0

    def _checar_disponibilidade(self, hora):
        return self.horarios[hora] == 0

    def __repr__(self):
        return f"{self.nome} ({self.categoria}) - Código SAP: {self.codigo_sap}"


def cadastrar_ferramentas():
    # Carregar a planilha do Excel
    df = pd.read_excel("CodigosSAP2.xlsx")  # Altere para o caminho da sua planilha

    ferramentas = {}
    for index, row in df.iterrows():
        ferramenta = Ferramenta(row["Descrição do Material/Equipamento"], row["Categoria"], row["Código SAP"])
        ferramentas[row["Descrição do Material/Equipamento"]] = ferramenta

    return Disponibilidades(ferramentas)


def sair(disponibilidades):
    disponibilidades.salvar_ferramentas()


def main():
    if os.path.exists("ferramentas.txt"):
        disponibilidades = Disponibilidades({})
        disponibilidades.carregar_ferramentas()
    else:
        disponibilidades = cadastrar_ferramentas()

    while True:
        print("\n")
        print("Bem-vindo ao sistema de cadastro de ferramentas!")
        print("Escolha o que deseja fazer:")
        print("1. Listar ferramentas disponíveis")
        print("2. Fazer uma nova reserva")
        print("3. Cancelar uma reserva")
        print("4. Checar disponibilidade de uma ferramenta")
        print("5. Novo dia")
        print("6. Sair\n")

        escolha = input("Digite o número da opção desejada: ")
        match escolha:
            case "1":
                disponibilidades.listar_ferramentas()
                
            case "2":
                ferramenta = input("Digite o nome da ferramenta: ")
                
                if disponibilidades.existe_ferramenta(ferramenta):
                    try:
                        horas = input("Digite a(s) hora(s) da reserva (ex: 9 ou 9-11): ")
                        if '-' in horas:
                            inicio, fim = map(int, horas.split('-'))
                            for hora in range(inicio, fim + 1):
                                disponibilidades.nova_reserva(ferramenta, hora)
                            print(f"Reserva feita para {ferramenta} das {inicio}h às {fim}h.")
                        else:
                            hora = int(horas)
                            disponibilidades.nova_reserva(ferramenta, hora)
                            print(f"Reserva feita para {ferramenta} às {hora}h.")
                    except ValueError:
                        print("Hora(s) inválida(s). Por favor, digite um número inteiro ou um intervalo válido.")
            
            case "3":
                ferramenta = input("Digite o nome da ferramenta: ")

                if disponibilidades.existe_ferramenta(ferramenta):
                    try:
                        horas = input("Digite a(s) hora(s) da reserva a cancelar (ex: 9 ou 9-11): ")
                        if '-' in horas:
                            inicio, fim = map(int, horas.split('-'))
                            for hora in range(inicio, fim + 1):
                                disponibilidades.cancelar_reserva(ferramenta, hora)
                            print(f"Reserva cancelada para {ferramenta} das {inicio}h às {fim}h.")
                        else:
                            hora = int(horas)
                            disponibilidades.cancelar_reserva(ferramenta, hora)
                            print(f"Reserva cancelada para {ferramenta} às {hora}h.")
                    except ValueError:
                        print("Hora(s) inválida(s). Por favor, digite um número inteiro ou um intervalo válido.")

            case "4":
                ferramenta = input("Digite o nome da ferramenta: ")

                if disponibilidades.existe_ferramenta(ferramenta):
                    try:
                        horas = input("Digite a(s) hora(s) da reserva (ex: 9 ou 9-11): ")
                        if '-' in horas:
                            inicio, fim = map(int, horas.split('-'))
                            for hora in range(inicio, fim + 1):
                                disponibilidade = disponibilidades.checar_disponibilidade(ferramenta, hora)
                                print(f"Hora {hora}: {'Disponível' if disponibilidade else 'Indisponível'}")
                        else:
                            hora = int(horas)
                            disponibilidade = disponibilidades.checar_disponibilidade(ferramenta, hora)
                            print(f"Hora {hora}: {'Disponível' if disponibilidade else 'Indisponível'}")
                    except ValueError:
                        print("Hora(s) inválida(s). Por favor, digite um número inteiro ou um intervalo válido.")
            
            case "5":
                disponibilidades.novo_dia()
                print("Novo dia iniciado. Todas as reservas foram canceladas.")

            case "6":
                sair(disponibilidades)
                print("Dados salvos. Saindo do sistema.")
                break



if __name__ == "__main__":
    main()
