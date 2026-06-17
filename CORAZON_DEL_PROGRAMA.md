# ICT Tourism Analytics — Corazón del programa

## Proyecto general

Aplicación modular en Python + Streamlit para convertir datos turísticos históricos del ICT en soporte real para la toma de decisiones.

El programa no existe solo para mostrar gráficas. Existe para resolver un problema más importante: medir bien la información, limpiarla, comparar escenarios y traducir esa evidencia en decisiones más confiables.

## Descripción

ICT Tourism Analytics organiza una serie histórica con distintos formatos, rangos y niveles de calidad en un flujo analítico único.

La aplicación integra diagnóstico descriptivo, pronóstico, control estadístico de procesos, simulación Monte Carlo y programación lineal. Cada técnica aporta una lectura distinta del mismo fenómeno: cómo se comporta el turismo, cómo puede evolucionar y cómo conviene actuar con ese contexto.

## Problema que resuelve

El problema principal no es la falta de datos, sino la dificultad para medirlos y usarlos de forma consistente.

- Las hojas del ICT no siempre comparten la misma estructura.
- Existen series con distintos periodos de cobertura.
- Hay valores atípicos y rupturas fuertes, especialmente 2020.
- Sin limpieza y normalización, el análisis termina siendo frágil o engañoso.

Por eso el proyecto primero ordena la información y después la interpreta.

## Objetivo

Arreglar el problema de medición de los datos turísticos y el flujo completo que eso arrastra: carga, limpieza, validación, análisis, pronóstico, incertidumbre y decisión.

El objetivo operativo es simple: pasar de datos dispersos a decisiones sustentadas.

## Solución

La solución está pensada como una cadena de decisión:

- `DataLoader` identifica, limpia y normaliza las series.
- El dashboard descriptivo permite entender la historia del dato.
- Los pronósticos comparan modelos para estimar escenarios futuros.
- El I-Chart detecta si el proceso se mantiene bajo control.
- Monte Carlo mide incertidumbre con escenarios simulados.
- La optimización distribuye presupuesto bajo restricciones.

Cada bloque resuelve una parte distinta del mismo problema general.

## Arquitectura y decisiones

- Separación por módulos para evitar un archivo monolítico.
- `app.py` actúa como orquestador de la interfaz.
- `constants.py` concentra parámetros fijos con justificación metodológica.
- `limitations.py` expone las limitaciones para que el usuario no sobreinterprete resultados.
- El flujo está diseñado para que cada técnica tenga un rol claro y no compita con las demás.

La idea base es que los métodos no se usan como adorno estadístico, sino como instrumentos de decisión.

## Flujo de datos

El recorrido del sistema es este:

1. Se carga el Excel del ICT.
2. Se detectan hojas, filas útiles y columnas relevantes.
3. Se limpian valores, años repetidos y formatos inconsistentes.
4. Se generan vistas descriptivas y validaciones básicas.
5. Se ejecutan métodos analíticos según el módulo elegido.
6. Se muestran resultados, límites, bandas, percentiles o soluciones óptimas.

Ese flujo evita que una mala medición contamine la toma de decisiones posterior.

## Módulos principales

- [app.py](app.py): punto de entrada y navegación principal.
- [modules/data_loader.py](modules/data_loader.py): carga y limpieza de las hojas del ICT.
- [modules/descriptive.py](modules/descriptive.py): análisis histórico y visualización base.
- [modules/forecasting.py](modules/forecasting.py): comparación de modelos de pronóstico.
- [modules/spc.py](modules/spc.py): control estadístico con I-Chart.
- [modules/montecarlo.py](modules/montecarlo.py): simulación de escenarios futuros.
- [modules/optimization.py](modules/optimization.py): asignación óptima de presupuesto.
- [modules/limitations.py](modules/limitations.py): límites metodológicos visibles.
- [modules/constants.py](modules/constants.py): parámetros y supuestos del sistema.

## Validación y calidad

La aplicación incorpora validaciones que ayudan a confiar en el resultado antes de interpretar el análisis.

- Se verifica el periodo completo de la serie.
- Se muestran años faltantes cuando existen.
- Se comparan modelos por error.
- Se documentan supuestos y límites de cada técnica.
- Se mantiene reproducibilidad mediante constantes y semilla fija donde aplica.

## Impacto

El valor del proyecto está en que convierte un repositorio histórico en una herramienta útil para planificación y soporte operativo.

En lugar de depender solo de intuición o lectura manual de tablas, el usuario puede observar tendencias, medir variabilidad, simular incertidumbre y fundamentar asignaciones de recursos.

## Puntos clave

- El proyecto centra la atención en el problema de medición.
- La app no usa una sola técnica, sino un flujo completo de análisis.
- Las decisiones están respaldadas por métodos cuantitativos distintos.
- El año 2020 se trata como evento especial, no como comportamiento normal.
- La estructura modular facilita mantenimiento y lectura.

## Stack tecnológico

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- PuLP
- OpenPyXL

## Artefactos de ingeniería

- Carga automática del archivo Excel del ICT.
- Dashboard histórico para lectura rápida.
- Comparación formal de pronósticos.
- Control estadístico de proceso con opción de excluir 2020.
- Simulación Monte Carlo con percentiles y fan chart.
- Modelo lineal con sensibilidad y precio sombra.

## Qué debe quedar claro al exponerlo

1. El problema no es solo visualizar datos, sino medirlos bien.
2. La app convierte datos desordenados en un flujo analítico confiable.
3. Cada técnica aporta una decisión distinta: describir, predecir, controlar, simular u optimizar.
4. El objetivo final es apoyar decisiones más sólidas sobre turismo.

## Cierre

ICT Tourism Analytics resume una idea simple: cuando los datos se miden y se interpretan con método, dejan de ser solo información y se vuelven criterio para decidir.