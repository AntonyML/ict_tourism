# Explicación Analítica del Sistema ICT Tourism Analytics

Este documento explica, de forma educativa y profesional, cómo interpretar la aplicación **Análisis de Turismo ICT**. El objetivo no es solo describir gráficas, sino comprender qué significa cada módulo, qué método usa, qué decisiones permite tomar y cómo explicarlo en una exposición académica o profesional.

La aplicación analiza datos de llegadas internacionales a Costa Rica usando cinco enfoques complementarios:

- **Dashboard descriptivo:** entiende qué ocurrió históricamente.
- **Pronósticos:** estima qué podría ocurrir en el futuro.
- **Control estadístico de procesos:** identifica años normales y años anómalos.
- **Simulación Monte Carlo:** evalúa incertidumbre y escenarios posibles.
- **Programación Lineal:** optimiza la asignación de recursos promocionales.

---

## Módulo 1: Dashboard Descriptivo

### 1. Resumen simple del módulo

El dashboard descriptivo muestra una fotografía histórica del turismo internacional hacia Costa Rica. Su objetivo es responder preguntas básicas pero importantes:

- ¿Cómo han evolucionado las llegadas internacionales?
- ¿En qué años hubo crecimiento o caída?
- ¿Qué pasó en 2020?
- ¿De qué zonas geográficas vienen más visitantes?
- ¿Qué tan importante es la vía aérea dentro del turismo receptor?

Este módulo sirve para comprender el contexto antes de hacer análisis más avanzados. En turismo, no se puede pronosticar ni optimizar correctamente sin saber primero cómo se ha comportado el mercado.

### 2. Explicación técnica

Este módulo usa **estadística descriptiva** y visualización de datos. Trabaja principalmente con:

- Serie histórica de llegadas totales.
- Llegadas por vía aérea.
- Llegadas por zona geográfica.
- Variación porcentual anual calculada a partir de la serie total.

Los cálculos principales son:

- Variación anual:

```text
Var % = ((Total año actual - Total año anterior) / Total año anterior) * 100
```

- Participación aproximada de la vía aérea:

```text
Participación aérea = (Llegadas vía aérea / Llegadas totales) * 100
```

El módulo genera gráficos interactivos con Plotly para explorar tendencias, caídas, recuperaciones y distribución geográfica.

### 3. Explicación para presentar a compañeros

Una forma clara de presentarlo sería:

> "Este primer módulo nos permite entender el comportamiento histórico del turismo internacional en Costa Rica. Antes de aplicar modelos predictivos o técnicas de optimización, necesitamos saber qué ha pasado. Aquí observamos la evolución de las llegadas totales, los años de crecimiento y caída, y la distribución de turistas por zona geográfica. El año 2020 se destaca porque representa una ruptura extraordinaria causada por la pandemia, lo que permite diferenciar entre comportamiento normal y eventos atípicos."

También se puede decir:

> "Este módulo funciona como el punto de partida del análisis. Nos ayuda a contextualizar los datos y a identificar patrones importantes para la toma de decisiones turísticas."

### 4. Interpretación de las gráficas

#### Gráfica: Serie histórica de llegadas totales

**A. Qué muestra**  
Muestra la evolución de las llegadas internacionales totales a Costa Rica a lo largo del tiempo.

**B. Qué significan los ejes**  
El eje X representa los años. El eje Y representa la cantidad de llegadas internacionales.

**C. Qué representan los colores**  
La línea principal muestra la trayectoria histórica. El año 2020 se marca visualmente como un evento excepcional.

**D. Patrones importantes**  
Normalmente se observa una tendencia de crecimiento de largo plazo, con interrupciones puntuales. El año 2020 destaca por una caída abrupta.

**E. Conclusiones**  
Costa Rica ha tenido una expansión turística importante, pero el turismo es sensible a choques externos como pandemias, crisis económicas o restricciones de movilidad.

