import pyodbc
import pandas as pd
import numpy as np
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class MaintenanceReportGenerator:
    def __init__(self):
        self.conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=RONI\\SQLEXPRESS;"
            "DATABASE=GATEC_MEC;"
            "Trusted_Connection=yes;"
        )
        self.styles = getSampleStyleSheet()
        self.custom_styles = self._create_custom_styles()

    def _create_custom_styles(self):
        """Cria estilos personalizados para o relatório"""
        custom_styles = {
            'Warning': ParagraphStyle(
                'Warning',
                parent=self.styles['Normal'],
                textColor=colors.red,
                spaceAfter=20
            ),
            'Title': ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1  # Centralizado
            ),
            'Subtitle': ParagraphStyle(
                'CustomSubtitle',
                parent=self.styles['Heading2'],
                fontSize=14,
                spaceAfter=20,
                spaceBefore=20
            ),
            'TableHeader': ParagraphStyle(
                'TableHeader',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=colors.white
            )
        }
        return custom_styles

    def get_maintenance_data(self):
        """Coleta dados de manutenção com validações"""
        try:
            query = """
            WITH MaintenanceMetrics AS (
                SELECT 
                    e.COD_EQUIPAMENTO,
                    e.EQP_ANO_FABRIC,
                    e.ID_CLASSE,
                    e.EQP_STATUS,
                    COUNT(os.COD_OS) as total_os,
                    MAX(os.OS_DATA) as ultima_manutencao,
                    MIN(os.OS_DATA) as primeira_manutencao
                FROM GA_EQP_EQUIPAMENTO e
                LEFT JOIN GA_EQP_OS os ON e.COD_EQUIPAMENTO = os.COD_EQUIPAMENTO
                WHERE e.EQP_STATUS = 1
                GROUP BY 
                    e.COD_EQUIPAMENTO,
                    e.EQP_ANO_FABRIC,
                    e.ID_CLASSE,
                    e.EQP_STATUS
            )
            SELECT * FROM MaintenanceMetrics
            """
            with pyodbc.connect(self.conn_str) as conn:
                df = pd.read_sql(query, conn)
            return df, None
        except Exception as e:
            return None, str(e)

    def generate_report(self, output_filename='RelatorioManutencao.pdf'):
        """Gera relatório PDF completo"""
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Conteúdo do relatório
        story = []

        # Título
        story.append(Paragraph(
            "Relatório de Análise de Manutenção de Equipamentos",
            self.custom_styles['Title']
        ))
        story.append(Paragraph(
            f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 30))

        # Coleta e valida dados
        data, error = self.get_maintenance_data()
        
        # Seção de Advertências
        story.append(Paragraph("Advertências Importantes", self.custom_styles['Subtitle']))
        warnings = [
            "Este relatório utiliza dados do sistema GATEC_MEC e sua precisão depende da qualidade dos registros de manutenção.",
            "As datas de manutenção devem ser verificadas quanto à sua consistência nos registros originais.",
            "A classificação de equipamentos deve ser validada com a equipe operacional.",
            "Equipamentos inativos foram excluídos desta análise."
        ]
        for warning in warnings:
            story.append(Paragraph(warning, self.custom_styles['Warning']))

        if error:
            story.append(Paragraph(
                f"ERRO NA COLETA DE DADOS: {error}",
                self.custom_styles['Warning']
            ))
            doc.build(story)
            return

        # Análise dos Dados
        if not data.empty:
            # Estatísticas Gerais
            story.append(Paragraph("Estatísticas Gerais", self.custom_styles['Subtitle']))
            stats_data = [
                ["Métrica", "Valor"],
                ["Total de Equipamentos", str(len(data))],
                ["Média de OS por Equipamento", f"{data['total_os'].mean():.2f}"],
                ["Equipamentos sem Manutenção", str(len(data[data['total_os'] == 0]))],
                ["Data da Última Manutenção", str(data['ultima_manutencao'].max())]
            ]
            stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOX', (0, 0), (-1, -1), 2, colors.black)
            ]))
            story.append(stats_table)
            story.append(Spacer(1, 20))

            # Análise por Classe
            story.append(Paragraph("Análise por Classe de Equipamento", self.custom_styles['Subtitle']))
            class_analysis = data.groupby('ID_CLASSE').agg({
                'COD_EQUIPAMENTO': 'count',
                'total_os': ['sum', 'mean']
            }).round(2)
            
            class_data = [["Classe", "Qtd. Equip.", "Total OS", "Média OS"]]
            for idx in class_analysis.index:
                class_data.append([
                    str(idx),
                    str(class_analysis.loc[idx, ('COD_EQUIPAMENTO', 'count')]),
                    str(class_analysis.loc[idx, ('total_os', 'sum')]),
                    f"{class_analysis.loc[idx, ('total_os', 'mean')]:.2f}"
                ])

            class_table = Table(class_data, colWidths=[1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
            class_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(class_table)

            # Recomendações
            story.append(Paragraph("Recomendações", self.custom_styles['Subtitle']))
            recommendations = [
                "1. Revisar o plano de manutenção preventiva para equipamentos com alta frequência de OS.",
                "2. Investigar equipamentos sem registros de manutenção nos últimos 12 meses.",
                "3. Validar a classificação dos equipamentos para garantir a correta categorização.",
                "4. Implementar um processo de validação dos registros de manutenção."
            ]
            for rec in recommendations:
                story.append(Paragraph(rec, self.styles['Normal']))
                story.append(Spacer(1, 10))

        doc.build(story)
        print(f"Relatório gerado com sucesso: {output_filename}")

if __name__ == "__main__":
    report_gen = MaintenanceReportGenerator()
    report_gen.generate_report()