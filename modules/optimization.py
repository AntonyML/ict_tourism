"""Programación lineal para asignar presupuesto promocional por zona geográfica."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pulp

from modules.constants import CAPACITY_MINIMUM, CAPACITY_SCALE_FACTOR
from modules.data_loader import DataLoader


@dataclass
class OptimizationResult:
    """Resultado de la optimización lineal."""

    solution: dict[str, float]
    optimal_value: float
    shadow_prices: dict[str, float]
    allocation_table: pd.DataFrame
    figure: go.Figure
    status: str


def _normalize_shares(zone_df_share: pd.DataFrame) -> pd.DataFrame:
    shares = zone_df_share[DataLoader.ZONE_COLUMNS].astype(float).copy()
    if shares.max().max() > 1:
        shares = shares / 100.0
    return shares


def _capacity_from_history(zone_df_actual: pd.DataFrame) -> dict[str, float]:
    """Calcula capacidad máxima por zona usando factor de escala de constants.py.

    Capacidad = últimas llegadas × máximo crecimiento histórico × CAPACITY_SCALE_FACTOR
    Mínimo garantizado = últimas llegadas × CAPACITY_MINIMUM

    Ver constants.py para justificación de CAPACITY_SCALE_FACTOR = 1.2.
    """
    capacities: dict[str, float] = {}
    for zone in DataLoader.ZONE_COLUMNS:
        series = zone_df_actual[zone].astype(float)
        latest = float(zone_df_actual.loc[2025, zone] if 2025 in zone_df_actual.index else series.iloc[-1])
        pct_growth = series.pct_change().replace([np.inf, -np.inf], np.nan).dropna()
        max_growth = max(float(pct_growth.max()) if not pct_growth.empty else 0.0, 0.05)
        capacities[zone] = max(latest * max_growth * CAPACITY_SCALE_FACTOR, latest * CAPACITY_MINIMUM)
    return capacities


def build_and_solve_lp(
    zone_df_actual: pd.DataFrame,
    zone_df_share: pd.DataFrame,
    budget: float,
) -> tuple[dict[str, float], float, dict[str, float]]:
    """Construye y resuelve el modelo PuLP de asignación promocional."""
    if budget <= 0:
        raise ValueError("El presupuesto debe ser mayor que cero.")

    efficiencies = _normalize_shares(zone_df_share).mean().to_dict()
    capacities = _capacity_from_history(zone_df_actual)

    problem = pulp.LpProblem("ICT_promotional_budget_allocation", pulp.LpMaximize)
    variables = {
        zone: pulp.LpVariable(f"x_{index}", lowBound=0, upBound=capacities[zone], cat="Continuous")
        for index, zone in enumerate(DataLoader.ZONE_COLUMNS)
    }
    problem += pulp.lpSum(efficiencies[zone] * variables[zone] for zone in DataLoader.ZONE_COLUMNS), "Llegadas_proyectadas"
    problem += pulp.lpSum(variables.values()) <= budget, "Presupuesto"

    solver = pulp.PULP_CBC_CMD(msg=False)
    problem.solve(solver)

    solution = {zone: float(variables[zone].value() or 0.0) for zone in DataLoader.ZONE_COLUMNS}
    optimal_value = float(pulp.value(problem.objective) or 0.0)
    shadow_prices = {
        name: float(constraint.pi) if getattr(constraint, "pi", None) is not None else 0.0
        for name, constraint in problem.constraints.items()
    }
    shadow_prices["Estado"] = float(1 if pulp.LpStatus[problem.status] == "Optimal" else 0)
    return solution, optimal_value, shadow_prices


def sensitivity_analysis(
    zone_df_actual: pd.DataFrame,
    zone_df_share: pd.DataFrame,
    base_budget: float,
    variations_pct: list[float] | None = None,
) -> pd.DataFrame:
    """Análisis de sensibilidad: cómo varía Z ante cambios en el presupuesto.

    Calcula el valor óptimo (Z) para distintos niveles de presupuesto
    (±10%, ±5% y 0% respecto al presupuesto base).

    El precio sombra de cada fila indica el incremento marginal de Z
    por unidad adicional de presupuesto en ese nivel.
    """
    if variations_pct is None:
        variations_pct = [-10.0, -5.0, 0.0, 5.0, 10.0]

    rows: list[dict[str, object]] = []
    for pct in variations_pct:
        adjusted = base_budget * (1 + pct / 100.0)
        _, opt_value, sp = build_and_solve_lp(zone_df_actual, zone_df_share, adjusted)
        rows.append(
            {
                "Cambio presupuesto": f"{pct:+.1f}%",
                "Presupuesto": round(adjusted, 2),
                "Valor objetivo (Z)": round(opt_value, 6),
                "Precio sombra": round(sp.get("Presupuesto", 0.0), 8),
            }
        )
    return pd.DataFrame(rows)


def render_optimization_module(zone3_df: pd.DataFrame, zone4_df: pd.DataFrame, budget: float) -> OptimizationResult:
    """Resuelve el modelo y devuelve objetos listos para presentación."""
    solution, optimal_value, shadow_prices = build_and_solve_lp(zone3_df, zone4_df, budget)
    efficiencies = _normalize_shares(zone4_df).mean()
    capacities = _capacity_from_history(zone3_df)
    table = pd.DataFrame(
        {
            "Zona": list(solution.keys()),
            "Asignación óptima": list(solution.values()),
            "Eficiencia (eᵢ)": [round(efficiencies[zone], 4) for zone in solution],
            "Capacidad estimada (Cᵢ)": [round(capacities[zone], 0) for zone in solution],
        }
    )
    fig = go.Figure(
        go.Bar(
            x=table["Zona"],
            y=table["Asignación óptima"],
            marker_color="#2563eb",
            name="Asignación",
        )
    )
    fig.update_layout(
        title="Asignación óptima de presupuesto por zona",
        xaxis_title="Zona",
        yaxis_title="Presupuesto asignado",
        template="plotly_white",
    )
    status = "Óptimo" if shadow_prices.get("Estado") == 1 else "No óptimo"
    shadow_prices = {key: value for key, value in shadow_prices.items() if key != "Estado"}
    return OptimizationResult(
        solution=solution,
        optimal_value=optimal_value,
        shadow_prices=shadow_prices,
        allocation_table=table,
        figure=fig,
        status=status,
    )
