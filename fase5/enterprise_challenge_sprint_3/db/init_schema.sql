-- ============================================================================
-- Schema de Inicialização - Sistema de Monitoramento Industrial
-- Hermes Reply Challenge - Fase 5
-- ============================================================================
-- 
-- Este script cria o schema normalizado para armazenar dados de sensores
-- industriais com foco em predição de falhas usando DuckDB
-- 
-- Características:
-- - Normalização em 3FN para eliminar redundância
-- - Constraints de integridade referencial
-- - Índices otimizados para consultas ML
-- - Suporte a diferentes tipos de máquinas
-- ============================================================================

-- Limpar schema existente (se necessário)
-- Remover views primeiro (dependem das tabelas)
DROP VIEW IF EXISTS vw_failure_timeline;
DROP VIEW IF EXISTS vw_machine_status;
DROP VIEW IF EXISTS vw_ml_dataset;

-- Remover tabelas (ordem inversa para respeitar foreign keys)
DROP TABLE IF EXISTS failure_predictions;
DROP TABLE IF EXISTS machine_specific_sensors;
DROP TABLE IF EXISTS ai_monitoring;
DROP TABLE IF EXISTS maintenance_records;
DROP TABLE IF EXISTS sensor_readings;
DROP TABLE IF EXISTS machines;

-- ============================================================================
-- 1. TABELA PRINCIPAL: machines
-- ============================================================================
-- Armazena informações básicas das máquinas industriais
CREATE TABLE machines (
    machine_id VARCHAR(50) PRIMARY KEY,                    -- ID único da máquina
    machine_type VARCHAR(50) NOT NULL,                     -- Tipo (Mixer, Chiller, etc.)
    installation_year INTEGER NOT NULL,                    -- Ano de instalação
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,        -- Timestamp de criação
    
    -- Constraints de validação
    CONSTRAINT chk_installation_year 
        CHECK (installation_year BETWEEN 1990 AND 2050)
);

-- ============================================================================
-- 2. LEITURAS DOS SENSORES PRINCIPAIS
-- ============================================================================
-- Armazena dados dos sensores universais presentes em todas as máquinas
CREATE TABLE sensor_readings (
    reading_id BIGINT PRIMARY KEY,                         -- Chave primária sequencial
    machine_id VARCHAR(50) NOT NULL,                       -- Referência à máquina
    operational_hours DOUBLE NOT NULL,                     -- Horas operacionais
    temperature_c DOUBLE NOT NULL,                         -- Temperatura em Celsius
    vibration_mms DOUBLE NOT NULL,                         -- Vibração em mm/s
    sound_db DOUBLE NOT NULL,                              -- Nível de som em dB
    oil_level_pct DOUBLE NOT NULL,                         -- Nível de óleo em %
    coolant_level_pct DOUBLE NOT NULL,                     -- Nível de refrigerante em %
    power_consumption_kw DOUBLE NOT NULL,                  -- Consumo de energia em kW
    reading_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp da leitura
    
    -- Constraints de validação básicas
    CONSTRAINT chk_operational_hours CHECK (operational_hours >= 0),
    CONSTRAINT chk_oil_level CHECK (oil_level_pct BETWEEN 0 AND 100),
    CONSTRAINT chk_coolant_level CHECK (coolant_level_pct BETWEEN 0 AND 100),
    
    -- Chave estrangeira
    CONSTRAINT fk_sensor_readings_machine 
        FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
);

-- ============================================================================
-- 3. HISTÓRICO DE MANUTENÇÃO
-- ============================================================================
-- Armazena informações sobre manutenção e histórico de falhas
CREATE TABLE maintenance_records (
    maintenance_id BIGINT PRIMARY KEY,                     -- Chave primária
    machine_id VARCHAR(50) NOT NULL,                       -- Referência à máquina
    last_maintenance_days_ago INTEGER NOT NULL,            -- Dias desde última manutenção
    maintenance_history_count INTEGER NOT NULL,            -- Total de manutenções
    failure_history_count INTEGER NOT NULL,                -- Total de falhas
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,       -- Timestamp do registro
    
    -- Constraints de validação
    CONSTRAINT chk_maintenance_days CHECK (last_maintenance_days_ago >= 0),
    CONSTRAINT chk_maintenance_count CHECK (maintenance_history_count >= 0),
    CONSTRAINT chk_failure_count CHECK (failure_history_count >= 0),
    
    -- Chave estrangeira
    CONSTRAINT fk_maintenance_records_machine 
        FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
);

