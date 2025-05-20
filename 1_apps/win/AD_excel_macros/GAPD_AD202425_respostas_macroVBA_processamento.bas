Option Explicit

' =================================================================
' Macro principal
' =================================================================
Public Sub ReordenarColunasComConversaovCGPT_Flexivel_Corrigido()
    Dim wsO As Worksheet, wsD As Worksheet
    Dim ultimaLinha As Long, ultimaColuna As Long
    Dim i As Long, j As Long, novaColIndex As Long
    Dim tipo As Variant, raw As String, mappedVal As Variant
    Dim keepTxt As String

    Application.ScreenUpdating = False

    keepTxt = "Response Type,Start Date (UTC),Stage Date (UTC)," & _
              "Submit Date (UTC),Network ID,Tags," & _
              "Coisas para manter,Coisas para melhorar,sua relaÃ§Ã£o com"

    Set wsO = ThisWorkbook.ActiveSheet
    If wsO Is Nothing Then
        MsgBox "Nenhuma planilha ativa encontrada.", vbExclamation
        Exit Sub
    End If
    
    ultimaLinha = wsO.Cells(wsO.Rows.Count, 1).End(xlUp).Row
    ultimaColuna = wsO.Cells(1, wsO.Columns.Count).End(xlToLeft).Column

    If ultimaLinha <= 1 And IsEmpty(wsO.Cells(1, 1).Value) Then
        MsgBox "A planilha de origem parece estar vazia.", vbInformation
        Exit Sub
    End If

    Set wsD = ThisWorkbook.Sheets.Add(After:=wsO)
    wsD.Name = "Dados_Flex_" & Format(Now, "yymmdd_hhnnss") ' Adicionado segundos para evitar conflito de nome

    ' Copia perguntas (coluna A inteira da origem para destino)
    wsO.Range("A1:A" & ultimaLinha).Copy Destination:=wsD.Range("A1")

    novaColIndex = 2 ' ComeÃ§a a preencher a partir da coluna B na planilha de destino
    For Each tipo In Array("autoavaliaÃ§Ã£o", "liderado", "colega gestor", "diretor")
        For j = 2 To ultimaColuna ' Itera pelas colunas da planilha de origem (a partir da B)
            ' Verifica se o cabeÃ§alho da coluna na origem contÃ©m o 'tipo' atual
            If InStr(1, CStr(wsO.Cells(1, j).Value), CStr(tipo), vbTextCompare) > 0 Then
                ' Copia a coluna inteira da origem para a nova posiÃ§Ã£o na destino
                wsO.Range(wsO.Cells(1, j), wsO.Cells(ultimaLinha, j)).Copy Destination:=wsD.Cells(1, novaColIndex)
                
                ' Processa as respostas na coluna recÃ©m-copiada na planilha de destino
                For i = 2 To ultimaLinha ' ComeÃ§a da linha 2 para pular o cabeÃ§alho
                    raw = CStr(wsD.Cells(i, novaColIndex).Value2)
                    mappedVal = MapResponse(raw)
                    
                    With wsD.Cells(i, novaColIndex)
                        .Value = mappedVal
                        ' Verifica se o cabeÃ§alho desta coluna estÃ¡ na lista 'keepTxt'
                        ' OU se o valor mapeado nÃ£o Ã© numÃ©rico. Se sim, formata como Texto.
                        If InStr(1, keepTxt, CStr(wsD.Cells(1, novaColIndex).Value), vbTextCompare) > 0 _
                           Or Not IsNumeric(mappedVal) Then
                            .NumberFormat = "@" ' Formato Texto
                        Else
                            .NumberFormat = "0"  ' Formato NÃºmero (sem casas decimais)
                        End If
                    End With
                Next i
                novaColIndex = novaColIndex + 1 ' Prepara para a prÃ³xima coluna na planilha de destino
            End If
        Next j
    Next tipo

    ' Remove linhas de metadados se existirem
    Call RemoveMetadataLines(wsD)

    ' Insere linhas em branco entre seÃ§Ãµes especÃ­ficas, se encontradas
    Call InsertBlankLinesAfterSections(wsD)

    ' FormataÃ§Ã£o final da planilha de destino
    If wsD.Cells(1, 1).Value <> "" Then ' SÃ³ formata se houver dados
        With wsD.Range("A1").CurrentRegion
            .Columns.AutoFit
            .Font.Name = "Courier New"
            With .Rows(1)
                .Font.Bold = True
                .Interior.Color = RGB(240, 240, 240)
            End With
        End With
        Call AdjustColumnWidths(wsD) ' Aplica largura de coluna padronizada
        wsD.Cells.Font.Name = "Courier New" ' Garante a fonte para todas as cÃ©lulas
    End If

    Application.ScreenUpdating = True
    MsgBox "ConcluÃ­do com conversÃ£o por regex flexÃ­vel (corrigido).", vbInformation
