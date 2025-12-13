from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from openpyxl import load_workbook


# -----------------------------
# Domain primitives
# -----------------------------
@dataclass(frozen=True)
class CellRef:
    value: str


@dataclass(frozen=True)
class LegId:
    value: str


@dataclass(frozen=True)
class BlockId:
    value: str


@dataclass(frozen=True)
class Strike:
    value: float


@dataclass(frozen=True)
class PremiumPerArroba:
    value: float

    def abs(self) -> "PremiumPerArroba":
        return PremiumPerArroba(abs(self.value))


@dataclass(frozen=True)
class Contracts:
    value: float

    def abs(self) -> float:
        return float(abs(self.value))


@dataclass(frozen=True)
class PriceGrid:
    values: np.ndarray

    @staticmethod
    def from_range(min_price: float, max_price: float, points: int) -> "PriceGrid":
        return PriceGrid(np.linspace(min_price, max_price, points))


@dataclass(frozen=True)
class PayoffCurve:
    values: np.ndarray

    def plus(self, other: "PayoffCurve") -> "PayoffCurve":
        return PayoffCurve(self.values + other.values)

    def scaled(self, factor: float) -> "PayoffCurve":
        return PayoffCurve(self.values * float(factor))


# -----------------------------
# Options domain
# -----------------------------
@dataclass(frozen=True)
class OptionKind:
    value: str  # "call" | "put"

    def is_put(self) -> bool:
        return self.value == "put"


@dataclass(frozen=True)
class PositionKind:
    value: str  # "short" | "long"

    @staticmethod
    def from_contracts(contracts: Contracts) -> "PositionKind":
        if contracts.value < 0.0:
            return PositionKind("short")
        return PositionKind("long")


@dataclass(frozen=True)
class OptionLeg:
    leg_id: LegId
    label: str
    kind: OptionKind
    strike: Strike
    premium: PremiumPerArroba
    contracts: Contracts


@dataclass(frozen=True)
class OptionBlock:
    block_id: BlockId
    label: str
    legs: tuple[OptionLeg, ...]

    def strikes(self) -> list[float]:
        return [leg.strike.value for leg in self.legs]


# -----------------------------
# Excel access
# -----------------------------
class Worksheet:
    def __init__(self, sheet) -> None:
        self._sheet = sheet

    def float_at(self, ref: CellRef) -> float:
        value = self._sheet[ref.value].value
        if value is None:
            raise ValueError(f"Célula vazia: {ref.value}")
        return float(value)

    def value_at(self, addr: str):
        return self._sheet[addr].value

    def iter_cells(self, row_min: int, row_max: int, col_min: int, col_max: int):
        for row in self._sheet.iter_rows(
            min_row=row_min, max_row=row_max, min_col=col_min, max_col=col_max
        ):
            for cell in row:
                yield cell


class WorkbookReader:
    def __init__(self, path: Path, sheet_name: str) -> None:
        self._path = path
        self._sheet_name = sheet_name

    def load_sheet(self) -> Worksheet:
        workbook = load_workbook(self._path, data_only=True)
        sheet = workbook[self._sheet_name]
        return Worksheet(sheet)


# -----------------------------
# Discovery
# -----------------------------
@dataclass(frozen=True)
class LegCandidate:
    leg_id: LegId
    label: str
    kind: OptionKind
    value_col: str
    strike_cell: CellRef
    premium_cell: CellRef
    contracts_cell: CellRef

    def to_leg(self, ws: Worksheet) -> OptionLeg:
        return OptionLeg(
            leg_id=self.leg_id,
            label=self.label,
            kind=self.kind,
            strike=Strike(ws.float_at(self.strike_cell)),
            premium=PremiumPerArroba(ws.float_at(self.premium_cell)),
            contracts=Contracts(ws.float_at(self.contracts_cell)),
        )


