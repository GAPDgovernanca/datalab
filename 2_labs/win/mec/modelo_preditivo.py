from sqlalchemy import create_engine
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Configuração da conexão com o SQL Server
server = 'RONI\\SQLEXPRESS'
database = 'GATEC_MEC'
driver = 'ODBC Driver 17 for SQL Server'

connection_string = f"mssql+pyodbc:///?odbc_connect=" + \
    f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes"
engine = create_engine(connection_string)

# Query para extrair os dados
query = "SELECT TOP 100 * FROM GA_CLE_ORCAMENTOS;"  # Ajustar para mais dados
data = pd.read_sql(query, engine)

# Transformar colunas datetime para valores numéricos
data['DT_INI_NUM'] = data['DT_INI'].astype('int64') // 10**9
data['DT_FIM_NUM'] = data['DT_FIM'].astype('int64') // 10**9

# Selecionar features e alvo
features = data.drop(columns=[
    'CHK_BLOQUEAR', 'DSC_ORC', 'DT_INI', 'DT_FIM', 'ROWID',
    'DT_ULT_ATU_LIST', 'DT_ULT_ATU_REAL', 'DT_ULT_ATU_ORC', 'LST_PRO', 'LST_EMPR'
])
target = data['CHK_BLOQUEAR']

# Simular classes, se necessário
if target.nunique() == 1:
    target.iloc[0:len(target)//2] = 1

# Tratar valores ausentes
features = features.fillna(0)

# Dividir os dados
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

# Verificar se é necessário balancear manualmente
if y_train.value_counts().min() == 1:
    minority_class = y_train.value_counts().idxmin()
    X_minority = X_train[y_train == minority_class]
    y_minority = y_train[y_train == minority_class]
    X_train = pd.concat([X_train, X_minority])
    y_train = pd.concat([y_train, y_minority])

print("\nDistribuição ajustada no conjunto de treino:")
print(y_train.value_counts())

# Treinar o modelo com reponderação de classes
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# Fazer previsões
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

# Avaliar o desempenho
print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred, zero_division=1))

print("\nAUC-ROC:", roc_auc_score(y_test, y_proba))
