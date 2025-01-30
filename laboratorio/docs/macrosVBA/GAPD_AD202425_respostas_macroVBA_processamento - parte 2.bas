Attribute VB_Name = "Module1"
Sub InsertBlankLinesAfterSections_CORRIGIDO()
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim currentRow As Long
    Dim sectionHeaders As Variant
    Dim Header As Variant
    Dim headerProcessed As Boolean
    
    Application.ScreenUpdating = False
    
    Set ws = ThisWorkbook.Sheets("Dados_Reorganizados_250125_2117")
    
    If ws.ProtectContents Then
        MsgBox "Desproteja a planilha antes de executar a macro.", vbExclamation
        Exit Sub
    End If
    
    ' Define os cabeçalhos de seção
    sectionHeaders = Array("Coisas para manter sobre", "Coisas para melhorar sobre")
    
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    headerProcessed = False
    
    For currentRow = lastRow To 1 Step -1
        For Each Header In sectionHeaders
            ' Verifica se a célula contém um cabeçalho de seção
            If InStr(1, ws.Cells(currentRow, 1).Value, Header, vbTextCompare) > 0 Then
                If Not headerProcessed Then
                    ' Insere uma linha após o cabeçalho
                    ws.Rows(currentRow + 1).Insert
                    headerProcessed = True
                End If
                Exit For
            End If
        Next Header
        
        ' Reseta a flag se a linha atual NÃO é um cabeçalho
        If Not IsHeader(ws.Cells(currentRow, 1).Value, sectionHeaders) Then
            headerProcessed = False
        End If
    Next currentRow
    
    Application.ScreenUpdating = True
    MsgBox "Linha em branco inserida após cada seção.", vbInformation
End Sub

' Função auxiliar para verificar se uma célula é um cabeçalho
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
