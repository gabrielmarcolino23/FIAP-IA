"""
Pipeline ETL - CSV para DuckDB
Hermes Reply Challenge - Fase 5

Este script carrega os dados do CSV simulado para o banco DuckDB
seguindo o modelo normalizado criado.

Funcionalidades:
- Leitura e validação do CSV de origem
- Transformação e limpeza dos dados
- Carregamento para tabelas normalizadas
- Geração de IDs únicos sequenciais
- Logs detalhados do processo
"""

import pandas as pd
import duckdb
import numpy as np
from pathlib import Path
import logging
from typing import Dict
from datetime import datetime
import sys

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_process.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class SensorDataETL:
    """Classe para gerenciar o processo ETL dos dados de sensores"""
    
    def __init__(self, csv_path: str, db_path: str, schema_path: str):
        """
        Inicializa o processo ETL
        
        Args:
            csv_path: Caminho para o arquivo CSV de origem
            db_path: Caminho para o banco DuckDB
            schema_path: Caminho para o script de schema SQL
        """
        self.csv_path = Path(csv_path)
        self.db_path = Path(db_path)
        self.schema_path = Path(schema_path)
        self.connection = None
        self.df_raw = None
        
    def connect_database(self) -> None:
        """Conecta ao banco DuckDB e cria o schema"""
        try:
            self.connection = duckdb.connect(str(self.db_path))
            logger.info(f"Conectado ao banco DuckDB: {self.db_path}")
            
            # Executar script de schema
            if self.schema_path.exists():
                with open(self.schema_path, 'r', encoding='utf-8') as f:
                    schema_sql = f.read()
                self.connection.execute(schema_sql)
                logger.info("Schema criado com sucesso")
            else:
                logger.warning(f"Arquivo de schema não encontrado: {self.schema_path}")
                
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco: {e}")
            raise
    
    def load_csv_data(self) -> None:
        """Carrega e valida os dados do CSV"""
        try:
            logger.info(f"Carregando dados do CSV: {self.csv_path}")
            self.df_raw = pd.read_csv(self.csv_path)
            
            logger.info(f"Dados carregados: {self.df_raw.shape[0]:,} registros, {self.df_raw.shape[1]} colunas")
            logger.info(f"Memória utilizada: {self.df_raw.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            # Validações básicas
            self._validate_data()
            
        except Exception as e:
            logger.error(f"Erro ao carregar CSV: {e}")
            raise
    
    def _validate_data(self) -> None:
        """Valida a qualidade dos dados carregados"""
        logger.info("Validando qualidade dos dados...")
        
        # Verificar colunas obrigatórias
        required_columns = [
            'Machine_ID', 'Machine_Type', 'Installation_Year',
            'Temperature_C', 'Vibration_mms', 'Sound_dB',
            'Failure_Within_7_Days', 'Remaining_Useful_Life_days'
        ]
        
        missing_columns = [col for col in required_columns if col not in self.df_raw.columns]
        if missing_columns:
            raise ValueError(f"Colunas obrigatórias ausentes: {missing_columns}")
        
        # Verificar valores ausentes em colunas críticas
        critical_nulls = self.df_raw[required_columns].isnull().sum()
        if critical_nulls.sum() > 0:
            logger.warning(f"Valores ausentes encontrados: \\n{critical_nulls[critical_nulls > 0]}")
        
        # Verificar duplicatas
        duplicates = self.df_raw.duplicated().sum()
        if duplicates > 0:
            logger.warning(f"Encontradas {duplicates:,} linhas duplicadas")
            
        logger.info("Validação concluída")
    
    def transform_data(self) -> Dict[str, pd.DataFrame]:
        """Transforma os dados para o modelo normalizado"""
        logger.info("Iniciando transformação dos dados...")
        
        # Preparar dados limpos
        df = self.df_raw.copy()
        
        # Converter tipos de dados
        df['AI_Supervision'] = df['AI_Supervision'].astype(bool)
        df['Failure_Within_7_Days'] = df['Failure_Within_7_Days'].astype(bool)
        
        # Gerar timestamps simulados (distribuídos ao longo do ano)
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 12, 31)
        date_range = pd.date_range(start_date, end_date, periods=len(df))
        np.random.shuffle(date_range.values)  # Embaralhar para simular dados reais
        
        # 1. Tabela machines
        machines_df = df[['Machine_ID', 'Machine_Type', 'Installation_Year']].drop_duplicates()
        machines_df['created_at'] = start_date
        machines_df.columns = ['machine_id', 'machine_type', 'installation_year', 'created_at']
        
        # 2. Tabela sensor_readings
        sensor_readings_df = df[[
            'Machine_ID', 'Operational_Hours', 'Temperature_C', 'Vibration_mms',
            'Sound_dB', 'Oil_Level_pct', 'Coolant_Level_pct', 'Power_Consumption_kW'
        ]].copy()
        sensor_readings_df['reading_id'] = range(1, len(sensor_readings_df) + 1)
        sensor_readings_df['reading_timestamp'] = date_range
        sensor_readings_df.columns = [
            'machine_id', 'operational_hours', 'temperature_c', 'vibration_mms',
            'sound_db', 'oil_level_pct', 'coolant_level_pct', 'power_consumption_kw',
            'reading_id', 'reading_timestamp'
        ]
        sensor_readings_df = sensor_readings_df[[
            'reading_id', 'machine_id', 'operational_hours', 'temperature_c',
            'vibration_mms', 'sound_db', 'oil_level_pct', 'coolant_level_pct',
            'power_consumption_kw', 'reading_timestamp'
        ]]
        
        # 3. Tabela maintenance_records
        maintenance_df = df[[
            'Machine_ID', 'Last_Maintenance_Days_Ago', 'Maintenance_History_Count',
            'Failure_History_Count'
        ]].copy()
        maintenance_df['maintenance_id'] = range(1, len(maintenance_df) + 1)
        maintenance_df['recorded_at'] = date_range
        maintenance_df.columns = [
            'machine_id', 'last_maintenance_days_ago', 'maintenance_history_count',
            'failure_history_count', 'maintenance_id', 'recorded_at'
        ]
        maintenance_df = maintenance_df[[
            'maintenance_id', 'machine_id', 'last_maintenance_days_ago',
            'maintenance_history_count', 'failure_history_count', 'recorded_at'
        ]]
        
        # 4. Tabela ai_monitoring
        ai_monitoring_df = df[[
            'Machine_ID', 'AI_Supervision', 'AI_Override_Events',
            'Error_Codes_Last_30_Days'
        ]].copy()
        ai_monitoring_df['ai_record_id'] = range(1, len(ai_monitoring_df) + 1)
        ai_monitoring_df['monitored_at'] = date_range
        ai_monitoring_df.columns = [
            'machine_id', 'ai_supervision', 'ai_override_events',
            'error_codes_last_30_days', 'ai_record_id', 'monitored_at'
        ]
        ai_monitoring_df = ai_monitoring_df[[
            'ai_record_id', 'machine_id', 'ai_supervision', 'ai_override_events',
            'error_codes_last_30_days', 'monitored_at'
        ]]
        
        # 5. Tabela machine_specific_sensors
        specific_sensors_df = df[[
            'Machine_ID', 'Laser_Intensity', 'Hydraulic_Pressure_bar',
            'Coolant_Flow_L_min', 'Heat_Index'
        ]].copy()
        specific_sensors_df['specific_sensor_id'] = range(1, len(specific_sensors_df) + 1)
        specific_sensors_df['measured_at'] = date_range
        
        # Substituir valores vazios por None
        for col in ['Laser_Intensity', 'Hydraulic_Pressure_bar', 'Coolant_Flow_L_min', 'Heat_Index']:
            specific_sensors_df[col] = specific_sensors_df[col].replace('', None)
            specific_sensors_df[col] = pd.to_numeric(specific_sensors_df[col], errors='coerce')
        
        specific_sensors_df.columns = [
            'machine_id', 'laser_intensity', 'hydraulic_pressure_bar',
            'coolant_flow_l_min', 'heat_index', 'specific_sensor_id', 'measured_at'
        ]
        specific_sensors_df = specific_sensors_df[[
            'specific_sensor_id', 'machine_id', 'laser_intensity',
            'hydraulic_pressure_bar', 'coolant_flow_l_min', 'heat_index', 'measured_at'
        ]]
        
        # 6. Tabela failure_predictions
        failure_predictions_df = df[[
            'Machine_ID', 'Remaining_Useful_Life_days', 'Failure_Within_7_Days'
        ]].copy()
        failure_predictions_df['prediction_id'] = range(1, len(failure_predictions_df) + 1)
        failure_predictions_df['predicted_at'] = date_range
        failure_predictions_df.columns = [
            'machine_id', 'remaining_useful_life_days', 'failure_within_7_days',
            'prediction_id', 'predicted_at'
        ]
        failure_predictions_df = failure_predictions_df[[
            'prediction_id', 'machine_id', 'remaining_useful_life_days',
            'failure_within_7_days', 'predicted_at'
        ]]
        
        transformed_tables = {
            'machines': machines_df,
            'sensor_readings': sensor_readings_df,
            'maintenance_records': maintenance_df,
            'ai_monitoring': ai_monitoring_df,
            'machine_specific_sensors': specific_sensors_df,
            'failure_predictions': failure_predictions_df
        }
        
        # Log da transformação
        for table_name, table_df in transformed_tables.items():
            logger.info(f"Tabela {table_name}: {len(table_df):,} registros")
        
        return transformed_tables
    
    def load_to_database(self, tables: Dict[str, pd.DataFrame]) -> None:
        """Carrega os dados transformados para o banco"""
        logger.info("Carregando dados para o banco DuckDB...")
        
        # Ordem de inserção (respeitando dependências FK)
        load_order = [
            'machines', 'sensor_readings', 'maintenance_records',
            'ai_monitoring', 'machine_specific_sensors', 'failure_predictions'
        ]
        
        try:
            for table_name in load_order:
                if table_name in tables:
                    df = tables[table_name]
                    
                    # Inserir dados usando DuckDB
                    self.connection.execute(f"DELETE FROM {table_name}")  # Limpar tabela
                    self.connection.register(f'{table_name}_temp', df)
                    
                    columns = ', '.join(df.columns)
                    placeholders = ', '.join([f'{table_name}_temp.{col}' for col in df.columns])
                    
                    insert_sql = f"""
                    INSERT INTO {table_name} ({columns})
                    SELECT {placeholders} FROM {table_name}_temp
                    """
                    
                    self.connection.execute(insert_sql)
                    self.connection.unregister(f'{table_name}_temp')
                    
                    # Verificar inserção
                    count = self.connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
                    logger.info(f"✓ {table_name}: {count:,} registros inseridos")
                
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            raise
    
    def validate_loaded_data(self) -> None:
        """Valida os dados carregados no banco"""
        logger.info("Validando dados carregados...")
        
        try:
            # Verificar contagens
            tables = ['machines', 'sensor_readings', 'maintenance_records', 
                     'ai_monitoring', 'machine_specific_sensors', 'failure_predictions']
            
            for table in tables:
                count = self.connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                logger.info(f"{table}: {count:,} registros")
            
            # Verificar integridade referencial
            fk_check_sql = """
            SELECT 
                (SELECT COUNT(*) FROM sensor_readings sr 
                 LEFT JOIN machines m ON sr.machine_id = m.machine_id 
                 WHERE m.machine_id IS NULL) as orphan_sensor_readings,
                 
                (SELECT COUNT(*) FROM failure_predictions fp 
                 LEFT JOIN machines m ON fp.machine_id = m.machine_id 
                 WHERE m.machine_id IS NULL) as orphan_predictions
            """
            
            result = self.connection.execute(fk_check_sql).fetchone()
            if result[0] == 0 and result[1] == 0:
                logger.info("✓ Integridade referencial validada")
            else:
                logger.warning(f"Registros órfãos encontrados: {result}")
            
            # Verificar distribuição de falhas
            failure_dist = self.connection.execute("""
                SELECT failure_within_7_days, COUNT(*) as count
                FROM failure_predictions 
                GROUP BY failure_within_7_days
            """).fetchall()
            
            logger.info("Distribuição de falhas:")
            for failure, count in failure_dist:
                percentage = (count / sum([x[1] for x in failure_dist])) * 100
                logger.info(f"  {failure}: {count:,} ({percentage:.2f}%)")
            
        except Exception as e:
            logger.error(f"Erro na validação: {e}")
            raise
    
    def close_connection(self) -> None:
        """Fecha a conexão com o banco"""
        if self.connection:
            self.connection.close()
            logger.info("Conexão com banco fechada")
    
    def run_etl_pipeline(self) -> None:
        """Executa o pipeline completo de ETL"""
        try:
            logger.info("=== INICIANDO PIPELINE ETL ===")
            start_time = datetime.now()
            
            # Passo 1: Conectar ao banco
            self.connect_database()
            
            # Passo 2: Carregar CSV
            self.load_csv_data()
            
            # Passo 3: Transformar dados
            transformed_tables = self.transform_data()
            
            # Passo 4: Carregar no banco
            self.load_to_database(transformed_tables)
            
            # Passo 5: Validar dados
            self.validate_loaded_data()
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info("=== PIPELINE ETL CONCLUÍDO ===")
            logger.info(f"Tempo total: {duration}")
            logger.info(f"Banco DuckDB criado: {self.db_path}")
            
        except Exception as e:
            logger.error(f"Falha no pipeline ETL: {e}")
            raise
        finally:
            self.close_connection()

def main():
    """Função principal para executar o ETL"""
    
    # Caminhos dos arquivos
    project_root = Path(__file__).parent.parent.parent
    csv_path = project_root / "data/raw/factory_sensor_simulator_2040.csv"
    db_path = project_root / "db/hermes_reply.duckdb"
    schema_path = project_root / "db/init_schema.sql"
    
    # Verificar se o arquivo CSV existe
    if not csv_path.exists():
        logger.error(f"Arquivo CSV não encontrado: {csv_path}")
        return
    
    # Criar diretório do banco se não existir
    db_path.parent.mkdir(exist_ok=True)
    
    # Executar ETL
    etl = SensorDataETL(
        csv_path=str(csv_path),
        db_path=str(db_path),
        schema_path=str(schema_path)
    )
    
    etl.run_etl_pipeline()

if __name__ == "__main__":
    main()