**F. Decisiones que ayuda a tomar**  
Permite planificar infraestructura, promoción turística, capacidad hotelera y estrategias de recuperación después de crisis.

#### Gráfica: Variación porcentual anual

**A. Qué muestra**  
Muestra cuánto creció o cayó el turismo cada año en términos porcentuales.

**B. Qué significan los ejes**  
El eje X muestra los años. El eje Y muestra el porcentaje de crecimiento o caída.

**C. Qué representan los colores**  
Las barras positivas representan crecimiento. Las barras negativas representan reducción de llegadas.

**D. Patrones importantes**  
Los años con barras muy altas indican recuperaciones o expansiones rápidas. Las barras negativas fuertes indican crisis.

**E. Conclusiones**  
No solo importa cuántos turistas llegan, sino la velocidad a la que el mercado crece o se contrae.

**F. Decisiones que ayuda a tomar**  
Ayuda a identificar cuándo reforzar campañas, cuándo investigar causas de caída y cuándo aprovechar ciclos positivos.

#### Gráfica: Llegadas por zona geográfica en 2025

**A. Qué muestra**  
Compara cuántos visitantes llegaron desde cada zona geográfica.

**B. Qué significan los ejes**  
El eje X muestra cantidad de llegadas. El eje Y muestra las zonas: América del Norte, Europa, América Central, América del Sur, Caribe y Otras zonas.

**C. Qué representan los colores**  
El color uniforme permite comparar magnitudes sin distraer con categorías adicionales.

**D. Patrones importantes**  
Las zonas con barras más largas son los mercados emisores más relevantes.

**E. Conclusiones**  
Si una zona concentra gran parte de las llegadas, Costa Rica depende mucho de ese mercado. Esto puede ser una fortaleza, pero también un riesgo.

**F. Decisiones que ayuda a tomar**  
Permite decidir dónde invertir en promoción, qué mercados diversificar y qué conectividad aérea fortalecer.

### 5. Interpretación de tablas

Aunque el dashboard descriptivo se centra en gráficas, las tablas base representan:

- **Año:** periodo observado.
- **Total:** cantidad de llegadas internacionales.
- **Vía aérea:** llegadas por aeropuertos.
- **Zonas geográficas:** origen de los visitantes.

Valores altos indican mercados o años fuertes. Valores bajos pueden indicar menor demanda, crisis o mercados con oportunidad de crecimiento.

### 6. Explicación de métodos

**Análisis descriptivo**  
Sirve para resumir y comprender datos históricos. No predice, sino que explica lo que ya ocurrió.

**KPIs turísticos**  
Son indicadores clave, como llegadas totales, crecimiento anual y participación por zona. Ayudan a medir el desempeño del sector.

**Series históricas**  
Son datos ordenados por tiempo. En turismo permiten observar tendencias, ciclos y eventos anómalos.

### 7. Ejemplos prácticos

- Si América del Norte concentra la mayoría de visitantes, el ICT podría reforzar campañas en Estados Unidos, Canadá y México.
- Si Europa crece lentamente, se podrían revisar conexiones aéreas, precios o campañas de posicionamiento.
- Si la vía aérea representa la mayor parte de llegadas, los aeropuertos y aerolíneas se vuelven estratégicos.

### 8. Posibles preguntas del profesor o jurado

**Pregunta:** ¿Por qué empezar con un dashboard descriptivo?  
**Respuesta:** Porque permite entender el contexto histórico antes de aplicar modelos predictivos. Sin análisis descriptivo, los modelos pueden interpretarse mal.

**Pregunta:** ¿Por qué se destaca 2020?  
**Respuesta:** Porque fue un año atípico por la pandemia. No representa el comportamiento normal del turismo, sino una causa especial.

**Pregunta:** ¿Qué aporta analizar por zonas?  
**Respuesta:** Permite identificar mercados emisores principales y evaluar dependencia o diversificación turística.

### 9. Conclusiones del módulo

