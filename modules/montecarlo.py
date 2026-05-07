"""Ajuste probabilístico y simulación Monte Carlo para llegadas turísticas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats


@dataclass
class FittedDistribution:
    """Distribución ajustada seleccionada por AIC."""

    name: str
    distribution: Any
    params: tuple[float, ...]
    aic: float

    def rvs(self, size: int | tuple[int, ...], random_state: int | None = None) -> np.ndarray:
        """Muestra tasas aleatorias desde la distribución ajustada."""
        return self.distribution.rvs(*self.params, size=size, random_state=random_state)

    def pdf(self, values: np.ndarray) -> np.ndarray:
        """Evalúa la densidad ajustada."""
        return self.distribution.pdf(values, *self.params)


def fit_distribution(growth_series: pd.Series) -> FittedDistribution:
    """Ajusta normal, logística y cauchy, eligiendo la menor AIC."""
    values = pd.to_numeric(growth_series, errors="coerce").dropna().astype(float).to_numpy()
    if len(values) < 2:
        raise ValueError("Se requieren al menos dos tasas de crecimiento para ajustar una distribución.")

    candidates = {"Normal": stats.norm, "Logística": stats.logistic, "Cauchy": stats.cauchy}
    fitted: list[FittedDistribution] = []
    for name, distribution in candidates.items():
        params = distribution.fit(values)
        log_likelihood = np.sum(distribution.logpdf(values, *params))
        k = len(params)
        aic = float(2 * k - 2 * log_likelihood)
        fitted.append(FittedDistribution(name=name, distribution=distribution, params=params, aic=aic))
    return min(fitted, key=lambda item: item.aic)


def simulate(
    dist_fitted: FittedDistribution,
    n_simulations: int,
    n_years: int = 5,
    current_total: float = 0.0,
) -> pd.DataFrame:
    """Genera caminos estocásticos de llegadas para 2026-2030."""
    if current_total <= 0:
        raise ValueError("current_total debe ser mayor que cero.")
    sampled_rates = dist_fitted.rvs(size=(n_simulations, n_years), random_state=42)
    sampled_rates = np.clip(sampled_rates, -0.95, 2.0)
    totals = np.empty_like(sampled_rates, dtype=float)
    previous = np.full(n_simulations, current_total, dtype=float)
    for column in range(n_years):
        previous = previous * (1 + sampled_rates[:, column])
        totals[:, column] = previous
    years = list(range(2026, 2026 + n_years))
    return pd.DataFrame(totals, columns=years)


def plot_fan_chart(simulations_df: pd.DataFrame) -> go.Figure:
    """Crea un fan chart con percentiles P10, P50 y P90."""
    summary = simulations_df.quantile([0.10, 0.50, 0.90]).T
    summary.columns = ["P10", "P50", "P90"]
    years = summary.index.astype(int)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=summary["P90"], mode="lines", line=dict(width=0), showlegend=False))
    fig.add_trace(
        go.Scatter(
            x=years,
            y=summary["P10"],
            mode="lines",
            fill="tonexty",
            fillcolor="rgba(37, 99, 235, 0.20)",
            line=dict(width=0),
            name="Banda P10-P90",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years,
            y=summary["P50"],
            mode="lines+markers",
            name="Mediana P50",
            line=dict(color="#2563eb", width=3),
        )
    )
    fig.update_layout(
        title="Fan chart de llegadas proyectadas",
        xaxis_title="Año",
        yaxis_title="Llegadas",
        template="plotly_white",
        hovermode="x unified",
    )
    return fig


def create_growth_histogram(growth_rates: np.ndarray, dist_fitted: FittedDistribution) -> go.Figure:
    """Grafica histograma de tasas simuladas con curva de densidad ajustada."""
    values = np.asarray(growth_rates, dtype=float).ravel()
    x_min, x_max = np.nanpercentile(values, [1, 99])
    x_grid = np.linspace(x_min, x_max, 250)
    fig = go.Figure()
    fig.add_trace(
        go.Histogram(x=values, histnorm="probability density", nbinsx=50, name="Tasas simuladas", marker_color="#0f766e")
    )
    fig.add_trace(
        go.Scatter(x=x_grid, y=dist_fitted.pdf(x_grid), mode="lines", name=f"Distribución {dist_fitted.name}", line=dict(color="#dc2626", width=2))
    )
    fig.update_layout(
        title="Distribución de tasas de crecimiento simuladas",
        xaxis_title="Tasa de crecimiento",
        yaxis_title="Densidad",
        template="plotly_white",
    )
    return fig


def render_montecarlo_module(growth_df: pd.DataFrame, total_df: pd.DataFrame, n_simulations: int) -> dict[str, object]:
    """Ejecuta ajuste y simulación, devolviendo figuras y tabla resumen."""
    growth_clean = growth_df[(growth_df["Año"] > 2021) & (growth_df["Año"] != 2020)]["Crecimiento"]
    fitted = fit_distribution(growth_clean)
    current_total = float(total_df.loc[2025, "Total"] if 2025 in total_df.index else total_df.iloc[-1]["Total"])
    simulations = simulate(fitted, n_simulations=n_simulations, n_years=5, current_total=current_total)
    rates = simulations.pct_change(axis=1)
    rates.iloc[:, 0] = simulations.iloc[:, 0] / current_total - 1
    summary = simulations.quantile([0.10, 0.50, 0.90]).T.reset_index()
    summary.columns = ["Año", "P10", "P50", "P90"]
    return {
        "distribution": fitted,
        "histogram": create_growth_histogram(rates.to_numpy(), fitted),
        "fan_chart": plot_fan_chart(simulations),
        "summary": summary,
    }
