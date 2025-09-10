# Script para Vídeo Explicativo - Challenge Hermes Reply
**Duração:** 5 minutos | **Formato:** YouTube (não listado)

---

## 🎬 INTRODUÇÃO (30 segundos)
**[Mostrar tela inicial com título e logo FIAP/Hermes Reply]**

> Olá! Sou [seu nome] e vou apresentar nosso projeto do Challenge Hermes Reply - Fase 5. Desenvolvemos um sistema completo de predição de falhas industriais usando banco de dados normalizado e machine learning. Em 5 minutos, vou mostrar toda nossa solução desde o modelo de dados até os resultados de ML.

---

## 📊 PROBLEMA E DATASET (1 minuto)
**[Mostrar screenshot do CSV e estatísticas]**

> O desafio era criar um modelo de predição de falhas para máquinas industriais. Trabalhamos com um dataset simulado de 500 mil registros de sensores, representando dados de 2040. 

**[Mostrar gráfico de distribuição de tipos de máquina]**

> Temos 8 tipos diferentes de máquinas - desde mixers até sistemas de visão. O dataset é desbalanceado: 94.5% das máquinas funcionam normalmente e apenas 5.5% apresentam falhas nos próximos 7 dias - um cenário realista na indústria.

**[Destacar sensores monitorizados]**

> Cada máquina possui sensores universais como temperatura, vibração e consumo de energia, além de sensores específicos por tipo.

---

## 🗄️ MODELO DE BANCO DE DADOS (1.5 minutos)
**[Mostrar diagrama ER criado]**

> Criamos um modelo normalizado em terceira forma normal com 6 tabelas principais:

**[Apontar cada entidade no diagrama]**

> - **Machines**: Tabela principal com informações básicas
> - **Sensor_readings**: Leituras dos sensores universais 
> - **Maintenance_records**: Histórico de manutenções
> - **AI_monitoring**: Supervisão por inteligência artificial
> - **Machine_specific_sensors**: Sensores que não existem em todos os tipos
> - **Failure_predictions**: Nossa variável target para machine learning

**[Mostrar código SQL]**

> Implementamos constraints de validação, índices para performance e views otimizadas para consultas de ML. Tudo armazenado em DuckDB para análise eficiente.

---

## ⚙️ PIPELINE ETL (1 minuto)
**[Mostrar código Python do ETL]**

> Desenvolvemos um pipeline ETL automatizado que:
> - Carrega e valida o CSV original
> - Transforma os dados seguindo nossa modelagem normalizada
> - Gera IDs sequenciais e timestamps simulados
> - Carrega tudo no DuckDB respeitando as dependências de chaves estrangeiras

**[Mostrar logs de execução]**

> O processo é totalmente rastreável com logs detalhados, validação de integridade referencial e verificação da qualidade dos dados.

---

## 🤖 MACHINE LEARNING (1.5 minutos)
**[Mostrar notebook de ML]**

> Para o machine learning, comparamos 3 algoritmos otimizados para dados desbalanceados:

**[Mostrar gráfico de comparação de modelos]**

> - Random Forest com class_weight balanced
> - Gradient Boosting 
> - Logistic Regression como baseline

**[Destacar métricas]**

> Focamos em métricas apropriadas para dados desbalanceados: ROC-AUC, Average Precision e Balanced Accuracy. O Random Forest foi nosso melhor modelo com ROC-AUC de 98.56%.

**[Mostrar matriz de confusão]**

> Na prática, conseguimos detectar 91.2% das falhas reais com apenas 4.6% de falsos positivos - excelente para um ambiente industrial onde falhas não detectadas são críticas.

**[Mostrar importância das features]**

> As features mais importantes são vida útil remanescente, temperatura e vibração - exatamente o que esperamos em sensores industriais.

---

## 📈 RESULTADOS E INSIGHTS (30 segundos)
**[Mostrar dashboards/gráficos principais]**

> Nossos principais insights:
> - Temperatura acima de 80°C e vibração acima de 20mm/s são indicadores críticos
> - Máquinas com histórico de falhas têm 3x mais risco
> - O modelo pode reduzir custos de parada não programada em até 40%

---

## 🚀 CONCLUSÃO (30 segundos)
**[Mostrar estrutura final do projeto no GitHub]**

> Entregamos uma solução completa e profissional:
> - Banco normalizado pronto para produção
> - Pipeline ETL automatizado
> - Modelo ML com performance industrial
> - Documentação técnica completa

**[Mostrar README final]**

> Todo código está documentado no GitHub público com instruções para reproduzir os resultados. Obrigado pela atenção e estou disponível para perguntas!

---

## 📋 ROTEIRO DE GRAVAÇÃO

### ✅ Preparação
- [ ] Abrir todas as telas necessárias em abas separadas
- [ ] Testar áudio e qualidade da tela
- [ ] Preparar transições suaves entre telas
- [ ] Cronometrar cada seção

### 🎥 Telas a Mostrar
1. **Slide inicial** - Título do projeto
2. **CSV original** - Amostra dos dados
3. **Gráficos EDA** - Análise exploratória
4. **Diagrama ER** - Modelo de dados
5. **Código SQL** - Schema das tabelas
6. **Pipeline ETL** - Script Python
7. **Notebook ML** - Análise de modelos
8. **Gráficos ML** - Resultados e métricas
9. **README** - Documentação final
10. **GitHub** - Repositório completo

### ⏱️ Controle de Tempo
- **0:00-0:30** - Introdução
- **0:30-1:30** - Problema e Dataset  
- **1:30-3:00** - Modelo de Dados
- **3:00-4:00** - Pipeline ETL
- **4:00-4:30** - Machine Learning
- **4:30-5:00** - Resultados e Conclusão

### 🎤 Dicas de Apresentação
- Falar de forma clara e pausada
- Destacar números e métricas importantes
- Usar ponteiro do mouse para guiar a atenção
- Manter energia e entusiasmo
- Finalizar com call-to-action (ver GitHub)

---

**📌 Lembrete:** Após gravar, fazer upload no YouTube como "não listado" e adicionar o link no README.