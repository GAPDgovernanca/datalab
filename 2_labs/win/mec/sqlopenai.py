import os
import openai
import pyodbc
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from functools import lru_cache
from typing import Dict, List, Optional

class SQLOpenAIAssistant:
    def __init__(self):
        self.api_key = self._load_api_key()
        self.client = openai.OpenAI(api_key=self.api_key)
        self.engine = self._create_db_connection()
        self.conversation_history = []
        self.schema_context = self._build_schema_context()
    
    def _load_api_key(self) -> str:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        return api_key
    
    def _create_db_connection(self):
        connection_string = (
            "mssql+pyodbc://@RONI\\SQLEXPRESS/GATEC_MEC"
            "?driver=ODBC Driver 17 for SQL Server"
        )
        return create_engine(connection_string)
    
    def list_tables(self) -> pd.DataFrame:
        """List tables with improved filtering"""
        query = """
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        AND TABLE_SCHEMA = 'dbo'
        AND TABLE_NAME NOT LIKE 'TMPEQP%'
        AND TABLE_NAME NOT LIKE 'SEQ_%'
        ORDER BY TABLE_NAME
        """
        return pd.read_sql(query, self.engine)
    
    def list_columns(self, table_name: str) -> pd.DataFrame:
        """List columns for a specific table using SQL Server compatible parameterization"""
        try:
            query = """
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                CHARACTER_MAXIMUM_LENGTH,
                IS_NULLABLE
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = ?
            ORDER BY ORDINAL_POSITION
            """
            return pd.read_sql(query, self.engine, params=(table_name,))
        except Exception as e:
            print(f"Note: Skipping table {table_name} - {str(e)}")
            return pd.DataFrame()

    def show_tables(self) -> str:
        """Display available tables in the database"""
        try:
            tables = self.list_tables()
            return "Available tables:\n" + "\n".join(tables['TABLE_NAME'].tolist())
        except Exception as e:
            return f"Error listing tables: {str(e)}"

    def describe_table(self, table_name: str) -> str:
        """Describe table structure"""
        try:
            columns = self.list_columns(table_name)
            if columns.empty:
                return f"No information available for table {table_name}"
            return f"Table Structure for {table_name}:\n" + columns.to_string()
        except Exception as e:
            return f"Error describing table: {str(e)}"

    def get_table_preview(self, table_name: str) -> str:
        """Get a preview of table data"""
        try:
            # Get row count
            count_query = f"SELECT COUNT(*) as count FROM [{table_name}]"
            row_count = pd.read_sql(count_query, self.engine).iloc[0]['count']
            
            # Get sample data
            sample_query = f"SELECT TOP 5 * FROM [{table_name}]"
            sample = pd.read_sql(sample_query, self.engine)
            
            preview = f"""
    Table: {table_name}
    Total Records: {row_count}

    Sample Data:
    {sample.to_string()}
    """
            return preview
        except Exception as e:
            return f"Error previewing table: {str(e)}"


        def direct_query(self, query: str) -> str:
            """Execute a SQL query directly without OpenAI"""
            try:
                result = pd.read_sql(query, self.engine)
                return result.to_string()
            except Exception as e:
                return f"Error executing query: {str(e)}"

        def get_sample_data(self, table_name: str, limit: int = 5) -> pd.DataFrame:
            """Get sample data from a table"""
            try:
                query = "SELECT TOP ? * FROM [?]"
                return pd.read_sql(query, self.engine, params=(limit, table_name))
            except Exception as e:
                raise Exception(f"Error retrieving sample data for table {table_name}: {str(e)}")

        def get_table_stats(self, table_name: str) -> Dict:
            """Get basic statistics for numeric columns in a table"""
            try:
                columns = self.list_columns(table_name)
                numeric_columns = columns[columns['DATA_TYPE'].isin(['int', 'decimal', 'float', 'numeric'])]
                
                stats = {}
                for _, col in numeric_columns.iterrows():
                    column_name = col['COLUMN_NAME']
                    query = f"""
                    SELECT 
                        COUNT(*) as count,
                        AVG(CAST({column_name} AS FLOAT)) as mean,
                        MIN({column_name}) as min,
                        MAX({column_name}) as max
                    FROM [{table_name}]
                    WHERE {column_name} IS NOT NULL
                    """
                    try:
                        result = pd.read_sql(query, self.engine)
                        stats[column_name] = result.to_dict('records')[0]
                    except Exception as e:
                        print(f"Warning: Could not calculate stats for column {column_name}: {str(e)}")
                        continue
                
                return stats
            except Exception as e:
                raise Exception(f"Error calculating table statistics: {str(e)}")

        def analyze_table(self, table_name: str) -> Dict:
            """Comprehensive table analysis"""
            try:
                columns = self.list_columns(table_name)
                sample = self.get_sample_data(table_name)
                stats = self.get_table_stats(table_name)
                
                return {
                    "columns": columns.to_dict('records'),
                    "sample_data": sample.to_dict('records'),
                    "statistics": stats
                }
            except Exception as e:
                return {"error": str(e)}
        
def main():
    assistant = SQLOpenAIAssistant()
    print("\n🔹 SQL Database Assistant 🔹")
    print("\nAvailable commands:")
    print("1. Basic Commands:")
    print("   - show tables")
    print("   - describe <table_name>")
    print("   - preview <table_name>")
    print("   - exit")
    print("\n2. Query Commands:")
    print("   - query <sql_statement>")
    
    while True:
        try:
            user_input = input("\n🟢 Command> ").strip()
            
            if user_input.lower() == 'exit':
                break
            elif user_input.lower() == 'show tables':
                print("\n", assistant.show_tables())
            elif user_input.lower().startswith('describe '):
                table_name = user_input[9:].strip()
                print("\n", assistant.describe_table(table_name))
            elif user_input.lower().startswith('preview '):
                table_name = user_input[8:].strip()
                print("\n", assistant.get_table_preview(table_name))
            elif user_input.lower().startswith('query '):
                sql = user_input[6:].strip()
                print("\n", assistant.direct_query(sql))
            else:
                print("\nUnknown command. Type a command from the list above.")
            
        except KeyboardInterrupt:
            print("\nExiting gracefully...")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()