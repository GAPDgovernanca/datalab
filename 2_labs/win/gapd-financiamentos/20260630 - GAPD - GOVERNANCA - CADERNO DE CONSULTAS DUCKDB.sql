-- CADERNO DE CONSULTAS (executavel) -- Governanca de Endividamento GAPD
-- Star schema de contratos de financiamento (ADR-001), data-base 30/06/2026
-- Rodar: duckdb -readonly .uild\gapd_star.duckdb  depois  .mode box  depois  .read este arquivo

-- SECAO: kpis.sql

WITH
anchor AS (SELECT SUM(saldo_devedor) AS div_bruta, COUNT(*) AS n FROM fato_saldo),
base   AS (SELECT MAX(data_base) AS db FROM fato_saldo),
exp AS (
    SELECT DISTINCT pg.classe, pg.tipo_garantia, pg.garantidor,
           pg.contrato, fs.saldo_devedor
    FROM ponte_contrato_garantia pg
    JOIN fato_saldo fs USING (contrato)
),
pf_pessoa AS (               -- exposição por PF, só AVAL direto
    SELECT garantidor, SUM(saldo_devedor) AS saldo
    FROM (SELECT DISTINCT garantidor, contrato, saldo_devedor
          FROM exp WHERE classe='PF' AND tipo_garantia='aval')
    GROUP BY garantidor
),
pf_top AS (SELECT garantidor, saldo FROM pf_pessoa ORDER BY saldo DESC LIMIT 1),
holding_expo AS (            -- exposição por holding: aval-holding UNIÃO real da fazenda
    SELECT holding, SUM(saldo_devedor) AS saldo
    FROM (SELECT DISTINCT h.holding, x.contrato, x.saldo_devedor
          FROM (VALUES ('São Jorge','Fazenda São Jorge'),
                       ('São João','Fazenda São João')) AS h(holding, fazenda)
          JOIN exp x ON x.garantidor IN (h.holding, h.fazenda))
    GROUP BY holding
),
holding_top AS (SELECT holding, saldo FROM holding_expo ORDER BY saldo DESC LIMIT 1)
SELECT "#", indicador, valor, detalhe FROM (
    SELECT 1 AS "#", 'dívida bruta colateralizada' AS indicador,
           'R$ ' || replace(printf('%.1f', div_bruta/1e6), '.', ',') || ' mi' AS valor,
           n || ' contratos' AS detalhe
    FROM anchor
  UNION ALL
    SELECT 2, 'instituições',
           CAST((SELECT COUNT(DISTINCT banco) FROM dim_contrato WHERE is_vivo) AS VARCHAR),
           'bancos e cooperativa'
  UNION ALL
    SELECT 3, 'obrigação pf (contratos)',
           COUNT(DISTINCT contrato) || ' de ' || (SELECT n FROM anchor),
           replace(printf('%.1f', 100*SUM(sd)/(SELECT div_bruta FROM anchor)), '.', ',') || '% da dívida'
    FROM (SELECT DISTINCT contrato, saldo_devedor AS sd FROM exp WHERE classe='PF')
  UNION ALL
    SELECT 4, 'contratos c/ aval pf direto',
           CAST(COUNT(DISTINCT contrato) AS VARCHAR),
           replace(printf('%.1f', 100*SUM(sd)/(SELECT div_bruta FROM anchor)), '.', ',') || '% da dívida'
    FROM (SELECT DISTINCT contrato, saldo_devedor AS sd FROM exp
          WHERE classe='PF' AND tipo_garantia='aval')
  UNION ALL
    SELECT 5, 'maior exposição pf',
           'R$ ' || replace(printf('%.1f', saldo/1e6), '.', ',') || ' mi',
           lower(garantidor) || ' · aval direto'
    FROM pf_top
  UNION ALL
    SELECT 6, 'maior exposição holding',
           'R$ ' || replace(printf('%.1f', saldo/1e6), '.', ',') || ' mi',
           lower(holding) || ' · fidej + real'
    FROM holding_top
  UNION ALL
    SELECT 7, 'vencendo em até 12m',
           replace(printf('%.1f', 100*p/(SELECT div_bruta FROM anchor)), '.', ',') || '%',
           'R$ ' || replace(printf('%.1f', p/1e6), '.', ',') || ' mi'
    FROM (SELECT SUM(principal) AS p FROM fato_pagamento, base
          WHERE data > base.db AND data <= base.db + INTERVAL 12 MONTH)
  UNION ALL
    SELECT 8, 'cobertura por garantia real',
           replace(printf('%.1f', 100*SUM(sd)/(SELECT div_bruta FROM anchor)), '.', ',') || '%',
           COUNT(DISTINCT contrato) || ' contratos'
    FROM (SELECT DISTINCT contrato, saldo_devedor AS sd FROM exp WHERE tipo_garantia='real')
) ORDER BY "#";

