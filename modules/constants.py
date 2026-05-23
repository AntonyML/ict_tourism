"""Constantes del sistema ICT Tourism Analytics.

Centraliza todos los valores fijos del proyecto con justificación metodológica
completa para cada decisión de diseño.
"""

# ---------------------------------------------------------------------------
# SPC — Control estadístico de procesos
# ---------------------------------------------------------------------------
SPC_D2: float = 1.128
"""Constante d2 para I-Chart con subgrupo n=2 (rango móvil de dos observaciones).

Referencia: Montgomery, D. C. (2020). Introduction to statistical quality
control (8th ed.). Wiley. Tabla de constantes de control, d2 para n=2.

Justificación: d2 es la constante de insesgadez para convertir el rango
móvil promedio en un estimador de sigma. El valor 1.128 corresponde
específicamente a subgrupos de tamaño 2 (diferencias entre observaciones
consecutivas), que es la configuración estándar del I-Chart.
"""

# ---------------------------------------------------------------------------
# Pronósticos
# ---------------------------------------------------------------------------
FORECAST_MA_WINDOW: int = 3
"""Ventana del promedio móvil (años).

Justificación: Ventana de 3 años equilibra suavizado del ruido aleatorio
y sensibilidad ante cambios de tendencia. En series turísticas anuales,
3 años captura ciclos de corto plazo (crisis, recuperación) sin introducir
lag excesivo en la respuesta del modelo.

Alternativas consideradas:
  - Ventana 2: Demasiado sensible al ruido año a año.
  - Ventana 5: Lento para detectar cambios recientes; oculta pandemia.
"""

FORECAST_ALPHA: float = 0.3
"""Parámetro de suavizamiento del SES (Simple Exponential Smoothing).

Justificación: α = 0.3 es un valor MODERADO que:
  - Pondera historia reciente (últimas observaciones cuentan más).
  - No descarta completamente el pasado (α no cercano a 1).
  - Apropiado para series turísticas con tendencia suave y ciclos largos.

El valor se mantiene FIJO (no optimizado) deliberadamente para:
  - Comparar los tres modelos bajo condiciones controladas de parámetro.
  - Evitar que SES sobreajuste a datos recientes del período post-pandemia.
  - Proporcionar contraste claro con Holt, que SÍ optimiza automáticamente.

Rango válido: 0 < α ≤ 1
  - α → 0: Pronósticos muy inertes (ignoran cambios recientes).
  - α → 1: Pronósticos muy reactivos (naïve, sin memoria histórica).

Referencia: Makridakis, S., Wheelwright, S. C., & Hyndman, R. J. (1998).
Forecasting: Methods and applications (3rd ed.). Wiley.
"""

FORECAST_HORIZON: list[int] = list(range(2025, 2031))
"""Años del horizonte de pronóstico: 2025-2030 (6 valores).

Justificación:
  - Relevante para planificación estratégica turística (3-5 años es estándar).
  - Cercano suficiente para ser confiable; lejano suficiente para tendencia.
  - Incluye 2025 (parcialmente observado) como primer año proyectado.

Horizontes más largos introducen incertidumbre exponencial no justificable.
"""

# ---------------------------------------------------------------------------
# Simulación Monte Carlo
# ---------------------------------------------------------------------------
MONTECARLO_N_YEARS: int = 5
"""Años proyectados en la simulación (2026-2030 inclusive)."""

MONTECARLO_PROJECTION_START: int = 2026
"""Primer año proyectado por Monte Carlo."""

MONTECARLO_GROWTH_CLIP: tuple[float, float] = (-0.95, 2.0)
"""Límites de recorte de tasas de crecimiento simuladas.

Justificación:
  - Límite inferior -0.95: Evita caídas superiores al 95% del total de
    llegadas (implausibles salvo colapso total del sector). La mayor caída
    histórica registrada fue ~65% en 2020 (pandemia COVID-19).
  - Límite superior 2.0: Evita crecimientos superiores al 200% que
    distorsionarían la distribución simulada (nunca observado en la serie).

Este recorte cubre el 99.9% de escenarios históricamente realistas.
"""

POST_PANDEMIC_YEAR_START: int = 2022
"""Primer año del periodo post-pandemia para ajuste distribucional de Monte Carlo.

Justificación:
  - Excluye 2020: Año pandemia (evento anómalo, causa especial verificada).
  - Excluye 2021: Año de recuperación atípica tras confinamiento.
  - Usa 2022-2025: Período que refleja la dinámica estructural post-COVID,
    la condición más plausible como base para proyectar 2026-2030.

Limitación reconocida: Solo 3-4 observaciones disponibles. Este es un
ajuste estadísticamente frágil. Se acepta por coherencia metodológica:
incluir 2008-2019 introduciría sesgo hacia condiciones obsoletas del mercado.
"""

MONTECARLO_RANDOM_SEED: int = 42
"""Semilla para reproducibilidad completa de la simulación.

Cualquier usuario con los mismos datos obtiene exactamente los mismos
escenarios simulados. Valor 42 es convención en ciencia de datos.
"""

# ---------------------------------------------------------------------------
# Optimización Lineal
# ---------------------------------------------------------------------------
CAPACITY_SCALE_FACTOR: float = 1.2
"""Factor multiplicador aplicado al máximo crecimiento histórico por zona.

Justificación:
  - El factor 1.2 establece una capacidad máxima 20% superior al mayor
    crecimiento observado históricamente en cada zona geográfica.
  - Es un factor CONSERVADOR: no asume que todas las zonas puedan crecer
    simultáneamente a su máximo histórico (lo cual es irreal en la práctica).
  - Refleja que existen límites reales de capacidad (infraestructura aérea,
    oferta hotelera, capacidad de procesamiento en fronteras).

Supuesto declarado: Factor fijo. No varía entre zonas ni en el tiempo.
"""

CAPACITY_MINIMUM: float = 0.02
"""Fracción mínima del valor base como capacidad mínima por zona.

Justificación: Garantiza que incluso zonas pequeñas (Caribe, Otras zonas)
tengan una capacidad de presupuestación mínima del 2% de sus llegadas base.
Evita que el modelo excluya zonas por capacidad cero.
"""

N_ZONES: int = 6
"""Número de zonas geográficas del ICT.

Zonas: América del Norte, Europa, América del Sur,
       América Central, Caribe, Otras zonas.

Referencia: Instituto Costarricense de Turismo (2025).
Series_sitio_web_ICT_2025.xlsx, Cuadros 3 y 4.
"""
