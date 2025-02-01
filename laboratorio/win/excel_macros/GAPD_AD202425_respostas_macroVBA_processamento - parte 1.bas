Attribute VB_Name = "Module2"
' =================================================================
' Macro: ReordenarColunasComConversaovGPT
' Objetivo: Reorganizar colunas e converter dados de avalia��o
' preservando formatos espec�ficos e padr�es visuais
' =================================================================

Sub ReordenarColunasComConversaovCGPT()
    ' Declara��o de vari�veis para manipula��o de planilhas
    Dim wsOrigem As Worksheet, wsDestino As Worksheet
    Dim dict As Object
    Dim headerRange As Range, cell As Range
    Dim ultimaLinha As Long, ultimaColuna As Long
    Dim i As Long, j As Long, k As Long
    Dim originalData As Variant
    Dim novoHeaders() As String
    Dim novaColunaIndex As Long
    
    ' ----------------------------------------------------------------
    ' Configura��o do dicion�rio para convers�o de valores
    ' Mapeia textos para valores num�ricos conforme escala definida
    ' ----------------------------------------------------------------
    Set dict = CreateObject("Scripting.Dictionary")
    dict.CompareMode = vbTextCompare
    dict("Nunca acontece") = 1
    dict("Quase nunca acontece") = 2
    dict("Ocorre de vez em quando") = 3
    dict("Acontece com frequ�ncia") = 4
    dict("Acontece o tempo todo") = 5
    dict("N�o sei avaliar") = "null"
    
    ' ----------------------------------------------------------------
    ' Define campos que devem permanecer como texto
    ' Evita convers�o indevida de campos espec�ficos
    ' ----------------------------------------------------------------
    Dim keepAsText As String
    keepAsText = "Response Type,Start Date (UTC),Stage Date (UTC),Submit Date (UTC),Network ID,Tags," & _
                 "Coisas para manter,Coisas para melhorar,sua rela��o com"
    
    ' Define planilha de origem como a planilha ativa
    Set wsOrigem = ThisWorkbook.ActiveSheet
    
    ' ----------------------------------------------------------------
    ' Determina as dimens�es da planilha de origem
    ' Encontra �ltima linha e �ltima coluna com dados
    ' ----------------------------------------------------------------
    ultimaLinha = wsOrigem.Cells(wsOrigem.Rows.Count, 1).End(xlUp).Row
    ultimaColuna = wsOrigem.Cells(1, wsOrigem.Columns.Count).End(xlToLeft).Column
    
    ' ----------------------------------------------------------------
    ' Cria nova planilha para os dados reorganizados
    ' Nome inclui timestamp para identifica��o �nica
    ' ----------------------------------------------------------------
    Set wsDestino = ThisWorkbook.Sheets.Add(After:=wsOrigem)
    wsDestino.Name = "Dados_Reorganizados_" & Format(Now, "yymmdd_hhnn")
    
    ' Copia primeira coluna (perguntas) para a nova planilha
    wsOrigem.Range(wsOrigem.Cells(1, 1), wsOrigem.Cells(ultimaLinha, 1)).Copy _
        Destination:=wsDestino.Range("A1")
    
    ' ----------------------------------------------------------------
    ' Define ordem de reorganiza��o das colunas
    ' Sequ�ncia: autoavalia��o, liderado, colega gestor, diretor
    ' ----------------------------------------------------------------
    Dim tiposRelacao As Variant
    tiposRelacao = Array("autoavalia��o", "liderado", "colega gestor", "diretor")
    
    novaColunaIndex = 2 ' Inicia ap�s a coluna de perguntas
    
    ' ----------------------------------------------------------------
    ' Loop principal: processa cada tipo de rela��o
    ' Reorganiza e converte dados conforme necess�rio
    ' ----------------------------------------------------------------
    For Each tipo In tiposRelacao
        ' Busca colunas do tipo atual
        For j = 2 To ultimaColuna
            If InStr(1, wsOrigem.Cells(1, j).Value, tipo, vbTextCompare) > 0 Then
                ' Copia coluna completa
                wsOrigem.Range(wsOrigem.Cells(1, j), wsOrigem.Cells(ultimaLinha, j)).Copy _
                    Destination:=wsDestino.Cells(1, novaColunaIndex)
                
                ' Processa cada c�lula da coluna
                For i = 2 To ultimaLinha
                    Dim valorAtual As String
                    Dim celulaDestino As Range
                    Set celulaDestino = wsDestino.Cells(i, novaColunaIndex)
                    
                    valorAtual = Trim(celulaDestino.Text)
                    
                    ' Verifica se deve manter como texto
                    If i = 1 Or InStr(1, keepAsText, wsDestino.Cells(1, novaColunaIndex).Value, vbTextCompare) > 0 Then
                        celulaDestino.NumberFormat = "@"
                    Else
                        ' Converte valores conforme dicion�rio
                        If dict.exists(valorAtual) Then
                            If dict(valorAtual) = "null" Then
                                celulaDestino.Value = "null"
                                celulaDestino.NumberFormat = "@"
                            Else
                                celulaDestino.Value = dict(valorAtual)
                                celulaDestino.NumberFormat = "0"
                            End If
                        ElseIf Trim(valorAtual) = "" Then
                            ' Trata c�lulas vazias
                            celulaDestino.Value = "null"
                            celulaDestino.NumberFormat = "@"
                        End If
                    End If
                Next i
                
                novaColunaIndex = novaColunaIndex + 1
            End If
        Next j
    Next tipo

    ' ----------------------------------------------------------------
    ' REMOVE LINHAS INDESEJADAS (Response Type, Start Date, etc.)
    ' ----------------------------------------------------------------
    Dim linhasParaExcluir As Variant
    Dim cel As Range
    Dim rowIndex As Long ' Substitui "i" por "rowIndex" para evitar conflitos
    
    linhasParaExcluir = Array("Response Type", "Start Date (UTC)", "Stage Date (UTC)", "Submit Date (UTC)", "Network ID", "Tags")
    
    ' Loop reverso para exclus�o segura
    For rowIndex = wsDestino.Cells(wsDestino.Rows.Count, 1).End(xlUp).Row To 1 Step -1
        Set cel = wsDestino.Cells(rowIndex, 1)
        If Not IsError(Application.Match(cel.Value, linhasParaExcluir, 0)) Then
            wsDestino.Rows(rowIndex).Delete
        End If
    Next rowIndex

    ' ----------------------------------------------------------------
    ' Formata��o visual da planilha resultante
    ' Aplica estilos e formatos consistentes
    ' ----------------------------------------------------------------
    With wsDestino.Range("A1").CurrentRegion
        ' Remove AutoFit anterior
        .Columns.AutoFit
        ' Define fonte padr�o
        .Font.Name = "Courier New"
        
        ' Formata cabe�alho
        With .Rows(1)
            .Font.Bold = True
            .WrapText = False
            .Font.Name = "Courier New"
            .Interior.Color = RGB(240, 240, 240)
        End With
    End With
    
    ' Garante fonte Courier New em toda a planilha
    wsDestino.Cells.Font.Name = "Courier New"
    
    ' ----------------------------------------------------------------
    ' Define largura padr�o para todas as colunas
    ' Converte 70 pixels para pontos (unidade do Excel)
    ' ----------------------------------------------------------------
    Dim larguraEmPontos As Double
    larguraEmPontos = 70 / 7.5
    
    ' Aplica largura padr�o em todas as colunas
    Dim col As Long
    For col = 1 To ultimaColuna
        wsDestino.Columns(col).ColumnWidth = larguraEmPontos
    Next col
    
    ' ----------------------------------------------------------------
    ' Exibe mensagem de conclus�o com resumo das a��es realizadas
    ' ----------------------------------------------------------------
    MsgBox "Reorganiza��o e convers�o conclu�das!" & vbNewLine & _
           "- Valores num�ricos configurados para c�lculos" & vbNewLine & _
           "- C�lulas vazias preenchidas com 'null'" & vbNewLine & _
           "- Fonte configurada como Courier New", vbInformation
End Sub