El dashboard descriptivo enseña cómo ha evolucionado el turismo internacional en Costa Rica, identifica mercados clave y muestra el impacto de eventos extraordinarios. Es fundamental para formular preguntas, justificar modelos y orientar decisiones estratégicas.

---

## Módulo 2: Pronósticos

### 1. Resumen simple del módulo

El módulo de pronósticos estima cómo podrían comportarse las llegadas internacionales entre 2025 y 2030. Su objetivo es anticipar el futuro usando patrones históricos.

Ayuda a responder:

- ¿Cuántos turistas podrían llegar en los próximos años?
- ¿Qué modelo predice mejor los datos históricos?
- ¿Qué tan confiable parece la proyección?
- ¿Cómo cambia el resultado si excluimos 2020?

Este módulo es útil para planificación turística, capacidad hotelera, conectividad aérea, presupuesto promocional e inversión pública.

### 2. Explicación técnica

El módulo usa **series temporales**, que son datos ordenados por año. Entrena modelos con datos desde el año seleccionado hasta 2024 y proyecta el horizonte 2025-2030.

Modelos usados:

- Promedio móvil.
- Suavizamiento exponencial simple.
- Holt con tendencia.

Métricas usadas:

- **MAE:** error absoluto promedio.
- **RMSE:** error cuadrático medio, penaliza errores grandes.
- **MAPE:** error porcentual promedio.

El mejor modelo se selecciona usando el menor RMSE.

### 3. Explicación para presentar a compañeros

Una explicación oral posible:

> "En este módulo dejamos de mirar solamente el pasado y empezamos a estimar el futuro. Usamos modelos de series temporales que aprenden del comportamiento histórico de las llegadas internacionales. La aplicación compara tres modelos y selecciona el que comete menos error en el periodo de entrenamiento. Además, permite excluir el año 2020 porque fue un evento extraordinario que puede distorsionar el aprendizaje del modelo."

Para explicar la gráfica:

> "La línea histórica muestra los datos reales. La línea ajustada muestra cómo el modelo reproduce el pasado. La línea de pronóstico muestra la proyección hacia 2030. Si el ajuste dentro de muestra es razonable, podemos tener más confianza en la tendencia proyectada, aunque siempre con cautela."

### 4. Interpretación de las gráficas

#### Gráfica: Histórico, ajuste y pronóstico 2025-2030

**A. Qué muestra**  
Muestra tres elementos: datos históricos reales, ajuste del mejor modelo y proyección futura.

**B. Qué significan los ejes**  
El eje X representa los años. El eje Y representa llegadas internacionales.

**C. Qué representan los colores**  
La serie histórica muestra los valores reales. La línea de ajuste representa el modelo dentro del periodo de entrenamiento. La línea punteada o resaltada representa el pronóstico futuro.

**D. Patrones importantes**  
Si la línea del modelo sigue de cerca la serie histórica, el modelo captura bien la tendencia. Si se aleja mucho, el pronóstico debe tomarse con más cautela.

**E. Conclusiones**  
El pronóstico no es una verdad exacta. Es un escenario estadístico basado en el comportamiento pasado.

**F. Decisiones que ayuda a tomar**  
Ayuda a estimar demanda futura, planificar infraestructura turística, diseñar campañas y anticipar necesidades de transporte, hoteles y servicios.

#### Interpretación de intervalos o bandas de confianza

Cuando aparecen bandas, representan incertidumbre. Una banda más ancha significa mayor incertidumbre. Una banda estrecha indica que el modelo estima un rango más concentrado.

En exposición se puede decir:

> "La proyección central es el escenario más esperado, pero las bandas muestran que existe un rango posible. En turismo esto es importante porque la demanda depende de factores externos como economía internacional, conectividad aérea, tipo de cambio, seguridad y eventos globales."

### 5. Interpretación de tablas

#### Tabla de métricas de modelos

Columnas:

