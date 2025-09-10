# 🎥 Guia para Vídeos Demonstrativos - FarmTech Solutions

## 📋 Visão Geral

Você precisa criar **2 vídeos de até 5 minutos cada**, demonstrando:
1. **Vídeo 1:** Funcionamento do notebook de Machine Learning
2. **Vídeo 2:** Comparação de custos na calculadora AWS

**Configuração YouTube:** "Não listado" (unlisted)

---

## 🎬 VÍDEO 1: Machine Learning Demonstration

### ⏱️ Duração: Até 5 minutos

### 📝 Roteiro Detalhado:

#### **Introdução (30 segundos)**
- "Olá! Sou [SEU_NOME], RM [SEU_RM]"
- "Hoje vou demonstrar nossa solução de ML para a FarmTech Solutions"
- "Analisamos dados de culturas agrícolas para prever rendimento de safras"

#### **Dataset e Análise Exploratória (1 minuto)**
- Abrir o notebook Jupyter
- Mostrar o carregamento dos dados (crop_yield.csv)
- Destacar: "157 registros, 4 tipos de culturas"
- Mostrar rapidamente gráficos de distribuição
- Comentar: "Identificamos correlações entre temperatura e rendimento"

#### **Machine Learning Não Supervisionado (1 minuto)**
- Mostrar resultado da clusterização
- "Encontramos X clusters que agrupam condições similares"
- Mostrar visualização dos clusters
- "Detectamos Y outliers - cenários discrepantes"
- Mostrar gráfico de outliers

#### **Modelos Preditivos (2 minutos)**
- "Testamos 5 algoritmos diferentes"
- Mostrar tabela de comparação dos modelos
- "O melhor modelo foi [NOME] com R² de [VALOR]"
- Mostrar gráfico de predições vs valores reais
- "Este modelo permite prever rendimento com precisão de X%"

#### **Conclusão (30 segundos)**
- "A solução permite otimizar cultivos e detectar anomalias"
- "Próximos passos: deploy na AWS para uso em produção"
- "Obrigado!"

### 🎯 Pontos Importantes:
- **Mostrar código executado** (não só código estático)
- **Destacar visualizações** mais importantes
- **Explicar resultados** de forma clara
- **Mencionar aplicação prática** na agricultura

---

## 🎬 VÍDEO 2: AWS Cost Analysis

### ⏱️ Duração: Até 5 minutos

### 📝 Roteiro Detalhado:

#### **Introdução (30 segundos)**
- "Agora vou demonstrar nossa análise de custos AWS"
- "Comparamos hosting entre São Paulo e Virgínia"
- "Para uma API que processa dados de sensores agrícolas"

#### **Especificações Técnicas (30 segundos)**
- "Precisamos de: 2 CPUs, 1 GiB RAM, 5 Gbps rede, 50 GB storage"
- "Máquina Linux simples, modelo On-Demand"

#### **Calculadora AWS - São Paulo (1.5 minutos)**
- Abrir calculator.aws
- "Primeiro, região América do Sul - São Paulo"
- Configurar passo a passo:
  - Selecionar EC2
  - Escolher instância (t3.nano/micro)
  - Configurar storage (50 GB EBS)
  - Mostrar cálculo final
- "Custo mensal: $X.XX"

#### **Calculadora AWS - Virgínia (1.5 minutos)**
- "Agora, mesma configuração para Virgínia"
- Repetir processo
- "Custo mensal: $X.XX"
- "Diferença de $X.XX por mês"

#### **Análise e Decisão Final (1 minuto)**
- "Mas custo não é o único fator!"
- **Latência:** "Sensores no Brasil - São Paulo tem latência menor"
- **LGPD:** "Lei brasileira exige dados no território nacional"
- **Decisão:** "Escolhemos São Paulo apesar de [mais caro/mais barato]"
- "Prioridade: conformidade legal e performance técnica"

#### **Conclusão (30 segundos)**
- "Solução técnica e financeiramente viável"
- "Próximo passo: implementação da arquitetura"

