from sqlalchemy import create_engine
import pandas as pd

# Configuração da conexão
server = 'RONI\\SQLEXPRESS'
database = 'GATEC_MEC'
driver = 'ODBC Driver 17 for SQL Server'

# Criar a engine
connection_string = f"mssql+pyodbc:///?odbc_connect=" + \
    f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes"
engine = create_engine(connection_string)

query = "SELECT TOP 10 * FROM GA_CLE_ORCAMENTOS;"
data = pd.read_sql(query, engine)