- **Modelo:** técnica usada para pronosticar.
- **MAE:** error promedio en número de llegadas.
- **RMSE:** error que penaliza más los errores grandes.
- **MAPE:** error promedio en porcentaje.

Filas:

- Cada fila representa un modelo distinto.

Cómo interpretar:

- Menor MAE significa menor error promedio.
- Menor RMSE significa mejor control de errores grandes.
- Menor MAPE significa mejor precisión relativa.
- El modelo con menor RMSE se selecciona como mejor modelo.

Insight importante:

Si dos modelos tienen errores parecidos, se puede preferir el más simple. Si un modelo mejora mucho el RMSE, captura mejor la dinámica histórica.

### 6. Explicación de cada método

#### Promedio móvil

**Qué es**  
Un método que pronostica usando el promedio de los últimos años.

**Para qué sirve**  
Suaviza fluctuaciones y captura tendencias recientes.

**Cómo funciona**  
Si se usa una ventana de 3 años, el pronóstico se basa en el promedio de los últimos tres valores.

**Ventajas**  
Es simple, fácil de explicar y robusto.

**Limitaciones**  
Puede reaccionar lento ante cambios fuertes y no modela tendencia explícita.

#### Suavizamiento exponencial simple

**Qué es**  
Un método que da más peso a datos recientes y menos peso a datos antiguos.

**Para qué sirve**  
Es útil cuando se quiere reflejar comportamiento reciente sin ignorar totalmente el pasado.

**Cómo funciona**  
Usa un parámetro alpha. Un alpha alto da más importancia al último dato. Un alpha bajo suaviza más la serie.

**Ventajas**  
Es flexible y más dinámico que un promedio simple.

**Limitaciones**  
No modela tendencia de forma explícita.

#### Holt con tendencia

**Qué es**  
Un modelo de suavizamiento que considera nivel y tendencia.

**Para qué sirve**  
Es útil cuando la serie muestra crecimiento o disminución sostenida.

**Cómo funciona**  
Estima el nivel actual de la serie y una pendiente o tendencia.

**Ventajas**  
Puede proyectar crecimiento futuro.

**Limitaciones**  
Si ocurre un choque inesperado, puede sobreestimar o subestimar.

### 7. Ejemplos prácticos

- Si el pronóstico indica aumento de turistas, hoteles pueden planificar más habitaciones, personal y servicios.
- Si se espera crecimiento moderado, el ICT puede orientar campañas a mercados con mayor potencial.
- Si el modelo cambia mucho al excluir 2020, significa que la pandemia distorsiona el comportamiento histórico.

### 8. Posibles preguntas del profesor o jurado

**Pregunta:** ¿Por qué excluir 2020?  
**Respuesta:** Porque fue un año atípico causado por la pandemia. Excluirlo permite entrenar el modelo con una dinámica más representativa del turismo normal.

**Pregunta:** ¿El pronóstico garantiza que eso ocurrirá?  
**Respuesta:** No. Un pronóstico es una estimación basada en datos históricos, no una certeza.

**Pregunta:** ¿Por qué usar RMSE para elegir el mejor modelo?  
**Respuesta:** Porque penaliza más los errores grandes, lo cual es importante en planificación turística.

### 9. Conclusiones del módulo

El módulo de pronósticos permite anticipar escenarios futuros y comparar modelos de predicción. Su principal valor es apoyar la planificación, aunque sus resultados deben interpretarse con incertidumbre y contexto.

---

## Módulo 3: Control Estadístico de Procesos

### 1. Resumen simple del módulo

Este módulo analiza si la variación anual del turismo se comporta de forma estable o si existen años anómalos. Usa un gráfico de control llamado **I-Chart**.

Sirve para detectar si un año tuvo un comportamiento fuera de lo normal, por ejemplo 2020 por la pandemia o años de recuperación muy acelerada.

### 2. Explicación técnica

El módulo usa:

- Media de la variación anual.
- Desviación estándar.
- Límites de control:

```text
LCS = media + 3 * sigma
LC = media
LCI = media - 3 * sigma
```

