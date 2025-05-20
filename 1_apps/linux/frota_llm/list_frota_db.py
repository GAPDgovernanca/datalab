import sqlite3
import pandas as pd

def execute_query(db_file, query, params=None):
    """
    Executes an SQL query against the database and handles errors.

    Args:
        db_file (str): The path to the SQLite database file.
        query (str): The SQL query to execute.
        params (tuple, optional): Parameters to substitute into the query. Defaults to None.

    Returns:
        pandas.DataFrame: The results of the query as a DataFrame, or None if an error occurred.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        print("Executing query:", query)
        if params:
            print("With parameters:", params)
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # Get column names from cursor description
        column_names = [description[0] for description in cursor.description]

        results = cursor.fetchall()

        # Create a DataFrame
        df = pd.DataFrame(results, columns=column_names)
        return df
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_equipment_data(db_file, equipment_id):
    """
    Retrieves all data for a specific equipment from the database.

    Args:
        db_file (str): The path to the SQLite database file.
        equipment_id (int): The ID of the equipment to retrieve data for.

    Returns:
        pandas.DataFrame: The data for the equipment as a DataFrame, or None if an error occurred.
    """
    sql_query = """
        SELECT
            de.id_equipamento,
            de.modelo,
            de.usuario,
            de.classe,
            de.data_criacao,
            fu.id AS uso_id,
            fu.tipo_medidor,
            fu.uso_estimado,
            fu.uso_realizado,
            fu.uso_diferenca,
            fu.data_referencia AS uso_data_referencia,
            fu.data_processamento AS uso_data_processamento,
            fc.id AS custo_id,
            fc.custo_hora_estimado,
            fc.custo_hora_realizado,
            fc.custo_hora_diferenca,
            fc.total_estimado,
            fc.total_realizado,
            fc.total_diferenca,
            fc.data_referencia AS custo_data_referencia,
            fc.data_processamento AS custo_data_processamento,
            fco.id AS combustivel_id,
            fco.comb_litros_estimado,
            fco.comb_litros_realizado,
            fco.comb_litros_diferenca,
            fco.comb_valor_unitario_estimado,
            fco.comb_valor_unitario_realizado,
            fco.comb_valor_unitario_diferenca,
            fco.comb_total_estimado,
            fco.comb_total_realizado,
            fco.comb_total_diferenca,
            fco.data_referencia AS combustivel_data_referencia,
            fco.data_processamento AS combustivel_data_processamento,
            fm.id AS manutencao_id,
            fm.lubrificantes_estimado,
            fm.lubrificantes_realizado,
            fm.lubrificantes_diferenca,
            fm.filtros_estimado,
            fm.filtros_realizado,
            fm.filtros_diferenca,
            fm.graxas_estimado,
            fm.graxas_realizado,
            fm.graxas_diferenca,
            fm.pecas_servicos_estimado,
            fm.pecas_servicos_realizado,
            fm.pecas_servicos_diferenca,
            fm.data_referencia AS manutencao_data_referencia,
            fm.data_processamento AS manutencao_data_processamento,
            fr.id AS reforma_id,
            fr.reforma_estimado,
            fr.reforma_realizado,
            fr.reforma_diferenca,
            fr.data_referencia AS reforma_data_referencia,
            fr.data_processamento AS reforma_data_processamento
        FROM
            dim_equipamento AS de
        LEFT JOIN
            fato_uso AS fu ON de.id_equipamento = fu.id_equipamento
        LEFT JOIN
            fato_custo AS fc ON de.id_equipamento = fc.id_equipamento
        LEFT JOIN
            fato_combustivel AS fco ON de.id_equipamento = fco.id_equipamento
        LEFT JOIN
            fato_manutencao AS fm ON de.id_equipamento = fm.id_equipamento
        LEFT JOIN
            fato_reforma AS fr ON de.id_equipamento = fr.id_equipamento
        WHERE
            de.id_equipamento = ?;
    """
    df = execute_query(db_file, sql_query, (equipment_id,))
    return df

# Example usage:
database_file = 'frota.db'
equipment_id = 3721
df = get_equipment_data(database_file, equipment_id)

if df is not None:
    print(df)
else:
    print("No results returned or an error occurred.")
