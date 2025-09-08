#!/usr/bin/env python3
"""
Análise Comparativa - Diferentes Abordagens para Predição de Falhas
Usando apenas bibliotecas do scikit-learn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Machine Learning imports - apenas scikit-learn
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, 
    roc_curve, precision_recall_curve, average_precision_score,
    balanced_accuracy_score, f1_score
)

# Configurações
plt.rcParams['figure.figsize'] = (12, 8)
sns.set_style("whitegrid")
np.random.seed(42)

# Caminhos
PROJECT_ROOT = Path('./')
DB_PATH = PROJECT_ROOT / 'db/hermes_reply.duckdb'
REPORTS_PATH = PROJECT_ROOT / 'reports/figures'
REPORTS_PATH.mkdir(parents=True, exist_ok=True)

print("📚 Bibliotecas carregadas com sucesso!")
print(f"📁 Diretório de relatórios: {REPORTS_PATH}")
print("🚀 Usando HistGradientBoostingClassifier (equivalente ao LightGBM)!")

def load_data_from_db(db_path):
    """Carrega dados do DuckDB"""
    import duckdb
    
    conn = duckdb.connect(str(db_path))
    
    query = """
    SELECT 
        machine_id, machine_type, installation_year, operational_hours,
        temperature_c, vibration_mms, sound_db, oil_level_pct, coolant_level_pct,
        power_consumption_kw, last_maintenance_days_ago, maintenance_history_count,
        failure_history_count, ai_supervision, ai_override_events,
        error_codes_last_30_days, remaining_useful_life_days, failure_within_7_days
    FROM vw_ml_dataset
    ORDER BY machine_id
    """
    
    df = conn.execute(query).df()
    conn.close()
    
    print(f"📊 Dados carregados: {df.shape[0]:,} registros, {df.shape[1]} features")
    return df

def simulate_data():
    """Simula dados para demonstração"""
    print("📊 Simulando dados para demonstração...")
    np.random.seed(42)
    n_samples = 50000
    
    df = pd.DataFrame({
        'installation_year': np.random.randint(2015, 2024, n_samples),
        'temperature_c': np.random.normal(60, 15, n_samples),
        'vibration_mms': np.random.normal(10, 5, n_samples),
        'sound_db': np.random.normal(75, 10, n_samples),
        'oil_level_pct': np.random.uniform(0, 100, n_samples),
        'coolant_level_pct': np.random.uniform(0, 100, n_samples),
        'power_consumption_kw': np.random.normal(150, 80, n_samples),
        'last_maintenance_days_ago': np.random.randint(0, 365, n_samples),
        'maintenance_history_count': np.random.randint(0, 10, n_samples),
        'failure_history_count': np.random.randint(0, 5, n_samples),
        'ai_override_events': np.random.randint(0, 5, n_samples),
        'error_codes_last_30_days': np.random.randint(0, 10, n_samples),
        'ai_supervision': np.random.choice([0, 1], n_samples),
        'machine_type': np.random.choice(['Type_A', 'Type_B', 'Type_C', 'Type_D'], n_samples),
        'operational_hours': np.random.uniform(0, 100000, n_samples),
        'remaining_useful_life_days': np.random.uniform(0, 1000, n_samples)
    })
    
    # Target correlacionado com algumas features para simular padrões realistas
    failure_prob = ((df['temperature_c'] > 75).astype(int) * 0.15 + 
                    (df['vibration_mms'] > 15).astype(int) * 0.15 +
                    (df['oil_level_pct'] < 30).astype(int) * 0.2 +
                    (df['failure_history_count'] > 2).astype(int) * 0.25 +
                    (df['error_codes_last_30_days'] > 5).astype(int) * 0.15)
    
    df['failure_within_7_days'] = np.random.binomial(1, failure_prob * 0.3)
    
    return df

def analyze_data_leakage(df, target_col='failure_within_7_days'):
    """Analisa correlações suspeitas"""
    
    print("\n🔍 ANÁLISE DE DATA LEAKAGE")
    print("=" * 40)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if target_col in numeric_cols:
        numeric_cols.remove(target_col)
    
    target = df[target_col].astype(int)
    
    correlations = []
    for col in numeric_cols:
        if df[col].notna().sum() > 0:
            corr = df[col].corr(target)
            if not pd.isna(corr):
                correlations.append({'feature': col, 'correlation': abs(corr)})
    
    correlations_df = pd.DataFrame(correlations).sort_values('correlation', ascending=False)
    
    print("\n🚨 TOP 10 CORRELAÇÕES:")
    print(correlations_df.head(10).to_string())
    
    high_corr = correlations_df[correlations_df['correlation'] > 0.8]
    if len(high_corr) > 0:
        print(f"\n⚠️ {len(high_corr)} features com correlação > 0.8 (suspeitas):")
        print(high_corr.to_string())
    else:
        print("\n✅ Nenhuma correlação suspeita > 0.8 encontrada")
    
    return correlations_df

def prepare_external_approach(df):
    """Abordagem do notebook externo"""
    print("\n🔴 ABORDAGEM EXTERNA - Feature Engineering Agressivo")
    
    df_ext = df.copy()
    
    # Incluir operational_hours (potencial data leakage)
    features = [
        'installation_year', 'operational_hours', 'temperature_c', 'vibration_mms',
        'sound_db', 'oil_level_pct', 'coolant_level_pct', 'power_consumption_kw',
        'last_maintenance_days_ago', 'maintenance_history_count', 'failure_history_count',
        'ai_override_events', 'error_codes_last_30_days', 'ai_supervision'
    ]
    
    X_ext = df_ext[[col for col in features if col in df_ext.columns]].copy()
    y_ext = df_ext['failure_within_7_days']
    
    # One-hot encoding para machine_type
    if 'machine_type' in df_ext.columns:
        machine_dummies = pd.get_dummies(df_ext['machine_type'], prefix='machine')
        X_ext = pd.concat([X_ext, machine_dummies], axis=1)
    
    print(f"   Features: {X_ext.shape[1]}, Samples: {X_ext.shape[0]:,}")
    return X_ext, y_ext

def prepare_our_approach(df):
    """Nossa abordagem conservadora"""
    print("\n🔵 NOSSA ABORDAGEM - Conservadora (sem data leakage)")
    
    # Features seguras (removido operational_hours)
    safe_features = [
        'installation_year', 'temperature_c', 'vibration_mms',
        'sound_db', 'oil_level_pct', 'coolant_level_pct', 'power_consumption_kw',
        'last_maintenance_days_ago', 'maintenance_history_count', 'failure_history_count',
        'ai_override_events', 'error_codes_last_30_days', 'ai_supervision'
    ]
    
    X_our = df[[col for col in safe_features if col in df.columns]].copy()
    y_our = df['failure_within_7_days']
    
    # Label encoding para machine_type
    if 'machine_type' in df.columns:
        le = LabelEncoder()
        X_our['machine_type_encoded'] = le.fit_transform(df['machine_type'])
    
    print(f"   Features: {X_our.shape[1]}, Samples: {X_our.shape[0]:,}")
    return X_our, y_our

def prepare_hybrid_approach(df):
    """Abordagem híbrida otimizada"""
    print("\n🟢 ABORDAGEM HÍBRIDA - Balanceada")
    
    # Features base seguras
    base_features = [
        'installation_year', 'temperature_c', 'vibration_mms',
        'sound_db', 'oil_level_pct', 'coolant_level_pct', 'power_consumption_kw',
        'last_maintenance_days_ago', 'maintenance_history_count', 'failure_history_count',
        'ai_override_events', 'error_codes_last_30_days', 'ai_supervision'
    ]
    
    X_hybrid = df[[col for col in base_features if col in df.columns]].copy()
    
    # Feature engineering inteligente (com tratamento de infinitos)
    if 'temperature_c' in X_hybrid.columns and 'vibration_mms' in X_hybrid.columns:
        X_hybrid['temp_vibration_ratio'] = X_hybrid['temperature_c'] / (X_hybrid['vibration_mms'].abs() + 1)
    
    if 'oil_level_pct' in X_hybrid.columns and 'coolant_level_pct' in X_hybrid.columns:
        X_hybrid['fluid_levels_avg'] = (X_hybrid['oil_level_pct'] + X_hybrid['coolant_level_pct']) / 2
    
    if 'maintenance_history_count' in X_hybrid.columns and 'last_maintenance_days_ago' in X_hybrid.columns:
        X_hybrid['maintenance_efficiency'] = X_hybrid['maintenance_history_count'] / (X_hybrid['last_maintenance_days_ago'].abs() + 1)
    
    # Tratar valores infinitos e NaN
    X_hybrid = X_hybrid.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    # One-hot encoding para machine_type
    if 'machine_type' in df.columns:
        machine_dummies = pd.get_dummies(df['machine_type'], prefix='machine', drop_first=True)
        X_hybrid = pd.concat([X_hybrid, machine_dummies], axis=1)
    
    y_hybrid = df['failure_within_7_days']
    
    print(f"   Features: {X_hybrid.shape[1]}, Samples: {X_hybrid.shape[0]:,}")
    print("   Features criadas: temp_vibration_ratio, fluid_levels_avg, maintenance_efficiency")
    return X_hybrid, y_hybrid

def train_and_evaluate_models(X, y, approach_name, test_size=0.3):
    """Treina e avalia múltiplos modelos"""
    
    print(f"\n🚀 TREINANDO MODELOS - {approach_name}")
    print("=" * 50)
    
    # Split dos dados
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    print(f"   Treino: {X_train.shape[0]:,}, Teste: {X_test.shape[0]:,}")
    print(f"   Target distribution: {y_train.value_counts(normalize=True).to_dict()}")
    
    # Normalização
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Modelos a testar
    models = {
        'HistGradientBoosting': HistGradientBoostingClassifier(
            max_depth=6, max_iter=100, learning_rate=0.1, random_state=42
        ),
        'Random Forest': RandomForestClassifier(
            n_estimators=100, max_depth=10, class_weight='balanced', 
            random_state=42, n_jobs=-1
        ),
        'Logistic Regression': LogisticRegression(
            class_weight='balanced', max_iter=1000, random_state=42
        )
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\n📊 {name}:")
        
        # Usar dados normalizados para LR
        if 'Logistic' in name:
            X_tr, X_te = X_train_scaled, X_test_scaled
        else:
            X_tr, X_te = X_train, X_test
        
        # Treinar
        model.fit(X_tr, y_train)
        
        # Predições
        y_pred = model.predict(X_te)
        y_pred_proba = model.predict_proba(X_te)[:, 1]
        
        # Métricas
        metrics = {
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'f1_score': f1_score(y_test, y_pred),
            'balanced_accuracy': balanced_accuracy_score(y_test, y_pred),
            'average_precision': average_precision_score(y_test, y_pred_proba)
        }
        
        results[f"{approach_name} - {name}"] = metrics
        
        print(f"   ROC-AUC: {metrics['roc_auc']:.4f}")
        print(f"   F1-Score: {metrics['f1_score']:.4f}")
        print(f"   Balanced Accuracy: {metrics['balanced_accuracy']:.4f}")
        print(f"   Average Precision: {metrics['average_precision']:.4f}")
        
        # Matriz de confusão básica
        cm = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = cm.ravel()
        print(f"   Confusion Matrix: TN={tn}, FP={fp}, FN={fn}, TP={tp}")
    
    return results

def create_comparison_visualization(comparison_df, save_path):
    """Cria visualização da comparação"""
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    metrics_to_plot = ['roc_auc', 'f1_score', 'balanced_accuracy', 'average_precision']
    
    for i, metric in enumerate(metrics_to_plot):
        ax = axes[i//2, i%2]
        
        # Cores por abordagem
        colors = []
        for idx in comparison_df.index:
            if 'External' in idx:
                colors.append('red')
            elif 'Our' in idx:
                colors.append('blue')
            else:
                colors.append('green')
        
        bars = ax.bar(range(len(comparison_df)), comparison_df[metric], color=colors)
        ax.set_title(f'{metric.replace("_", " ").title()}', fontweight='bold', fontsize=12)
        ax.set_ylabel('Score')
        ax.set_xticks(range(len(comparison_df)))
        ax.set_xticklabels([name.replace(' - ', '\n') for name in comparison_df.index], 
                          rotation=45, ha='right', fontsize=9)
        ax.grid(axis='y', alpha=0.3)
        
        # Valores nas barras
        for bar, value in zip(bars, comparison_df[metric]):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                   f'{value:.3f}', ha='center', va='bottom', fontsize=8)
    
    # Legenda personalizada
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', label='External Notebook'),
        Patch(facecolor='blue', label='Our Approach'),
        Patch(facecolor='green', label='Hybrid Approach')
    ]
    fig.legend(handles=legend_elements, loc='upper center', 
               bbox_to_anchor=(0.5, 0.95), ncol=3, fontsize=12)
    
    plt.suptitle('Comparative Analysis Results', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    print(f"📊 Visualização salva em: {save_path}")

def main():
    """Função principal"""
    
    print("🎯 ANÁLISE COMPARATIVA - PREDIÇÃO DE FALHAS INDUSTRIAIS")
    print("=" * 60)
    
    # Carregar dados
    try:
        if DB_PATH.exists():
            df_raw = load_data_from_db(DB_PATH)
        else:
            df_raw = simulate_data()
    except Exception as e:
        print(f"⚠️ Erro ao carregar dados: {e}")
        df_raw = simulate_data()
    
    print(f"\n🎯 Target distribution: {df_raw['failure_within_7_days'].value_counts(normalize=True).to_dict()}")
    
    # Análise de data leakage
    correlation_analysis = analyze_data_leakage(df_raw)
    
    # Preparar todas as abordagens
    print("\n" + "=" * 60)
    print("PREPARAÇÃO DAS TRÊS ABORDAGENS")
    print("=" * 60)
    
    X_external, y_external = prepare_external_approach(df_raw)
    X_our, y_our = prepare_our_approach(df_raw)
    X_hybrid, y_hybrid = prepare_hybrid_approach(df_raw)
    
    # Treinar todos os modelos
    print("\n" + "=" * 60)
    print("TREINAMENTO E AVALIAÇÃO")
    print("=" * 60)
    
    all_results = {}
    
    results_ext = train_and_evaluate_models(X_external, y_external, "External", test_size=0.2)
    results_our = train_and_evaluate_models(X_our, y_our, "Our", test_size=0.4)
    results_hyb = train_and_evaluate_models(X_hybrid, y_hybrid, "Hybrid", test_size=0.3)
    
    all_results.update(results_ext)
    all_results.update(results_our)
    all_results.update(results_hyb)
    
    # Análise final
    print("\n" + "=" * 60)
    print("RESULTADOS FINAIS")
    print("=" * 60)
    
    # Criar DataFrame de comparação
    comparison_df = pd.DataFrame(all_results).T
    comparison_df = comparison_df.round(4)
    
    print("\n🏆 RANKING FINAL POR ROC-AUC:")
    ranking = comparison_df.sort_values('roc_auc', ascending=False)
    print(ranking.to_string())
    
    # Melhor modelo
    best_model = ranking.index[0]
    best_metrics = ranking.iloc[0]
    
    print(f"\n🥇 MELHOR MODELO: {best_model}")
    print(f"   ROC-AUC: {best_metrics['roc_auc']:.4f}")
    print(f"   F1-Score: {best_metrics['f1_score']:.4f}")
    print(f"   Balanced Accuracy: {best_metrics['balanced_accuracy']:.4f}")
    print(f"   Average Precision: {best_metrics['average_precision']:.4f}")
    
    # Análise por abordagem
    print("\n📊 ANÁLISE POR ABORDAGEM:")
    external_avg = comparison_df[comparison_df.index.str.contains('External')]['roc_auc'].mean()
    our_avg = comparison_df[comparison_df.index.str.contains('Our')]['roc_auc'].mean()
    hybrid_avg = comparison_df[comparison_df.index.str.contains('Hybrid')]['roc_auc'].mean()
    
    print(f"🔴 External: {external_avg:.4f} (média ROC-AUC)")
    print(f"🔵 Our: {our_avg:.4f} (média ROC-AUC)")
    print(f"🟢 Hybrid: {hybrid_avg:.4f} (média ROC-AUC)")
    
    # Determinar melhor abordagem
    approach_scores = {'External': external_avg, 'Our': our_avg, 'Hybrid': hybrid_avg}
    best_approach = max(approach_scores, key=approach_scores.get)
    
    print(f"\n🎖️ MELHOR ABORDAGEM: {best_approach} (ROC-AUC médio: {approach_scores[best_approach]:.4f})")
    
    # Visualização
    create_comparison_visualization(comparison_df, REPORTS_PATH / 'comparative_analysis_results.png')
    
    # Conclusões
    print("\n" + "=" * 60)
    print("🎯 CONCLUSÕES E RECOMENDAÇÕES")
    print("=" * 60)
    
    print(f"\n🏆 MELHOR MODELO GERAL: {best_model}")
    print(f"Performance: ROC-AUC = {best_metrics['roc_auc']:.4f}")
    
    print("\n💡 INSIGHTS:")
    if hybrid_avg > max(external_avg, our_avg):
        print("   ✅ Abordagem híbrida oferece melhor equilíbrio")
        print("   • Combina feature engineering inteligente com validação rigorosa")
        print("   • Features engineered melhoram performance sem data leakage")
    elif external_avg > our_avg:
        print("   📈 Notebook externo supera nossa abordagem conservadora")
        print("   • Feature engineering mais agressivo pode ser benéfico")
        print("   • Mas cuidado com possível data leakage (operational_hours)")
        print(f"   • Diferença de performance: {external_avg - our_avg:.4f}")
    else:
        print("   🛡️ Abordagem conservadora mantém-se competitiva")
        print("   • Validação rigorosa garante resultados confiáveis")
    
    print("\n🚀 RECOMENDAÇÕES:")
    if best_metrics['roc_auc'] > 0.75:
        print("   ✅ Performance BOA para ambiente industrial")
        status = "PRONTO PARA PILOTO"
    elif best_metrics['roc_auc'] > 0.65:
        print("   🟡 Performance MODERADA - necessita otimizações")
        status = "NECESSITA MELHORIAS"
    else:
        print("   ❌ Performance BAIXA - revisar completamente")
        status = "REVISAR ABORDAGEM"
    
    print(f"   Status: {status}")
    print("   • Implementar modelo híbrido com monitoramento contínuo")
    print("   • Otimizar threshold baseado em custos de negócio")
    print("   • Coletar mais dados e features relevantes")
    print("   • Validação temporal quando possível")
    
    # Salvar resumo
    summary = f"""
