Attribute VB_Name = "Module1"
' =================================================================
' Macro: ReordenarColunasComConversaovCGPT
' Objetivo: Reorganizar colunas, converter dados e inserir linhas em branco ap�s se��es
' =================================================================
Sub ReordenarColunasComConversaovCGPT()
    ' Declara��o de vari�veis
    Dim wsOrigem As Worksheet, wsDestino As Worksheet
    Dim dict As Object
    Dim ultimaLinha As Long, ultimaColuna As Long
    Dim i As Long, j As Long, novaColunaIndex As Long, rowIndex As Long, col As Long
    Dim keepAsText As String, valorAtual As String
    Dim tiposRelacao As Variant, tipo As Variant
    Dim linhasParaExcluir As Variant, cel As Range
    Dim larguraEmPontos As Double
    
    ' Configura��o inicial
    Application.ScreenUpdating = False
    Set dict = CreateObject("Scripting.Dictionary")
    
    ' Configura��o do dicion�rio de convers�o
    dict.CompareMode = vbTextCompare
    dict("Nunca acontece") = 1
    dict("Quase nunca acontece") = 2
    dict("Ocorre de vez em quando") = 3
    dict("Acontece com frequ�ncia") = 4
    dict("Acontece o tempo todo") = 5
    dict("N�o sei avaliar") = "null"
    
    ' Campos que permanecem como texto
    keepAsText = "Response Type,Start Date (UTC),Stage Date (UTC),Submit Date (UTC),Network ID,Tags," & _
                 "Coisas para manter,Coisas para melhorar,sua rela��o com"
    
    ' Define planilha de origem
    Set wsOrigem = ThisWorkbook.ActiveSheet
    
    ' Determina dimens�es da planilha
    ultimaLinha = wsOrigem.Cells(wsOrigem.Rows.Count, 1).End(xlUp).Row
    ultimaColuna = wsOrigem.Cells(1, wsOrigem.Columns.Count).End(xlToLeft).Column
    
    ' Cria planilha de destino
    Set wsDestino = ThisWorkbook.Sheets.Add(After:=wsOrigem)
    wsDestino.Name = "Dados_Reorganizados_" & Format(Now, "yymmdd_hhnn")
    
    ' Copia coluna de perguntas
    wsOrigem.Range(wsOrigem.Cells(1, 1), wsOrigem.Cells(ultimaLinha, 1)).Copy Destination:=wsDestino.Range("A1")
    
    ' Reorganiza colunas por tipo de rela��o
    tiposRelacao = Array("autoavalia��o", "liderado", "colega gestor", "diretor")
    novaColunaIndex = 2
    
    For Each tipo In tiposRelacao
        For j = 2 To ultimaColuna
            If InStr(1, wsOrigem.Cells(1, j).Value, tipo, vbTextCompare) > 0 Then
                ' Copia e converte dados
                wsOrigem.Range(wsOrigem.Cells(1, j), wsOrigem.Cells(ultimaLinha, j)).Copy Destination:=wsDestino.Cells(1, novaColunaIndex)
                
                For i = 2 To ultimaLinha
                    valorAtual = Trim(wsDestino.Cells(i, novaColunaIndex).Text)
                    
                    If InStr(1, keepAsText, wsDestino.Cells(1, novaColunaIndex).Value, vbTextCompare) > 0 Then
                        wsDestino.Cells(i, novaColunaIndex).NumberFormat = "@"
                    Else
                        If dict.exists(valorAtual) Then
                            If dict(valorAtual) = "null" Then
                                wsDestino.Cells(i, novaColunaIndex).Value = "null"
                                wsDestino.Cells(i, novaColunaIndex).NumberFormat = "@"
                            Else
                                wsDestino.Cells(i, novaColunaIndex).Value = dict(valorAtual)
                                wsDestino.Cells(i, novaColunaIndex).NumberFormat = "0"
                            End If
                        ElseIf Trim(valorAtual) = "" Then
                            wsDestino.Cells(i, novaColunaIndex).Value = "null"
                            wsDestino.Cells(i, novaColunaIndex).NumberFormat = "@"
                        End If
                    End If
                Next i
                
                novaColunaIndex = novaColunaIndex + 1
            End If
        Next j
    Next tipo
    
    ' Remove linhas indesejadas
    linhasParaExcluir = Array("Response Type", "Start Date (UTC)", "Stage Date (UTC)", "Submit Date (UTC)", "Network ID", "Tags")
    For rowIndex = wsDestino.Cells(wsDestino.Rows.Count, 1).End(xlUp).Row To 1 Step -1
        Set cel = wsDestino.Cells(rowIndex, 1)
        If Not IsError(Application.Match(cel.Value, linhasParaExcluir, 0)) Then
            wsDestino.Rows(rowIndex).Delete
        End If
    Next rowIndex
    
    ' Insere linhas em branco ap�s se��es
    InsertBlankLinesAfterSections wsDestino
    
    ' Formata��o final
    With wsDestino.Range("A1").CurrentRegion
        .Columns.AutoFit
        .Font.Name = "Courier New"
        With .Rows(1)
            .Font.Bold = True
            .Interior.Color = RGB(240, 240, 240)
        End With
    End With
    
    ' Define largura das colunas
    larguraEmPontos = 70 / 7.5
    For col = 1 To wsDestino.Cells(1, wsDestino.Columns.Count).End(xlToLeft).Column
        wsDestino.Columns(col).ColumnWidth = larguraEmPontos
    Next col
    
    ' ============== INSER��O 2: FONTE PARA TODAS AS C�LULAS ==============
    wsDestino.Cells.Font.Name = "Courier New"
    ' ======================================================================
    
    ' Finaliza��o
    Application.ScreenUpdating = True
    MsgBox "Processo conclu�do: Dados reorganizados, convertidos e linhas em branco inseridas.", vbInformation
End Sub

' =================================================================
' Fun��o: InsertBlankLinesAfterSections
' Objetivo: Insere uma linha em branco ap�s cada se��o identificada
' =================================================================
Sub InsertBlankLinesAfterSections(ws As Worksheet)
    Dim lastRow As Long, currentRow As Long
    Dim sectionHeaders As Variant, Header As Variant
    Dim headerProcessed As Boolean
    
    sectionHeaders = Array("Coisas para manter sobre", "Coisas para melhorar sobre")
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    headerProcessed = False
    
    For currentRow = lastRow To 1 Step -1
        For Each Header In sectionHeaders
            If InStr(1, ws.Cells(currentRow, 1).Value, Header, vbTextCompare) > 0 Then
                If Not headerProcessed Then
                    ws.Rows(currentRow + 1).Insert
                    ws.Rows(currentRow + 1).Font.Name = "Courier New"  '<--- NOVO
                    headerProcessed = True
                End If
                Exit For
            End If
        Next Header
        
        If Not IsHeader(ws.Cells(currentRow, 1).Value, sectionHeaders) Then
            headerProcessed = False
        End If
    Next currentRow
End Sub

' =================================================================
' Fun��o: IsHeader
' Objetivo: Verifica se uma c�lula cont�m um cabe�alho de se��o
' =================================================================
Function IsHeader(cellValue As String, headers As Variant) As Boolean
    Dim Header As Variant
    For Each Header In headers
        If InStr(1, cellValue, Header, vbTextCompare) > 0 Then
            IsHeader = True
            Exit Function
        End If
    Next Header
    IsHeader = False
End Function

