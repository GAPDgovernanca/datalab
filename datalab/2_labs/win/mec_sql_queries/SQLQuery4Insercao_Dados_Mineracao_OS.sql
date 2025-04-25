/*
==========================================================================================================
    Nome: Insercao_Dados_Mineracao_OS.sql
    Descrição: 
        Este script insere na tabela `MINERACAO_DADOS_OS` do banco `GATEC_MEC_MINERACAO` os dados 
        minerados das ordens de serviço (OS) extraídas do banco `GATEC_MEC`. Ele permite a seleção 
        dinâmica de filtros, incluindo:
        
        - Empresa (`COD_EMPR`).
        - Motivo específico (`COD_MOTIVO`) ou múltiplos motivos a excluir (`COD_MOTIVO_EXCLUIR`).
        - Intervalo de anos de entrada (`ANO_INICIO` e `ANO_FIM`).
        - Se nenhum filtro for especificado, a query insere todas as OS disponíveis.

    Estrutura:
        - Insere dados da OS, equipamentos, motivos, oficinas, e outras informações relevantes.
        - Mantém um campo `DATA_INSERCAO` para registrar a data de carga dos dados.
        - Pode ser executado periodicamente para atualizar os dados minerados.

    Uso:
        1. **Certifique-se de que a tabela `MINERACAO_DADOS_OS` já foi criada** executando 
           o script `Criacao_Tabela_Mineracao_OS.sql`.
        2. Defina os filtros desejados modificando as variáveis `@COD_EMPR`, `@COD_MOTIVO`, etc.
        3. Execute o script para inserir os dados no banco `GATEC_MEC_MINERACAO`.

    Autor: Roni Chittoni
    Data: 20250208
==========================================================================================================
*/


USE GATEC_MEC_MINERACAO;
GO

-- ============================================
-- 🛠️ Declaração das variáveis de parâmetro
-- Essas variáveis permitem personalizar os filtros antes da execução da query
-- Para extrair todos os dados, basta manter os valores como NULL
-- ============================================
DECLARE @COD_EMPR INT = NULL;							-- Filtra por empresa específica (NULL retorna todas)
DECLARE @COD_MOTIVO INT = NULL;						-- Filtra por um motivo específico (NULL retorna todos)
DECLARE @COD_MOTIVO_EXCLUIR VARCHAR(MAX) = NULL;	-- Lista de motivos a serem excluídos (ex: '5,8,12') ou NULL para não excluir nenhum
DECLARE @ANO_INICIO INT = NULL;						-- Define o ano inicial para filtrar OS por data de entrada (NULL retorna desde o primeiro registro)
DECLARE @ANO_FIM INT = NULL;						-- Define o ano final para filtrar OS por data de entrada (NULL retorna até o último registro)

-- ============================================
-- 🚀 Inserção dos dados minerados na tabela
-- Os dados são extraídos do banco `GATEC_MEC` e armazenados em `GATEC_MEC_MINERACAO`
-- Se a tabela `MINERACAO_DADOS_OS` já existir, novos dados serão adicionados sem excluir os antigos
-- ============================================
INSERT INTO MINERACAO_DADOS_OS (
    COD_OS, ROWID, ID_USUARIO, COD_EMPR, COD_FUNC, ID_OS_EQP,
    OS_DT_ENTRADA, OS_DT_SAIDA, OS_DT_COMUNICACAO, OS_DT_PREVISAO,
    OS_OBSERVACAO, OS_STATUS, OS_SITUACAO, OS_TIPO,
    OS_MEDIDOR, OS_MEDIDOR_SAIDA, OS_OPORTUNIDADE,
    COD_EQUIPAMENTO, EQP_ANO_FABRIC, EQP_PLACA,
    COD_MOTIVO, MOTIVO_DESC, COD_OFICINA, OFICINA_DESC
)
SELECT
    -- Identificadores principais
    os.COD_OS,
    os.ROWID,
    os.ID_USUARIO,
    os.COD_EMPR,
    os.COD_FUNC,
	os.ID_OS_EQP,

    -- Datas e Horas
    os.OS_DT_ENTRADA,
    os.OS_DT_SAIDA,
    os.OS_DT_COMUNICACAO,
    os.OS_DT_PREVISAO,

    -- Informações sobre a OS
    os.OS_OBSERVACAO,
    os.OS_STATUS,
    os.OS_SITUACAO,
    os.OS_TIPO,
	os.OS_MEDIDOR,
	os.OS_MEDIDOR_SAIDA,
	os.OS_OPORTUNIDADE,

    -- Dados de Equipamentos
    eq.COD_EQUIPAMENTO,
    eq.EQP_ANO_FABRIC,
    eq.EQP_PLACA,

    -- Dados de Motivos
    mot.COD_MOTIVO,
    mot.DSC_MOTIVO AS MOTIVO_DESC,

    -- Dados de Oficina
    ofi.COD_OFICINA,
    ofi.DSC_OFICINA AS OFICINA_DESC

FROM GATEC_MEC.dbo.GA_OFI_OS os
LEFT JOIN GATEC_MEC.dbo.GA_EQP_EQUIPAMENTO eq ON os.COD_EQUIPAMENTO = eq.COD_EQUIPAMENTO
LEFT JOIN GATEC_MEC.dbo.GA_AGD_AGREGADOS ag ON os.COD_AGREG = ag.AGD_CODIGO
LEFT JOIN GATEC_MEC.dbo.GA_OFI_MOT_ENTRADA mot ON os.COD_MOTIVO = mot.COD_MOTIVO
LEFT JOIN GATEC_MEC.dbo.GA_OFI_OFICINA ofi ON os.COD_OFICINA = ofi.COD_OFICINA

-- ============================================
-- 🎯 Filtros aplicados (parâmetros dinâmicos)
-- Os filtros são opcionais e só serão aplicados caso os valores sejam diferentes de NULL
-- ============================================
WHERE (@COD_EMPR IS NULL OR os.COD_EMPR = @COD_EMPR)  -- Filtra por empresa se um valor for definido
AND (@COD_MOTIVO IS NULL OR os.COD_MOTIVO = @COD_MOTIVO)  -- Filtra por motivo específico se definido
AND (@ANO_INICIO IS NULL OR YEAR(os.OS_DT_ENTRADA) >= @ANO_INICIO)  -- Filtra por ano inicial se definido
AND (@ANO_FIM IS NULL OR YEAR(os.OS_DT_ENTRADA) <= @ANO_FIM)  -- Filtra por ano final se definido
AND (
    @COD_MOTIVO_EXCLUIR IS NULL  -- Se @COD_MOTIVO_EXCLUIR for NULL, não exclui nenhum motivo
    OR os.COD_MOTIVO NOT IN (
        SELECT value FROM STRING_SPLIT(@COD_MOTIVO_EXCLUIR, ',')
    )
)

-- Ordena os resultados por data de entrada da OS para facilitar a análise
ORDER BY os.OS_DT_ENTRADA;
GO