### 🎯 Pontos Importantes:
- **Mostrar calculadora funcionando** (não só screenshots)
- **Explicar cada configuração** que você faz
- **Destacar diferenças de preço** claramente
- **Justificar decisão** com argumentos técnicos e legais

---

## 🛠️ Ferramentas de Gravação

### Opções Gratuitas:
1. **OBS Studio** (Recomendado)
   - Gratuito e profissional
   - Controle total da qualidade
   
2. **Loom** (Web-based)
   - Fácil de usar
   - Upload direto para nuvem
   
3. **Windows Game Bar** (Windows 10/11)
   - Win + G para abrir
   - Gravação simples

4. **QuickTime** (Mac)
   - Gravação de tela nativa

### Configurações Recomendadas:
- **Resolução:** 1080p (1920x1080)
- **Frame Rate:** 30 fps
- **Áudio:** Certifique-se que está claro
- **Tamanho:** Máximo 25 GB por vídeo (limite YouTube)

---

## 📤 Upload no YouTube

### Passo a Passo:
1. **Login** no YouTube Studio
2. **Criar** → **Enviar vídeos**
3. **Arrastar arquivos** ou selecionar
4. **Título sugerido:**
   - Vídeo 1: "FarmTech ML Analysis - [SEU_NOME] - FIAP IA Fase 5"
   - Vídeo 2: "FarmTech AWS Cost Analysis - [SEU_NOME] - FIAP IA Fase 5"
5. **Descrição:**
```
Demonstração do projeto FarmTech Solutions - Análise de Machine Learning para rendimento de safras agrícolas.

Desenvolvido para FIAP - Curso de Inteligência Artificial - Fase 5
Autor: [SEU_NOME] - RM [SEU_RM]

GitHub: [LINK_DO_SEU_REPOSITÓRIO]
```
6. **Visibilidade:** ⚠️ **NÃO LISTADO** (Unlisted)
7. **Publicar**

### ⚠️ IMPORTANTE:
- **NUNCA coloque como "Público"**
- **Use "Não listado"** para que só quem tem o link acesse
- **Copie os links** e adicione no README

---

## 📋 Checklist de Qualidade

### Antes de Gravar:
- [ ] Notebook funcionando completamente
- [ ] Calculadora AWS aberta e testada
- [ ] Roteiro revisado
- [ ] Ambiente silencioso
- [ ] Tela limpa (feche outras abas)

### Durante a Gravação:
- [ ] Falar claramente e devagar
- [ ] Mostrar cursor na tela
- [ ] Não correr nos cliques
- [ ] Explicar cada ação
- [ ] Respeitar tempo limite (5 min)

### Após a Gravação:
- [ ] Assistir vídeo completo
- [ ] Verificar áudio e vídeo
- [ ] Confirmar que todos os pontos foram cobertos
- [ ] Upload como "Não listado"
- [ ] Copiar links para README
- [ ] Testar links funcionando

---

## 🎯 Dicas para um Bom Vídeo

### ✅ Faça:
- **Pratique** antes de gravar
- **Fale naturalmente** como se explicasse para um colega
- **Destaque** os resultados mais importantes
- **Use zoom** quando necessário para mostrar detalhes
- **Pause** brevemente entre seções

### ❌ Evite:
- Falar muito rápido
- Pular etapas importantes  
- Ficar em silêncio por muito tempo
- Erros de navegação (practice first!)
- Ultrapassar 5 minutos

---

## 📎 Links Úteis

- **Calculadora AWS:** https://calculator.aws/
- **YouTube Studio:** https://studio.youtube.com/
- **OBS Studio:** https://obsproject.com/
- **Loom:** https://www.loom.com/

---

## 📞 Suporte

Se tiver dificuldades:
1. **Teste** as ferramentas antes da gravação final
2. **Pratique** o roteiro algumas vezes
3. **Grave** em sessões menores se necessário
4. **Não tenha pressa** - qualidade é importante

---

*🎬 Lembre-se: Os vídeos são uma demonstração do seu trabalho técnico. Mostre confiança e conhecimento do que desenvolveu!*