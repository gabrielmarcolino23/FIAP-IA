#!/usr/bin/env python3
"""
Script standalone para treinamento do modelo ML
Hermes Reply Challenge - Fase 5

Este script permite executar o treinamento e avaliação do modelo
diretamente via linha de comando, independente do Jupyter.
"""

import pandas as pd
import numpy as np
import duckdb
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import joblib
import json
from datetime import datetime
import argparse
import sys
import logging

# Machine Learning imports
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, 
    roc_curve, precision_recall_curve, average_precision_score,
    balanced_accuracy_score, f1_score
)

# Configuração
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
np.random.seed(42)

class IndustrialFailurePrediction:
    """Classe para predição de falhas industriais"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.db_path = project_root / 'db/hermes_reply.duckdb'
        self.reports_path = project_root / 'reports/figures'
        self.models_path = project_root / 'models'
        
        # Criar diretórios necessários
        self.reports_path.mkdir(parents=True, exist_ok=True)
        self.models_path.mkdir(parents=True, exist_ok=True)
        
        # Configurar matplotlib
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.style.use('default')
        
    def load_data(self) -> pd.DataFrame:
        """Carrega dados do DuckDB ou CSV"""
        
        if self.db_path.exists():
            logger.info(f"Carregando dados do DuckDB: {self.db_path}")
            conn = duckdb.connect(str(self.db_path))
            
            query = """
            SELECT 
                machine_id, machine_type, installation_year, operational_hours,
                temperature_c, vibration_mms, sound_db, oil_level_pct,
                coolant_level_pct, power_consumption_kw, last_maintenance_days_ago,
                maintenance_history_count, failure_history_count, ai_supervision,
                ai_override_events, error_codes_last_30_days,
                remaining_useful_life_days, failure_within_7_days
            FROM vw_ml_dataset
            ORDER BY machine_id
            """
            
            df = conn.execute(query).df()
            conn.close()
            
        else:
            # Fallback para CSV
            csv_path = self.project_root / 'data/raw/factory_sensor_simulator_2040.csv'
            logger.info(f"DuckDB não encontrado. Carregando CSV: {csv_path}")
            df = pd.read_csv(csv_path)
            
            # Renomear colunas para padronizar
            column_mapping = {
                'Machine_ID': 'machine_id',
                'Machine_Type': 'machine_type',
                'Installation_Year': 'installation_year',
                'Operational_Hours': 'operational_hours',
                'Temperature_C': 'temperature_c',
                'Vibration_mms': 'vibration_mms',
                'Sound_dB': 'sound_db',
                'Oil_Level_pct': 'oil_level_pct',
                'Coolant_Level_pct': 'coolant_level_pct',
                'Power_Consumption_kW': 'power_consumption_kw',
                'Last_Maintenance_Days_Ago': 'last_maintenance_days_ago',
                'Maintenance_History_Count': 'maintenance_history_count',
                'Failure_History_Count': 'failure_history_count',
                'AI_Supervision': 'ai_supervision',
                'AI_Override_Events': 'ai_override_events',
                'Error_Codes_Last_30_Days': 'error_codes_last_30_days',
                'Remaining_Useful_Life_days': 'remaining_useful_life_days',
                'Failure_Within_7_Days': 'failure_within_7_days'
            }
            df = df.rename(columns=column_mapping)
        
        logger.info(f"Dados carregados: {df.shape[0]:,} registros, {df.shape[1]} colunas")
        return df
    
    def prepare_features(self, df: pd.DataFrame) -> tuple:
        """Prepara features para modelagem (SEM DATA LEAKAGE)"""
        
        numeric_features = [
            'installation_year',              # Idade da máquina (OK)
            'temperature_c',                  # Sensor físico (OK)
            'vibration_mms',                  # Sensor físico (OK) 
            'sound_db',                       # Sensor físico (OK)
            'oil_level_pct',                  # Sensor físico (OK)
            'coolant_level_pct',              # Sensor físico (OK)
            'power_consumption_kw',           # Sensor físico (OK)
            'last_maintenance_days_ago',      # Histórico real (OK)
            'maintenance_history_count',      # Histórico real (OK)
            'failure_history_count',          # Histórico real (OK)
            'ai_override_events',             # Eventos operacionais (OK)
            'error_codes_last_30_days'        # Erros recentes (OK)
        ]
        
        # Preparar features
        X = df[numeric_features + ['machine_type', 'ai_supervision']].copy()
        
        # Encoder para machine_type
        le_machine_type = LabelEncoder()
        X['machine_type_encoded'] = le_machine_type.fit_transform(X['machine_type'])
        X = X.drop('machine_type', axis=1)
        
        # Converter boolean para int
        X['ai_supervision'] = X['ai_supervision'].astype(int)
        
        # Target
        y = df['failure_within_7_days'].astype(int)
        
        logger.info(f"Features preparadas: {X.shape[1]} colunas")
        logger.info(f"Target balanceamento: {y.mean()*100:.2f}% positivos")
        
        return X, y, le_machine_type
    
    def train_models(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """Treina e avalia modelos com validação mais rigorosa"""
        
        # Split estratificado (mantendo proporção de classes)
        # Usando test_size maior para validação mais robusta
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.4, random_state=42, stratify=y
        )
        
        logger.info(f"Split treino/teste: {len(X_train):,} / {len(X_test):,}")
        logger.info(f"Proporção falhas - Treino: {y_train.mean()*100:.2f}% | Teste: {y_test.mean()*100:.2f}%")
        
        # Normalização
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Modelos com hiperparâmetros mais conservadores (anti-overfitting)
        models = {
            'Random Forest': RandomForestClassifier(
                n_estimators=50,              # Reduzido para evitar overfitting
                class_weight='balanced',      # Importante para dados desbalanceados
                max_depth=5,                  # Reduzido para regularização
                min_samples_split=50,         # Aumentado para evitar overfitting
                min_samples_leaf=20,          # Adicionado para regularização
                max_features='sqrt',          # Reduzir correlação entre árvores
                random_state=42, 
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=50,              # Reduzido
                learning_rate=0.05,           # Reduzido (mais conservador)
                max_depth=3,                  # Reduzido para regularização
                min_samples_split=50,         # Aumentado
                min_samples_leaf=20,          # Adicionado
                subsample=0.8,                # Adicionado para regularização
                random_state=42
            ),
            'Logistic Regression': LogisticRegression(
                class_weight='balanced',      # Balanceamento de classes
                max_iter=2000,                # Aumentado para convergência
                C=0.1,                        # Regularização forte
                random_state=42
            )
        }
        
        results = {}
        
        for name, model in models.items():
            logger.info(f"Treinando {name}...")
            
            # Escolher dados corretos
            if 'Logistic' in name:
                X_tr, X_te = X_train_scaled, X_test_scaled
            else:
                X_tr, X_te = X_train.values, X_test.values
            
            # Treinar
            model.fit(X_tr, y_train)
            
            # Predições
            y_pred = model.predict(X_te)
            y_pred_proba = model.predict_proba(X_te)[:, 1]
            
            # Métricas
            metrics = {
                'balanced_accuracy': balanced_accuracy_score(y_test, y_pred),
                'f1_score': f1_score(y_test, y_pred),
                'roc_auc': roc_auc_score(y_test, y_pred_proba),
                'average_precision': average_precision_score(y_test, y_pred_proba)
            }
            
            results[name] = {
                'model': model,
                'metrics': metrics,
                'predictions': y_pred,
                'probabilities': y_pred_proba,
                'test_data': (X_te, y_test)
            }
            
            logger.info(f"{name} - ROC-AUC: {metrics['roc_auc']:.4f}")
        
        # Salvar objetos de preprocessing
        joblib.dump(scaler, self.models_path / 'scaler.pkl')
        
        return results, (X_train, X_test, y_train, y_test), scaler
    
    def select_best_model(self, results: dict) -> tuple:
        """Seleciona o melhor modelo baseado no ROC-AUC"""
        
        best_name = max(results.keys(), 
                       key=lambda x: results[x]['metrics']['roc_auc'])
        best_model = results[best_name]['model']
        best_metrics = results[best_name]['metrics']
        
        logger.info(f"Melhor modelo: {best_name}")
        logger.info(f"ROC-AUC: {best_metrics['roc_auc']:.4f}")
        
        return best_name, best_model, best_metrics
    
    def create_visualizations(self, results: dict, best_name: str) -> None:
        """Cria visualizações dos resultados"""
        
        # 1. Comparação de modelos
        metrics_df = pd.DataFrame({
            name: res['metrics'] for name, res in results.items()
        }).T
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        metrics_list = ['balanced_accuracy', 'f1_score', 'roc_auc', 'average_precision']
        colors = ['skyblue', 'lightcoral', 'lightgreen']
        
        for i, metric in enumerate(metrics_list):
            ax = axes[i//2, i%2]
            bars = metrics_df[metric].plot(kind='bar', ax=ax, color=colors)
            ax.set_title(f'{metric.replace("_", " ").title()}')
            ax.set_ylabel('Score')
            ax.tick_params(axis='x', rotation=45)
            ax.set_ylim(0, 1)
            
            for j, v in enumerate(metrics_df[metric]):
                ax.text(j, v + 0.01, f'{v:.3f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(self.reports_path / 'model_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Matriz de confusão do melhor modelo
        best_preds = results[best_name]['predictions']
        _, y_test = results[best_name]['test_data']
        
        cm = confusion_matrix(y_test, best_preds)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=['Sem Falha', 'Com Falha'],
                    yticklabels=['Sem Falha', 'Com Falha'])
        plt.title(f'Matriz de Confusão - {best_name}')
        plt.xlabel('Predito')
        plt.ylabel('Real')
        plt.tight_layout()
        plt.savefig(self.reports_path / 'confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Curvas ROC e PR
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        colors = ['blue', 'red', 'green']
        
        for i, (name, res) in enumerate(results.items()):
            _, y_test = res['test_data']
            y_proba = res['probabilities']
            
            # ROC
            fpr, tpr, _ = roc_curve(y_test, y_proba)
            auc_score = res['metrics']['roc_auc']
            ax1.plot(fpr, tpr, color=colors[i], lw=2, 
                     label=f'{name} (AUC = {auc_score:.3f})')
            
            # PR
            precision, recall, _ = precision_recall_curve(y_test, y_proba)
            ap_score = res['metrics']['average_precision']
            ax2.plot(recall, precision, color=colors[i], lw=2,
                     label=f'{name} (AP = {ap_score:.3f})')
        
        # Configurar ROC
        ax1.plot([0, 1], [0, 1], 'k--', lw=1, alpha=0.8)
        ax1.set_xlim([0.0, 1.0])
        ax1.set_ylim([0.0, 1.05])
        ax1.set_xlabel('Taxa de Falsos Positivos')
        ax1.set_ylabel('Taxa de Verdadeiros Positivos')
        ax1.set_title('Curvas ROC')
        ax1.legend(loc="lower right")
        ax1.grid(True, alpha=0.3)
        
        # Configurar PR
        baseline = y_test.mean()
        ax2.axhline(y=baseline, color='k', linestyle='--', alpha=0.8)
        ax2.set_xlim([0.0, 1.0])
        ax2.set_ylim([0.0, 1.05])
        ax2.set_xlabel('Recall')
        ax2.set_ylabel('Precision')
        ax2.set_title('Curvas Precision-Recall')
        ax2.legend(loc="lower left")
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.reports_path / 'roc_pr_curves.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Visualizações salvas em: {self.reports_path}")
    
    def save_model_and_results(self, best_name: str, best_model, 
                              best_metrics: dict, feature_names: list) -> None:
        """Salva o modelo e resultados"""
        
        # Salvar modelo
        model_filename = f'{best_name.lower().replace(" ", "_")}_model.pkl'
        joblib.dump(best_model, self.models_path / model_filename)
        
        # Salvar metadados
        metadata = {
            'model_name': best_name,
            'model_file': model_filename,
            'metrics': best_metrics,
            'feature_names': feature_names,
            'training_date': datetime.now().isoformat(),
            'model_version': '1.0.0'
        }
        
        with open(self.models_path / 'model_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Modelo salvo: {self.models_path / model_filename}")
        logger.info(f"Metadados salvos: {self.models_path / 'model_metadata.json'}")
    
    def run_training_pipeline(self) -> None:
        """Pipeline completo de treinamento"""
        
        logger.info("=== INICIANDO TREINAMENTO DE MODELO ML ===")
        start_time = datetime.now()
        
        # 1. Carregar dados
        df = self.load_data()
        
        # 2. Preparar features
        X, y, label_encoder = self.prepare_features(df)
        
        # 3. Treinar modelos
        results, splits, scaler = self.train_models(X, y)
        
        # 4. Selecionar melhor modelo
        best_name, best_model, best_metrics = self.select_best_model(results)
        
        # 5. Criar visualizações
        self.create_visualizations(results, best_name)
        
        # 6. Salvar modelo e resultados
        self.save_model_and_results(best_name, best_model, best_metrics, list(X.columns))
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        logger.info("=== TREINAMENTO CONCLUÍDO ===")
        logger.info(f"Tempo total: {duration}")
        logger.info(f"Melhor modelo: {best_name} (ROC-AUC: {best_metrics['roc_auc']:.4f})")

def main():
    parser = argparse.ArgumentParser(description='Treinar modelo de predição de falhas')
    parser.add_argument('--project-root', type=str, default='.',
                       help='Caminho raiz do projeto')
    
    args = parser.parse_args()
    
    project_root = Path(args.project_root)
    if not project_root.exists():
        logger.error(f"Diretório não encontrado: {project_root}")
        sys.exit(1)
    
    # Executar treinamento
    trainer = IndustrialFailurePrediction(project_root)
    trainer.run_training_pipeline()

if __name__ == "__main__":
    main()