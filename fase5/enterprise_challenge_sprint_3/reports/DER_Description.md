# Diagrama Entidade-Relacionamento (DER) - Sistema de Monitoramento Industrial

## Visão Geral
Este modelo de dados foi projetado para armazenar informações de sensores industriais com foco em predição de falhas, seguindo princípios de normalização para garantir integridade referencial e eficiência.

## Entidades e Relacionamentos

### 1. **machines** (Tabela Principal)
**Descrição:** Representa as máquinas industriais do sistema
- `machine_id` (PK) - VARCHAR(50) - Identificador único da máquina
- `machine_type` - VARCHAR(50) - Tipo da máquina (Mixer, Industrial_Chiller, etc.)
- `installation_year` - INTEGER - Ano de instalação
- `created_at` - TIMESTAMP - Data de criação do registro

**Justificativa:** Centraliza informações básicas das máquinas, permitindo rastreabilidade e categorização.

### 2. **sensor_readings** (Leituras dos Sensores)
**Descrição:** Armazena leituras principais dos sensores de cada máquina
- `reading_id` (PK) - BIGINT IDENTITY - Chave primária sequencial
- `machine_id` (FK) - VARCHAR(50) - Referência à máquina
- `operational_hours` - DOUBLE - Horas operacionais da máquina
- `temperature_c` - DOUBLE - Temperatura em Celsius
- `vibration_mms` - DOUBLE - Vibração em mm/s
- `sound_db` - DOUBLE - Nível de som em decibéis
- `oil_level_pct` - DOUBLE - Nível de óleo em percentual
- `coolant_level_pct` - DOUBLE - Nível de refrigerante em percentual
- `power_consumption_kw` - DOUBLE - Consumo de energia em kW
- `reading_timestamp` - TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Justificativa:** Concentra sensores universais presentes em todas as máquinas.

### 3. **maintenance_records** (Histórico de Manutenção)
**Descrição:** Registra informações sobre manutenção das máquinas
- `maintenance_id` (PK) - BIGINT IDENTITY
- `machine_id` (FK) - VARCHAR(50)
- `last_maintenance_days_ago` - INTEGER - Dias desde última manutenção
- `maintenance_history_count` - INTEGER - Número total de manutenções
- `failure_history_count` - INTEGER - Número total de falhas
- `recorded_at` - TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Justificativa:** Separação de responsabilidades, facilitando consultas sobre histórico de manutenção.

### 4. **ai_monitoring** (Monitoramento por IA)
**Descrição:** Dados relacionados à supervisão por inteligência artificial
- `ai_record_id` (PK) - BIGINT IDENTITY
- `machine_id` (FK) - VARCHAR(50)
- `ai_supervision` - BOOLEAN - Se a máquina está sob supervisão de IA
- `ai_override_events` - INTEGER - Número de eventos de override da IA
- `error_codes_last_30_days` - INTEGER - Códigos de erro nos últimos 30 dias
- `monitored_at` - TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Justificativa:** Isolamento de funcionalidades específicas de IA, permitindo evolução independente.

### 5. **machine_specific_sensors** (Sensores Específicos)
**Descrição:** Sensores que não estão presentes em todos os tipos de máquinas
- `specific_sensor_id` (PK) - BIGINT IDENTITY
- `machine_id` (FK) - VARCHAR(50)
- `laser_intensity` - DOUBLE - Intensidade do laser (nullable)
- `hydraulic_pressure_bar` - DOUBLE - Pressão hidráulica em bar (nullable)
- `coolant_flow_l_min` - DOUBLE - Fluxo de refrigerante em L/min (nullable)
- `heat_index` - DOUBLE - Índice de calor (nullable)
- `measured_at` - TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Justificativa:** Evita campos NULL desnecessários na tabela principal, mantendo flexibilidade para diferentes tipos de máquinas.

### 6. **failure_predictions** (Predições de Falha)
**Descrição:** Labels e predições para machine learning
- `prediction_id` (PK) - BIGINT IDENTITY
- `machine_id` (FK) - VARCHAR(50)
- `remaining_useful_life_days` - DOUBLE - Vida útil remanescente em dias
- `failure_within_7_days` - BOOLEAN - Falha prevista em 7 dias (TARGET ML)
- `predicted_at` - TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Justificativa:** Separação clara entre dados operacionais e targets/labels para ML.

## Cardinalidades e Relacionamentos

1. **machines** 1:N **sensor_readings**
   - Uma máquina pode ter múltiplas leituras de sensores ao longo do tempo

2. **machines** 1:N **maintenance_records**
   - Uma máquina pode ter múltiplos registros de manutenção

3. **machines** 1:N **ai_monitoring**
   - Uma máquina pode ter múltiplos registros de monitoramento IA

4. **machines** 1:N **machine_specific_sensors**
   - Uma máquina pode ter múltiplas leituras de sensores específicos

5. **machines** 1:N **failure_predictions**
   - Uma máquina pode ter múltiplas predições de falha ao longo do tempo

## Constraints e Validações

### Check Constraints:
- `oil_level_pct BETWEEN 0 AND 100`
- `coolant_level_pct BETWEEN 0 AND 100`
- `temperature_c > -273.15` (acima do zero absoluto)
- `vibration_mms >= 0`
- `sound_db >= 0`
- `power_consumption_kw >= 0`
- `installation_year BETWEEN 1990 AND 2050`
- `operational_hours >= 0`

### Foreign Key Constraints:
- Todas as tabelas filhas referenciam `machines.machine_id`
- `ON DELETE CASCADE` para manter integridade referencial

## Índices Sugeridos

### Índices de Performance:
- `idx_sensor_readings_machine_timestamp` - Para consultas por máquina e período
- `idx_failure_predictions_machine_target` - Para consultas ML
- `idx_maintenance_machine_date` - Para análise de manutenção
- `idx_machine_type` - Para análise por tipo de máquina

## Vantagens do Modelo

1. **Normalização:** Elimina redundância e garante consistência
2. **Escalabilidade:** Permite adição de novos sensores sem reestruturação
3. **Performance:** Índices otimizados para consultas ML e analíticas
4. **Flexibilidade:** Suporta diferentes tipos de máquinas e sensores
5. **Integridade:** Constraints garantem qualidade dos dados
6. **Auditabilidade:** Timestamps em todas as tabelas

## Integração com ML

O modelo facilita:
- **Feature Engineering:** Joins eficientes entre tabelas relacionadas
- **Time Series Analysis:** Dados temporais organizados cronologicamente
- **Target Variable:** `failure_within_7_days` claramente identificada
- **Data Quality:** Constraints garantem dados válidos para treinamento