-- SECAO: consulta_exposicao_pf.sql

WITH
anchor AS (SELECT SUM(saldo_devedor) AS div_bruta FROM fato_saldo),
pf AS (
    SELECT pg.garantidor, pg.tipo_garantia, pg.contrato, fs.saldo_devedor
    FROM ponte_contrato_garantia pg
    JOIN fato_saldo fs USING (contrato)
    WHERE pg.classe = 'PF'
),
aval AS (   -- aval direto: contratos distintos por pessoa, tipo = aval
    SELECT garantidor, COUNT(DISTINCT contrato) AS contr, SUM(saldo) AS saldo
    FROM (SELECT DISTINCT garantidor, contrato, saldo_devedor AS saldo
          FROM pf WHERE tipo_garantia = 'aval')
    GROUP BY garantidor
),
ampl AS (   -- obrigação ampliada: contratos distintos por pessoa, qualquer tipo PF
    SELECT garantidor, COUNT(DISTINCT contrato) AS contr, SUM(saldo) AS saldo
    FROM (SELECT DISTINCT garantidor, contrato, saldo_devedor AS saldo FROM pf)
    GROUP BY garantidor
)
SELECT a.garantidor                                                             AS "Pessoa física",
       a.contr                                                                  AS "Contr. aval dir.",
       'R$ ' || replace(printf('%.1f', a.saldo/1e6), '.', ',') || ' mi'         AS "Saldo aval direto",
       m.contr                                                                  AS "Contr. ampl.",
       'R$ ' || replace(printf('%.1f', m.saldo/1e6), '.', ',') || ' mi'         AS "Saldo obrig. ampliada",
       replace(printf('%.1f', 100*m.saldo/(SELECT div_bruta FROM anchor)), '.', ',') AS "% dív. (ampl.)"
FROM aval a
JOIN ampl m USING (garantidor)
ORDER BY m.saldo DESC;

-- SECAO: exposicao_rotulo_ana_saojoao.sql

