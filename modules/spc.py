"""Control estadístico de procesos mediante gráfico I-Chart para variaciones ICT."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def compute_i_chart_limits(data: pd.DataFrame | pd.Series, exclude_2020: bool = False) -> dict[str, float]:
    """Calcula media, LCS y LCI usando tres desviaciones estándar globales."""
    if isinstance(data, pd.DataFrame):
        values_df = data[["Año", "Var %"]].copy()
    else:
        values_df = data.rename("Var %").reset_index().rename(columns={"index": "Año"})
    if exclude_2020:
        values_df = values_df[values_df["Año"] != 2020]
    values = values_df["Var %"].astype(float).dropna()
    mean = float(values.mean())
    sigma = float(values.std(ddof=1))
    return {"LCS": mean + 3 * sigma, "LC": mean, "LCI": mean - 3 * sigma, "Sigma": sigma}


def plot_i_chart(data: pd.DataFrame, limits: dict[str, float], title: str) -> go.Figure:
    """Grafica puntos individuales, límites de control y violaciones."""
    chart_df = data[["Año", "Var %"]].copy()
    chart_df["Fuera de límites"] = (chart_df["Var %"] > limits["LCS"]) | (chart_df["Var %"] < limits["LCI"])
    colors = np.where(chart_df["Fuera de límites"], "#dc2626", "#2563eb")
    if 2020 in chart_df["Año"].values:
        colors = np.where(chart_df["Año"] == 2020, "#7c2d12", colors)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=chart_df["Año"],
            y=chart_df["Var %"],
            mode="lines+markers",
            marker=dict(color=colors, size=8),
            line=dict(color="#94a3b8"),
            name="Var %",
        )
    )
    for key, color, dash in [("LCS", "#dc2626", "dash"), ("LC", "#111827", "solid"), ("LCI", "#dc2626", "dash")]:
        fig.add_hline(y=limits[key], line_color=color, line_dash=dash, annotation_text=key)
    if 2020 in chart_df["Año"].values:
        value_2020 = float(chart_df.loc[chart_df["Año"] == 2020, "Var %"].iloc[0])
        fig.add_annotation(
            x=2020,
            y=value_2020,
            text="Causa especial 2020",
            showarrow=True,
            arrowhead=2,
            ax=50,
            ay=-35,
            bgcolor="white",
            bordercolor="#7c2d12",
        )
    fig.update_layout(
        title=title,
        xaxis_title="Año",
        yaxis_title="Variación %",
        template="plotly_white",
        hovermode="x unified",
    )
    return fig


def render_spc_module(var_df: pd.DataFrame, exclude_2020: bool = False) -> dict[str, object]:
    """Devuelve figura, límites e interpretación automática del I-Chart."""
    limits = compute_i_chart_limits(var_df, exclude_2020=exclude_2020)
    figure = plot_i_chart(var_df, limits, "I-Chart de variación porcentual anual")
    out_of_control = var_df[(var_df["Var %"] > limits["LCS"]) | (var_df["Var %"] < limits["LCI"])]
    if out_of_control.empty:
        interpretation = "El proceso no muestra puntos fuera de los límites de control calculados."
    else:
        years = ", ".join(str(int(year)) for year in out_of_control["Año"])
        interpretation = f"El proceso no está bajo control estadístico: hay señales fuera de límites en {years}."
    return {"figure": figure, "limits": limits, "interpretation": interpretation}