End Sub

' =================================================================
' Mapeia resposta usando regex
' =================================================================
Public Function MapResponse(ByVal resp As String) As Variant
    Dim norm As String
    norm = NormalizeResponse(resp)
    
    If Len(norm) = 0 Then
        MapResponse = "null": Exit Function ' Retorna "null" para respostas vazias apÃ³s normalizaÃ§Ã£o
    End If

    ' Teste de padrÃµes em ordem de especificidade
    If RegexTest(norm, "\bnunca.*acontece\b") Then
        MapResponse = 1
    ElseIf RegexTest(norm, "\bquase.*nunca.*acontece\b") Then
        MapResponse = 2
    ElseIf RegexTest(norm, "\bocorre.*vez.*em.*quando\b") Then
        MapResponse = 3
    ElseIf RegexTest(norm, "\bacontece com frequencia\b") Then ' <<< PATCH APLICADO AQUI
        MapResponse = 4
    ElseIf RegexTest(norm, "\bacontece.*tempo.*todo\b") Then
        MapResponse = 5
    ElseIf RegexTest(norm, "\bnao.*sei.*avaliar\b") Then
        MapResponse = "null"
    Else
        MapResponse = resp ' Se nenhum padrÃ£o corresponder, retorna a resposta original
    End If
End Function

' =================================================================
' Normaliza texto (lower, remove acentos, chars especiais, espaÃ§os)
' =================================================================
Public Function NormalizeResponse(ByVal txt As String) As String
    Dim s As String, i As Long
    Dim fromChars As String, toChars As String

    s = LCase$(txt)
    s = Replace(s, Chr(160), " ") ' Non-breaking space
    s = Replace(s, vbTab, " ")
    s = Replace(s, vbCrLf, " ")
    s = Replace(s, vbCr, " ")
    s = Replace(s, vbLf, " ")

    fromChars = "Ã¡Ã Ã£Ã¢Ã¤Ã©Ã¨ÃªÃ«Ã­Ã¬Ã®Ã¯Ã³Ã²ÃµÃ´Ã¶ÃºÃ¹Ã»Ã¼Ã§Ã±"
    toChars = "aaaaaeeeeiiiiooooouuuucn"
    For i = 1 To Len(fromChars)
        s = Replace(s, Mid$(fromChars, i, 1), Mid$(toChars, i, 1))
    Next i

    ' Remove tudo que nÃ£o for a-z, 0-9 ou espaÃ§o
    ' Ã‰ importante que esta etapa venha depois da remoÃ§Ã£o de acentos
    Dim rgx As Object
    Set rgx = CreateObject("VBScript.RegExp")
    With rgx
        .Global = True
        .IgnoreCase = False ' JÃ¡ estÃ¡ em minÃºsculas
        .pattern = "[^a-z0-9 ]"
        s = .Replace(s, "")
    End With

    s = Trim$(s) ' Remove espaÃ§os no inÃ­cio e fim
    ' Remove espaÃ§os duplos/mÃºltiplos no meio da string
    Do While InStr(s, "  ") > 0
        s = Replace(s, "  ", " ")
    Loop

    NormalizeResponse = s
End Function

' =================================================================
' Testa regex no texto
' =================================================================
Public Function RegexTest(ByVal txt As String, ByVal pattern As String) As Boolean
    Dim rgx As Object
    Set rgx = CreateObject("VBScript.RegExp")
    With rgx
        .Global = False ' Procura apenas a primeira ocorrÃªncia, o que Ã© eficiente para .Test
        .IgnoreCase = True ' Embora o texto normalizado jÃ¡ esteja em minÃºsculas, Ã© uma boa prÃ¡tica
        .pattern = pattern
        RegexTest = .Test(txt)
    End With
End Function

