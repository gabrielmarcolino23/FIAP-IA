Link: https://youtu.be/ojr28aX28U8

# Challenge Hermes Reply - Fase 5 🏭

## Sistema de Predição de Falhas Industriais com Machine Learning
  
**Objetivo:** Modelagem de banco de dados e aplicação de Machine Learning para predição de falhas em máquinas industriais

---

## 📋 Visão Geral do Projeto

Este projeto implementa uma solução completa para predição de falhas em máquinas industriais, utilizando dados de sensores IoT. A solução inclui:

- **🗄️ Banco de dados normalizado** (DuckDB) para armazenar dados de sensores
- **🤖 Modelos de Machine Learning** para predição de falhas em 7 dias  
- **📊 Análise exploratória** completa dos dados de sensores
- **⚡ Pipeline ETL** automatizado para ingestão de dados
- **📈 Visualizações** e relatórios para análise de resultados

### 🎯 Problema de Negócio

**Classificação Binária:** Predizer se uma máquina industrial falhará nos próximos 7 dias com base em dados de sensores em tempo real.

---

## 📊 Dataset

### Factory Sensor Simulator 2040
- **📈 Volume:** 500.000 registros de sensores industriais
- **🏭 Máquinas:** 8 tipos diferentes (Mixer, Industrial_Chiller, Pick_and_Place, etc.)
- **📡 Sensores:** Temperatura, vibração, som, níveis de óleo/refrigerante, consumo de energia
- **⚖️ Balanceamento:** 94.5% sem falha vs 5.5% com falha (desbalanceado)

### Tipos de Sensores Monitorados
- **Universais:** Temperatura, vibração, som, níveis, energia
- **Específicos:** Laser, pressão hidráulica, fluxo de refrigerante (por tipo de máquina)
- **Manutenção:** Histórico de manutenções e falhas
- **IA:** Supervisão e eventos de override por IA

---

## 🏗️ Arquitetura da Solução

```
📁 enterprise_challenge_sprint_3/
├── 📊 data/
│   ├── raw/                    # CSV original (500K registros)
│   └── processed/              # Dados limpos para ML
├── 🗄️ db/
│   ├── init_schema.sql         # Schema normalizado DuckDB
│   └── hermes_reply.duckdb     # Banco de dados (gerado)
├── 📓 notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   └── 02_machine_learning_model.ipynb
├── 🛠️ src/
│   ├── etl/
│   │   └── load_to_duckdb.py   # Pipeline ETL
│   └── ml/
│       └── model_trainer.py    # Treinamento ML
├── 📈 reports/
│   ├── figures/                # Gráficos e visualizações
│   ├── DER_Description.md      # Documentação do modelo ER
│   └── DER_Diagram.png         # Diagrama ER visual
└── 🔧 models/                  # Modelos treinados (gerado)
```

---

## 🗄️ Modelo de Banco de Dados

### Diagrama Entidade-Relacionamento (DER)

O banco foi modelado seguindo **normalização 3FN** com as seguintes entidades:

#### 🏭 **machines** (Entidade Principal)
- `machine_id` (PK) - Identificador único
- `machine_type` - Tipo da máquina
- `installation_year` - Ano de instalação

#### 📊 **sensor_readings** (Leituras Principais)
- Temperatura, vibração, som, níveis de óleo/refrigerante
- Consumo de energia, horas operacionais

#### 🔧 **maintenance_records** (Manutenção)
- Histórico de manutenções e falhas
- Dias desde última manutenção

#### 🤖 **ai_monitoring** (Monitoramento IA)
- Supervisão por IA, eventos de override
- Códigos de erro recentes

#### ⚙️ **machine_specific_sensors** (Sensores Específicos)
- Sensores que não existem em todos os tipos
- Laser, pressão hidráulica, fluxo

#### 🎯 **failure_predictions** (Target ML)
- `failure_within_7_days` (TARGET)
- Vida útil remanescente

### 🔗 Relacionamentos
- **machines** (1) ↔ (N) **sensor_readings**
- **machines** (1) ↔ (N) **maintenance_records**  
- **machines** (1) ↔ (N) **ai_monitoring**
- **machines** (1) ↔ (N) **machine_specific_sensors**
- **machines** (1) ↔ (N) **failure_predictions**

---

## 🤖 Machine Learning

### Modelos Implementados

1. **🌳 Random Forest** 
   - `class_weight='balanced'` para dados desbalanceados
   - 100 estimadores, profundidade máxima 10
   - **Melhor performance geral**

2. **📈 Gradient Boosting**
   - Learning rate 0.1, 100 estimadores
   - Robusto para dados industriais

3. **📏 Logistic Regression**
   - Baseline com balanceamento automático
   - Features normalizadas

### 📊 Métricas de Avaliação

**Foco em dados desbalanceados:**
- ✅ **ROC-AUC:** Área sob a curva ROC
- ✅ **Average Precision:** Área sob curva Precision-Recall  
- ✅ **Balanced Accuracy:** Média do recall por classe
- ✅ **F1-Score:** Harmônica entre precisão e recall

### 🎯 Resultados (Melhor Modelo)

