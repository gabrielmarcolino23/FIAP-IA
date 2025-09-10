# 📊 Guia de Análise de Custos AWS - FarmTech Solutions

## 🎯 Objetivo
Comparar custos de hospedagem da API de Machine Learning entre as regiões de **São Paulo (BR)** e **Virgínia do Norte (EUA)** usando a Calculadora AWS.

---

## ⚙️ Configuração Especificada

### Requisitos da Máquina
- **CPUs:** 2
- **Memória:** 1 GiB RAM
- **Rede:** Até 5 Gbps
- **Armazenamento:** 50 GB (HD)
- **Tipo:** Linux simples
- **Modelo de Cobrança:** On-Demand 100%

---

## 🌐 Como Acessar a Calculadora AWS

1. **Acesse:** https://calculator.aws/
2. **Idioma:** Pode usar em português ou inglês
3. **Clique em:** "Criar estimativa"

---

## 📋 Passo a Passo Detalhado

### 1. Configuração Básica
1. **Selecione:** Amazon EC2
2. **Região 1:** America do Sul (São Paulo) - sa-east-1
3. **Descrição:** "FarmTech ML API - São Paulo"

### 2. Especificações da Instância
1. **Sistema Operacional:** Linux
2. **Tipo de Instância:** 
   - Procure por instâncias com:
   - 2 vCPUs
   - 1 GiB de memória
   - Sugestão: **t3.nano** ou **t3.micro** (verifique especificações)

### 3. Configurações de Rede
1. **Largura de banda:** Até 5 Gbps
2. **Transferência de dados:** Considere 10 GB/mês (estimativa conservadora)

### 4. Armazenamento
1. **EBS General Purpose SSD (gp3):** 50 GB
2. **IOPS:** Padrão (3,000 IOPS)

### 5. Repetir para Virgínia
1. **Nova estimativa**
2. **Região 2:** US East (N. Virginia) - us-east-1
3. **Mesmas configurações**

---

## 📸 Screenshots Necessários

Salve as seguintes imagens na pasta `aws_screenshots/`:

1. **`sao_paulo_estimate.png`**
   - Estimativa completa para São Paulo
   - Incluindo breakdown de custos

2. **`virginia_estimate.png`**
   - Estimativa completa para Virgínia
   - Incluindo breakdown de custos

3. **`comparison_summary.png`** (opcional)
   - Comparação lado a lado se disponível

---

## 📊 Dados para Coletar

### Para cada região, anote:

#### Custos Mensais:
- [ ] **Instância EC2:** $____/mês
- [ ] **Armazenamento EBS:** $____/mês  
- [ ] **Transferência de dados:** $____/mês
- [ ] **Total:** $____/mês

#### Custos Anuais:
- [ ] **Total anual:** $____/ano

---

## 🏆 Análise de Decisão

### Critérios de Avaliação:

#### 1. **Custo**
- Qual região é mais barata?
- Diferença percentual entre as regiões
- Impacto no orçamento anual

#### 2. **Latência para Sensores**
- **São Paulo:** ✅ Baixa latência (local)
- **Virgínia:** ❌ Alta latência (~150-200ms)

#### 3. **Conformidade Legal (LGPD)**
- **São Paulo:** ✅ Dados permanecem no Brasil
- **Virgínia:** ❌ Dados fora do território nacional

#### 4. **Acesso Rápido aos Dados**
- **São Paulo:** ✅ Acesso direto aos sensores locais
- **Virgínia:** ❌ Dependente de conexão internacional

---

## 📝 Modelo de Justificativa

### Estrutura da Decisão:

```markdown
## Análise Comparativa de Custos AWS

### Resultados da Calculadora:

| Componente | São Paulo (BR) | Virgínia (EUA) | Diferença |
|------------|----------------|----------------|-----------|
| EC2 Instance | $XX.XX/mês | $XX.XX/mês | $XX.XX |
| EBS Storage | $XX.XX/mês | $XX.XX/mês | $XX.XX |
| Data Transfer | $XX.XX/mês | $XX.XX/mês | $XX.XX |
| **TOTAL** | **$XX.XX/mês** | **$XX.XX/mês** | **$XX.XX** |

### Recomendação Final: [São Paulo/Virgínia]

#### Justificativa:
1. **Custo-benefício:** [Explicar o impacto financeiro]
2. **Requisitos técnicos:** [Latência, acesso aos sensores]
3. **Conformidade legal:** [LGPD e armazenamento local]
4. **Escalabilidade futura:** [Considerações de crescimento]

### Fatores Decisivos:
- 🎯 **Latência crítica** para dados de sensores em tempo real
- 📊 **LGPD compliance** exige armazenamento nacional
- 💰 **Diferença de custo** de $XX.XX (X%) justifica/não justifica
- 🔗 **Conectividade local** reduz dependências externas
```

---

## ⚠️ Dicas Importantes

1. **Verificar preços atuais:** Os preços AWS mudam frequentemente
2. **Considerar Reserved Instances:** Para economia a longo prazo
3. **Monitorar custos extras:** NAT Gateway, Load Balancer, etc.
4. **Backup e redundância:** Podem impactar custos
5. **Crescimento futuro:** Considerar escalabilidade

---

## 🎥 Vídeo Demonstrativo

### Roteiro para o Vídeo (5 min):

1. **Introdução (30s):** Explicar objetivo da análise
2. **Calculadora AWS (2min):** Mostrar configuração passo a passo
3. **São Paulo (1min):** Configurar e mostrar custos
4. **Virgínia (1min):** Configurar e mostrar custos  
5. **Comparação (30s):** Lado a lado dos resultados
6. **Justificativa (1min):** Explicar decisão final

### Pontos Importantes no Vídeo:
- Mostrar claramente as configurações
- Explicar cada item de custo
- Destacar diferenças entre regiões
- Justificar escolha considerando fatores técnicos e legais

---

## ✅ Checklist Final

- [ ] Acessei a calculadora AWS
- [ ] Configurei instância para São Paulo  
- [ ] Configurei instância para Virgínia
- [ ] Salvei screenshots de ambas as estimativas
- [ ] Anotei todos os custos detalhados
- [ ] Analisei fatores além do custo
- [ ] Criei justificativa técnica
- [ ] Atualizei o README com os resultados
- [ ] Gravei vídeo demonstrativo
- [ ] Publiquei vídeo como "não listado" no YouTube

---

*💡 Lembre-se: A decisão deve considerar não apenas o custo, mas principalmente os requisitos técnicos e legais do projeto!*