"""Punto de entrada Streamlit para la aplicación modular de análisis turístico del ICT."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from modules.data_loader import DataLoader
from modules.descriptive import render_dashboard
from modules.forecasting import compare_models, render_forecasting_module
from modules.montecarlo import render_montecarlo_module
from modules.optimization import render_optimization_module
from modules.spc import render_spc_module


st.set_page_config(page_title="ICT Tourism Analytics", page_icon="📈", layout="wide")


@st.cache_data(show_spinner=False)
def load_data() -> dict[str, pd.DataFrame]:
    """Carga todas las hojas limpias del Excel."""
    return {
        "total": DataLoader.load_total_arrivals(),
        "air": DataLoader.load_air_arrivals(),
        "zone3": DataLoader.load_by_zone("Cuadro 3"),
        "zone4": DataLoader.load_by_zone("Cuadro 4"),
        "variation": DataLoader.load_annual_variation(),
        "growth": DataLoader.load_growth_rates(),
    }


def show_descriptive(data: dict[str, pd.DataFrame]) -> None:
    """Renderiza el dashboard descriptivo."""
    st.header("Dashboard descriptivo")
    dashboard = render_dashboard(data["total"], data["air"], data["zone3"])
    for chart in dashboard["charts"]:
        st.plotly_chart(chart["figure"], use_container_width=True)
        st.caption(chart["text"])


def show_forecasting(data: dict[str, pd.DataFrame]) -> None:
    """Renderiza controles y resultados de pronóstico."""
    st.header("Pronósticos")
    config = render_forecasting_module(data["total"])
    col_a, col_b = st.columns([1, 1])
    with col_a:
        start_year = st.slider(
            "Año de inicio del entrenamiento",
            min_value=int(config["start_year_min"]),
            max_value=int(config["start_year_max"]),
            value=int(config["start_year_default"]),
        )
    with col_b:
        exclude_2020 = st.checkbox("Excluir 2020 del entrenamiento", value=False)

    st.caption("El entrenamiento usa los datos desde el año seleccionado hasta 2024. El horizonte fijo es 2025-2030.")
    if st.button("Comparar modelos", type="primary"):
        try:
            result = compare_models(data["total"], start_year=start_year, exclude_2020=exclude_2020)
            st.subheader("Tabla comparativa de métricas")
            st.dataframe(result.metrics, use_container_width=True, hide_index=True)
            st.success(f"Mejor modelo por RMSE: {result.best_model}")
            st.plotly_chart(result.figure, use_container_width=True)
        except Exception as exc:
            st.error(f"No fue posible ajustar los modelos: {exc}")


def show_spc(data: dict[str, pd.DataFrame]) -> None:
    """Renderiza el módulo de control estadístico."""
    st.header("Control estadístico de procesos")
    exclude_2020 = st.toggle("Excluir 2020", value=False)
    result = render_spc_module(data["variation"], exclude_2020=exclude_2020)
    st.plotly_chart(result["figure"], use_container_width=True)
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("LCI", f"{result['limits']['LCI']:.2f}%")
    col_b.metric("LC", f"{result['limits']['LC']:.2f}%")
    col_c.metric("LCS", f"{result['limits']['LCS']:.2f}%")
    st.info(result["interpretation"])


def show_montecarlo(data: dict[str, pd.DataFrame]) -> None:
    """Renderiza simulación Monte Carlo."""
    st.header("Simulación Monte Carlo")
    n_simulations = st.slider("Número de simulaciones", 1_000, 50_000, 10_000, step=1_000)
    if st.button("Ejecutar simulación", type="primary"):
        try:
            result = render_montecarlo_module(data["growth"], data["total"], n_simulations=n_simulations)
            st.success(f"Distribución seleccionada por AIC: {result['distribution'].name}")
            st.plotly_chart(result["histogram"], use_container_width=True)
            st.plotly_chart(result["fan_chart"], use_container_width=True)
            st.subheader("Resumen de percentiles")
            st.dataframe(result["summary"], use_container_width=True, hide_index=True)
            st.caption("P10, P50 y P90 representan escenarios donde 10%, 50% y 90% de las simulaciones quedan por debajo de ese valor.")
        except Exception as exc:
            st.error(f"No fue posible ejecutar la simulación: {exc}")


def show_optimization(data: dict[str, pd.DataFrame]) -> None:
    """Renderiza programación lineal de presupuesto."""
    st.header("Programación Lineal")
    budget = st.number_input(
        "Presupuesto total hipotético",
        min_value=1_000.0,
        value=10_000_000.0,
        step=100_000.0,
        format="%.2f",
    )
    if st.button("Optimizar", type="primary"):
        try:
            result = render_optimization_module(data["zone3"], data["zone4"], budget=budget)
            st.success(f"Estado del modelo: {result.status}")
            st.dataframe(result.allocation_table, use_container_width=True, hide_index=True)
            st.plotly_chart(result.figure, use_container_width=True)
            st.metric("Valor máximo de llegadas proyectadas", f"{result.optimal_value:,.2f}")
            budget_shadow = result.shadow_prices.get("Presupuesto", 0.0)
            st.metric("Precio sombra del presupuesto", f"{budget_shadow:,.6f}")
            st.caption("Interpretación: incremento marginal estimado de llegadas por cada unidad adicional de presupuesto, bajo los supuestos del modelo.")
            st.subheader("Supuestos declarados")
            st.markdown(
                """
                - Eficiencia basada en participación promedio histórica por zona.
                - Capacidad máxima basada en crecimiento máximo observado y aplicada a llegadas de 2025 con factor 1.2.
                - El presupuesto no tiene costo fijo por zona.
                - Las variables son continuas y representan esfuerzo de mercadeo asignado.
                """
            )
        except Exception as exc:
            st.error(f"No fue posible resolver la optimización: {exc}")


def main() -> None:
    """Orquesta la navegación principal de la app."""
    st.title("Análisis de Turismo ICT")
    st.caption("Aplicación modular para explorar, pronosticar y optimizar indicadores turísticos de Costa Rica.")

    try:
        data = load_data()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.stop()
    except Exception as exc:
        st.error(f"No fue posible cargar o limpiar el Excel del ICT: {exc}")
        st.stop()

    option = st.sidebar.radio(
        "Seleccione un módulo",
        [
            "Dashboard descriptivo",
            "Pronósticos",
            "Control estadístico de procesos",
            "Simulación Monte Carlo",
            "Programación Lineal",
        ],
    )

    if option == "Dashboard descriptivo":
        show_descriptive(data)
    elif option == "Pronósticos":
        show_forecasting(data)
    elif option == "Control estadístico de procesos":
        show_spc(data)
    elif option == "Simulación Monte Carlo":
        show_montecarlo(data)
    elif option == "Programación Lineal":
        show_optimization(data)


if __name__ == "__main__":
    main()