Donde:

- **LCS:** límite de control superior.
- **LC:** línea central.
- **LCI:** límite de control inferior.
- **Sigma:** desviación estándar.

Si un punto cae fuera de los límites, se interpreta como señal de causa especial.

### 3. Explicación para presentar a compañeros

Se puede presentar así:

> "Este módulo no busca pronosticar, sino evaluar estabilidad. En turismo, algunos cambios son normales: un año puede crecer más o menos. Pero si la variación se sale demasiado del rango esperado, eso indica un evento especial. El gráfico de control nos ayuda a distinguir entre variación normal y señales extraordinarias."

Para conectar con Costa Rica:

> "El año 2020 aparece como una causa especial porque la caída turística no fue parte del comportamiento normal del mercado, sino consecuencia de un evento externo global."

### 4. Interpretación de las gráficas

#### Gráfica: I-Chart de variación porcentual anual

**A. Qué muestra**  
Muestra la variación porcentual anual del turismo y sus límites de control.

**B. Qué significan los ejes**  
El eje X representa los años. El eje Y representa la variación porcentual de llegadas.

**C. Qué representan los colores**  
Los puntos normales aparecen en un color base. Los puntos fuera de límites se resaltan en rojo o color especial. El año 2020 se marca como causa especial.

**D. Patrones importantes**  
Un punto muy por debajo del límite inferior indica una caída extraordinaria. Un punto por encima del límite superior indica una recuperación o crecimiento inusualmente alto.

**E. Conclusiones**  
Si hay puntos fuera de límites, el proceso turístico no se comportó de forma estadísticamente estable.

**F. Decisiones que ayuda a tomar**  
Permite investigar causas de anomalías y diseñar planes de contingencia para crisis.

### 5. Interpretación de tablas

El módulo muestra métricas como:

- **LCI:** límite inferior.
- **LC:** promedio histórico.
- **LCS:** límite superior.

Cómo interpretarlas:

- Si un año está entre LCI y LCS, se considera dentro de variabilidad esperada.
- Si está por debajo de LCI, indica caída extraordinaria.
- Si está por encima de LCS, indica crecimiento extraordinario.

### 6. Explicación de cada método

#### Gráfico de control I-Chart

**Qué es**  
Una herramienta estadística para monitorear datos individuales en el tiempo.

**Para qué sirve**  
Detecta si un proceso está estable o si hay señales anormales.

**Cómo funciona**  
Calcula una línea central y límites basados en la variabilidad histórica.

**Por qué se usa**  
Porque el turismo tiene fluctuaciones normales, pero también puede sufrir choques externos.

**Ventajas**  
Es visual, simple y útil para alertas tempranas.

### 7. Ejemplos prácticos

- Una caída extrema por pandemia aparece fuera de control.
- Una recuperación muy acelerada después de fronteras cerradas también puede aparecer como señal especial.
- Si varios años consecutivos se acercan al límite inferior, podría indicar pérdida de competitividad turística.

### 8. Posibles preguntas del profesor o jurado

**Pregunta:** ¿Qué significa que el proceso esté fuera de control?  
**Respuesta:** Significa que al menos un año tuvo una variación demasiado extrema para considerarse normal.

**Pregunta:** ¿Fuera de control significa que el turismo está mal administrado?  
**Respuesta:** No necesariamente. Puede deberse a causas externas como pandemia, crisis económica o restricciones de viaje.

**Pregunta:** ¿Para qué sirve excluir 2020?  
**Respuesta:** Para calcular límites de control más representativos de años normales.

### 9. Conclusiones del módulo

Este módulo ayuda a detectar anomalías y diferenciar variabilidad normal de eventos extraordinarios. Es importante para gestión de riesgo, monitoreo institucional y toma de decisiones preventivas.

---

## Módulo 4: Simulación Monte Carlo

### 1. Resumen simple del módulo

