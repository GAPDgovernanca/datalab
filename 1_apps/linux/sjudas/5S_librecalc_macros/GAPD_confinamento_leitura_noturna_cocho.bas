Option Explicit

'========================
' Configurações
'========================
Const COR_DESTAQ As Long = &H3333FF   ' RGB(255,51,51) em ordem BGR do LibreOffice

'========================
' Entrada principal
'========================
Sub DestacarRecorrencia()
    Dim oSel As Object : oSel = ThisComponent.CurrentSelection
    If oSel Is Nothing Then
        MsgBox "Selecione a matriz.", 48, "Recorrência"
        Exit Sub
    End If
    If Not oSel.supportsService("com.sun.star.sheet.SheetCellRange") Then
        MsgBox "Selecione um intervalo de células da matriz.", 48, "Recorrência"
        Exit Sub
    End If

    Dim n As Long
    n = CLng(InputBox("Comprimento da sequência (ex.: 4 ou 2):", "Recorrência", "4"))
    If n <= 0 Then Exit Sub

    Dim modo As String
    modo = Trim(InputBox("Tipo: '=' para 'igual a N' | '>=' para 'maior ou igual a N'", "Recorrência", "="))

    Dim limpar As Integer
    limpar = MsgBox("Limpar cores prévias no intervalo?", 35, "Recorrência")
    If limpar = 6 Then LimparCoresIntervalo oSel

    ColorirSequencias oSel, n, (modo = ">="), COR_DESTAQ

    MsgBox "Concluído.", 64, "Recorrência"
End Sub

'========================
' Utilitários
'========================
Sub LimparCoresIntervalo(oRange As Object)
    Dim r As Long, c As Long
    For r = 0 To oRange.Rows.Count - 1
        For c = 0 To oRange.Columns.Count - 1
            oRange.getCellByPosition(c, r).CellBackColor = -1  'sem cor
        Next c
    Next r
End Sub

' Núcleo: detecta corridas de 1 por linha e colore apenas as que atendem N
Sub ColorirSequencias(oRange As Object, N As Long, geMode As Boolean, cor As Long)
    Dim R As Long, C As Long, cols As Long, rows As Long
    cols = oRange.Columns.Count
    rows = oRange.Rows.Count

    For R = 0 To rows - 1
        Dim runLen As Long : runLen = 0
        Dim startCol As Long : startCol = -1

        For C = 0 To cols - 1
            Dim v As Double
            v = Valor01(oRange.getCellByPosition(C, R))

            If v = 1 Then
                If runLen = 0 Then startCol = C
                runLen = runLen + 1
            End If

            If (v <> 1) Or (C = cols - 1) Then
                If runLen > 0 Then
                    Dim qualifica As Boolean
                    If geMode Then
                        qualifica = (runLen >= N)
                    Else
                        qualifica = (runLen = N)
                    End If

                    If qualifica Then
                        Dim k As Long, endCol As Long
                        endCol = IIf(v = 1 And C = cols - 1, C, C - 1)
                        For k = startCol To endCol
                            oRange.getCellByPosition(k, R).CellBackColor = cor
                        Next k
                    End If

                    runLen = 0
                    startCol = -1
                End If
            End If
        Next C
    Next R
End Sub

' Converte célula em 0/1 de forma robusta (valor ou texto)
Private Function Valor01(oCell As Object) As Double
    Dim s As String
    If oCell.Type = com.sun.star.table.CellContentType.VALUE Then
        Valor01 = IIf(oCell.Value = 1, 1, 0)
    Else
        s = Trim(oCell.String)
        If s = "1" Then
            Valor01 = 1
        Else
            Valor01 = 0
        End If
    End If
End Function

