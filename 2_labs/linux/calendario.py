from docx import Document
from docx.shared import Pt, Inches, Cm
from docx.enum.section import WD_ORIENT

# 1. Criação do documento
doc = Document()

# 2. Configuração para LANDSCAPE (Paisagem)
section = doc.sections[0]
new_width, new_height = section.page_height, section.page_width
section.orientation = WD_ORIENT.LANDSCAPE
section.page_width = new_width
section.page_height = new_height

# Margens (opcional, para dar mais espaço)
section.left_margin = Cm(1.27)
section.right_margin = Cm(1.27)
section.top_margin = Cm(1.27)
section.bottom_margin = Cm(1.27)

# Título
doc.add_heading('Calendário Integrado: Governança & Safra (2025/2026)', 0)

# 3. Dados consolidados (Reordenados para iniciar em ABRIL)
data = [
    ("Abril", "Avaliação Trimestral de Desempenho Q3", 
     "• Resultados Q3 (Out-Dez).\n• Evento de início de ano.\n• Políticas de Gestão e Risco.\nObs: Foco no trimestre anterior.", 
     "AVB; Pessoas", 
     "• [Pau Dalho] Cana Safra: Início Colheita (1ª quinzena)\n• [Pau Dalho] Cana Plantio: Fim (1ª quinzena)\n• [Canadá] Cana Safra: Início Colheita (1ª quinzena)\n• [Canadá] Cana Plantio: Fim (1ª quinzena)\n• [Rancho Alegre] Soja: Fim Colheita (1ª Quinzena)"),

    ("Maio", "Estratégia Corporativa e Cenário Financeiro", 
     "• Definir evento anual de liderança.\n• Painel de indicadores (ROA, ROIC, TIR).\n• Fluxo de caixa e endividamento.\n• Políticas de Gestão e Risco.\nObs: Fundamenta decisões de julho.", 
     "Pessoas; ECOWA; AVB", 
     "-"),

    ("Junho", "Apresentação de Resultados (Safra anterior)", 
     "• Resultados operacionais por unidade e consolidado.\n• Políticas de Gestão e Risco.\nObs: Consolidação da performance anual.", 
     "AVB", 
     "• [São Judas] Safrinha Milho: Fim Colheita (1ª Semana)\n• [Rancho Alegre] Safrinha Milho: Fim Colheita (1ª Semana)"),

    ("Julho", "Discussões Estratégicas de Longo Prazo", 
     "• Planejamento estratégico LP: revisão anual.\n• Políticas de Gestão e Risco.\nObs: Alinhamento com tendências.", 
     "ECOWA", 
     "-"),

    ("Agosto", "Avaliação Trimestral de Desempenho Q1", 
     "• Resultados Q1 (Abr-Jun).\n• Políticas de Gestão e Risco.\nObs: Avaliação dos primeiros meses.", 
     "AVB", 
     "-"),

    ("Setembro", "Monitoramento de Políticas Corporativas", 
     "• Políticas de Gestão e Risco (foco exclusivo).\nObs: Monitoramento de políticas internas.", 
     "ECOWA", 
     "• [São Judas] Milho: Início Plantio (1ª Quinzena)"),

    ("Outubro", "Espaço para Demandas Especiais (ad hoc)", 
     "• Demandas emergenciais.\n• Políticas de Gestão e Risco.\nObs: Revisões excepcionais.", 
     "ECOWA", 
     "• [Rancho Alegre] Soja: Início Plantio (1ª Quinzena)\n• [São Judas] Soja: Início Plantio (1ª Quinzena)\n• [Pau Dalho] Cana Safra: Fim Colheita (2ª quinzena)\n• [Pau Dalho] Soja: Início Plantio (2ª quinzena)\n• [Pau Dalho] Milho: Início Plantio (2ª quinzena)\n• [Canadá] Cana Safra: Fim Colheita (2ª quinzena)"),

    ("Novembro", "Avaliação Trimestral de Desempenho Q2", 
     "• Resultados Q2 (Jul-Set).\n• Políticas de Gestão e Risco.\nObs: Visão de desempenho meses centrais.", 
     "AVB; ECOWA", 
     "• [Canadá] Soja: Início Plantio (1ª Quinzena)"),

    ("Dezembro", "Projeções do Ano Safra", 
     "• Simulações fechamento ano safra.\n• Políticas de Gestão e Risco.\nObs: Insumo para CAPEX de fevereiro.", 
     "AVB; ECOWA", 
     "-"),

    ("Janeiro", "Recesso", 
     "• Período de recesso, sem reuniões agendadas.\nObs: Período reservado para recesso institucional.", 
     "-", 
     "• [São Judas] Safrinha Milho: Início Plantio (1ª Quinzena)\n• [São Judas] Soja: Fim Colheita (2ª Quinzena)\n• [São Judas] Milho: Fim Colheita (2ª Quinzena)"),

    ("Fevereiro", "Planejamento de Investimentos e Estrutura de Capital", 
     "• Apresentação CAPEX próxima safra.\n• Estrutura de capital.\n• Políticas de Gestão e Risco (mensal).\nObs: Base para definição de metas em março.", 
     "AVB; MOP; ECOWA", 
     "• [Pau Dalho] Cana Plantio: Início (1ª quinzena)\n• [Pau Dalho] Soja: Fim Colheita (1ª Quinzena)\n• [Pau Dalho] Milho: Fim Colheita (2ª Quinzena)\n• [Canadá] Cana Plantio: Início (2ª quinzena)\n• [Canadá] Soja: Fim Colheita (2ª Quinzena)\n• [Rancho Alegre] Safrinha Milho: Início Plantio (2ª Quinzena)"),

    ("Março", "Definição de Metas e Aprovação Orçamentária", 
     "• Aprovação do Orçamento Operacional.\n• Estabelecimento das metas das Unidades.\n• Plano de comunicação das metas.\n• Políticas de Gestão e Risco.\nObs: Metas monitoradas trimestralmente.", 
     "AVB; MOP; ECOWA", 
     "-")
]

# 4. Criação da Tabela
table = doc.add_table(rows=1, cols=5)
table.style = 'Table Grid'

# Cabeçalho
hdr_cells = table.rows[0].cells
headers = ['Mês', 'Foco (Conselho)', 'Pautas e Entregas', 'Responsável', 'Atividades Safra']
for i, text in enumerate(headers):
    paragraph = hdr_cells[i].paragraphs[0]
    run = paragraph.add_run(text)
    run.bold = True

# Preenchimento
for mes, foco, pautas, resp, safra in data:
    row_cells = table.add_row().cells
    row_cells[0].text = mes
    row_cells[1].text = foco
    row_cells[2].text = pautas
    row_cells[3].text = resp
    row_cells[4].text = safra

# 5. Salvar o arquivo
file_name = 'Calendario_Safra_Conselho_Landscape.docx'
doc.save(file_name)
print(f"Arquivo '{file_name}' gerado com sucesso em formato Paisagem (Início: Abril).")