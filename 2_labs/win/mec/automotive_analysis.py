import pyodbc
import pandas as pd
import numpy as np
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class MaintenanceAnalyzer:
    def __init__(self):
        self.conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=RONI\\SQLEXPRESS;"
            "DATABASE=GATEC_MEC;"
            "Trusted_Connection=yes;"
        )
        self.styles = getSampleStyleSheet()
        self.custom_styles = self._create_styles()

    def _create_styles(self):
        return {
            'Title': ParagraphStyle(
                'CustomTitle', parent=self.styles['Heading1'],
                fontSize=16, spaceAfter=30, alignment=1
            ),
            'SectionHeader': ParagraphStyle(
                'SectionHeader', parent=self.styles['Heading2'],
                fontSize=14, textColor=colors.HexColor('#2C5282'),
                spaceBefore=20, spaceAfter=12
            ),
            'AnalysisText': ParagraphStyle(
                'AnalysisText', parent=self.styles['Normal'],
                fontSize=10, spaceBefore=6, spaceAfter=6
            )
        }

    def get_maintenance_data(self):
        query = """
        SELECT 
            e.COD_EQUIPAMENTO,
            e.EQP_ANO_FABRIC,
            e.ID_CLASSE,
            c.DSC_CLASSE,
            e.EQP_USUARIO,
            COUNT(os.COD_OS) as total_os,
            COUNT(DISTINCT YEAR(os.OS_DATA)) as anos_com_manutencao
        FROM GA_EQP_EQUIPAMENTO e
        LEFT JOIN GA_EQP_OS os ON e.COD_EQUIPAMENTO = os.COD_EQUIPAMENTO
        LEFT JOIN GA_EQP_CLASSE c ON e.ID_CLASSE = c.ID_CLASSE
        WHERE e.EQP_STATUS = 1
        GROUP BY 
            e.COD_EQUIPAMENTO,
            e.EQP_ANO_FABRIC,
            e.ID_CLASSE,
            c.DSC_CLASSE,
            e.EQP_USUARIO
        """
        with pyodbc.connect(self.conn_str) as conn:
            df = pd.read_sql(query, conn)
            df['media_os_ano'] = df['total_os'] / df['anos_com_manutencao'].apply(lambda x: max(x, 1))
            df['idade'] = datetime.now().year - df['EQP_ANO_FABRIC']
            return df

    def calculate_z_scores(self, series):
        return (series - series.mean()) / series.std() if series.std() > 0 else pd.Series(0, index=series.index)

    def analyze_class_patterns(self, df):
        results = {}
        for classe, classe_name in zip(df['ID_CLASSE'].unique(), df['DSC_CLASSE'].unique()):
            class_data = df[df['ID_CLASSE'] == classe].copy()
            if len(class_data) >= 5:
                stats = {
                    'nome': classe_name,
                    'mean': class_data['media_os_ano'].mean(),
                    'std': class_data['media_os_ano'].std(),
                    'count': len(class_data),
                    'quartiles': class_data['media_os_ano'].quantile([0.25, 0.5, 0.75])
                }
                class_data['z_score'] = self.calculate_z_scores(class_data['media_os_ano'])
                desvios = {
                    'acima': class_data[class_data['z_score'] > 2],
                    'abaixo': class_data[class_data['z_score'] < -1]
                }
                results[classe] = {
                    'stats': stats,
                    'desvios': desvios,
                    'data': class_data
                }
        return results

    def create_table(self, data, colwidths):
        table = Table(data, colWidths=colwidths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C5282')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        return table

    def create_report(self, filename='RelatorioManutencao.pdf'):
        doc = SimpleDocTemplate(
            filename, pagesize=letter,
            rightMargin=72, leftMargin=72,
            topMargin=72, bottomMargin=72
        )
        story = []
        story.append(Paragraph(
            "Análise de Padrões de Manutenção por Classe de Equipamento",
            self.custom_styles['Title']
        ))
        story.append(Paragraph(
            f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            self.custom_styles['AnalysisText']
        ))
        story.append(Spacer(1, 20))

        try:
            df = self.get_maintenance_data()
            analysis = self.analyze_class_patterns(df)
            
            for classe, dados in analysis.items():
                story.append(Paragraph(
                    f"Classe: {dados['stats']['nome']} (ID: {classe})",
                    self.custom_styles['SectionHeader']
                ))
                
                stats_data = [
                    ["Indicador", "Valor"],
                    ["Total de Equipamentos", f"{dados['stats']['count']}"],
                    ["Média de OS/ano", f"{dados['stats']['mean']:.2f}"],
                    ["Mediana de OS/ano", f"{dados['stats']['quartiles'][0.5]:.2f}"],
                    ["Desvio Padrão", f"{dados['stats']['std']:.2f}"]
                ]
                story.append(self.create_table(stats_data, [2*inch, 1.5*inch]))
                story.append(Spacer(1, 10))
                
                if not dados['desvios']['acima'].empty:
                    story.append(Paragraph(
                        "Equipamentos com Manutenção Acima do Padrão",
                        self.custom_styles['AnalysisText']
                    ))
                    high_data = [["Equipamento", "OS/Ano", "Z-Score", "Idade"]]
                    for _, row in dados['desvios']['acima'].iterrows():
                        high_data.append([
                            str(row['COD_EQUIPAMENTO']),
                            f"{row['media_os_ano']:.1f}",
                            f"{row['z_score']:+.1f}σ",
                            f"{row['idade']} anos"
                        ])
                    story.append(self.create_table(high_data, [1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch]))
                    story.append(Spacer(1, 10))
                story.append(Spacer(1, 20))

            notes = [
                "• Análise baseada apenas em equipamentos ativos",
                "• Z-Score: número de desvios padrão em relação à média da classe",
                "• Z-Score > 2σ indica desvio significativo alto",
                "• Média OS/ano considera apenas anos com registros"
            ]
            story.append(Paragraph("Notas Técnicas", self.custom_styles['SectionHeader']))
            for note in notes:
                story.append(Paragraph(note, self.custom_styles['AnalysisText']))
        
        except Exception as e:
            story.append(Paragraph(f"Erro na análise: {str(e)}", self.custom_styles['AnalysisText']))
        
        doc.build(story)
        print(f"Relatório gerado: {filename}")

if __name__ == "__main__":
    analyzer = MaintenanceAnalyzer()
    analyzer.create_report()