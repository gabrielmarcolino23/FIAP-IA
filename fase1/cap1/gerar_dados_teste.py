import random
import math
from datetime import datetime
import os
from farmtech_solutions import SistemaAgricola, Cultura

def gerar_dados_teste(num_culturas: int = 10):
    """
    Gera dados de teste com valores aleatórios para culturas e insumos.
    
    Args:
        num_culturas (int): Número de culturas a serem geradas
    """
    sistema = SistemaAgricola()
    
    insumos_cafe = [
        {"nome": "Fertilizante NPK", "min": 0.5, "max": 2.0},
        {"nome": "Herbicida", "min": 0.3, "max": 1.0},
        {"nome": "Fungicida", "min": 0.2, "max": 0.8},
        {"nome": "Inseticida", "min": 0.2, "max": 0.8}
    ]
    
    insumos_soja = [
        {"nome": "Fertilizante NPK", "min": 0.8, "max": 2.5},
        {"nome": "Herbicida", "min": 0.5, "max": 1.5},
        {"nome": "Fungicida", "min": 0.3, "max": 1.0},
        {"nome": "Inseticida", "min": 0.3, "max": 1.0}
    ]
    
    for _ in range(num_culturas):

        nome = random.choice(sistema.tipos_cultura)
        
        area = random.uniform(100, 10000)
        
        ruas = random.randint(5, 50)
        
        comprimento_rua = random.uniform(10, 100)

        cultura = Cultura(nome, area, ruas, comprimento_rua)
        
        insumos_disponiveis = insumos_cafe if nome == "Café" else insumos_soja
        num_insumos = random.randint(2, len(insumos_disponiveis))
        insumos_selecionados = random.sample(insumos_disponiveis, num_insumos)
        
        for insumo in insumos_selecionados:
            quantidade = random.uniform(insumo["min"], insumo["max"])
            cultura.insumos.append({
                "nome": insumo["nome"],
                "quantidade": quantidade
            })
        
        sistema.adicionar_cultura(cultura)
    
    sistema.exportar_dados_csv()
    print(f"\nDados de teste gerados com sucesso! {num_culturas} culturas foram criadas.")

if __name__ == "__main__":
    data_dir = "fase1/cap1/data"
    os.makedirs(data_dir, exist_ok=True)

    gerar_dados_teste(10) 