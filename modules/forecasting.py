"""Modelos de pronóstico y métricas para series de llegadas turísticas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from numpy.typing import ArrayLike, NDArray
from statsmodels.tsa.holtwinters import Holt, SimpleExpSmoothing


@dataclass
class ForecastingResult:
    """Resultado completo de la comparación de modelos."""

    metrics: pd.DataFrame
    best_model: str
    figure: go.Figure


def moving_average(series: ArrayLike, window: int) -> NDArray[np.float64]:
    """Calcula pronósticos de promedio móvil no centrado alineados con la serie."""
    values = np.asarray(series, dtype=float)
    if window <= 0:
        raise ValueError("window debe ser mayor que cero.")
    if len(values) < window:
        return np.full(len(values), np.nan)
    kernel = np.ones(window) / window
    valid = np.convolve(values, kernel, mode="valid")
    return np.concatenate([np.full(window - 1, np.nan), valid])


def simple_exponential_smoothing(series: ArrayLike, alpha: float) -> Any:
    """Ajusta Simple Exponential Smoothing con statsmodels."""
    values = np.asarray(series, dtype=float)
    model = SimpleExpSmoothing(values, initialization_method="estimated")
    return model.fit(smoothing_level=alpha, optimized=True)


def holt_trend(series: ArrayLike) -> Any:
    """Ajusta Holt lineal sin componente estacional."""
    values = np.asarray(series, dtype=float)
    model = Holt(values, initialization_method="estimated")
    return model.fit(optimized=True)


def calculate_metrics(actual: ArrayLike, predicted: ArrayLike) -> dict[str, float]:
    """Calcula MAE, RMSE y MAPE ignorando valores NaN."""
    actual_arr = np.asarray(actual, dtype=float)
    pred_arr = np.asarray(predicted, dtype=float)
    mask = ~(np.isnan(actual_arr) | np.isnan(pred_arr)) & (actual_arr != 0)
    if not np.any(mask):
        return {"MAE": np.nan, "RMSE": np.nan, "MAPE": np.nan}
    errors = actual_arr[mask] - pred_arr[mask]
    mae = float(np.mean(np.abs(errors)))
    rmse = float(np.sqrt(np.mean(errors**2)))
    mape = float(np.mean(np.abs(errors / actual_arr[mask])) * 100)
    return {"MAE": mae, "RMSE": rmse, "MAPE": mape}


def compare_models(
    total_df: pd.DataFrame,
    start_year: int = 1990,
    exclude_2020: bool = False,
    horizon_years: list[int] | None = None,
) -> ForecastingResult:
    """Compara MA, SES y Holt, y crea la figura del mejor modelo."""
    horizon = horizon_years or list(range(2025, 2031))
    train_df = total_df[(total_df["Año"] >= start_year) & (total_df["Año"] <= 2024)].copy()
    if exclude_2020:
        train_df = train_df[train_df["Año"] != 2020]
    if len(train_df) < 6:
        raise ValueError("Se requieren al menos seis observaciones para comparar modelos.")

    y_train = train_df["Total"].astype(float).to_numpy()
    years_train = train_df["Año"].astype(int).to_numpy()

    ma_pred = moving_average(y_train, window=3)
    ses_fit = simple_exponential_smoothing(y_train, alpha=0.3)
    ses_pred = np.asarray(ses_fit.fittedvalues, dtype=float)
    holt_fit = holt_trend(y_train)
    holt_pred = np.asarray(holt_fit.fittedvalues, dtype=float)

    model_predictions = {
        "Promedio móvil": ma_pred,
        "Suavizamiento exponencial simple": ses_pred,
        "Holt tendencia": holt_pred,
    }
    metrics_df = pd.DataFrame(
        [{"Modelo": name, **calculate_metrics(y_train, prediction)} for name, prediction in model_predictions.items()]
    )
    best_model = str(metrics_df.sort_values("RMSE").iloc[0]["Modelo"])

    if best_model == "Promedio móvil":
        last_window = y_train[-3:].copy()
        future = []
        for _ in horizon:
            next_value = float(np.mean(last_window))
            future.append(next_value)
            last_window = np.append(last_window[1:], next_value)
        best_in_sample = ma_pred
    elif best_model == "Suavizamiento exponencial simple":
        future = np.asarray(ses_fit.forecast(len(horizon)), dtype=float)
        best_in_sample = ses_pred
    else:
        future = np.asarray(holt_fit.forecast(len(horizon)), dtype=float)
        best_in_sample = holt_pred

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=total_df["Año"],
            y=total_df["Total"],
            mode="lines+markers",
            name="Histórico completo",
            line=dict(color="#334155", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years_train,
            y=best_in_sample,
            mode="lines",
            name=f"Ajuste dentro de muestra: {best_model}",
            line=dict(color="#2563eb", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=horizon,
            y=future,
            mode="lines+markers",
            name="Pronóstico 2025-2030",
            line=dict(color="#16a34a", width=3, dash="dash"),
        )
    )

    if best_model == "Holt tendencia":
        residual_std = float(np.nanstd(y_train - best_in_sample))
        upper = np.asarray(future) + 1.96 * residual_std
        lower = np.asarray(future) - 1.96 * residual_std
        fig.add_trace(go.Scatter(x=horizon, y=upper, mode="lines", line=dict(width=0), showlegend=False))
        fig.add_trace(
            go.Scatter(
                x=horizon,
                y=lower,
                mode="lines",
                fill="tonexty",
                fillcolor="rgba(22, 163, 74, 0.18)",
                line=dict(width=0),
                name="Banda aproximada 95%",
            )
        )

    fig.add_vline(x=2020, line_dash="dash", line_color="#dc2626")
    fig.add_annotation(x=2020, y=float(total_df.loc[2020, "Total"]) if 2020 in total_df.index else None, text="2020", showarrow=True)
    fig.update_layout(
        title=f"Mejor modelo por RMSE: {best_model}",
        xaxis_title="Año",
        yaxis_title="Llegadas",
        template="plotly_white",
        hovermode="x unified",
    )
    metrics_df[["MAE", "RMSE", "MAPE"]] = metrics_df[["MAE", "RMSE", "MAPE"]].round(2)
    return ForecastingResult(metrics=metrics_df, best_model=best_model, figure=fig)


def render_forecasting_module(total_df: pd.DataFrame) -> dict[str, object]:
    """Devuelve metadatos de controles para que app.py renderice el módulo."""
    min_year = int(total_df["Año"].min())
    return {
        "title": "Pronósticos",
        "start_year_min": min_year,
        "start_year_max": 2020,
        "start_year_default": 1990 if min_year <= 1990 else min_year,
        "horizon": "2025-2030",
    }
