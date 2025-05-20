from sqlalchemy import create_engine
import pandas as pd

# Configuração da conexão com o SQL Server
server = 'RONI\\SQLEXPRESS'  # Seu servidor
database = 'GATEC_MEC'       # Seu banco de dados
driver = 'ODBC Driver 17 for SQL Server'

# Criar a engine do SQLAlchemy
connection_string = f"mssql+pyodbc:///?odbc_connect=" + \
    f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes"
engine = create_engine(connection_string)

try:
    # Consulta para listar todas as tabelas disponíveis
    query_tables = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';"
    tables = pd.read_sql(query_tables, engine)
    print("Tabelas disponíveis no banco:")
    print(tables)

    # Consulta para listar colunas das tabelas
    query_columns = "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS;"
    columns = pd.read_sql(query_columns, engine)
    print("Estrutura das tabelas:")
    print(columns)
except Exception as e:
    print(f"Erro ao executar as consultas: {e}")

