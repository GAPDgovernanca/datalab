import pyodbc

# Configuração inicial
DB_CONFIG = {
    'server': 'RONI\\SQLEXPRESS',
    'database': 'GATEC_MEC',
    'driver': 'ODBC Driver 17 for SQL Server'
}

# String de conexão
conn_string = f"DRIVER={{{DB_CONFIG['driver']}}};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};Trusted_Connection=yes;"

try:
    # Conectando ao banco de dados
    with pyodbc.connect(conn_string) as conn:
        cursor = conn.cursor()
        
        # Consulta para explorar a tabela GA_OFI_OFICINA
        query = "SELECT TOP 1000 * FROM GA_OFI_OFICINA"
        cursor.execute(query)
        
        # Recuperar e exibir os resultados
        columns = [column[0] for column in cursor.description]
        results = cursor.fetchall()
        
        print(f"Colunas: {columns}")
        for row in results:
            print(row)
            
except pyodbc.Error as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
