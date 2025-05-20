# maintenance_predictor.py
import logging
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
from sqlalchemy import create_engine
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from prefect import flow, task

# Configuração inicial
logging.basicConfig(level=logging.INFO)
DB_CONFIG = {
    'server': 'RONI\\SQLEXPRESS',
    'database': 'GATEC_MEC',
    'driver': 'ODBC Driver 17 for SQL Server'
}

class MaintenancePredictor:
    def __init__(self):
        self.engine = self._create_db_connection()
        self.model = None
        self.features = None
        self.target = 'FALHA_CRITICA'
    
    def _create_db_connection(self):
        """Cria conexão com o banco de dados"""
        connection_string = (
            f"mssql+pyodbc:///?odbc_connect="
            f"DRIVER={{{DB_CONFIG['driver']}}};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"Trusted_Connection=yes"
        )
        return create_engine(connection_string)

    @task(name="Carregar dados")
    def load_data(self):
        """Carrega e junta dados das tabelas relacionadas"""
        query = """
        SELECT 
            eq.COD_EQUIPAMENTO, eq.COD_CRIT, eq.COD_MODELO,
            os.COD_OS, os.DT_ABERTURA, os.COD_MOTIVO, os.OS_SITUACAO,
            mov.ID_MOV_AGD, mov.DT_MOV, mov.COD_RETIRADA
        FROM GA_EQP_EQUIPAMENTO eq
        LEFT JOIN GA_OFI_OS os 
            ON eq.COD_EQUIPAMENTO = os.COD_EQUIPAMENTO
        LEFT JOIN GA_AGD_MOV_AGD mov 
            ON eq.COD_EQUIPAMENTO = mov.COD_EQUIPAMENTO
        """
        try:
            df = pd.read_sql(query, self.engine)
            logging.info(f"Dados carregados. Shape: {df.shape}")
            return df
        except Exception as e:
            logging.error(f"Erro ao carregar dados: {str(e)}")
            raise

    @task(name="Pré-processamento")
    def preprocess_data(self, df):
        """Transformação completa dos dados"""
        # Engenharia de features temporal
        df['DIAS_ULTIMA_MANUTENCAO'] = (
            pd.to_datetime('now') - pd.to_datetime(df['DT_ABERTURA'])
        ).dt.days
        
        # Variável alvo
        df[self.target] = df['OS_SITUACAO'].apply(
            lambda x: 1 if x in ['EMERGENCIA', 'FALHA_GRAVE'] else 0
        )
        
        # Tratamento de datas
        for col in ['DT_ABERTURA', 'DT_MOV']:
            df[col] = pd.to_datetime(df[col])
            df[f'MES_{col.split("_")[-1]}'] = df[col].dt.month
            df[f'ANO_{col.split("_")[-1]}'] = df[col].dt.year
        
        # Codificação categórica
        categorical_features = ['COD_CRIT', 'COD_MOTIVO']
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        encoded = self.encoder.fit_transform(df[categorical_features])
        df_encoded = pd.DataFrame(
            encoded.toarray(),
            columns=self.encoder.get_feature_names_out(categorical_features)
        )
        
        return pd.concat([df.drop(categorical_features, axis=1), df_encoded], axis=1)

    @task(name="Treinar modelo")
    def train_model(self, df):
        """Treinamento com validação temporal"""
        # Divisão temporal
        train = df[df['DT_ABERTURA'] < '2023-01-01']
        test = df[df['DT_ABERTURA'] >= '2023-01-01']
        
        # Features e target
        features = [c for c in df.columns if c not in [self.target, 'DT_ABERTURA', 'DT_MOV']]
        self.features = features
        
        # Pipeline de modelagem
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), ['DIAS_ULTIMA_MANUTENCAO']),
                ('cat', 'passthrough', [c for c in features if 'COD_' in c])
            ])
        
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', RandomForestClassifier(
                class_weight='balanced',
                random_state=42,
                n_jobs=-1
            ))
        ])
        
        # Tuning de hiperparâmetros
        param_grid = {
            'model__n_estimators': [100, 200],
            'model__max_depth': [3, 5, None]
        }
        
        tscv = TimeSeriesSplit(n_splits=3)
        grid_search = GridSearchCV(
            pipeline,
            param_grid,
            cv=tscv,
            scoring='roc_auc'
        )
        
        grid_search.fit(train[features], train[self.target])
        self.model = grid_search.best_estimator_
        
        # Avaliação
        preds = self.model.predict(test[features])
        probs = self.model.predict_proba(test[features])[:,1]
        
        logging.info("\nRelatório de Classificação:")
        logging.info(classification_report(test[self.target], preds))
        logging.info(f"AUC-ROC: {roc_auc_score(test[self.target], probs):.2f}")
        
        return self.model

    @task(name="Salvar artefatos")
    def save_artifacts(self):
        """Persistência do modelo e metadados"""
        joblib.dump(self.model, 'modelo_final.pkl')
        joblib.dump(self.encoder, 'encoder.pkl')
        pd.Series(self.features).to_csv('features.csv', index=False)
        logging.info("Artefatos salvos: modelo.pkl, encoder.pkl, features.csv")

    @task(name="Visualizar resultados")
    def visualize_results(self, df):
        """Geração de visualizações interativas"""
        fig = px.scatter_matrix(
            df,
            dimensions=['DIAS_ULTIMA_MANUTENCAO', 'COD_CRIT_ALTA', 'MES_ABERTURA'],
            color=self.target,
            title='Distribuição de Features por Status de Falha'
        )
        fig.write_html('visualizacao_features.html')
        
        fig2 = px.histogram(
            df,
            x='DIAS_ULTIMA_MANUTENCAO',
            nbins=50,
            color=self.target,
            barmode='overlay',
            title='Distribuição Temporal de Falhas'
        )
        fig2.write_html('histograma_temporal.html')

    @flow(name="Pipeline Principal")
    def main_flow(self):
        """Fluxo de execução principal"""
        df_raw = self.load_data()
        df_processed = self.preprocess_data(df_raw)
        model = self.train_model(df_processed)
        self.save_artifacts()
        self.visualize_results(df_processed)
        
    def predict_new_data(self, new_data):
        """Método para previsão em novos dados"""
        processed_data = self.preprocess_data(new_data)
        features = processed_data[self.features]
        return self.model.predict_proba(features)[:,1]

# Execução
if __name__ == "__main__":
    predictor = MaintenancePredictor()
    predictor.main_flow()
    
    # Exemplo de uso com novos dados
    new_data_query = "SELECT * FROM GA_EQP_EQUIPAMENTO WHERE COD_CRIT = 'ALTA'"
    new_data = pd.read_sql(new_data_query, predictor.engine)
    predictions = predictor.predict_new_data(new_data)
    pd.Series(predictions, index=new_data['COD_EQUIPAMENTO']).to_csv('novas_previsoes.csv')