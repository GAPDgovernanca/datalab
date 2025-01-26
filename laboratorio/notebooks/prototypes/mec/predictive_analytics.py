import pyodbc
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class MaintenanceInsights:
    def __init__(self):
        self.conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=RONI\\SQLEXPRESS;"
            "DATABASE=GATEC_MEC;"
            "Trusted_Connection=yes;"
        )

    def get_comprehensive_maintenance_data(self):
        """Coleta dados abrangentes de manutenção para análise gerencial"""
        query = """
        WITH MaintenanceMetrics AS (
            SELECT 
                e.COD_EQUIPAMENTO,
                e.EQP_ANO_FABRIC,
                e.ID_CLASSE,
                e.EQP_STATUS,
                e.EQP_VALOR,
                COUNT(os.COD_OS) as total_os,
                MAX(os.OS_DATA) as ultima_manutencao,
                DATEDIFF(day, MIN(os.OS_DATA), MAX(os.OS_DATA)) as periodo_manutencao
            FROM GA_EQP_EQUIPAMENTO e
            LEFT JOIN GA_EQP_OS os ON e.COD_EQUIPAMENTO = os.COD_EQUIPAMENTO
            WHERE e.EQP_STATUS = 1
            GROUP BY 
                e.COD_EQUIPAMENTO,
                e.EQP_ANO_FABRIC,
                e.ID_CLASSE,
                e.EQP_STATUS,
                e.EQP_VALOR
        )
        SELECT 
            m.*,
            CASE 
                WHEN periodo_manutencao > 0 THEN 
                    CAST(total_os AS FLOAT) / periodo_manutencao * 365
                ELSE 0 
            END as frequencia_anual_os
        FROM MaintenanceMetrics m
        """
        
        with pyodbc.connect(self.conn_str) as conn:
            return pd.read_sql(query, conn)

    def analyze_maintenance_efficiency(self):
        """Gera insights estratégicos para gestão de manutenção"""
        print("\nRELATÓRIO DE INSIGHTS ESTRATÉGICOS DE MANUTENÇÃO")
        print(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print("=" * 70)

        df = self.get_comprehensive_maintenance_data()
        
        # Calcula idade dos equipamentos
        df['idade_equipamento'] = datetime.now().year - df['EQP_ANO_FABRIC']
        
        # Análise por classe de equipamento
        class_analysis = df.groupby('ID_CLASSE').agg({
            'COD_EQUIPAMENTO': 'count',
            'total_os': ['sum', 'mean'],
            'frequencia_anual_os': 'mean',
            'idade_equipamento': 'mean'
        }).round(2)
        
        # Identifica equipamentos críticos
        df['indice_criticidade'] = (
            df['frequencia_anual_os'] * df['idade_equipamento'] / 
            df['idade_equipamento'].mean()
        )
        
        critical_equipment = df.nlargest(10, 'indice_criticidade')

        # Análise de intervalos entre manutenções
        df['intervalo_medio'] = np.where(
            df['total_os'] > 0,
            df['periodo_manutencao'] / df['total_os'],
            0
        )

        print("\nINSIGHT 1: EQUIPAMENTOS CRÍTICOS QUE REQUEREM ATENÇÃO IMEDIATA")
        print("-" * 70)
        for _, equip in critical_equipment.iterrows():
            print(f"\nEquipamento: {equip['COD_EQUIPAMENTO']}")
            print(f"Classe: {equip['ID_CLASSE']}")
            print(f"Idade: {equip['idade_equipamento']} anos")
            print(f"Frequência anual de manutenções: {equip['frequencia_anual_os']:.2f}")

        print("\nINSIGHT 2: ANÁLISE DE EFICIÊNCIA POR CLASSE DE EQUIPAMENTO")
        print("-" * 70)
        for classe, metrics in class_analysis.iterrows():
            print(f"\nClasse {classe}:")
            print(f"Total de equipamentos: {metrics[('COD_EQUIPAMENTO', 'count')]:.0f}")
            print(f"Média de OS por equipamento: {metrics[('total_os', 'mean')]:.2f}")
            print(f"Frequência anual média de manutenções: {metrics[('frequencia_anual_os', 'mean')]:.2f}")

        print("\nINSIGHT 3: RECOMENDAÇÕES PARA OTIMIZAÇÃO")
        print("-" * 70)

        # Identifica classes com alta frequência de manutenção
        high_maintenance_classes = class_analysis[
            class_analysis[('frequencia_anual_os', 'mean')] > 
            class_analysis[('frequencia_anual_os', 'mean')].mean()
        ]

        for classe in high_maintenance_classes.index:
            mean_freq = high_maintenance_classes.loc[classe, ('frequencia_anual_os', 'mean')]
            print(f"\nClasse {classe} - Frequência: {mean_freq:.2f} manutenções/ano")
            print("Recomendação: Avaliar causa raiz das manutenções frequentes e considerar:")
            print("- Revisão do plano de manutenção preventiva")
            print("- Análise de fornecedores de peças e serviços")
            print("- Treinamento específico para equipe de manutenção")

        return {
            'critical_equipment': critical_equipment,
            'class_analysis': class_analysis,
            'high_maintenance_classes': high_maintenance_classes
        }

if __name__ == "__main__":
    analyzer = MaintenanceInsights()
    results = analyzer.analyze_maintenance_efficiency()