La simulación Monte Carlo crea muchos escenarios posibles sobre el futuro del turismo. En lugar de dar una sola predicción, muestra un rango de posibilidades.

Sirve para responder:

- ¿Qué podría pasar si el crecimiento es alto?
- ¿Qué podría pasar si el crecimiento es bajo?
- ¿Cuál es un escenario probable?
- ¿Qué riesgo existe de quedar por debajo de cierto nivel?

Esto es muy útil porque el turismo es incierto.

### 2. Explicación técnica

El módulo usa tasas históricas de crecimiento post-pandemia y ajusta una distribución probabilística. Prueba distribuciones como:

- Normal.
- Logística.
- Cauchy.

Selecciona la mejor usando AIC, un criterio que compara ajuste estadístico.

Luego genera miles de simulaciones para 2026-2030:

```text
Llegadas futuras = Llegadas actuales * (1 + tasa simulada)
```

El resultado se resume con percentiles:

- **P10:** escenario bajo.
- **P50:** mediana o escenario central.
- **P90:** escenario alto.

### 3. Explicación para presentar a compañeros

Una explicación oral sería:

> "A diferencia del pronóstico tradicional, Monte Carlo no genera una única respuesta. Genera miles de escenarios posibles usando tasas de crecimiento aleatorias basadas en el comportamiento histórico. Esto permite analizar incertidumbre. En turismo, esto es importante porque no sabemos con certeza cómo se comportarán los mercados internacionales."

Para explicar el fan chart:

> "La línea central representa el escenario mediano. La banda muestra un rango probable. Si la banda se abre con los años, significa que la incertidumbre aumenta conforme miramos más lejos en el futuro."

### 4. Interpretación de las gráficas

#### Gráfica: Histograma de tasas de crecimiento simuladas

**A. Qué muestra**  
Muestra la distribución de las tasas de crecimiento generadas por la simulación.

**B. Qué significan los ejes**  
El eje X muestra tasas de crecimiento. El eje Y muestra densidad o frecuencia relativa.

**C. Qué representan los colores**  
Las barras representan tasas simuladas. La línea representa la distribución ajustada.

**D. Patrones importantes**  
Si la distribución está concentrada, los escenarios son más estables. Si tiene colas largas, hay mayor riesgo de eventos extremos.

**E. Conclusiones**  
El crecimiento turístico futuro tiene incertidumbre. No basta con mirar un promedio.

**F. Decisiones que ayuda a tomar**  
Permite preparar escenarios conservadores, moderados y optimistas.

#### Gráfica: Fan chart de llegadas proyectadas

**A. Qué muestra**  
Muestra el rango probable de llegadas internacionales entre 2026 y 2030.

**B. Qué significan los ejes**  
El eje X muestra los años proyectados. El eje Y muestra llegadas internacionales.

**C. Qué representan los colores**  
La línea central es P50. La banda sombreada representa el rango entre P10 y P90.

**D. Patrones importantes**  
Si la banda se amplía, la incertidumbre aumenta. Si la mediana sube, el escenario central es de crecimiento.

**E. Conclusiones**  
El futuro turístico debe analizarse como rango de escenarios, no como un número fijo.

**F. Decisiones que ayuda a tomar**  
Ayuda a diseñar políticas flexibles: presupuesto mínimo, escenario esperado y capacidad para demanda alta.

### 5. Interpretación de tablas

#### Tabla resumen P10, P50, P90

Columnas:

- **Año:** periodo proyectado.
- **P10:** escenario conservador. Solo 10% de simulaciones quedan por debajo.
- **P50:** escenario central o mediano.
- **P90:** escenario optimista. El 90% de simulaciones quedan por debajo.

Cómo interpretar:

- Si P10 es bajo, existe riesgo de menor demanda.
- Si P90 es alto, existe oportunidad de crecimiento fuerte.
- La diferencia entre P10 y P90 mide incertidumbre.

### 6. Explicación de cada método

#### Simulación Monte Carlo

