"""Programación lineal para asignar presupuesto promocional por zona geográfica."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pulp

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
    capacities: dict[str, float] = {}
    for zone in DataLoader.ZONE_COLUMNS:
        series = zone_df_actual[zone].astype(float)
        latest = float(zone_df_actual.loc[2025, zone] if 2025 in zone_df_actual.index else series.iloc[-1])
        pct_growth = series.pct_change().replace([np.inf, -np.inf], np.nan).dropna()
        max_growth = max(float(pct_growth.max()) if not pct_growth.empty else 0.0, 0.05)
        capacities[zone] = max(latest * max_growth * 1.2, latest * 0.02)
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


def render_optimization_module(zone3_df: pd.DataFrame, zone4_df: pd.DataFrame, budget: float) -> OptimizationResult:
    """Resuelve el modelo y devuelve objetos listos para presentación."""
    solution, optimal_value, shadow_prices = build_and_solve_lp(zone3_df, zone4_df, budget)
    efficiencies = _normalize_shares(zone4_df).mean()
    capacities = _capacity_from_history(zone3_df)
    table = pd.DataFrame(
        {
            "Zona": list(solution.keys()),
            "Asignación óptima": list(solution.values()),
            "Eficiencia": [efficiencies[zone] for zone in solution],
            "Capacidad estimada": [capacities[zone] for zone in solution],
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
