import sqlite3

# Caminho relativo para o banco de dados SQLite
db_path = "frota.db"

try:
    # Conectando ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ativar suporte a chaves estrangeiras (PRAGMA deve ser executado separadamente)
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Comando SQL para listar os relacionamentos
    query = """
    SELECT 
        m.name AS table_name,
        p."from" AS column_name,
        p."table" AS referenced_table,
        p."to" AS referenced_column
    FROM sqlite_master m
    JOIN pragma_foreign_key_list(m.name) p
    WHERE m.type = 'table' AND p."id" IS NOT NULL;
    """

    # Executar a consulta principal
    cursor.execute(query)
    rows = cursor.fetchall()

    # Salvar o resultado em um arquivo .txt
    output_file = "relationships.txt"
    with open(output_file, "w") as file:
        file.write("Table Name\tColumn Name\tReferenced Table\tReferenced Column\n")
        for row in rows:
            file.write("\t".join(map(str, row)) + "\n")

    print(f"Relações exportadas para {output_file}")

except sqlite3.OperationalError as e:
    print(f"Erro ao acessar o banco de dados: {e}")
except sqlite3.ProgrammingError as e:
    print(f"Erro de programação SQL: {e}")

finally:
    # Garantir que a conexão será fechada
    if 'conn' in locals():
        conn.close()
