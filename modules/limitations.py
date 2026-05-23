"""Documentación de limitaciones metodológicas por módulo.

Este módulo centraliza las advertencias académicas de cada técnica
implementada, para que sean visibles al usuario en la interfaz.
"""

from __future__ import annotations

LIMITATIONS: dict[str, dict[str, str | list[str]]] = {
    "descriptive": {
        "title": "Limitaciones del Análisis Descriptivo",
        "items": [
            "Los datos provienen de publicaciones del ICT; cambios metodológicos en la recolección pueden afectar la comparabilidad entre periodos históricos.",
            "El año 2020 se analiza como evento extraordinario. Sus valores incluyen distorsiones por confinamiento y cierre de fronteras que no reflejan comportamiento estructural del sector.",
            "Los datos de llegadas por vía aérea están disponibles solo desde 1976; la serie completa (llegadas totales) parte de 1951.",
        ],
    },
    "forecasting": {
        "title": "Limitaciones de los Modelos de Pronóstico",
        "items": [
            "Parámetro α = 0.3 (SES) es fijo para mantener condiciones controladas de comparación entre los tres modelos. No se optimiza automáticamente.",
            "Ventana del promedio móvil = 3 años. Se requieren al menos 6 observaciones históricas para que la comparación sea significativa.",
            "Horizonte de 5 años (2025-2030): la incertidumbre aumenta con la distancia temporal. Los valores proyectados en 2029-2030 tienen mayor margen de error.",
            "La banda de confianza (~95%) se calcula a partir de residuos históricos del modelo seleccionado; no es un intervalo de predicción estadísticamente formal.",
            "Excluir 2020 del entrenamiento asume que la condición post-COVID es el régimen estructural dominante para el horizonte proyectado.",
        ],
    },
    "spc": {
        "title": "Limitaciones del I-Chart",
        "items": [
            "El I-Chart asume independencia entre observaciones consecutivas. Las series turísticas pueden presentar autocorrelación, lo que podría afectar la interpretación de señales.",
            "Los límites de control se calculan sobre toda la serie histórica disponible. Puntos extremos como 2020 sesgan el cálculo del rango móvil promedio cuando no se excluyen.",
            "La opción de excluir 2020 es metodológicamente válida para obtener límites representativos de la variabilidad normal, pero elimina información real del proceso.",
            "El método solo detecta causas especiales mediante la regla de los 3 sigmas. No implementa reglas adicionales de Western Electric (rachas, tendencias).",
        ],
    },
    "montecarlo": {
        "title": "Limitaciones Críticas de la Simulación Monte Carlo",
        "items": [
            "⚠ LIMITACIÓN ESTADÍSTICA: El ajuste de distribución se realiza con solo 4 años de datos (2022-2025). Con tan pocas observaciones, el ajuste es estadísticamente frágil.",
            "Esta decisión es metodológicamente deliberada: el período post-pandemia es el más representativo de la dinámica turística actual. Incluir datos 2008-2019 introduciría sesgo hacia condiciones obsoletas.",
            "La simulación asume independencia temporal entre las tasas de crecimiento de un año a otro. En la realidad, el turismo presenta autocorrelación positiva (años buenos tienden a seguir años buenos).",
            "El recorte de tasas simuladas entre -0.95 y 2.0 es una decisión de diseño que evita escenarios implausibles, pero cualquier cambio en estos límites modifica los resultados.",
            "La incertidumbre del fan chart crece año a año. Las proyecciones de 2029-2030 tienen bandas P10-P90 muy amplias que deben interpretarse con precaución.",
            "El criterio AIC selecciona la mejor distribución entre las tres candidatas (Normal, Logística, Cauchy). Con solo 4 puntos, esta selección puede ser inestable.",
        ],
    },
    "optimization": {
        "title": "Limitaciones del Modelo de Programación Lineal",
        "items": [
            "Los coeficientes de eficiencia (eᵢ) se calculan como la participación promedio histórica de cada zona. Este es un proxy de eficiencia relativa, no una medida directa de retorno sobre inversión promocional.",
            "Las capacidades máximas (Cᵢ) se estiman multiplicando el máximo crecimiento histórico observado por un factor 1.2 sobre las llegadas más recientes. Este factor es conservador y puede no reflejar las condiciones actuales de capacidad de cada mercado.",
            "El modelo asume que el presupuesto es infinitamente divisible entre zonas, sin costos fijos por mercado. En la realidad, abrir promoción en una nueva zona tiene costos mínimos de entrada.",
            "No incorpora variables exógenas como competidores regionales, variaciones en conectividad aérea o eventos geopolíticos que podrían modificar la eficiencia por zona.",
            "El valor óptimo Z es un escalar adimensional ponderado (no llegadas absolutas). Su interpretación es comparativa, no literal.",
            "La solución óptima es válida únicamente bajo los supuestos declarados. Cambios en la estructura de mercados invalidan los coeficientes de eficiencia.",
        ],
    },
}


def render_limitations(module_name: str) -> str:
    """Retorna texto markdown con las limitaciones de un módulo."""
    if module_name not in LIMITATIONS:
        return "No hay limitaciones documentadas para este módulo."
    lim = LIMITATIONS[module_name]
    lines = [f"**{lim['title']}**\n"]
    for item in lim["items"]:  # type: ignore[union-attr]
        lines.append(f"- {item}")
    return "\n".join(lines)
