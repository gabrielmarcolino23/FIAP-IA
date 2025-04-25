import json
from datetime import datetime
import os

# Dicionário com as faixas ideais para cada cultura
FAIXAS_IDEAIS = {
    'milho': {
        'umidade': {'min': 20, 'max': 30},
        'ph': {'min': 5.5, 'max': 6.5},
        'fosforo': {'min': 10, 'max': 20},
        'potassio': {'min': 20, 'max': 40}
    },
    'soja': {
        'umidade': {'min': 25, 'max': 35},
        'ph': {'min': 6.0, 'max': 7.0},
        'fosforo': {'min': 15, 'max': 25},
        'potassio': {'min': 25, 'max': 45}
    },
    'cana': {
        'umidade': {'min': 30, 'max': 40},
        'ph': {'min': 5.0, 'max': 6.0},
        'fosforo': {'min': 20, 'max': 30},
        'potassio': {'min': 30, 'max': 50}
    }
}

def validar_dados(valor, tipo, min_valor, max_valor):
    """
    Valida se o valor está dentro da faixa permitida e é numérico.
    """
    try:
        valor = float(valor)
        if min_valor <= valor <= max_valor:
            return True, valor
        return False, f"Valor deve estar entre {min_valor} e {max_valor}"
    except ValueError:
        return False, "Valor deve ser numérico"

def coletar_dados_solo():
    """
    Coleta e valida os dados do solo do usuário.
    """
    print("\n=== Coleta de Dados do Solo ===")
    
    # Coletar cultura
    while True:
        cultura = input("Digite a cultura (milho/soja/cana): ").lower()
        if cultura in FAIXAS_IDEAIS:
            break
        print("Cultura inválida. Escolha entre milho, soja ou cana.")
    
    # Coletar e validar umidade
    while True:
        umidade = input("Digite a umidade do solo (%): ")
        valido, resultado = validar_dados(umidade, 'umidade', 0, 100)
        if valido:
            umidade = resultado
            break
        print(resultado)
    
    # Coletar e validar pH
    while True:
        ph = input("Digite o pH do solo: ")
        valido, resultado = validar_dados(ph, 'ph', 3, 10)
        if valido:
            ph = resultado
            break
        print(resultado)
    
    # Coletar e validar fósforo
    while True:
        fosforo = input("Digite o nível de fósforo (mg/dm³): ")
        valido, resultado = validar_dados(fosforo, 'fosforo', 0, 100)
        if valido:
            fosforo = resultado
            break
        print(resultado)
    
    # Coletar e validar potássio
    while True:
        potassio = input("Digite o nível de potássio (mg/dm³): ")
        valido, resultado = validar_dados(potassio, 'potassio', 0, 100)
        if valido:
            potassio = resultado
            break
        print(resultado)
    
    return {
        'cultura': cultura,
        'umidade': umidade,
        'ph': ph,
        'fosforo': fosforo,
        'potassio': potassio,
        'data': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def analisar_dados(dados):
    """
    Analisa os dados do solo e gera recomendações.
    """
    cultura = dados['cultura']
    faixas = FAIXAS_IDEAIS[cultura]
    recomendacoes = []
    
    # Análise de umidade
    if dados['umidade'] < faixas['umidade']['min']:
        recomendacoes.append(f"Aplicar {(faixas['umidade']['min'] - dados['umidade']) * 0.1:.1f} litros de água por m²")
    elif dados['umidade'] > faixas['umidade']['max']:
        recomendacoes.append("Reduzir irrigação - solo muito úmido")
    
    # Análise de pH
    if dados['ph'] < faixas['ph']['min']:
        recomendacoes.append(f"Adicionar calcário (pH ideal: {faixas['ph']['min']:.1f})")
    elif dados['ph'] > faixas['ph']['max']:
        recomendacoes.append(f"Adicionar enxofre (pH ideal: {faixas['ph']['max']:.1f})")
    
    # Análise de fósforo
    if dados['fosforo'] < faixas['fosforo']['min']:
        recomendacoes.append("Aplicar fertilizante com mais fósforo")
    elif dados['fosforo'] > faixas['fosforo']['max']:
        recomendacoes.append("Reduzir aplicação de fósforo")
    
    # Análise de potássio
    if dados['potassio'] < faixas['potassio']['min']:
        recomendacoes.append("Aplicar fertilizante com mais potássio")
    elif dados['potassio'] > faixas['potassio']['max']:
        recomendacoes.append("Reduzir aplicação de potássio")
    
    if not recomendacoes:
        recomendacoes.append("Solo em condições ideais para a cultura")
    
    return recomendacoes

def salvar_diagnostico(dados, recomendacoes):
    """
    Salva o diagnóstico em um arquivo JSON.
    """
    diagnostico = {
        'dados': dados,
        'recomendacoes': recomendacoes
    }
    
    try:
        with open('diagnosticos.json', 'r') as f:
            diagnosticos = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        diagnosticos = []
    
    diagnosticos.append(diagnostico)
    
    with open('diagnosticos.json', 'w') as f:
        json.dump(diagnosticos, f, indent=4)

def visualizar_historico():
    """
    Exibe o histórico de diagnósticos.
    """
    try:
        with open('diagnosticos.json', 'r') as f:
            diagnosticos = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Nenhum diagnóstico encontrado.")
        return
    
    print("\n=== Histórico de Diagnósticos ===")
    for i, diagnostico in enumerate(diagnosticos, 1):
        dados = diagnostico['dados']
        print(f"\nDiagnóstico {i} - {dados['data']}")
        print(f"Cultura: {dados['cultura']}")
        print(f"Umidade: {dados['umidade']}%")
        print(f"pH: {dados['ph']}")
        print(f"Fósforo: {dados['fosforo']} mg/dm³")
        print(f"Potássio: {dados['potassio']} mg/dm³")
        print("\nRecomendações:")
        for rec in diagnostico['recomendacoes']:
            print(f"- {rec}")

def menu_principal():
    """
    Exibe o menu principal e gerencia as opções.
    """
    while True:
        print("\n=== Diagnóstico Inteligente de Solo ===")
        print("1. Realizar novo diagnóstico")
        print("2. Visualizar histórico")
        print("3. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            dados = coletar_dados_solo()
            recomendacoes = analisar_dados(dados)
            salvar_diagnostico(dados, recomendacoes)
            
            print("\n=== Recomendações ===")
            for rec in recomendacoes:
                print(f"- {rec}")
                
        elif opcao == '2':
            visualizar_historico()
            
        elif opcao == '3':
            print("Encerrando o sistema...")
            break
            
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal() 