class BaseLegFinder:
    _pattern = re.compile(r"^(Call|Put)[_\\s\\-].+", re.IGNORECASE)

    def __init__(self, ws: Worksheet) -> None:
        self._ws = ws

    def find(self) -> list[LegCandidate]:
        candidates: list[LegCandidate] = []
        for cell in self._ws.iter_cells(row_min=1, row_max=1, col_min=1, col_max=500):
            if not isinstance(cell.value, str):
                continue
            label = cell.value.strip()
            if not self._pattern.match(label):
                continue
            kind = self._infer_kind(label)
            candidates.append(self._candidate_from_label_cell(cell.coordinate, label, kind))
        return candidates

    def _infer_kind(self, label: str) -> OptionKind:
        if label.strip().upper().startswith("CALL"):
            return OptionKind("call")
        return OptionKind("put")

    def _candidate_from_label_cell(self, coord: str, label: str, kind: OptionKind) -> LegCandidate:
        col_letters = re.findall(r"[A-Z]+", coord)[0]
        value_col_index = self._col_to_int(col_letters) + 1
        value_col_letters = self._int_to_col(value_col_index)

        leg_id = LegId(f"{label}::{value_col_letters}")
        return LegCandidate(
            leg_id=leg_id,
            label=label,
            kind=kind,
            value_col=value_col_letters,
            strike_cell=CellRef(f"{value_col_letters}1"),
            premium_cell=CellRef(f"{value_col_letters}14"),
            contracts_cell=CellRef(f"{value_col_letters}7"),
        )

    def _col_to_int(self, col: str) -> int:
        result = 0
        for ch in col:
            result = result * 26 + (ord(ch) - ord("A") + 1)
        return result

    def _int_to_col(self, n: int) -> str:
        letters: list[str] = []
        while n > 0:
            n, rem = divmod(n - 1, 26)
            letters.append(chr(rem + ord("A")))
        return "".join(reversed(letters))


# -----------------------------
# Catalog (friendly selection)
# -----------------------------
class LegCatalog:
    def __init__(self, ws: Worksheet, candidates: Sequence[LegCandidate]) -> None:
        self._ws = ws
        self._candidates = [c for c in candidates if self._is_complete(c)]
        self._by_id = {c.leg_id.value: c for c in self._candidates}
        self._display_cache: dict[str, str] = {}

    def ids(self) -> list[str]:
        return list(self._by_id.keys())

    def candidate(self, leg_id: str) -> LegCandidate:
        return self._by_id[leg_id]

    def filtered_ids(self, text: str, kind: str) -> list[str]:
        needle = text.strip().lower()
        ids: list[str] = []
        for c in self._candidates:
            if kind != "Todos" and c.kind.value != kind:
                continue
            if needle and needle not in c.label.lower() and needle not in c.value_col.lower():
                continue
            ids.append(c.leg_id.value)
        return ids

    def display_name(self, leg_id: str) -> str:
        cached = self._display_cache.get(leg_id)
        if cached is not None:
            return cached

        c = self._by_id[leg_id]
        strike = self._safe_float(c.strike_cell.value)
        prem = self._safe_float(c.premium_cell.value)
        cts = self._safe_float(c.contracts_cell.value)

        name = (
            f"{c.label} | col {c.value_col} | "
            f"K={self._fmt(strike)} | prem={self._fmt(prem, 4)} | cts={self._fmt(cts)}"
        )
        self._display_cache[leg_id] = name
        return name

    def to_leg(self, leg_id: str) -> OptionLeg:
        return self._by_id[leg_id].to_leg(self._ws)

    def _is_complete(self, c: LegCandidate) -> bool:
        return (
            self._ws.value_at(c.strike_cell.value) is not None
            and self._ws.value_at(c.premium_cell.value) is not None
            and self._ws.value_at(c.contracts_cell.value) is not None
        )

    def _safe_float(self, addr: str) -> float | None:
        value = self._ws.value_at(addr)
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _fmt(self, value: float | None, decimals: int = 2) -> str:
        if value is None:
            return "N/A"
        return f"{value:.{decimals}f}"