**Qué es**  
Una técnica que usa números aleatorios para construir muchos futuros posibles.

**Para qué sirve**  
Evalúa riesgo e incertidumbre.

**Cómo funciona**  
Toma una distribución de crecimiento y genera miles de trayectorias posibles.

**Por qué se usa**  
Porque el turismo depende de muchos factores inciertos.

**Ventajas**  
Permite pensar en escenarios, no solo en promedios.

#### AIC

**Qué es**  
Criterio de información de Akaike.

**Para qué sirve**  
Compara distribuciones y elige la que mejor ajusta los datos sin complejidad innecesaria.

**Cómo interpretar**  
Menor AIC indica mejor equilibrio entre ajuste y simplicidad.

### 7. Ejemplos prácticos

- Si P10 para 2030 es bajo, los hoteles podrían evitar sobreinvertir.
- Si P90 es alto, el país debe revisar capacidad aeroportuaria y servicios turísticos.
- Si la banda de incertidumbre es amplia, conviene planificar con escenarios alternativos.

### 8. Posibles preguntas del profesor o jurado

**Pregunta:** ¿Por qué usar simulación si ya tenemos pronósticos?  
**Respuesta:** Porque el pronóstico da una trayectoria esperada, mientras Monte Carlo muestra incertidumbre y riesgo.

**Pregunta:** ¿Qué significa P50?  
**Respuesta:** Es la mediana de las simulaciones. La mitad de escenarios queda por encima y la mitad por debajo.

**Pregunta:** ¿Monte Carlo predice exactamente el futuro?  
**Respuesta:** No. Genera escenarios probables basados en supuestos estadísticos.

### 9. Conclusiones del módulo

Monte Carlo permite analizar el turismo bajo incertidumbre. Es especialmente útil para planificación estratégica, evaluación de riesgo y diseño de políticas flexibles.

---

## Módulo 5: Programación Lineal

### 1. Resumen simple del módulo

Este módulo busca responder una pregunta de decisión:

> ¿Cómo asignar un presupuesto promocional entre zonas geográficas para maximizar las llegadas proyectadas?

En lugar de repartir el presupuesto de forma intuitiva, usa optimización matemática.

### 2. Explicación técnica

El módulo usa **Programación Lineal** con PuLP.

Variables de decisión:

```text
x_i = esfuerzo o presupuesto asignado a la zona i
```

Función objetivo:

```text
Maximizar SUM(eficiencia_i * x_i)
```

Restricciones:

- La suma de asignaciones no puede exceder el presupuesto.
- Cada zona tiene una capacidad máxima basada en crecimiento histórico.
- Las variables no pueden ser negativas.

Datos usados:

- Llegadas por zona.
- Participación histórica por zona.
- Presupuesto hipotético definido por el usuario.

### 3. Explicación para presentar a compañeros

Una explicación oral sería:

> "Este módulo transforma el análisis en una decisión concreta. Si el ICT tuviera un presupuesto limitado para promoción internacional, la pregunta sería cómo distribuirlo entre regiones. La programación lineal permite encontrar una asignación óptima considerando eficiencia histórica y restricciones realistas."

Para explicar la solución:

> "La solución óptima no necesariamente reparte igual entre todas las zonas. Asigna más recursos donde el modelo estima mayor eficiencia o capacidad de crecimiento, respetando el límite total de presupuesto."

### 4. Interpretación de las gráficas

#### Gráfica: Asignación óptima por zona

**A. Qué muestra**  
Muestra cuánto presupuesto o esfuerzo promocional asigna el modelo a cada zona.

**B. Qué significan los ejes**  
El eje X muestra las zonas geográficas. El eje Y muestra la asignación óptima.

**C. Qué representan los colores**  
Las barras permiten comparar la cantidad asignada a cada zona.

**D. Patrones importantes**  
Las barras más altas indican zonas priorizadas por el modelo.

