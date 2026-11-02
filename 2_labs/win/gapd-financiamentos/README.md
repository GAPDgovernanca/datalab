# Star schema — Contratos de Financiamento (GAPD)

Implementação do **ADR-001**: camada semântica de governança em *star schema*,
materializada por *transform* determinístico.

```
fonte (2 planilhas do Financeiro)  →  validação na ingestão  →  star (DuckDB)
```

Fonte única de medida, sem re-derivação a cada ciclo/skill. A não-somabilidade da
exposição por garantidor é propriedade do modelo (a ponte), não nota de rodapé.

## Instalação

Ambiente virtual já configurado. Com a venv ativa, na raiz do projeto:

```powershell
pip install -r requirements.txt
```

## Uso

Coloque as duas planilhas do ciclo em `./data/` (a data-base é lida do prefixo
`AAAAMMDD` do nome do arquivo — nenhuma coluna de data de origem é usada):

```powershell
# build completo → ./build/gapd_star.duckdb
python build_star.py --sources ./data --out ./build

# também exporta parquet tipado por tabela (via COPY nativo do DuckDB)
python build_star.py --sources ./data --out ./build --parquet

# roda as consultas típicas do Conselho ao final
python build_star.py --sources ./data --out ./build --queries

# apenas valida a porta de entrada, sem gravar nada (exit 2 se reprovar)
python build_star.py --sources ./data --check
```

O build é **determinístico**: recria o `.duckdb` do zero a cada execução. Se
qualquer teste de aceitação duro falhar, o pipeline **recusa gravar** (exit 2).

## Testes

```powershell
pytest
```

Os testes constroem o star num DuckDB temporário a partir de `./data` e verificam
o **DB materializado** (não a memória): âncora, contagens, taxonomia fechada,
universos de contrato, dedup e não-aditividade.

## Arquitetura

```
star/
  config.py      Mapas conformados + taxonomia (23 rótulos) versionados em código.
                 Ponto único de taxonomia em aberto: MAQUINAS_TIPO (ratificação).
  ingest.py      Leitura, aparo de cabeçalho, normalização da chave `contrato`,
                 detecção de colunas fantasma / linhas órfãs (só detecta).
  validate.py    Porta de qualidade: falhas duras (recusam build) vs avisos.
  transform.py   Constrói 3 fatos, 4 dimensões conformadas, 1 ponte M:N.
  load.py        Materializa em DuckDB (primário) e parquet (opcional).
  queries.py     Consultas canônicas do Conselho + placar de reconciliação.
build_star.py    CLI orquestradora.
tests/           Testes de aceitação (pytest).
```

### Modelo dimensional

| Tabela | Grão | Origem |
|---|---|---|
| `fato_saldo` | Contrato × Data-base | GARANTIAS, dedup por Contrato |
| `fato_pagamento` | Contrato × Parcela × Data | PGTOS, `Parcela N#` preenchida |
| `fato_liberacao` | Contrato × Data desembolso | PGTOS, `Valor liberado` preenchido |
| `dim_contrato` | Contrato (união 140) | GARANTIAS ∪ PGTOS |
| `dim_banco` | Banco conformado (11) | união conformada (`BB↔Banco do Brasil`, `BBM↔Bocom`) |
| `dim_garantidor` | Garantidor (12) | parse de `Garantia` |
| `dim_tipo_garantia` | Tipo (5) | parse de `Garantia` |
| `dim_tempo` | Data presente | vencimentos + pagamentos + desembolsos |
| `ponte_contrato_garantia` | Contrato × Garantia (124) | GARANTIAS, parse de `Garantia` |

### Medida canônica de pagamento

`pagamento = principal + juros` com semântica **nan-safe** (parcela só-juros →
`pagamento = juros`). A coluna `Valor Total da Parcela` da fonte é **descartada**
(campo digitado, não decompõe, com nulo isolado e divergência de arredondamento).

### Não-aditividade da exposição

Exposição por garantidor = Σ `saldo_devedor` dos **contratos distintos** cobertos.
Somar entre garantidores **dupla-conta** o aval cruzado. No ciclo 30/06/2026 a
soma ingênua entre garantidores (~R$ 1,97 bi) é ~4,5× a âncora real (R$ 436,7 mi):

```python
from star import queries
queries.exposicao_por_garantidor("build/gapd_star.duckdb", classe="PF")
```

## Reconciliação (data-base 30/06/2026)

| Teste de aceitação | Esperado (pós-correção) | Resultado |
|---|---|---|
| Âncora Σ `saldo_devedor` (dedup) | R$ 436.684.394,56 | ✓ |
| Contratos vivos / linhas garantia | 31 / 124 | ✓ |
| PGTOS: total / pagamento / liberação | 751 / 646 / 156 | ✓ |
| Universos (GAR / PGTOS / ∩) | 31 / 139 / 30 | ✓ |
| Taxonomia fechada (23 rótulos) | fechada | ✓ |

## Achados de qualidade — resolvidos na fonte (ciclo 30/06/2026)

Detectados pela porta de ingestão no protótipo e **corrigidos nas planilhas** pelo
Departamento Financeiro (não contornados em código). Registro histórico:

- 2 colunas fantasma sem nome no PGTOS + 1 célula perdida (R$ 85.315,46) fora do
  esquema → colunas removidas, célula apurada.
- 4 linhas de pagamento sem `Parcela N#` (Credicitrus 8218024/8218038 → `1/1`;
  Itaú 13012156 → `1/2` e `2/2`) → parcelas preenchidas; agora entram em
  `fato_pagamento`.
- 2 linhas inteiramente vazias → excluídas.

Efeito: contagens de PGTOS re-baselinadas (753→751 total, 643→646 pagamento). A
âncora de saldo é imune (deriva só de `RELACAO GARANTIAS`). Se um ciclo futuro
reintroduzir qualquer um desses padrões, a porta de ingestão volta a sinalizá-lo
como aviso — sem jamais silenciá-lo.

> Pendências de higiene mais profunda, **não** bloqueantes, deixadas para segunda
> etapa: 51 linhas com predicado duplo (`Parcela N#` e `Valor liberado` na mesma
> linha, gerando registros de valor zero) e a chave `230106835 - SWAP` com sufixo
> textual. Nenhuma afeta medidas em R$; ver histórico de decisão.

## Ponto em aberto (ratificação)

`AF máquinas` / `Penhor máquinas` (6 linhas) classificados como **real**. Para
alocar a **operacional**, alterar `MAQUINAS_TIPO` em `star/config.py` — mudança de
uma linha; as outras 22 resoluções da taxonomia são inequívocas.