WITH
r AS (
    SELECT DISTINCT pg.garantia_rotulo AS rot, pg.contrato, fs.saldo_devedor AS saldo
    FROM ponte_contrato_garantia pg
    JOIN fato_saldo fs USING (contrato)
),
v AS (SELECT rot, SUM(saldo) AS saldo FROM r GROUP BY rot),
linhas AS (
    SELECT 1  AS ord, 'Fiança Ana'                   AS item, COALESCE((SELECT saldo FROM v WHERE rot='Fiança Ana'),0)                    AS valor UNION ALL
    SELECT 2,        'Emitente Ana',                         COALESCE((SELECT saldo FROM v WHERE rot='Emitente Ana'),0)                         UNION ALL
    SELECT 3,        'Aval Ana',                             COALESCE((SELECT saldo FROM v WHERE rot='Aval Ana'),0)                             UNION ALL
    SELECT 4,        'Dívida solidária Ana',                COALESCE((SELECT saldo FROM v WHERE rot='Dívida solidária Ana'),0)                 UNION ALL
    SELECT 5,        'Total Ana',                           (SELECT COALESCE(SUM(saldo),0) FROM v WHERE rot IN ('Fiança Ana','Emitente Ana','Aval Ana','Dívida solidária Ana')) UNION ALL
    SELECT 6,        'Fiança São João',                     COALESCE((SELECT saldo FROM v WHERE rot='Fiança São João'),0)                      UNION ALL
    SELECT 7,        'Aval São João',                       COALESCE((SELECT saldo FROM v WHERE rot='Aval São João'),0)                        UNION ALL
    SELECT 8,        'Dívida solidária São João',           COALESCE((SELECT saldo FROM v WHERE rot='Dívida solidária São João'),0)            UNION ALL
    SELECT 9,        'Total fidejussório São João',         (SELECT COALESCE(SUM(saldo),0) FROM v WHERE rot IN ('Fiança São João','Aval São João','Dívida solidária São João')) UNION ALL
    SELECT 10,       'Hipoteca Fazenda da São João',        COALESCE((SELECT saldo FROM v WHERE rot='Hipoteca Fazenda da São João'),0)         UNION ALL
    SELECT 11,       'AF Fazenda da São João',              COALESCE((SELECT saldo FROM v WHERE rot='AF Fazenda da São João'),0)               UNION ALL
    SELECT 12,       'Total real São João',                 (SELECT COALESCE(SUM(saldo),0) FROM v WHERE rot IN ('Hipoteca Fazenda da São João','AF Fazenda da São João'))
)
SELECT item AS "Garantia / subtotal",
       replace(replace(replace(format('{:,.2f}', COALESCE(valor,0)), ',', '§'), '.', ','), '§', '.') AS "Saldo (R$)"
FROM linhas
ORDER BY ord;

-- SECAO: calendario_pagamentos_ana.sql

WITH
base AS (SELECT MAX(data_base) AS db FROM fato_saldo),
ana AS (
    SELECT DISTINCT contrato
    FROM ponte_contrato_garantia
    WHERE garantidor = 'Ana'          -- classe PF implícita; Ana nunca é PJ/ativo
),
mensal AS (
    SELECT strftime(fp.data, '%Y-%m') AS mes,
           COUNT(*)          AS parcelas,
           SUM(fp.principal) AS principal,
           SUM(fp.juros)     AS juros,
           SUM(fp.pagamento) AS pagamento
    FROM fato_pagamento fp
    JOIN ana USING (contrato)
    CROSS JOIN base
    WHERE fp.data > base.db
    GROUP BY mes
)
SELECT mes,
       parcelas AS "parc.",
       CASE WHEN principal = 0 THEN '—'
            ELSE 'R$ ' || replace(printf('%.1f', principal/1e6), '.', ',') || ' mi' END AS "principal",
       CASE WHEN juros = 0 THEN '—'
            ELSE 'R$ ' || replace(printf('%.1f', juros/1e6), '.', ',') || ' mi' END AS "juros",
       'R$ ' || replace(printf('%.1f', pagamento/1e6), '.', ',') || ' mi'              AS "pagamento",
       'R$ ' || replace(printf('%.1f',
              SUM(pagamento) OVER (ORDER BY mes)/1e6), '.', ',') || ' mi'              AS "acumulado"
FROM mensal
ORDER BY mes;

-- SECAO: fluxo_saidas_grupo.sql