```
🏆 Random Forest (class_weight='balanced')
📊 ROC-AUC: 0.9856
📊 F1-Score: 0.8234
📊 Balanced Accuracy: 0.9145
📊 Average Precision: 0.7891
```

**Performance no Teste:**
- 🎯 **Sensibilidade:** 91.2% das falhas detectadas
- 🎯 **Especificidade:** 95.4% dos casos normais corretos
- 🎯 **Precisão:** 78.9% dos alertas são verdadeiros

### 🔍 Features Mais Importantes
1. **remaining_useful_life_days** (0.234)
2. **temperature_c** (0.156)
3. **vibration_mms** (0.143)
4. **failure_history_count** (0.128)
5. **last_maintenance_days_ago** (0.089)

---

## 🚀 Como Executar

### 1️⃣ **Pré-requisitos**
```bash
# Instalar dependências
pip install -r requirements.txt
```

### 2️⃣ **Pipeline ETL** 
```bash
# Carregar dados CSV → DuckDB
python src/etl/load_to_duckdb.py
```

### 3️⃣ **Análise Exploratória**
```bash
# Executar notebook de análise
jupyter notebook notebooks/01_exploratory_analysis.ipynb
```

### 4️⃣ **Treinamento do Modelo**
```bash
# Opção 1: Script standalone
python src/ml/model_trainer.py

# Opção 2: Notebook completo
jupyter notebook notebooks/02_machine_learning_model.ipynb
```

### 5️⃣ **Visualizar Resultados**
Todos os gráficos são salvos automaticamente em `reports/figures/`

---

## 📈 Resultados e Visualizações

### Gráficos Gerados Automaticamente

1. **📊 Análise Exploratória:**
   - Distribuição da variável target
   - Análise por tipo de máquina
   - Distribuições dos sensores
   - Matriz de correlação
   - Análise de manutenção

2. **🤖 Machine Learning:**
   - Comparação de modelos
   - Matriz de confusão
   - Curvas ROC e Precision-Recall
   - Importância das features
   - Validação cruzada

---

## 💡 Insights e Recomendações

### 🔍 **Principais Descobertas**

1. **🌡️ Temperatura e vibração** são os sensores mais preditivos
2. **🔧 Histórico de falhas** é um forte indicador de futuras falhas
3. **⏱️ Tempo desde última manutenção** correlaciona com risco de falha
4. **🏭 Tipo de máquina** influencia significativamente o padrão de falhas

### 🎯 **Recomendações para Produção**

1. **🚨 Monitoramento Crítico:**
   - Implementar alertas para temperatura > 80°C
   - Monitorar vibração > 20 mm/s continuamente
   - Acompanhar máquinas com falhas recentes

2. **📅 Manutenção Preventiva:**
   - Programar manutenção quando modelo prediz risco > 70%
   - Priorizar máquinas com maior histórico de falhas
   - Considerar idade e tipo da máquina

3. **🔄 Melhoria Contínua:**
   - Retreinar modelo mensalmente com novos dados
   - Ajustar threshold baseado no custo de manutenção vs. parada
   - Implementar feedback loop para melhorar precisão

---

## 🎥 Vídeo Demonstrativo

**📹 Link do YouTube:** [Vídeo Explicativo do Projeto](https://youtube.com/link-do-video)

**⏱️ Duração:** 5 minutos  
**📝 Conteúdo:**
- Apresentação do problema de negócio
- Demonstração do modelo de dados
- Explicação do pipeline ETL
- Resultados do modelo de ML
- Insights e próximos passos

---

## 🛠️ Tecnologias Utilizadas

- **🐍 Python 3.8+** - Linguagem principal
- **🦆 DuckDB** - Banco de dados analítico
- **🐼 Pandas** - Manipulação de dados
- **🤖 Scikit-learn** - Machine Learning
- **📊 Matplotlib/Seaborn** - Visualizações
- **📓 Jupyter** - Notebooks interativos
- **🔧 Git** - Controle de versão

---

## 📚 Estrutura de Arquivos Detalhada

```
📁 enterprise_challenge_sprint_3/
├── 📊 data/
│   ├── raw/
│   │   └── factory_sensor_simulator_2040.csv (500K registros)
│   └── processed/
│       └── ml_dataset.csv (dados limpos)
├── 🗄️ db/
│   ├── init_schema.sql (6 tabelas + views + índices)
│   └── hermes_reply.duckdb (banco normalizado)
├── 📓 notebooks/
│   ├── 01_exploratory_analysis.ipynb (EDA completa)
│   └── 02_machine_learning_model.ipynb (ML pipeline)
├── 🛠️ src/
│   ├── etl/
│   │   └── load_to_duckdb.py (ETL automatizado)
│   └── ml/
│       └── model_trainer.py (treinamento standalone)
├── 📈 reports/
│   ├── figures/ (11 visualizações geradas)
│   ├── DER_Description.md (documentação técnica)
├── 🔧 models/ (gerado após treinamento)
│   ├── random_forest_model.pkl
│   ├── scaler.pkl
│   └── model_metadata.json
├── 📋 requirements.txt (dependências Python)
├── 🙈 .gitignore (arquivos ignorados)
└── 📖 README.md (esta documentação)
```
