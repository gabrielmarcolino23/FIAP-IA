# 🌾 FarmTech Solutions - Análise de Rendimento de Safras

**Fase 5 - Machine Learning e Computação em Nuvem**  
**FIAP - Curso de Inteligência Artificial**

---

## 📋 Descrição do Projeto

Este projeto foi desenvolvido para a **FarmTech Solutions**, uma empresa que presta serviços de IA para fazendas de médio porte. O objetivo é analisar dados de condições ambientais (solo e temperatura) para prever o rendimento de diferentes culturas agrícolas utilizando técnicas de Machine Learning.

### 🎯 Objetivos

1. **Análise Exploratória:** Compreender os padrões nos dados de culturas agrícolas
2. **Machine Learning Não Supervisionado:** Identificar tendências através de clusterização e detectar outliers
3. **Machine Learning Supervisionado:** Desenvolver modelos preditivos para rendimento de safras
4. **Computação em Nuvem:** Análise de custos para hospedagem da solução na AWS

---

## 📊 Dataset

- **Fonte:** `crop_yield.csv`
- **Registros:** 157 observações
- **Culturas:** Cocoa beans, Oil palm fruit, Rice paddy, Rubber natural
- **Variáveis:**
  - Precipitação (mm/dia)
  - Umidade específica a 2 metros (g/kg)
  - Umidade relativa a 2 metros (%)
  - Temperatura a 2 metros (°C)
  - **Target:** Rendimento (toneladas/hectare)

---

## 🔬 Metodologia

### Machine Learning Não Supervisionado
- **Clusterização K-Means:** Identificação de padrões nas condições ambientais
- **Detecção de Outliers:** Isolation Forest para identificar cenários discrepantes

### Machine Learning Supervisionado
Foram desenvolvidos e comparados 5 modelos diferentes:

1. **Linear Regression** - Modelo base linear
2. **Random Forest Regressor** - Ensemble baseado em árvores
3. **Support Vector Regression (SVR)** - Modelo com kernel RBF
4. **Gradient Boosting Regressor** - Boosting para regressão
5. **Neural Network (MLP)** - Rede neural multicamadas

### Métricas de Avaliação
- **MAE (Mean Absolute Error):** Erro médio absoluto
- **MSE (Mean Squared Error):** Erro quadrático médio
- **RMSE (Root Mean Squared Error):** Raiz do erro quadrático médio
- **R² (Coefficient of Determination):** Coeficiente de determinação
- **Validação Cruzada:** 5-fold cross-validation

---

## 🚀 Como Executar

### Pré-requisitos
```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

### Execução
1. Clone o repositório
2. Navegue até a pasta do projeto
3. Abra o Jupyter Notebook: `farmtech_ml_analysis.ipynb`
4. Execute todas as células sequencialmente

---

## 📈 Principais Resultados

### Análise Exploratória
- **Correlações identificadas:** [A ser preenchido após execução]
- **Distribuições das variáveis:** [A ser preenchido após execução]
- **Padrões por cultura:** [A ser preenchido após execução]

### Clusterização
- **Número ótimo de clusters:** [A ser preenchido após execução]
- **Padrões identificados:** [A ser preenchido após execução]
- **Outliers detectados:** [A ser preenchido após execução]

### Modelos Preditivos
- **Melhor modelo:** [A ser preenchido após execução]
- **R² alcançado:** [A ser preenchido após execução]
- **RMSE:** [A ser preenchido após execução]

---

## ☁️ Análise de Computação em Nuvem

### Configuração AWS Analisada
- **CPUs:** 2
- **Memória:** 1 GiB
- **Rede:** Até 5 Gbps
- **Armazenamento:** 50 GB

### Comparação de Regiões
| Critério | São Paulo (BR) | Virgínia Norte (EUA) | Recomendação |
|----------|----------------|----------------------|--------------|
| **Custo Mensal** | [A ser preenchido] | [A ser preenchido] | [A ser preenchido] |
| **Latência** | Baixa (local) | Alta (internacional) | São Paulo |
| **Conformidade Legal** | ✅ LGPD Compliant | ❌ Restrições | São Paulo |
| **Acesso aos Sensores** | Rápido | Lento | São Paulo |

### 🏆 Recomendação Final
**Região escolhida:** São Paulo (BR)

**Justificativa:**
- Menor latência para acesso aos dados dos sensores
- Conformidade com a LGPD (Lei Geral de Proteção de Dados)
- Armazenamento de dados em território nacional
- [Análise de custo a ser completada]

---

## 🎥 Demonstração

### Vídeo 1: Machine Learning
- **Duração:** Até 5 minutos
- **Conteúdo:** Demonstração do notebook e resultados
- **Link:** [A ser inserido - YouTube não listado]

### Vídeo 2: Análise AWS
- **Duração:** Até 5 minutos  
- **Conteúdo:** Comparação de custos na calculadora AWS
- **Link:** [A ser inserido - YouTube não listado]

---

## 📁 Estrutura do Projeto

```
FarmTech/
├── README.md                           # Este arquivo
├── crop_yield.csv                      # Dataset original
├── farmtech_ml_analysis.ipynb          # Notebook principal (renomear)
└── aws_screenshots/                    # Screenshots da calculadora AWS
    ├── sao_paulo_estimate.png
    └── virginia_estimate.png
```

---

## 🏅 Pontos Fortes

- ✅ Análise exploratória abrangente
- ✅ Aplicação de técnicas não supervisionadas
- ✅ Comparação de múltiplos algoritmos
- ✅ Validação cruzada para robustez
- ✅ Visualizações informativas
- ✅ Análise de viabilidade em nuvem
- ✅ Considerações de conformidade legal

---

## ⚠️ Limitações

- Dataset relativamente pequeno (157 registros)
- Ausência de dados temporais
- Necessidade de validação com dados externos
- Limitação a 4 tipos de culturas

---

## 🔄 Melhorias Futuras

1. **Expansão do Dataset:** Incluir mais registros e culturas
2. **Feature Engineering:** Criar variáveis derivadas
3. **Séries Temporais:** Análise temporal dos dados
4. **Ensemble Methods:** Combinação de modelos
5. **Deploy em Produção:** Implementação da API na AWS

---

## 👥 Equipe

- **Nome:** [SEU_NOME_AQUI]
- **RM:** [SEU_RM_AQUI]
- **Curso:** Inteligência Artificial - FIAP
- **Fase:** 5

---

## 📞 Contato

Para dúvidas ou sugestões sobre este projeto:
- **GitHub:** [link do repositório]
- **Email:** [seu_email@fiap.com.br]

---

*🤖 Projeto desenvolvido como parte do currículo de Inteligência Artificial da FIAP - Fase 5*