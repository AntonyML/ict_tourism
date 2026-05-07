"""Gráficas históricas y objetos descriptivos para el dashboard ICT."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from modules.data_loader import DataLoader


def create_total_arrivals_chart(total_df: pd.DataFrame) -> go.Figure:
    """Crea una serie histórica de llegadas totales con énfasis en 2020."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=total_df["Año"],
            y=total_df["Total"],
            mode="lines+markers",
            name="Llegadas totales",
            line=dict(color="#166534", width=2.4),
            marker=dict(size=5),
        )
    )
    if 2020 in total_df.index:
        value_2020 = float(total_df.loc[2020, "Total"])
        fig.add_vline(x=2020, line_dash="dash", line_color="#dc2626")
        fig.add_annotation(
            x=2020,
            y=value_2020,
            text="Caída 2020",
            showarrow=True,
            arrowhead=2,
            ax=40,
            ay=-45,
            bgcolor="white",
            bordercolor="#dc2626",
        )
    fig.update_layout(
        title="Llegadas internacionales totales a Costa Rica",
        xaxis_title="Año",
        yaxis_title="Llegadas",
        hovermode="x unified",
        template="plotly_white",
    )
    return fig


def create_variation_chart(total_df: pd.DataFrame) -> go.Figure:
    """Calcula y grafica la variación porcentual anual con colores por signo."""
    variation_df = total_df[["Año", "Total"]].copy()
    variation_df["Var %"] = variation_df["Total"].pct_change() * 100
    variation_df = variation_df.dropna(subset=["Var %"])
    colors = ["#15803d" if value >= 0 else "#dc2626" for value in variation_df["Var %"]]
    fig = go.Figure(
        go.Bar(
            x=variation_df["Año"],
            y=variation_df["Var %"],
            marker_color=colors,
            name="Variación anual",
        )
    )
    if 2020 in variation_df["Año"].values:
        value_2020 = float(variation_df.loc[variation_df["Año"] == 2020, "Var %"].iloc[0])
        fig.add_annotation(
            x=2020,
            y=value_2020,
            text="Choque pandémico",
            showarrow=True,
            arrowhead=2,
            ax=50,
            ay=-30,
            bgcolor="white",
            bordercolor="#dc2626",
        )
    fig.update_layout(
        title="Variación porcentual anual de llegadas totales",
        xaxis_title="Año",
        yaxis_title="Variación %",
        template="plotly_white",
        hovermode="x unified",
    )
    return fig


def create_zone_2025_chart(zone_df: pd.DataFrame) -> go.Figure:
    """Crea un gráfico horizontal de llegadas por zona en 2025."""
    if 2025 in zone_df.index:
        zone_values = zone_df.loc[2025, DataLoader.ZONE_COLUMNS]
    else:
        zone_values = zone_df.iloc[-1][DataLoader.ZONE_COLUMNS]
    ordered = zone_values.sort_values()
    fig = go.Figure(
        go.Bar(
            x=ordered.values,
            y=ordered.index,
            orientation="h",
            marker_color="#0f766e",
            name="Llegadas por zona",
        )
    )
    fig.update_layout(
        title="Llegadas por zona geográfica en 2025",
        xaxis_title="Llegadas",
        yaxis_title="Zona",
        template="plotly_white",
    )
    return fig


def render_dashboard(total_df: pd.DataFrame, air_df: pd.DataFrame, zone_df: pd.DataFrame) -> dict[str, object]:
    """Devuelve figuras y textos introductorios para el dashboard descriptivo."""
    latest_year = int(total_df["Año"].max())
    air_share = None
    if latest_year in air_df.index and latest_year in total_df.index:
        air_share = float(air_df.loc[latest_year, "Vía aérea"] / total_df.loc[latest_year, "Total"] * 100)
    return {
        "title": "Dashboard descriptivo",
        "charts": [
            {
                "figure": create_total_arrivals_chart(total_df),
                "text": "La serie histórica permite ver la expansión de largo plazo del turismo receptor y el quiebre extraordinario observado en 2020.",
            },
            {
                "figure": create_variation_chart(total_df),
                "text": "Las barras separan los años de crecimiento y contracción para identificar ciclos, recuperaciones y choques atípicos.",
            },
            {
                "figure": create_zone_2025_chart(zone_df),
                "text": (
                    f"La distribución por zona muestra los mercados emisores más relevantes para {latest_year}."
                    + (f" En ese año, la vía aérea representó aproximadamente {air_share:,.1f}% del total." if air_share else "")
                ),
            },
        ],
    }
