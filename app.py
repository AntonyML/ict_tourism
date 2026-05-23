"""Punto de entrada Streamlit para la aplicación modular de análisis turístico del ICT."""

from __future__ import annotations

import logging
from collections.abc import Callable

import pandas as pd
import streamlit as st

from modules.constants import FORECAST_ALPHA, FORECAST_MA_WINDOW
from modules.data_loader import DataLoader
from modules.descriptive import render_dashboard
from modules.forecasting import compare_models, render_forecasting_module
from modules.limitations import render_limitations
from modules.montecarlo import render_montecarlo_module
from modules.optimization import render_optimization_module, sensitivity_analysis
from modules.spc import render_spc_module


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
LOGGER = logging.getLogger("ict_tourism")

st.set_page_config(page_title="ICT Tourism Analytics", page_icon=":chart_with_upwards_trend:", layout="wide")


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


def _show_data_banner(data: dict[str, pd.DataFrame]) -> None:
    """Muestra métricas de validación de los datos cargados."""
    total_df = data["total"]
    year_min = int(total_df["Año"].min())
    year_max = int(total_df["Año"].max())
    year_count = len(total_df)
    missing = sum(
        1 for y in range(year_min, year_max + 1) if y not in total_df["Año"].values
    )
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Fuente", "ICT 2025")
    col2.metric("Período", f"{year_min} – {year_max}")
    col3.metric("Registros anuales", year_count)
    col4.metric("Años faltantes", missing if missing > 0 else "Ninguno")


def render_section(section: Callable[[dict[str, pd.DataFrame]], None], data: dict[str, pd.DataFrame]) -> None:
    """Ejecuta cada sección con un límite de error amigable."""
    try:
        section(data)
    except Exception as exc:
        LOGGER.exception("Error al renderizar sección")
        st.error(f"No fue posible renderizar este módulo: {exc}")


def show_descriptive(data: dict[str, pd.DataFrame]) -> None:
    """Renderiza el dashboard descriptivo."""
    st.header("Dashboard descriptivo")
    with st.expander("  Limitaciones de este módulo"):
        st.markdown(render_limitations("descriptive"))
    dashboard = render_dashboard(data["total"], data["air"], data["zone3"])
    for chart in dashboard["charts"]:
        st.plotly_chart(chart["figure"], use_container_width=True)
        st.caption(chart["text"])