# -----------------------------
# Payoff engine
# -----------------------------
class PayoffModel:
    def __init__(self, grid: PriceGrid) -> None:
        self._s = grid.values

    def curve_for_leg(self, leg: OptionLeg) -> PayoffCurve:
        position = PositionKind.from_contracts(leg.contracts)
        premium = leg.premium.abs().value
        curve = self._curve_call(leg.strike.value, premium, position)
        if leg.kind.is_put():
            curve = self._curve_put(leg.strike.value, premium, position)
        return PayoffCurve(curve)

    def _curve_call(self, k: float, p: float, pos: PositionKind) -> np.ndarray:
        intrinsic = np.maximum(self._s - k, 0.0)
        if pos.value == "short":
            return p - intrinsic
        return intrinsic - p

    def _curve_put(self, k: float, p: float, pos: PositionKind) -> np.ndarray:
        intrinsic = np.maximum(k - self._s, 0.0)
        if pos.value == "short":
            return p - intrinsic
        return intrinsic - p


class CurveAggregator:
    def weighted_average(self, curves: Sequence[PayoffCurve], weights: Sequence[float]) -> PayoffCurve:
        matrix = np.vstack([c.values for c in curves])
        w = np.asarray(weights, dtype=float).reshape(-1, 1)
        total = float(w.sum())
        if total == 0.0:
            return PayoffCurve(np.zeros(matrix.shape[1]))
        return PayoffCurve((matrix * w).sum(axis=0) / total)


# -----------------------------
# Plotting
# -----------------------------
@dataclass(frozen=True)
class BlockResult:
    block: OptionBlock
    legs: Mapping[str, PayoffCurve]
    per_arroba: PayoffCurve
    total_reais: PayoffCurve
    abs_contracts_sum: float


class PlotBuilder:
    def __init__(self, grid: PriceGrid) -> None:
        self._x = grid.values

    def payoff_per_arroba(self, results: Sequence[BlockResult], portfolio: PayoffCurve, strikes: Sequence[float]) -> go.Figure:
        fig = go.Figure()

        for r in results:
            for leg_name, curve in r.legs.items():
                fig.add_trace(self._line(curve, f"{r.block.label} :: {leg_name}", 1))
            fig.add_trace(self._line(r.per_arroba, f"{r.block.label} (agregado R$/@)", 3))

        fig.add_trace(self._line(portfolio, "PORTFÓLIO (R$/@)", 5))

        for k in sorted(set(strikes)):
            fig.add_vline(x=float(k), line_width=1, line_dash="dash", opacity=0.5)

        fig.add_hline(y=0, line_width=1, line_dash="dash", opacity=0.6)

        fig.update_layout(
            title="Payoff por @ (R$/@) – blocos selecionados",
            xaxis_title="Preço (R$/@)",
            yaxis_title="Payoff (R$/@)",
            hovermode="x unified",
        )
        return fig

    def payoff_total_reais(self, results: Sequence[BlockResult], portfolio_total: PayoffCurve, strikes: Sequence[float]) -> go.Figure:
        fig = go.Figure()

        for r in results:
            fig.add_trace(self._line(r.total_reais, f"{r.block.label} (R$)", 3))

        fig.add_trace(self._line(portfolio_total, "PORTFÓLIO (R$)", 5))

        for k in sorted(set(strikes)):
            fig.add_vline(x=float(k), line_width=1, line_dash="dash", opacity=0.5)

        fig.add_hline(y=0, line_width=1, line_dash="dash", opacity=0.6)

        fig.update_layout(
            title="Payoff total aproximado (R$) – blocos selecionados",
            xaxis_title="Preço (R$/@)",
            yaxis_title="Payoff (R$)",
            hovermode="x unified",
        )
        return fig

    def _line(self, curve: PayoffCurve, name: str, width: int) -> go.Scatter:
        return go.Scatter(x=self._x, y=curve.values, mode="lines", name=name, line={"width": width})


