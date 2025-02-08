USE GATEC_MEC;
GO

SELECT 
    fk.name AS ForeignKeyName,
    OBJECT_NAME(fkc.parent_object_id) AS ParentTable,
    COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS ParentColumn,
    OBJECT_NAME(fkc.referenced_object_id) AS ReferencedTable,
    COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS ReferencedColumn
FROM sys.foreign_keys AS fk
INNER JOIN sys.foreign_key_columns AS fkc ON fk.object_id = fkc.constraint_object_id
WHERE 
    OBJECT_NAME(fkc.parent_object_id) IN ('GA_AGD_ENVIO', 'GA_AGD_LOTE_AGREGADOS', 'GA_AGD_SERVICOS', 'GA_OFI_OS')
    OR OBJECT_NAME(fkc.referenced_object_id) IN ('GA_AGD_ENVIO', 'GA_AGD_LOTE_AGREGADOS', 'GA_AGD_SERVICOS', 'GA_OFI_OS');