def show_forecasting(data: dict[str, pd.DataFrame]) -> None:
    """Renderiza controles y resultados de pronóstico."""
    st.header("Pronósticos")
    with st.expander("  Limitaciones de este módulo"):
        st.markdown(render_limitations("forecasting"))
    with st.expander("   Parámetros utilizados"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Promedio móvil**")
            st.code(f"Ventana = {FORECAST_MA_WINDOW} años", language="text")
            st.caption("Balance entre suavizado y sensibilidad a cambios.")
        with col2:
            st.markdown("**SES — Suavizamiento exponencial**")
            st.code(f"α = {FORECAST_ALPHA} (fijo, moderado)", language="text")
            st.caption("Fijo para comparación controlada entre modelos.")
        with col3:
            st.markdown("**Holt con tendencia**")
            st.code("α y β optimizados automáticamente", language="text")
            st.caption("Parámetros calibrados por máxima verosimilitud.")

    config = render_forecasting_module(data["total"])
    col_a, col_b = st.columns([1, 1])
    with col_a:
        start_year = st.slider(
            "Año de inicio del entrenamiento",
            min_value=int(config["start_year_min"]),
            max_value=int(config["start_year_max"]),
            value=int(config["start_year_default"]),
            key="forecast_start_year",
        )
    with col_b:
        exclude_2020 = st.checkbox("Excluir 2020 del entrenamiento", value=False, key="forecast_exclude_2020")

    st.caption("Entrenamiento: datos desde el año seleccionado hasta 2024. Horizonte fijo: 2025-2030.")
    if st.button("Comparar modelos", type="primary", key="forecast_compare_models"):
        try:
            with st.spinner("Ajustando modelos de pronóstico..."):
                result = compare_models(data["total"], start_year=start_year, exclude_2020=exclude_2020)
            st.subheader("Tabla comparativa de métricas")
            st.dataframe(result.metrics, use_container_width=True, hide_index=True)
            st.success(f"Mejor modelo por RMSE: **{result.best_model}**")
            st.plotly_chart(result.figure, use_container_width=True)
            st.caption("La banda sombreada representa la incertidumbre aproximada del 95%, calculada a partir de los residuos históricos del modelo seleccionado.")
        except Exception as exc:
            st.error(f"No fue posible ajustar los modelos: {exc}")


def show_spc(data: dict[str, pd.DataFrame]) -> None:
    """Renderiza el módulo de control estadístico."""
    st.header("Control estadístico de procesos")
    with st.expander("  Limitaciones de este módulo"):
        st.markdown(render_limitations("spc"))
    exclude_2020 = st.toggle("Excluir 2020 del cálculo de límites", value=False, key="spc_exclude_2020")
    st.caption("Excluir 2020 produce límites más representativos de la variabilidad normal del sector, sin el choque pandémico.")
    result = render_spc_module(data["variation"], exclude_2020=exclude_2020)
    st.plotly_chart(result["figure"], use_container_width=True)
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("LCI", f"{result['limits']['LCI']:.2f}%")
    col_b.metric("LC (media)", f"{result['limits']['LC']:.2f}%")
    col_c.metric("LCS", f"{result['limits']['LCS']:.2f}%")
    col_d.metric("σ̂ (MR̄/d₂)", f"{result['limits']['Sigma']:.4f}")
    st.info(result["interpretation"])
    st.caption("Método: σ̂ = MR̄ / d₂ (d₂ = 1.128). Los límites son ±3σ̂ alrededor de la media histórica. Referencia: Montgomery (2020).")


def show_montecarlo(data: dict[str, pd.DataFrame]) -> None:
    """Renderiza simulación Monte Carlo."""
    st.header("Simulación Monte Carlo")
    with st.expander("  Limitaciones de este módulo"):
        st.markdown(render_limitations("montecarlo"))
    n_simulations = st.slider(
        "Número de simulaciones",
        1_000,
        50_000,
        10_000,
        step=1_000,
        key="montecarlo_n_simulations",
    )
    st.caption("Mayor número de simulaciones produce resultados más estables, pero aumenta el tiempo de cómputo.")
    if st.button("Ejecutar simulación", type="primary", key="montecarlo_run"):
        try:
            with st.spinner("Ejecutando simulaciones..."):
                result = render_montecarlo_module(data["growth"], data["total"], n_simulations=n_simulations)
            dist_name = result["distribution"].name
            dist_aic = round(result["distribution"].aic, 4)
            st.success(f"Distribución seleccionada por AIC: **{dist_name}** (AIC = {dist_aic})")
            st.caption("El Criterio de Información de Akaike (AIC) selecciona la distribución con mejor ajuste penalizando la complejidad del modelo.")
            st.plotly_chart(result["histogram"], use_container_width=True)
            st.plotly_chart(result["fan_chart"], use_container_width=True)
            st.subheader("Resumen de percentiles proyectados")
            st.dataframe(result["summary"], use_container_width=True, hide_index=True)
            st.caption("P10: escenario conservador. P50: escenario mediano. P90: escenario optimista. La banda P10-P90 cubre el 80% de los escenarios simulados.")
        except Exception as exc:
            st.error(f"No fue posible ejecutar la simulación: {exc}")


def show_optimization(data: dict[str, pd.DataFrame]) -> None:
    """Renderiza programación lineal de presupuesto."""
    st.header("Programación Lineal")
    with st.expander("  Limitaciones de este módulo"):
        st.markdown(render_limitations("optimization"))
    with st.expander("📐 Supuestos del modelo"):
        st.markdown(
            """
            - **Eficiencia (eᵢ):** participación promedio histórica de cada zona en el total de llegadas (proxy de eficiencia relativa).
            - **Capacidad (Cᵢ):** máximo crecimiento histórico observado × factor 1.2 × llegadas base 2025. Factor declarado en `constants.py`.
            - **Función objetivo:** Maximizar Z = Σ eᵢ · xᵢ. El valor Z es un escalar adimensional, no llegadas absolutas.
            - **Restricciones:** presupuesto total ≤ B; xᵢ ≤ Cᵢ; xᵢ ≥ 0.
            - **Solver:** CBC (Coin-or Branch and Cut) vía PuLP.
            """
        )
    budget = st.number_input(
        "Presupuesto total hipotético",
        min_value=1_000.0,
        value=10_000_000.0,
        step=100_000.0,
        format="%.2f",
        key="optimization_budget",
    )
    if st.button("Optimizar", type="primary", key="optimization_run"):
        try:
            with st.spinner("Resolviendo modelo lineal..."):
                result = render_optimization_module(data["zone3"], data["zone4"], budget=budget)
            st.success(f"Estado del modelo: **{result.status}**")
            st.dataframe(result.allocation_table, use_container_width=True, hide_index=True)
            st.plotly_chart(result.figure, use_container_width=True)
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Valor objetivo (Z)", f"{result.optimal_value:,.6f}")
            budget_shadow = result.shadow_prices.get("Presupuesto", 0.0)
            col_m2.metric("Precio sombra del presupuesto", f"{budget_shadow:,.8f}")
            st.caption(
                "**Precio sombra:** incremento marginal de Z por cada unidad adicional de presupuesto. "
                "Si es positivo, la restricción presupuestaria es activa: más presupuesto mejora el resultado."
            )
            st.subheader("Análisis de sensibilidad")
            with st.spinner("Calculando sensibilidad..."):
                sens_df = sensitivity_analysis(data["zone3"], data["zone4"], budget)
            st.dataframe(sens_df, use_container_width=True, hide_index=True)
            st.caption("Muestra cómo varía el valor óptimo Z ante cambios de ±5% y ±10% en el presupuesto base.")
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

    _show_data_banner(data)

    option = st.sidebar.radio(
        "Seleccione un módulo",
        [
            "Dashboard descriptivo",
            "Pronósticos",
            "Control estadístico de procesos",
            "Simulación Monte Carlo",
            "Programación Lineal",
        ],
        key="main_navigation",
    )

    if option == "Dashboard descriptivo":
        render_section(show_descriptive, data)
    elif option == "Pronósticos":
        render_section(show_forecasting, data)
    elif option == "Control estadístico de procesos":
        render_section(show_spc, data)
    elif option == "Simulación Monte Carlo":
        render_section(show_montecarlo, data)
    elif option == "Programación Lineal":
        render_section(show_optimization, data)


if __name__ == "__main__":
    main()
