Sub ExtrairPrimeiroNumeroSelecionado
    Dim oPlanilha As Object
    Dim oIntervalo As Object
    Dim oCelula As Object
    Dim iLinha As Integer
    Dim iColuna As Integer
    Dim Conteudo As String
    Dim PrimeiroNumero As String
    Dim NumeroFinal As Double
    
    ' Obter a planilha ativa
    oPlanilha = ThisComponent.CurrentController.ActiveSheet
    
    ' Obter o intervalo selecionado pelo usuário
    oIntervalo = ThisComponent.CurrentSelection
    
    ' Verificar se a seleção é válida (apenas células)
    If oIntervalo.supportsService("com.sun.star.sheet.SheetCellRange") Then
        ' Percorrer cada célula no intervalo selecionado
        For iLinha = 0 To oIntervalo.Rows.Count - 1
            For iColuna = 0 To oIntervalo.Columns.Count - 1
                oCelula = oIntervalo.getCellByPosition(iColuna, iLinha)
                Conteudo = oCelula.getString()
                
                ' Resetar variáveis
                PrimeiroNumero = ""
                NumeroFinal = 0
                
                ' Remover apóstrofo inicial, se presente
                If Left(Conteudo, 1) = "'" Then
                    Conteudo = Mid(Conteudo, 2)
                End If
                
                ' Verificar se há conteúdo na célula
                If Conteudo <> "" Then
                    Dim i As Integer
                    For i = 1 To Len(Conteudo)
                        If IsNumeric(Mid(Conteudo, i, 1)) Then
                            PrimeiroNumero = Mid(Conteudo, i, 1) ' Captura o primeiro número encontrado
                            Exit For
                        End If
                    Next i
                End If
                
                ' Converter o número encontrado em um valor numérico real
                If PrimeiroNumero <> "" Then
                    NumeroFinal = CDbl(PrimeiroNumero)
                    oCelula.setValue(NumeroFinal) ' Define o valor como número na célula
                Else
                    oCelula.setString("") ' Limpa caso não tenha encontrado número
                End If
            Next iColuna
        Next iLinha
    Else
        MsgBox "Por favor, selecione um intervalo válido de células.", 16, "Erro de Seleção"
    End If
End Sub