-- ============================================================================
-- 4. MONITORAMENTO POR INTELIGÊNCIA ARTIFICIAL
-- ============================================================================
-- Dados relacionados à supervisão por IA e eventos de sistema
CREATE TABLE ai_monitoring (
    ai_record_id BIGINT PRIMARY KEY,                       -- Chave primária
    machine_id VARCHAR(50) NOT NULL,                       -- Referência à máquina
    ai_supervision BOOLEAN NOT NULL,                       -- Supervisão IA ativa
    ai_override_events INTEGER NOT NULL,                   -- Eventos de override
    error_codes_last_30_days INTEGER NOT NULL,             -- Erros nos últimos 30 dias
    monitored_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,      -- Timestamp do monitoramento
    
    -- Constraints de validação
    CONSTRAINT chk_override_events CHECK (ai_override_events >= 0),
    CONSTRAINT chk_error_codes CHECK (error_codes_last_30_days >= 0),
    
    -- Chave estrangeira
    CONSTRAINT fk_ai_monitoring_machine 
        FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
);

-- ============================================================================
-- 5. SENSORES ESPECÍFICOS POR TIPO DE MÁQUINA
-- ============================================================================
-- Sensores que não estão presentes em todos os tipos de máquinas
CREATE TABLE machine_specific_sensors (
    specific_sensor_id BIGINT PRIMARY KEY,                 -- Chave primária
    machine_id VARCHAR(50) NOT NULL,                       -- Referência à máquina
    laser_intensity DOUBLE,                                -- Intensidade laser (nullable)
    hydraulic_pressure_bar DOUBLE,                         -- Pressão hidráulica (nullable)
    coolant_flow_l_min DOUBLE,                             -- Fluxo refrigerante (nullable)
    heat_index DOUBLE,                                      -- Índice de calor (nullable)
    measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,       -- Timestamp da medição
    
    -- Sem constraints restritivos para permitir dados simulados realistas
    
    -- Chave estrangeira
    CONSTRAINT fk_specific_sensors_machine 
        FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
);

-- ============================================================================
-- 6. PREDIÇÕES DE FALHA (TARGET PARA MACHINE LEARNING)
-- ============================================================================
-- Labels e predições para modelos de machine learning
CREATE TABLE failure_predictions (
    prediction_id BIGINT PRIMARY KEY,                      -- Chave primária
    machine_id VARCHAR(50) NOT NULL,                       -- Referência à máquina
    remaining_useful_life_days DOUBLE NOT NULL,            -- Vida útil remanescente
    failure_within_7_days BOOLEAN NOT NULL,                -- TARGET: Falha em 7 dias
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,      -- Timestamp da predição
    
    -- Constraint básica apenas
    CONSTRAINT chk_remaining_life CHECK (remaining_useful_life_days >= 0),
    
    -- Chave estrangeira
    CONSTRAINT fk_failure_predictions_machine 
        FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
);

-- ============================================================================
-- CRIAÇÃO DE ÍNDICES PARA PERFORMANCE
-- ============================================================================

-- Índices para consultas por máquina e timestamp (time series)
CREATE INDEX idx_sensor_readings_machine_timestamp 
    ON sensor_readings(machine_id, reading_timestamp);

CREATE INDEX idx_maintenance_records_machine_date 
    ON maintenance_records(machine_id, recorded_at);

CREATE INDEX idx_ai_monitoring_machine_date 
    ON ai_monitoring(machine_id, monitored_at);