# -----------------------------
# App helpers
# -----------------------------
def save_upload(uploaded) -> Path:
    target = Path.cwd() / "uploaded_planilha.xlsx"
    target.write_bytes(uploaded.getbuffer())
    return target


def build_blocks(selection: Mapping[str, list[str]], catalog: LegCatalog) -> list[OptionBlock]:
    blocks: list[OptionBlock] = []
    for label, leg_ids in selection.items():
        legs = [catalog.to_leg(leg_id) for leg_id in leg_ids]
        blocks.append(OptionBlock(BlockId(label), label, tuple(legs)))
    return blocks


def summary_table(results: Sequence[BlockResult]) -> pd.DataFrame:
    rows: list[dict[str, float | str]] = []
    for r in results:
        strikes = [leg.strike.value for leg in r.block.legs]
        premiums = [leg.premium.value for leg in r.block.legs]
        contracts = [leg.contracts.value for leg in r.block.legs]
        rows.append(
            {
                "Bloco": r.block.label,
                "N legs": len(r.block.legs),
                "Strike min": float(min(strikes)),
                "Strike max": float(max(strikes)),
                "Prêmio min (R$/@)": float(min(premiums)),
                "Prêmio max (R$/@)": float(max(premiums)),
                "Contratos (soma)": float(sum(contracts)),
                "|Contratos| (soma)": float(r.abs_contracts_sum),
            }
        )
    return pd.DataFrame(rows)


