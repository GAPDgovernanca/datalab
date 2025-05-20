/*
==========================================================================================================
    Nome: Criacao_Tabela_Mineracao_OS.sql
    Descrição: 
        Este script cria a tabela `MINERACAO_DADOS_OS` no banco `GATEC_MEC_MINERACAO` para armazenar 
        os dados extraídos da mineração de ordens de serviço (OS). Ele verifica se a tabela já existe 
        antes de criá-la, garantindo que não ocorra duplicação. A tabela contém colunas essenciais para 
        análise de OS, incluindo informações de equipamentos, motivos, oficinas e observações.

    Estrutura Criada:
        - Armazena dados das OS mineradas, permitindo análises detalhadas.
        - Inclui um campo `DATA_INSERCAO` para rastrear a data de inserção dos dados.
        - Contém informações essenciais como ID da OS, empresa, equipamento, motivo, oficina, etc.

    Uso:
        1. Execute este script no banco `GATEC_MEC_MINERACAO`.
        2. Após criar a tabela, utilize a query de inserção (`Insercao_Dados_Mineracao_OS.sql`)
           para popular os dados extraídos.

    Autor: Roni Chittoni
    Data: 20250208
==========================================================================================================
*/


USE GATEC_MEC_MINERACAO;
GO

-- Verifica se a tabela já existe para evitar erro na criação
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'MINERACAO_DADOS_OS')
BEGIN
    CREATE TABLE MINERACAO_DADOS_OS (
        COD_OS INT,
        ROWID UNIQUEIDENTIFIER,
        ID_USUARIO INT,
        COD_EMPR INT,
        COD_FUNC INT,
        ID_OS_EQP INT,
        OS_DT_ENTRADA DATETIME,
        OS_DT_SAIDA DATETIME,
        OS_DT_COMUNICACAO DATETIME,
        OS_DT_PREVISAO DATETIME,
        OS_OBSERVACAO NVARCHAR(MAX),
        OS_STATUS NVARCHAR(50),
        OS_SITUACAO NVARCHAR(50),
        OS_TIPO NVARCHAR(50),
        OS_MEDIDOR DECIMAL(18,2),
        OS_MEDIDOR_SAIDA DECIMAL(18,2),
        OS_OPORTUNIDADE NVARCHAR(50),
        COD_EQUIPAMENTO INT,
        EQP_ANO_FABRIC INT,
        EQP_PLACA NVARCHAR(20),
        COD_MOTIVO INT,
        MOTIVO_DESC NVARCHAR(255),
        COD_OFICINA INT,
        OFICINA_DESC NVARCHAR(255),
        DATA_INSERCAO DATETIME DEFAULT GETDATE()
    );
END;
GO