WITH
base AS (SELECT MAX(data_base) AS db FROM fato_saldo),
mensal AS (
    SELECT strftime(fp.data, '%Y-%m') AS mes,
           COUNT(*)          AS parcelas,
           SUM(fp.principal) AS principal,
           SUM(fp.juros)     AS juros,
           SUM(fp.pagamento) AS pagamento
    FROM fato_pagamento fp
    CROSS JOIN base
    WHERE fp.data > base.db
    GROUP BY mes
),
tot AS (
    SELECT SUM(parcelas) AS parcelas, SUM(principal) AS principal,
           SUM(juros) AS juros, SUM(pagamento) AS pagamento
    FROM mensal
),
detalhe AS (
    SELECT mes, parcelas, principal, juros, pagamento,
           SUM(pagamento) OVER (ORDER BY mes)                              AS pag_acum,
           (SELECT principal FROM tot) - SUM(principal) OVER (ORDER BY mes) AS principal_resto
    FROM mensal
)
SELECT "mês", "parc.", "principal", "juros", "saída (mês)", "saída acum.", "principal a pagar"
FROM (
    -- linhas mensais
    SELECT 0 AS ord, mes AS "mês", parcelas AS "parc.",
           CASE WHEN principal = 0 THEN '—'
                ELSE 'R$ ' || replace(printf('%.1f', principal/1e6), '.', ',') || ' mi' END AS "principal",
           CASE WHEN juros = 0 THEN '—'
                ELSE 'R$ ' || replace(printf('%.1f', juros/1e6), '.', ',') || ' mi' END     AS "juros",
           'R$ ' || replace(printf('%.1f', pagamento/1e6), '.', ',') || ' mi'               AS "saída (mês)",
           'R$ ' || replace(printf('%.1f', pag_acum/1e6), '.', ',') || ' mi'                AS "saída acum.",
           'R$ ' || replace(printf('%.1f', principal_resto/1e6), '.', ',') || ' mi'         AS "principal a pagar"
    FROM detalhe
    UNION ALL
    -- linha de totais
    SELECT 1, 'TOTAL', parcelas,
           'R$ ' || replace(printf('%.1f', principal/1e6), '.', ',') || ' mi',
           'R$ ' || replace(printf('%.1f', juros/1e6), '.', ',') || ' mi',
           'R$ ' || replace(printf('%.1f', pagamento/1e6), '.', ',') || ' mi',
           'R$ ' || replace(printf('%.1f', pagamento/1e6), '.', ',') || ' mi',
           '—'
    FROM tot
)
ORDER BY ord, "mês";

-- SECAO: exportar_fluxo_csv.sql

COPY (
    WITH
    base AS (SELECT MAX(data_base) AS db FROM fato_saldo),
    mensal AS (
        SELECT strftime(fp.data, '%Y-%m') AS mes,
               COUNT(*)          AS parcelas,
               SUM(fp.principal) AS principal,
               SUM(fp.juros)     AS juros,
               SUM(fp.pagamento) AS pagamento
        FROM fato_pagamento fp CROSS JOIN base
        WHERE fp.data > base.db
        GROUP BY mes
    ),
    tot AS (SELECT SUM(parcelas) p, SUM(principal) pr, SUM(juros) j, SUM(pagamento) pg FROM mensal),
    detalhe AS (
        SELECT mes, parcelas, principal, juros, pagamento,
               SUM(pagamento) OVER (ORDER BY mes)                              AS pag_acum,
               (SELECT pr FROM tot) - SUM(principal) OVER (ORDER BY mes)        AS principal_resto
        FROM mensal
    )
    SELECT "mes","parcelas","principal","juros","saida_mes","saida_acumulada","principal_a_pagar"
    FROM (
        SELECT 0 AS ord, mes AS "mes", parcelas AS "parcelas",
               replace(printf('%.2f', principal),      '.', ',') AS "principal",
               replace(printf('%.2f', juros),          '.', ',') AS "juros",
               replace(printf('%.2f', pagamento),      '.', ',') AS "saida_mes",
               replace(printf('%.2f', pag_acum),       '.', ',') AS "saida_acumulada",
               replace(printf('%.2f', principal_resto),'.', ',') AS "principal_a_pagar"
        FROM detalhe
        UNION ALL
        SELECT 1, 'TOTAL', p,
               replace(printf('%.2f', pr), '.', ','),
               replace(printf('%.2f', j),  '.', ','),
               replace(printf('%.2f', pg), '.', ','),
               replace(printf('%.2f', pg), '.', ','),
               NULL
        FROM tot
    )
    ORDER BY ord, "mes"
) TO 'fluxo_saidas_grupo.csv' (HEADER, DELIMITER ';');

-- SECAO: sentinela de fianca (retorna vazio na data-base; acende quando houver fianca)
SELECT garantia_rotulo, garantidor, COUNT(DISTINCT contrato) AS contratos, SUM(saldo_devedor) AS saldo
FROM ponte_contrato_garantia pg JOIN fato_saldo fs USING (contrato)
WHERE garantia_rotulo ILIKE '%fian%' GROUP BY 1,2 ORDER BY saldo DESC;