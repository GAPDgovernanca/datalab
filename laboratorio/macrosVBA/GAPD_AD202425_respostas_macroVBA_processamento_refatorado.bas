Attribute VB_Name = "Module1"
' =====================================================================================
' MACRO: ReorganizarDadosAvaliacao
' OBJETIVO: Reorganizar dados de avaliação, converter escalas textuais para numéricas,
'           inserir separadores visuais entre seções e aplicar formatação padronizada.
' ESTRUTURA:
'   1. Configurações Iniciais
'   2. Processamento de Dados
'   3. Pós-Processamento e Formatação
' =====================================================================================

Option Explicit

Sub ReordenarColunasComConversaovCGPT()
    ' Declaração de variáveis
    Dim wsOrigem As Worksheet, wsDestino As Worksheet
    Dim dictConversao As Object
    Dim tiposRelacao() As Variant
    
    ' Configurações iniciais
    InicializarAplicacao
    
    ' Etapa 1/3: Configurar componentes principais
    Set dictConversao = CriarDicionarioConversao()
    tiposRelacao = Array("autoavaliação", "liderado", "colega gestor", "diretor")
    Set wsOrigem = ThisWorkbook.ActiveSheet
    Set wsDestino = CriarPlanilhaDestino(wsOrigem)
    
    ' Etapa 2/3: Processamento principal dos dados
    CopiarColunaPerguntas wsOrigem, wsDestino
    ReorganizarColunasPorTipo wsOrigem, wsDestino, tiposRelacao, dictConversao
    RemoverLinhasMetadados wsDestino
    InserirSeparadoresVisuais wsDestino
    
    ' Etapa 3/3: Aplicação de formatação final
    AplicarFormatacaoPadrao wsDestino
    DefinirLarguraColunas wsDestino, 70 ' Largura em pixels
    
    ' Finalização e limpeza
    FinalizarAplicacao wsDestino
End Sub

' =====================================================================================
' MÓDULO: FUNÇÕES DE SUPORTE
' =====================================================================================

Private Sub InicializarAplicacao()
    ' Desativa atualizações de tela e cálculos automáticos para performance
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False
End Sub

Private Function CriarDicionarioConversao() As Object
    ' Mapeia respostas textuais para valores numéricos/null
    Dim dict As Object
    Set dict = CreateObject("Scripting.Dictionary")
    dict.CompareMode = vbTextCompare
    
    With dict
        .Add "Nunca acontece", 1
        .Add "Quase nunca acontece", 2
        .Add "Ocorre de vez em quando", 3
        .Add "Acontece com frequência", 4
        .Add "Acontece o tempo todo", 5
        .Add "Não sei avaliar", "null"
    End With
    
    Set CriarDicionarioConversao = dict
End Function

Private Function CriarPlanilhaDestino(ByRef wsOrigem As Worksheet) As Worksheet
    ' Cria nova planilha com nome único baseado em timestamp
    Dim wsNovo As Worksheet
    Set wsNovo = ThisWorkbook.Sheets.Add(After:=wsOrigem)
    wsNovo.Name = "Dados_Reorganizados_" & Format(Now, "yymmdd_hhnn")
    Set CriarPlanilhaDestino = wsNovo
End Function

' =====================================================================================
' MÓDULO: PROCESSAMENTO DE DADOS
' =====================================================================================

Private Sub CopiarColunaPerguntas(ByRef origem As Worksheet, ByRef destino As Worksheet)
    ' Copia a coluna de perguntas (coluna A) para a planilha destino
    Dim ultimaLinha As Long
    ultimaLinha = origem.Cells(origem.Rows.Count, 1).End(xlUp).Row
    origem.Range(origem.Cells(1, 1), origem.Cells(ultimaLinha, 1)).Copy destino.Range("A1")
End Sub

