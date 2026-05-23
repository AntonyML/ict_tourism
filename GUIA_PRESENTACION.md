# GUÍA DE PRESENTACIÓN — ICT Tourism Analytics
## IF 7200 · Carlos Robles C39310 · Antony Monge C14887

---

## ESTRUCTURA DE LA PRESENTACIÓN (20 min mínimo)

### Bloque 1 — Contexto y problema (3 min)
- Costa Rica recibió más de 2.6 millones de visitantes en 2024.
- Los datos del ICT existen desde 1951 pero no se aprovechan con herramientas analíticas formales.
- El proyecto integra 5 técnicas cuantitativas en una sola aplicación web interactiva.

### Bloque 2 — Arquitectura del sistema (2 min)
- 6 módulos independientes: `data_loader`, `descriptive`, `forecasting`, `spc`, `montecarlo`, `optimization`.
- Cada módulo tiene responsabilidad única (principio SRP — Martin, 2003).
- Orquestador `app.py` coordina sin contener lógica de negocio.
- Constantes centralizadas en `constants.py` con justificación metodológica.

### Bloque 3 — Demo en vivo de los 5 módulos (12 min)

**Dashboard descriptivo (2 min)**
- Mostrar la evolución histórica 1951-2025.
- Señalar visualmente el choque de 2020.
- Mostrar la distribución por zona: América del Norte domina.

**Pronósticos (3 min)**
- Correr comparación MA / SES / Holt.
- Señalar la tabla de métricas MAE, RMSE, MAPE.
- Explicar por qué se selecciona el modelo con menor RMSE.
- Mostrar la banda de confianza ~95%.
- Mencionar: α = 0.3 fijo en SES para comparación controlada.

**Control estadístico (2 min)**
- Mostrar el I-Chart con límites LCI / LC / LCS.
- Señalar 2020 fuera de control.
- Activar el toggle "Excluir 2020" y mostrar cómo cambian los límites.
- Mencionar: σ̂ = MR̄ / d₂ (d₂ = 1.128, Montgomery 2020).

**Simulación Monte Carlo (3 min)**
- Correr con 10.000 simulaciones.
- Mostrar distribución seleccionada y su AIC.
- Mostrar el fan chart P10 / P50 / P90.
- Leer la tabla de percentiles para 2026-2030.

**Programación lineal (2 min)**
- Ingresar un presupuesto hipotético.
- Mostrar la asignación óptima por zona.
- Señalar el precio sombra y explicarlo.
- Mostrar la tabla de análisis de sensibilidad ±5% y ±10%.

### Bloque 4 — Limitaciones y conclusiones (3 min)
- Reconocer limitaciones (están documentadas en la app).
- Dar las 5 conclusiones del documento.
- Dar las 5 recomendaciones al ICT.

---

## RESPUESTAS PREPARADAS PARA PREGUNTAS

**"¿Por qué α = 0.3 en SES?"**
> Valor moderado que pondera historia reciente sin descartar el pasado. Se mantiene fijo deliberadamente para comparar los tres modelos bajo condiciones controladas de parámetro. Holt, en cambio, sí optimiza automáticamente. Está documentado en `constants.py`.

**"¿Por qué solo 4 años en Monte Carlo?"**
> Decisión metodológica. El período 2022-2025 refleja la dinámica turística post-COVID, que es la condición estructural más plausible para proyectar 2026-2030. Incluir datos 2008-2019 introduciría sesgo hacia condiciones obsoletas. La limitación está reconocida y visible en la aplicación.

**"¿Cómo funciona el I-Chart exactamente?"**
> Calculamos la media histórica de la variación porcentual anual (LC). El estimador de sigma usa el rango móvil promedio: σ̂ = MR̄ / d₂, donde d₂ = 1.128 para subgrupos de tamaño 2. Los límites son LC ± 3σ̂. Este es el método estándar para individuales según Montgomery (2020).

**"¿Qué representa el valor Z de la optimización?"**
> Z es un escalar adimensional ponderado: la suma de asignaciones multiplicadas por la participación histórica de cada zona. No son llegadas absolutas. Es una medida relativa de impacto; lo relevante es comparar soluciones entre distintos presupuestos.

**"¿Qué es el precio sombra?"**
> El incremento marginal del valor objetivo Z por cada unidad adicional de presupuesto disponible. Si es positivo, la restricción presupuestaria es activa: más presupuesto mejora el resultado. Sirve para fundamentar solicitudes de ampliación presupuestaria.

**"¿Por qué factor 1.2 en las capacidades?"**
> Factor conservador que establece la capacidad máxima por zona en un 20% por encima del mayor crecimiento histórico observado. Refleja que no todas las zonas pueden crecer simultáneamente a su máximo; hay límites reales de infraestructura. Documentado en `constants.py`.

**"¿Qué tan confiables son los pronósticos a 5 años?"**
> La incertidumbre crece con el horizonte, por eso mostramos la banda de confianza. Para planificación estratégica, 5 años es el horizonte estándar en turismo (planes estratégicos del ICT son típicamente 3-5 años). Monte Carlo cuantifica esa incertidumbre explícitamente con el fan chart.

**"¿Qué validación estadística tiene el proyecto?"**
> Comparación formal de tres modelos mediante MAE, RMSE y MAPE. Selección automática por menor error cuadrático. Precio sombra como análisis de sensibilidad en optimización. Resultados reproducibles: mismos datos + semilla 42 = mismos resultados.

---

## FÓRMULAS CLAVE (para si preguntan)

| Técnica | Fórmula |
|---|---|
| Promedio móvil | x̂ₜ = (1/n) Σ xₜ₋ᵢ |
| SES | ℓₜ = α·xₜ + (1-α)·ℓₜ₋₁ |
| Holt tendencia | ℓₜ = α·xₜ + (1-α)(ℓₜ₋₁+bₜ₋₁) |
| MAE | (1/n) Σ \|eₜ\| |
| RMSE | √( (1/n) Σ eₜ² ) |
| MAPE | (100/n) Σ \|eₜ/xₜ\| |
| I-Chart sigma | σ̂ = MR̄ / 1.128 |
| I-Chart límites | LC ± 3σ̂ |
| AIC | 2k − 2·ln(L) |
| Función objetivo LP | Maximizar Z = Σ eᵢ·xᵢ |

---

## REFERENCIAS RÁPIDAS

- Montgomery (2020) → I-Chart, d₂ = 1.128
- Akaike (1974) → Criterio AIC
- Britton et al. (1998) → Fan chart
- Martin (2003) → Principio SRP
- Davenport & Harris (2017) → Toma de decisiones basada en datos
- Anderson et al. (2016) → Métodos cuantitativos
- Winston (2004) → Programación lineal y Monte Carlo

---

## CHECKLIST PRE-PRESENTACIÓN

- [ ] `streamlit run app.py` corre sin errores
- [ ] Datos cargan correctamente (banner muestra período 1951-2025)
- [ ] Módulo de pronósticos: comparar modelos funciona
- [ ] I-Chart: toggle de 2020 funciona
- [ ] Monte Carlo: simulación completa con fan chart
- [ ] Optimización: solución óptima + tabla de sensibilidad
- [ ] Respuestas de arriba repasadas
- [ ] Documento físico o digital disponible para referencia
