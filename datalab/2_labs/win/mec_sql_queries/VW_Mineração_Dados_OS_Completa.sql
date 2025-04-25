/*
==========================================================================================================
    Nome: Mineração_Dados_OS_Completa.sql
    Descrição: 
        Esta query realiza a extração detalhada de informações sobre as Ordens de Serviço (OS) 
        registradas na tabela GA_OFI_OS, incluindo dados de equipamentos, agregados, motivos, 
        oficinas, classificação, projetos e solicitações de serviço.
        
        O objetivo é fornecer uma visão abrangente para análise e mineração de dados relacionados 
        à manutenção e gestão operacional dos equipamentos, permitindo flexibilidade na seleção 
        de parâmetros para personalização da consulta.

    Filtros Aplicados (dinâmicos):
        - Permite a escolha da empresa (COD_EMPR) ou retorna todas caso não informado.
        - Permite a seleção de um motivo específico (COD_MOTIVO) ou retorna todos caso não informado.
        - Permite a exclusão de múltiplos motivos informados na variável (COD_MOTIVO_EXCLUIR).
        - Permite a definição de um intervalo de anos para filtrar OS por data de entrada (ANO_INICIO e ANO_FIM).
        - Se nenhum filtro for informado, a query retorna todas as OS disponíveis.

    Tabelas Envolvidas:
        - GA_OFI_OS                (Tabela principal - Ordens de Serviço)
        - GA_EQP_EQUIPAMENTO       (Informações dos equipamentos)
        - GA_AGD_AGREGADOS         (Informações de agregados)
        - GA_OFI_MOT_ENTRADA       (Motivos de entrada da OS)
        - GA_OFI_OFICINA           (Oficinas responsáveis)
        - GA_OFI_CLASSIFICACAO_FEED (Classificação das OS)
        - GA_OFI_PROJETO           (Projetos associados)
        - GA_OFI_SOLIC_SERV        (Solicitações de serviço vinculadas)

    Autor: Roni Chittoni
    Data: 20250208
==========================================================================================================
*/


USE GATEC_MEC;
GO

-- Declaração das variáveis de parâmetro
DECLARE @COD_EMPR INT = NULL;							-- Defina um código de empresa específico ou NULL para trazer todas
DECLARE @COD_MOTIVO INT = NULL;						-- Defina um motivo específico ou NULL para trazer todos
DECLARE @COD_MOTIVO_EXCLUIR VARCHAR(MAX) = NULL;	-- Lista de motivos a serem excluídos (ex: '5,8,12') ou NULL para não excluir nenhum
DECLARE @ANO_INICIO INT = NULL;						-- Defina o ano inicial ou NULL para trazer desde o primeiro registro
DECLARE @ANO_FIM INT = NULL;						-- Defina o ano final ou NULL para trazer até o último registro

-- Consulta para mineração de dados da GA_OFI_OS
SELECT
    -- Identificadores
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

    -- Informações de Negócio
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

FROM GA_OFI_OS os
LEFT JOIN GA_EQP_EQUIPAMENTO eq ON os.COD_EQUIPAMENTO = eq.COD_EQUIPAMENTO
LEFT JOIN GA_AGD_AGREGADOS ag ON os.COD_AGREG = ag.AGD_CODIGO
LEFT JOIN GA_OFI_MOT_ENTRADA mot ON os.COD_MOTIVO = mot.COD_MOTIVO
LEFT JOIN GA_OFI_OFICINA ofi ON os.COD_OFICINA = ofi.COD_OFICINA

-- Filtros aplicados (parâmetros dinâmicos)
WHERE (@COD_EMPR IS NULL OR os.COD_EMPR = @COD_EMPR)  -- Filtra por empresa se um valor for definido
AND (@COD_MOTIVO IS NULL OR os.COD_MOTIVO = @COD_MOTIVO)  -- Filtra por motivo se um valor for definido
AND (@ANO_INICIO IS NULL OR YEAR(os.OS_DT_ENTRADA) >= @ANO_INICIO)  -- Filtra por ano inicial se definido
AND (@ANO_FIM IS NULL OR YEAR(os.OS_DT_ENTRADA) <= @ANO_FIM)  -- Filtra por ano final se definido
AND (
    @COD_MOTIVO_EXCLUIR IS NULL  -- Se @COD_MOTIVO_EXCLUIR for NULL, não exclui nenhum motivo
    OR os.COD_MOTIVO NOT IN (
        SELECT value FROM STRING_SPLIT(@COD_MOTIVO_EXCLUIR, ',')
    )
)

ORDER BY os.OS_DT_ENTRADA;
GO