**E. Conclusiones**  
El modelo identifica dónde el presupuesto tiene mayor rendimiento esperado bajo los supuestos definidos.

**F. Decisiones que ayuda a tomar**  
Ayuda a diseñar campañas internacionales, priorizar mercados y justificar técnicamente una asignación presupuestaria.

### 5. Interpretación de tablas

#### Tabla de asignación óptima

Columnas:

- **Zona:** mercado geográfico.
- **Asignación óptima:** presupuesto o esfuerzo recomendado.
- **Eficiencia:** participación promedio histórica de la zona.
- **Capacidad estimada:** límite máximo de crecimiento considerado razonable.

Filas:

- Cada fila representa una zona geográfica.

Cómo interpretar:

- Alta eficiencia significa que históricamente esa zona aporta mucho al total.
- Alta capacidad significa que aún hay espacio potencial de crecimiento.
- Alta asignación significa que el modelo recomienda priorizar esa zona.

#### Precio sombra

El precio sombra de la restricción de presupuesto indica cuánto aumentaría el objetivo si se agregara una unidad adicional de presupuesto, manteniendo los supuestos del modelo.

En lenguaje simple:

> "Nos dice cuánto valor adicional podríamos obtener si tuviéramos un poco más de presupuesto."

### 6. Explicación de cada método

#### Programación Lineal

**Qué es**  
Una técnica de optimización matemática.

**Para qué sirve**  
Encuentra la mejor decisión posible cuando hay restricciones.

**Cómo funciona**  
Define una función objetivo y restricciones. Luego busca la combinación de variables que maximiza o minimiza el objetivo.

**Por qué se usa**  
Porque el presupuesto turístico es limitado y debe asignarse eficientemente.

**Ventajas**  
Es transparente, justificable y útil para decisiones de recursos.

#### Restricciones

Son condiciones que el modelo debe respetar. Por ejemplo:

- No gastar más del presupuesto.
- No asignar valores negativos.
- No proyectar crecimientos irreales.

### 7. Ejemplos prácticos

- Si América del Norte tiene alta eficiencia, el modelo puede recomendar más promoción allí.
- Si Europa tiene potencial pero menor participación, podría recibir una asignación moderada.
- Si una zona tiene poca capacidad de crecimiento histórico, el modelo evita sobreasignar recursos.

### 8. Posibles preguntas del profesor o jurado

**Pregunta:** ¿Por qué no repartir el presupuesto por igual?  
**Respuesta:** Porque no todas las zonas tienen la misma eficiencia ni el mismo potencial de crecimiento.

**Pregunta:** ¿La solución óptima es una verdad absoluta?  
**Respuesta:** No. Depende de los supuestos del modelo. Es una recomendación técnica, no una decisión automática.

**Pregunta:** ¿Qué pasa si cambia el presupuesto?  
**Respuesta:** La asignación óptima puede cambiar porque las restricciones y capacidades se activan de forma distinta.

### 9. Conclusiones del módulo

La programación lineal permite pasar del análisis a la acción. Ayuda a justificar cómo distribuir recursos limitados de manera eficiente, transparente y basada en datos.

---

## Conclusión General del Sistema

La aplicación combina análisis descriptivo, predicción, control estadístico, simulación y optimización. Esto permite estudiar el turismo desde varias perspectivas:

- Qué ocurrió.
- Qué podría ocurrir.
- Qué años fueron anómalos.
- Qué riesgos existen.
- Qué decisiones conviene tomar.

En una exposición final, se puede resumir así:

> "Este sistema no solo visualiza datos turísticos. Integra métodos estadísticos y matemáticos para apoyar la toma de decisiones en turismo. Primero describe la evolución histórica, luego pronostica escenarios futuros, identifica anomalías, simula incertidumbre y finalmente propone una asignación óptima de recursos promocionales."

La principal fortaleza del sistema es que convierte datos históricos del ICT en información útil para planificación turística, gestión de riesgo, promoción internacional y toma de decisiones estratégicas.