Private Sub ReorganizarColunasPorTipo(ByRef origem As Worksheet, ByRef destino As Worksheet, _
                                      tipos() As Variant, dict As Object)
    ' Reorganiza colunas por categoria de relacionamento e converte valores
    Dim ultimaColuna As Long, novaColunaIndex As Long
    Dim tipo As Variant, j As Long
    
    ultimaColuna = origem.Cells(1, origem.Columns.Count).End(xlToLeft).Column
    novaColunaIndex = 2 ' Inicia após coluna de perguntas
    
    For Each tipo In tipos
        For j = 2 To ultimaColuna
            If ColunaPertenceAoRelacionamento(origem.Cells(1, j), tipo) Then
                ProcessarColuna origem, destino, j, novaColunaIndex, dict
                novaColunaIndex = novaColunaIndex + 1
            End If
        Next j
    Next tipo
End Sub

Private Function ColunaPertenceAoRelacionamento(ByRef celCabecalho As Range, tipo As Variant) As Boolean
    ' Verifica se o cabeçalho da coluna contém o tipo de relacionamento
    ColunaPertenceAoRelacionamento = InStr(1, celCabecalho.Value, tipo, vbTextCompare) > 0
End Function

Private Sub ProcessarColuna(ByRef origem As Worksheet, ByRef destino As Worksheet, _
                            colOrigem As Long, colDestino As Long, dict As Object)
    ' Copia e converte uma coluna individual
    Dim ultimaLinha As Long, i As Long
    Dim keepAsText As String
    
    keepAsText = "Response Type,Start Date (UTC),Stage Date (UTC),Submit Date (UTC)," & _
                 "Network ID,Tags,Coisas para manter,Coisas para melhorar,sua relação com"
    
    ' Copia dados brutos
    origem.Range(origem.Cells(1, colOrigem), origem.Cells(origem.Rows.Count, colOrigem).End(xlUp)) _
        .Copy destino.Cells(1, colDestino)
    
    ' Aplica conversão se necessário
    If Not DeveManterComoTexto(destino.Cells(1, colDestino), keepAsText) Then
        ultimaLinha = destino.Cells(destino.Rows.Count, colDestino).End(xlUp).Row
        For i = 2 To ultimaLinha
            ConverterValorCelula destino.Cells(i, colDestino), dict
        Next i
    End If
End Sub

Private Function DeveManterComoTexto(ByRef celCabecalho As Range, listaCampos As String) As Boolean
    ' Determina se a coluna deve permanecer como texto baseado no cabeçalho
    DeveManterComoTexto = InStr(1, listaCampos, celCabecalho.Value, vbTextCompare) > 0
End Function

Private Sub ConverterValorCelula(ByRef cel As Range, dict As Object)
    ' Converte valor textual para numérico ou null
    Dim valor As String
    valor = Trim(cel.Text)
    
    Select Case True
        Case dict.Exists(valor)
            cel.Value = dict(valor)
            ' Correção: Substituir If por IIF ou estrutura condicional
            If dict(valor) = "null" Then
                cel.NumberFormat = "@"
            Else
                cel.NumberFormat = "0"
            End If
            
        Case valor = ""
            cel.Value = "null"
            cel.NumberFormat = "@"
            
        Case Else
            ' Mantém valor original se não encontrado no dicionário
    End Select
End Sub

' =====================================================================================
' MÓDULO: PÓS-PROCESSAMENTO
' =====================================================================================

Private Sub RemoverLinhasMetadados(ByRef ws As Worksheet)
    ' Remove linhas com metadados técnicos
    Dim linhasParaExcluir As Variant, rowIndex As Long
    linhasParaExcluir = Array("Response Type", "Start Date (UTC)", "Stage Date (UTC)", _
                              "Submit Date (UTC)", "Network ID", "Tags")
    
    For rowIndex = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row To 1 Step -1
        If DeveExcluirLinha(ws.Cells(rowIndex, 1), linhasParaExcluir) Then
            ws.Rows(rowIndex).Delete
        End If
    Next rowIndex
End Sub

