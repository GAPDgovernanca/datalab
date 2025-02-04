# database/esquema.py
"""
Módulo: Esquema do Banco de Dados
Objetivo: Definir estrutura dimensional do banco de dados SQLite
"""

class EsquemaDimensional:
    """Define estrutura de tabelas do banco de dados"""
    
    # Dimensão Equipamento
    SQL_CRIAR_DIM_EQUIPAMENTO = """
    CREATE TABLE IF NOT EXISTS dim_equipamento (
        id_equipamento INTEGER PRIMARY KEY,
        modelo TEXT NOT NULL,
        usuario TEXT NOT NULL,
        classe TEXT NOT NULL,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
    )"""
    
    # Fatos de Uso
    SQL_CRIAR_FATO_USO = """
    CREATE TABLE IF NOT EXISTS fato_uso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_equipamento INTEGER,
        tipo_medidor TEXT CHECK(tipo_medidor IN ('H', 'KM', 'IND')),
        uso_estimado DECIMAL(15,2),
        uso_realizado DECIMAL(15,2),
        uso_diferenca DECIMAL(15,2),
        data_referencia DATETIME,
        data_processamento DATETIME,
        FOREIGN KEY(id_equipamento) REFERENCES dim_equipamento(id_equipamento)
    )"""
    
    # Fatos de Custo Operacional
    SQL_CRIAR_FATO_CUSTO = """
    CREATE TABLE IF NOT EXISTS fato_custo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_equipamento INTEGER,
        custo_hora_estimado DECIMAL(15,2),
        custo_hora_realizado DECIMAL(15,2),
        custo_hora_diferenca DECIMAL(15,2),
        total_estimado DECIMAL(15,2),
        total_realizado DECIMAL(15,2),
        total_diferenca DECIMAL(15,2),
        data_referencia DATETIME,
        data_processamento DATETIME,
        FOREIGN KEY(id_equipamento) REFERENCES dim_equipamento(id_equipamento)
    )"""
    
    # Fatos de Combustível
    SQL_CRIAR_FATO_COMBUSTIVEL = """
    CREATE TABLE IF NOT EXISTS fato_combustivel (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_equipamento INTEGER,
        comb_litros_estimado DECIMAL(15,2),
        comb_litros_realizado DECIMAL(15,2),
        comb_litros_diferenca DECIMAL(15,2),
        comb_valor_unitario_estimado DECIMAL(15,2),
        comb_valor_unitario_realizado DECIMAL(15,2),
        comb_valor_unitario_diferenca DECIMAL(15,2),
        comb_total_estimado DECIMAL(15,2),
        comb_total_realizado DECIMAL(15,2),
        comb_total_diferenca DECIMAL(15,2),
        data_referencia DATETIME,
        data_processamento DATETIME,
        FOREIGN KEY(id_equipamento) REFERENCES dim_equipamento(id_equipamento)
    )"""
    
    # Fatos de Manutenção
    SQL_CRIAR_FATO_MANUTENCAO = """
    CREATE TABLE IF NOT EXISTS fato_manutencao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_equipamento INTEGER,
        lubrificantes_estimado DECIMAL(15,2),
        lubrificantes_realizado DECIMAL(15,2),
        lubrificantes_diferenca DECIMAL(15,2),
        filtros_estimado DECIMAL(15,2),
        filtros_realizado DECIMAL(15,2),
        filtros_diferenca DECIMAL(15,2),
        graxas_estimado DECIMAL(15,2),
        graxas_realizado DECIMAL(15,2),
        graxas_diferenca DECIMAL(15,2),
        pecas_servicos_estimado DECIMAL(15,2),
        pecas_servicos_realizado DECIMAL(15,2),
        pecas_servicos_diferenca DECIMAL(15,2),
        data_referencia DATETIME,
        data_processamento DATETIME,
        FOREIGN KEY(id_equipamento) REFERENCES dim_equipamento(id_equipamento)
    )"""
    
    # Fatos de Reforma
    SQL_CRIAR_FATO_REFORMA = """
    CREATE TABLE IF NOT EXISTS fato_reforma (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_equipamento INTEGER,
        reforma_estimado DECIMAL(15,2),
        reforma_realizado DECIMAL(15,2),
        reforma_diferenca DECIMAL(15,2),
        data_referencia DATETIME,
        data_processamento DATETIME,
        FOREIGN KEY(id_equipamento) REFERENCES dim_equipamento(id_equipamento)
    )"""

    @classmethod
    def obter_todos_schemas(cls) -> list:
        """Retorna lista com todos os comandos SQL de criação"""
        return [
            cls.SQL_CRIAR_DIM_EQUIPAMENTO,
            cls.SQL_CRIAR_FATO_USO,
            cls.SQL_CRIAR_FATO_CUSTO,
            cls.SQL_CRIAR_FATO_COMBUSTIVEL,
            cls.SQL_CRIAR_FATO_MANUTENCAO,
            cls.SQL_CRIAR_FATO_REFORMA
        ]