' =================================================================
' Remove linhas de metadados
' =================================================================
Private Sub RemoveMetadataLines(ws As Worksheet)
    Dim arr As Variant, r As Long, lastRowCheck As Long
    arr = Array("Response Type", "Start Date (UTC)", "Stage Date (UTC)", _
                "Submit Date (UTC)", "Network ID", "Tags")
    
    lastRowCheck = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    
    For r = lastRowCheck To 1 Step -1 ' Itera de baixo para cima para evitar problemas ao deletar linhas
        If Not IsError(Application.Match(CStr(ws.Cells(r, 1).Value), arr, 0)) Then
            ws.Rows(r).Delete
        End If
    Next r
End Sub

' =================================================================
' Insere linhas em branco e cabeÃ§alhos de seÃ§Ã£o
' =================================================================
Public Sub InsertBlankLinesAfterSections(ws As Worksheet)
    Dim lastRow As Long, cur As Long, hdrs As Variant, h As Variant
    Dim processedSectionHeader As Boolean ' Renomeado para clareza
    
    hdrs = Array("Coisas para manter sobre", "Coisas para melhorar sobre")
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    
    processedSectionHeader = False ' Flag para controlar a inserÃ§Ã£o de apenas um cabeÃ§alho por seÃ§Ã£o
    
    ' Itera de baixo para cima para facilitar a inserÃ§Ã£o de linhas sem afetar Ã­ndices de loop
    For cur = lastRow To 1 Step -1
        Dim currentCellValue As String
        currentCellValue = CStr(ws.Cells(cur, 1).Value)
        
        Dim isKnownHeader As Boolean
        isKnownHeader = False
        
        For Each h In hdrs
            If InStr(1, currentCellValue, CStr(h), vbTextCompare) > 0 Then
                isKnownHeader = True
                If Not processedSectionHeader Then
                    ' Insere uma nova linha abaixo da linha do cabeÃ§alho da seÃ§Ã£o
                    ws.Rows(cur + 1).Insert
                    ' Copia o formato e conteÃºdo da primeira linha (cabeÃ§alho principal) para esta nova linha
                    ws.Rows(1).Copy Destination:=ws.Rows(cur + 1)
                    ' Aplica uma cor de fundo diferente para o cabeÃ§alho da seÃ§Ã£o inserido
                    ws.Rows(cur + 1).Interior.Color = RGB(200, 200, 200)
                    ws.Rows(cur + 1).Font.Bold = True ' Opcional: diferenciar do cabeÃ§alho principal
                    
                    processedSectionHeader = True ' Marca que um cabeÃ§alho foi inserido para esta seÃ§Ã£o
                End If
                Exit For ' Sai do loop de hdrs, pois jÃ¡ encontrou um correspondente
            End If
        Next h
        
        ' Se a linha atual NÃƒO Ã© um dos cabeÃ§alhos de seÃ§Ã£o conhecidos,
        ' reseta a flag para permitir que o prÃ³ximo cabeÃ§alho de seÃ§Ã£o seja processado.
        If Not isKnownHeader Then
            processedSectionHeader = False
        End If
    Next cur
End Sub

' =================================================================
' Ajusta largura de colunas para um valor fixo (aproximado)
' =================================================================
Private Sub AdjustColumnWidths(ws As Worksheet)
    Dim ptWidth As Double, c As Long, lastColData As Long
    
    ' Define a largura desejada em pontos (ex: 70) e converte para unidades de largura de coluna do Excel.
    ' A conversÃ£o exata pode variar ligeiramente com a fonte padrÃ£o, mas 7.5 Ã© uma aproximaÃ§Ã£o comum.
    ' O valor "70 / 7.5" parece arbitrÃ¡rio. Uma largura padrÃ£o de Excel Ã© ~8.43 para Calibri 11.
    ' Para "Courier New", a largura dos caracteres Ã© mais uniforme.
    ' Vamos usar uma largura que acomode uns 10-12 caracteres de Courier New, por exemplo, 12.
    ptWidth = 12 ' Ajuste este valor conforme necessÃ¡rio para Courier New.

    lastColData = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column
    If lastColData > 0 And ws.Cells(1, 1).Value <> "" Then ' SÃ³ ajusta se houver colunas
        For c = 1 To lastColData
            ws.Columns(c).ColumnWidth = ptWidth
        Next c
    End If
End Sub

