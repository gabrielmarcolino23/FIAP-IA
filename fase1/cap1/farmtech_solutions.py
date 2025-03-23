import math
import csv
import os
from typing import List, Dict, Tuple
from datetime import datetime

class Cultura:
    def __init__(self, nome: str, area: float, ruas: int, comprimento_rua: float):
        self.nome = nome
        self.area = area
        self.ruas = ruas
        self.comprimento_rua = comprimento_rua
        self.insumos: List[Dict[str, float]] = []

class SistemaAgricola:
    def __init__(self):
        self.culturas: List[Cultura] = []
        self.tipos_cultura = ["Café", "Soja"]
        
    def calcular_area_retangular(self, largura: float, comprimento: float) -> float:
        return largura * comprimento
    
    def calcular_area_circular(self, raio: float) -> float:
        return math.pi * (raio ** 2)
    
    def calcular_area_hexagonal(self, lado: float) -> float:
        # Área do hexágono regular = (3√3/2) * lado²
        return (3 * math.sqrt(3) / 2) * (lado ** 2)
    
    def adicionar_cultura(self, cultura: Cultura):
        self.culturas.append(cultura)
    
    def atualizar_cultura(self, indice: int, cultura: Cultura):
        if 0 <= indice < len(self.culturas):
            self.culturas[indice] = cultura
            return True
        return False
    
    def deletar_cultura(self, indice: int) -> bool:
        if 0 <= indice < len(self.culturas):
            self.culturas.pop(indice)
            return True
        return False
    
    def listar_culturas(self):
        for i, cultura in enumerate(self.culturas):
            print(f"\nCultura {i + 1}:")
            print(f"Nome: {cultura.nome}")
            print(f"Área: {cultura.area:.2f} m²")
            print(f"Número de ruas: {cultura.ruas}")
            print(f"Comprimento da rua: {cultura.comprimento_rua:.2f} m")
            if cultura.insumos:
                print("Insumos:")
                for j, insumo in enumerate(cultura.insumos, 1):
                    print(f"{j}. {insumo['nome']}: {insumo['quantidade']:.2f} L")
    
    def exportar_dados_csv(self):
        # Cria o diretório data se não existir
        data_dir = "fase1/cap1/data"
        os.makedirs(data_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(data_dir, f"dados_agricolas_{timestamp}.csv")
        
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Cabeçalho
            writer.writerow(['Cultura', 'Area', 'Numero_Ruas', 'Comprimento_Rua', 
                           'Insumo', 'Quantidade'])
            
            # Dados
            for cultura in self.culturas:
                if cultura.insumos:
                    for insumo in cultura.insumos:
                        writer.writerow([
                            cultura.nome,
                            f"{cultura.area:.2f}",
                            cultura.ruas,
                            f"{cultura.comprimento_rua:.2f}",
                            insumo['nome'],
                            f"{insumo['quantidade']:.2f}"
                        ])
                else:
                    writer.writerow([
                        cultura.nome,
                        f"{cultura.area:.2f}",
                        cultura.ruas,
                        f"{cultura.comprimento_rua:.2f}",
                        "",
                        ""
                    ])
        
        print(f"\nDados exportados com sucesso para o arquivo: {filename}")

def menu():
    print("\n=== FarmTech Solutions - Sistema de Gestão Agrícola ===")
    print("1. Entrada de dados")
    print("2. Saída de dados")
    print("3. Atualizar dados")
    print("4. Deletar dados")
    print("5. Exportar dados para análise estatística")
    print("6. Sair do programa")
    return input("\nEscolha uma opção: ")

def gerenciar_insumos(cultura: Cultura):
    while True:
        print("\n=== Gerenciamento de Insumos ===")
        print("1. Adicionar novo insumo")
        print("2. Editar insumo existente")
        print("3. Remover insumo")
        print("4. Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            nome_insumo = input("Nome do insumo: ")
            quantidade = float(input("Quantidade (L/m): "))
            cultura.insumos.append({
                "nome": nome_insumo,
                "quantidade": quantidade
            })
            print("\nInsumo adicionado com sucesso!")
            
        elif opcao == "2":
            if not cultura.insumos:
                print("\nNão há insumos para editar!")
                continue
                
            print("\nInsumos disponíveis:")
            for i, insumo in enumerate(cultura.insumos, 1):
                print(f"{i}. {insumo['nome']}: {insumo['quantidade']:.2f} L")
            
            try:
                indice = int(input("\nDigite o número do insumo para editar: ")) - 1
                if 0 <= indice < len(cultura.insumos):
                    nome_insumo = input("Novo nome do insumo: ")
                    quantidade = float(input("Nova quantidade (L/m): "))
                    cultura.insumos[indice] = {
                        "nome": nome_insumo,
                        "quantidade": quantidade
                    }
                    print("\nInsumo atualizado com sucesso!")
                else:
                    print("\nÍndice inválido!")
            except ValueError:
                print("\nPor favor, digite um número válido!")
                
        elif opcao == "3":
            if not cultura.insumos:
                print("\nNão há insumos para remover!")
                continue
                
            print("\nInsumos disponíveis:")
            for i, insumo in enumerate(cultura.insumos, 1):
                print(f"{i}. {insumo['nome']}: {insumo['quantidade']:.2f} L")
            
            try:
                indice = int(input("\nDigite o número do insumo para remover: ")) - 1
                if 0 <= indice < len(cultura.insumos):
                    cultura.insumos.pop(indice)
                    print("\nInsumo removido com sucesso!")
                else:
                    print("\nÍndice inválido!")
            except ValueError:
                print("\nPor favor, digite um número válido!")
                
        elif opcao == "4":
            break
        else:
            print("\nOpção inválida! Tente novamente.")

def entrada_dados(sistema: SistemaAgricola, cultura_existente: Cultura = None) -> Cultura:
    print("\n=== Entrada de Dados ===")
    print("Tipos de cultura disponíveis:")
    for i, tipo in enumerate(sistema.tipos_cultura, 1):
        print(f"{i}. {tipo}")
    
    while True:
        try:
            indice_cultura = int(input("\nEscolha o tipo de cultura (1-2): ")) - 1
            if 0 <= indice_cultura < len(sistema.tipos_cultura):
                nome = sistema.tipos_cultura[indice_cultura]
                break
            print("Opção inválida! Escolha 1 para Café ou 2 para Soja.")
        except ValueError:
            print("Por favor, digite um número válido.")
    
    print("\nTipos de área disponíveis:")
    print("1. Retangular")
    print("2. Circular")
    print("3. Hexagonal")
    
    while True:
        try:
            tipo_area = int(input("\nEscolha o tipo de área (1-3): "))
            if 1 <= tipo_area <= 3:
                break
            print("Opção inválida! Escolha entre 1 e 3.")
        except ValueError:
            print("Por favor, digite um número válido.")
    
    if tipo_area == 1:
        largura = float(input("Largura (m): "))
        comprimento = float(input("Comprimento (m): "))
        area = sistema.calcular_area_retangular(largura, comprimento)
    elif tipo_area == 2:
        raio = float(input("Raio (m): "))
        area = sistema.calcular_area_circular(raio)
    else:
        lado = float(input("Lado do hexágono (m): "))
        area = sistema.calcular_area_hexagonal(lado)
    
    ruas = int(input("Número de ruas: "))
    comprimento_rua = float(input("Comprimento da rua (m): "))
    
    # Se estiver atualizando uma cultura existente, mantém os insumos
    insumos = cultura_existente.insumos if cultura_existente else []
    
    cultura = Cultura(nome, area, ruas, comprimento_rua)
    cultura.insumos = insumos
    
    # Se estiver atualizando, mostra o gerenciador de insumos
    if cultura_existente:
        gerenciar_insumos(cultura)
    else:
        # Na entrada de dados, apenas permite adicionar insumos simples
        while True:
            adicionar_insumo = input("\nDeseja adicionar um insumo? (s/n): ").lower()
            if adicionar_insumo != 's':
                break
                
            nome_insumo = input("Nome do insumo: ")
            quantidade = float(input("Quantidade (L/m): "))
            cultura.insumos.append({
                "nome": nome_insumo,
                "quantidade": quantidade
            })
    
    return cultura

def main():
    sistema = SistemaAgricola()
    
    while True:
        opcao = menu()
        
        if opcao == "1":
            nova_cultura = entrada_dados(sistema)
            sistema.adicionar_cultura(nova_cultura)
            print("\nCultura cadastrada com sucesso!")
        elif opcao == "2":
            sistema.listar_culturas()
        elif opcao == "3":
            sistema.listar_culturas()
            try:
                indice = int(input("\nDigite o índice da cultura para atualizar: ")) - 1
                if 0 <= indice < len(sistema.culturas):
                    cultura_atualizada = entrada_dados(sistema, sistema.culturas[indice])
                    if sistema.atualizar_cultura(indice, cultura_atualizada):
                        print("\nCultura atualizada com sucesso!")
                    else:
                        print("\nErro ao atualizar a cultura!")
                else:
                    print("\nÍndice inválido!")
            except ValueError:
                print("\nPor favor, digite um número válido!")
        elif opcao == "4":
            sistema.listar_culturas()
            try:
                indice = int(input("\nDigite o índice da cultura para deletar: ")) - 1
                if sistema.deletar_cultura(indice):
                    print("\nCultura deletada com sucesso!")
                else:
                    print("\nÍndice inválido!")
            except ValueError:
                print("\nPor favor, digite um número válido!")
        elif opcao == "5":
            sistema.exportar_dados_csv()
        elif opcao == "6":
            print("\nObrigado por usar o FarmTech Solutions!")
            break
        else:
            print("\nOpção inválida! Tente novamente.")

if __name__ == "__main__":
    main() 