# -----------------------------
# Streamlit App
# -----------------------------
def main() -> None:
    st.set_page_config(layout="wide")
    st.title("Payoff – Blocos de Opções (Base) – seleção livre")

    uploaded = st.file_uploader("Carregue o arquivo Excel (.xlsx)", type=["xlsx"])
    if uploaded is None:
        st.stop()

    excel_path = save_upload(uploaded)

    sheet_name = st.sidebar.text_input("Aba (sheet) para ler", value="Base")
    ws = WorkbookReader(excel_path, sheet_name).load_sheet()

    candidates = BaseLegFinder(ws).find()
    if len(candidates) == 0:
        st.error("Não encontrei legs. Verifique se os rótulos na linha 1 começam com Call_ ou Put_.")
        st.stop()

    catalog = LegCatalog(ws, candidates)
    if len(catalog.ids()) == 0:
        st.error(
            "Encontrei rótulos de legs, mas vários estão incompletos (strike/prêmio/contratos vazios). "
            "Confirme se a aba Base tem valores nas linhas 1, 7 e 14 da coluna numérica do leg."
        )
        st.stop()


    st.subheader("Legs encontrados (para referência)")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "leg_id": c.leg_id.value,
                    "label": c.label,
                    "kind": c.kind.value,
                    "col": c.value_col,
                    "strike_cell": c.strike_cell.value,
                    "premium_cell": c.premium_cell.value,
                    "contracts_cell": c.contracts_cell.value,
                }
                for c in candidates
            ]
        ),
        use_container_width=True,
    )

    st.sidebar.subheader("Seleção de blocos")
    st.sidebar.caption("Crie blocos e selecione as pernas (legs) usando filtros.")

    if "blocks" not in st.session_state:
        st.session_state["blocks"] = {"Bloco 1": []}

    if st.sidebar.button("Adicionar bloco"):
        st.session_state["blocks"][f"Bloco {len(st.session_state['blocks']) + 1}"] = []

    block_names = list(st.session_state["blocks"].keys())
    active_block = st.sidebar.selectbox("Bloco para editar", options=block_names)

    filter_text = st.sidebar.text_input("Filtrar legs (texto)", value="")
    filter_kind = st.sidebar.selectbox("Tipo", options=["Todos", "call", "put"], index=0)

    available_ids = catalog.filtered_ids(filter_text, filter_kind)
    current = st.session_state["blocks"][active_block]

    chosen = st.sidebar.multiselect(
        "Selecione as pernas deste bloco",
        options=available_ids,
        default=[x for x in current if x in available_ids] or current,
        format_func=catalog.display_name,
    )
    st.session_state["blocks"][active_block] = chosen

    st.sidebar.caption("Renomeie os blocos para 'Put Dez 320', 'Call Jan 335' etc.")
    rename_from = st.sidebar.selectbox("Renomear bloco", options=block_names)
    rename_to = st.sidebar.text_input("Novo nome", value=rename_from)
    if st.sidebar.button("Aplicar rename"):
        name = rename_to.strip()
        if name and name != rename_from:
            st.session_state["blocks"][name] = st.session_state["blocks"].pop(rename_from)

    selection = {k: v for k, v in st.session_state["blocks"].items() if len(v) > 0}
    if len(selection) == 0:
        st.warning("Selecione ao menos 1 perna em algum bloco.")
        st.stop()

    blocks = build_blocks(selection, catalog)

    strikes_all = [s for b in blocks for s in b.strikes()]
    k_min = float(min(strikes_all))
    k_max = float(max(strikes_all))

    col1, col2, col3 = st.columns(3)
    s_min = col1.slider("S min (R$/@)", min_value=0.0, max_value=k_max + 300.0, value=max(0.0, k_min - 80.0), step=1.0)
    s_max = col2.slider("S max (R$/@)", min_value=0.0, max_value=k_max + 300.0, value=k_max + 80.0, step=1.0)
    points = col3.slider("Pontos", min_value=101, max_value=2001, value=401, step=50)

    if s_max < s_min:
        s_min, s_max = s_max, s_min

    col4, col5, col6 = st.columns(3)
    premium_mult = col4.slider("Multiplicador de prêmio (todos)", min_value=0.0, max_value=2.0, value=1.0, step=0.01)
    contracts_mult = col5.slider("Multiplicador de contratos (todos)", min_value=0.0, max_value=2.0, value=1.0, step=0.01)
    arrobas_per_contract = col6.number_input("@ por contrato", min_value=1.0, max_value=2000.0, value=330.0, step=1.0)

    show_total = st.checkbox("Mostrar payoff total aproximado (R$)", value=False)

    grid = PriceGrid.from_range(float(s_min), float(s_max), int(points))
    model = PayoffModel(grid)
    aggregator = CurveAggregator()

    results: list[BlockResult] = []
    portfolio = PayoffCurve(np.zeros_like(grid.values))

    for block in blocks:
        curves: list[PayoffCurve] = []
        weights: list[float] = []
        legs_map: dict[str, PayoffCurve] = {}
        abs_contracts_sum = 0.0

        for leg in block.legs:
            premium = PremiumPerArroba(leg.premium.abs().value * float(premium_mult))
            contracts = Contracts(leg.contracts.value * float(contracts_mult))
            adjusted = OptionLeg(leg.leg_id, leg.label, leg.kind, leg.strike, premium, contracts)

            curve = model.curve_for_leg(adjusted)
            legs_map[adjusted.label] = curve
            curves.append(curve)

            w = adjusted.contracts.abs()
            weights.append(w)
            abs_contracts_sum += w

        per_arroba = aggregator.weighted_average(curves, weights)
        portfolio = portfolio.plus(per_arroba)

        total_reais = per_arroba.scaled(abs_contracts_sum * float(arrobas_per_contract))
        results.append(BlockResult(block, legs_map, per_arroba, total_reais, abs_contracts_sum))

    plotter = PlotBuilder(grid)
    st.plotly_chart(plotter.payoff_per_arroba(results, portfolio, strikes_all), use_container_width=True)

    if show_total:
        portfolio_total = PayoffCurve(np.zeros_like(grid.values))
        for r in results:
            portfolio_total = portfolio_total.plus(r.total_reais)
        st.plotly_chart(plotter.payoff_total_reais(results, portfolio_total, strikes_all), use_container_width=True)

    st.subheader("Resumo dos blocos selecionados")
    st.dataframe(summary_table(results), use_container_width=True)


if __name__ == "__main__":
    main()