RESUMO ANÁLISE COMPARATIVA - PREDIÇÃO DE FALHAS INDUSTRIAIS
=========================================================

MELHOR MODELO: {best_model}
ROC-AUC: {best_metrics['roc_auc']:.4f}
F1-Score: {best_metrics['f1_score']:.4f}
Balanced Accuracy: {best_metrics['balanced_accuracy']:.4f}
Average Precision: {best_metrics['average_precision']:.4f}

RANKING ABORDAGENS (ROC-AUC médio):
1. {sorted(approach_scores.items(), key=lambda x: x[1], reverse=True)[0][0]}: {sorted(approach_scores.values(), reverse=True)[0]:.4f}
2. {sorted(approach_scores.items(), key=lambda x: x[1], reverse=True)[1][0]}: {sorted(approach_scores.values(), reverse=True)[1]:.4f}
3. {sorted(approach_scores.items(), key=lambda x: x[1], reverse=True)[2][0]}: {sorted(approach_scores.values(), reverse=True)[2]:.4f}

STATUS: {status}

INSIGHTS PRINCIPAIS:
- {'Abordagem híbrida é superior' if hybrid_avg > max(external_avg, our_avg) else 'Notebook externo supera abordagem conservadora' if external_avg > our_avg else 'Abordagem conservadora é competitiva'}
- Feature engineering {'inteligente melhora performance' if hybrid_avg > our_avg else 'agressivo pode trazer ganhos mas com riscos'}
- {'Validação rigorosa é essencial' if our_avg > 0.6 else 'Necessário coletar mais features relevantes'}

RECOMENDAÇÃO: {status}
"""
    
    summary_path = REPORTS_PATH / 'comparative_analysis_summary.txt'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"\n📄 Resumo completo salvo em: {summary_path}")
    
    # Salvar resultados detalhados
    results_path = REPORTS_PATH / 'detailed_results.csv'
    comparison_df.to_csv(results_path)
    print(f"📊 Resultados detalhados salvos em: {results_path}")
    
    print(f"\n✅ Análise comparativa concluída!")
    print(f"📁 Arquivos gerados em: {REPORTS_PATH}")

if __name__ == "__main__":
    main()