Private Function DeveExcluirLinha(ByRef cel As Range, listaExclusao As Variant) As Boolean
    ' Verifica se a linha contém um dos valores de exclusão
    DeveExcluirLinha = Not IsError(Application.Match(cel.Value, listaExclusao, 0))
End Function

Private Sub InserirSeparadoresVisuais(ByRef ws As Worksheet)
    ' Insere linhas de cabeçalho como separadores entre seções
    InsertBlankLinesAfterSections ws
End Sub

' =====================================================================================
' MÓDULO: FORMATAÇÃO
' =====================================================================================

Private Sub AplicarFormatacaoPadrao(ByRef ws As Worksheet)
    ' Aplica formatação visual consistente
    With ws.Range("A1").CurrentRegion
        .Columns.AutoFit
        .Font.Name = "Courier New"
        With .Rows(1)
            .Font.Bold = True
            .Interior.Color = RGB(240, 240, 240)
        End With
    End With
    
    ' Garante fonte uniforme em todas as células
    ws.Cells.Font.Name = "Courier New"
End Sub

Private Sub DefinirLarguraColunas(ByRef ws As Worksheet, larguraPixels As Long)
    ' Define largura uniforme para todas as colunas
    Dim col As Long, larguraPontos As Double
    larguraPontos = larguraPixels / 7.5 ' Conversão pixels para pontos
    
    For col = 1 To ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column
        ws.Columns(col).ColumnWidth = larguraPontos
    Next col
End Sub

' =====================================================================================
' MÓDULO: FINALIZAÇÃO
' =====================================================================================

Private Sub FinalizarAplicacao(ByRef wsDestino As Worksheet)
    ' Restaura configurações do Excel e exibe feedback
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    Application.EnableEvents = True
    
    wsDestino.Activate
    MsgBox "Processo concluído com sucesso:" & vbNewLine & _
           "- " & wsDestino.Name & " criada" & vbNewLine & _
           "- Dados convertidos e formatados", vbInformation
End Sub

' =====================================================================================
' COMPONENTE: InsertBlankLinesAfterSections (com comentários detalhados)
' =====================================================================================

Private Sub InsertBlankLinesAfterSections(ByRef ws As Worksheet)
    ' Insere linhas de cabeçalho como separadores entre seções
    ' Estratégia: Processamento reverso para manter integridade dos índices
    
    Dim sectionHeaders As Variant
    Dim lastRow As Long, currentRow As Long
    Dim Header As Variant, headerProcessed As Boolean
    
    ' Configurações
    sectionHeaders = Array("Coisas para manter sobre", "Coisas para melhorar sobre")
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    headerProcessed = False
    
    ' Loop reverso para evitar interferência nas linhas não processadas
    For currentRow = lastRow To 1 Step -1
        For Each Header In sectionHeaders
            ' Verifica correspondência parcial no início do texto
            If InStr(1, ws.Cells(currentRow, 1).Value, Header, vbTextCompare) > 0 Then
                If Not headerProcessed Then
                    ' Insere linha com cabeçalho formatado
                    ws.Rows(currentRow + 1).Insert
                    ws.Rows(1).Copy Destination:=ws.Rows(currentRow + 1)
                    ws.Rows(currentRow + 1).Interior.Color = RGB(200, 200, 200)
                    headerProcessed = True
                End If
                Exit For
            End If
        Next Header
        
        ' Reset do controle de processamento ao sair da seção
        If Not IsHeader(ws.Cells(currentRow, 1).Value, sectionHeaders) Then
            headerProcessed = False
        End If
    Next currentRow
End Sub

Private Function IsHeader(ByVal cellValue As String, headers As Variant) As Boolean
    ' Função auxiliar para verificação de cabeçalhos
    Dim Header As Variant
    For Each Header In headers
        If InStr(1, cellValue, Header, vbTextCompare) > 0 Then
            IsHeader = True
            Exit Function
        End If
    Next Header
    IsHeader = False
End Function