CREATE INDEX idx_specific_sensors_machine_date 
    ON machine_specific_sensors(machine_id, measured_at);

-- Índices para consultas ML
CREATE INDEX idx_failure_predictions_machine_target 
    ON failure_predictions(machine_id, failure_within_7_days);

CREATE INDEX idx_failure_predictions_date 
    ON failure_predictions(predicted_at);

-- Índice para análise por tipo de máquina
CREATE INDEX idx_machines_type 
    ON machines(machine_type);

-- Índices para sensores mais utilizados em análises
CREATE INDEX idx_sensor_readings_temperature 
    ON sensor_readings(temperature_c);

CREATE INDEX idx_sensor_readings_vibration 
    ON sensor_readings(vibration_mms);

CREATE INDEX idx_sensor_readings_power 
    ON sensor_readings(power_consumption_kw);

-- ============================================================================
-- VIEWS ÚTEIS PARA ANÁLISE E ML
-- ============================================================================

-- View completa para análise de machine learning
CREATE VIEW vw_ml_dataset AS
SELECT 
    m.machine_id,
    m.machine_type,
    m.installation_year,
    sr.operational_hours,
    sr.temperature_c,
    sr.vibration_mms,
    sr.sound_db,
    sr.oil_level_pct,
    sr.coolant_level_pct,
    sr.power_consumption_kw,
    mr.last_maintenance_days_ago,
    mr.maintenance_history_count,
    mr.failure_history_count,
    ai.ai_supervision,
    ai.ai_override_events,
    ai.error_codes_last_30_days,
    fp.remaining_useful_life_days,
    fp.failure_within_7_days,
    sr.reading_timestamp
FROM machines m
JOIN sensor_readings sr ON m.machine_id = sr.machine_id
JOIN maintenance_records mr ON m.machine_id = mr.machine_id
JOIN ai_monitoring ai ON m.machine_id = ai.machine_id
JOIN failure_predictions fp ON m.machine_id = fp.machine_id;

-- View para análise de status atual das máquinas
CREATE VIEW vw_machine_status AS
SELECT 
    m.machine_id,
    m.machine_type,
    m.installation_year,
    sr.operational_hours,
    sr.temperature_c,
    sr.vibration_mms,
    sr.power_consumption_kw,
    mr.last_maintenance_days_ago,
    ai.ai_supervision,
    fp.failure_within_7_days,
    sr.reading_timestamp as last_reading
FROM machines m
LEFT JOIN sensor_readings sr ON m.machine_id = sr.machine_id
LEFT JOIN maintenance_records mr ON m.machine_id = mr.machine_id  
LEFT JOIN ai_monitoring ai ON m.machine_id = ai.machine_id
LEFT JOIN failure_predictions fp ON m.machine_id = fp.machine_id;

-- View para análise temporal de falhas
CREATE VIEW vw_failure_timeline AS
SELECT 
    fp.machine_id,
    m.machine_type,
    fp.failure_within_7_days,
    fp.remaining_useful_life_days,
    fp.predicted_at,
    ROW_NUMBER() OVER (PARTITION BY fp.machine_id ORDER BY fp.predicted_at DESC) as recency_rank
FROM failure_predictions fp
JOIN machines m ON fp.machine_id = m.machine_id;

-- ============================================================================
-- COMENTÁRIOS FINAIS
-- ============================================================================

/*
SCHEMA SUMMARY:
===============

Tabelas Criadas:
1. machines (1) -> sensor_readings (N)
2. machines (1) -> maintenance_records (N)  
3. machines (1) -> ai_monitoring (N)
4. machines (1) -> machine_specific_sensors (N)
5. machines (1) -> failure_predictions (N)

Features:
- Normalização 3FN
- Constraints de integridade
- Índices otimizados
- Views para ML e análise
- Suporte a timestamps para auditoria
- Flexibilidade para diferentes tipos de máquinas

Next Steps:
1. Executar script ETL para carregar dados
2. Verificar integridade dos dados
3. Testar views e consultas
4. Executar análise ML
*/