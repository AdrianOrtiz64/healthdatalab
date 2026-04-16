# Lab 4 — Modelado Estadístico

En los labs anteriores:

- Construimos un EHR relacional y auditamos su calidad (Labs 0, 1, 1.1)
- Normalizamos semántica con ICD-10, LOINC y SNOMED-CT (Lab 2)
- Convertimos datos a FHIR y generamos poblaciones sintéticas con Synthea (Labs 3, 3.1)

Ahora la pregunta natural:

> Tenemos 108 pacientes sintéticos con datos demográficos, diagnósticos, signos vitales y laboratorios. **¿Podemos usar estos datos para hacer predicciones clínicas?**

---

## Objetivo del laboratorio

Aplicar **modelado estadístico** sobre los datos de Synthea (Lab 3.1) para:

- Construir una tabla analítica a partir de datos transaccionales (ingeniería de características)
- Realizar EDA clínico orientado a modelado
- Formular y probar hipótesis estadísticas con significado clínico
- Construir modelos de regresión lineal y logística
- Evaluar modelos con métricas apropiadas (R², ROC/AUC, calibración)
- Aplicar validación cruzada y detectar fuga de datos (data leakage)

---

## Qué vamos a construir

```
patients.csv ──┐
conditions.csv ─┤
encounters.csv ─┼──▶  df_model (108 filas x ~15 columnas)  ──▶  Modelos predictivos
medications.csv ┤     Una fila por paciente
observations.csv┘     Cada columna = feature
```

**Dos modelos:**
1. **Regresión lineal** — predecir gastos de salud (`HEALTHCARE_EXPENSES`)
2. **Regresión logística** — predecir diabetes (`has_diabetes`)

---

## Qué aprenderás

- Transformar datos transaccionales (un registro por evento) a formato analítico (un registro por paciente)
- Pruebas de hipótesis: t-test, chi-cuadrado, Mann-Whitney
- Regresión lineal múltiple con regularización (Ridge, Lasso)
- Regresión logística con interpretación de odds ratios
- Métricas: matriz de confusión, sensibilidad, especificidad, curva ROC, AUC, calibración
- Validación cruzada y el peligro de la fuga de datos
- Tradeoff sesgo-varianza en la práctica

---

## Flujo de trabajo

Sigue el flujo definido en `COURSE_SETUP.md`.

1. Actualiza `main`
2. Crea tu branch:

```bash
git checkout -b lab04-statistical-modeling/grupo-N
```

3. Trabaja únicamente en ese branch
4. Haz commits durante el proceso (hay 6 checkpoints)
5. Entrega con Pull Request

---

## Importante

Este laboratorio se guía completamente desde el notebook:

```
notebooks/Lab04_Modelado_Estadistico.ipynb
```

Los datos son los mismos CSVs de Synthea del Lab 3.1 (ya incluidos en `data/`).

---

## Antes de empezar

Verifica:

```bash
git branch
git remote -v
docker compose up -d
```

- No estás en `main`
- Tienes `origin` y `upstream`
- Docker está corriendo (jupyter)

---

## Resultado esperado

Al final deberías poder:

- Explicar la diferencia entre datos transaccionales y analíticos
- Interpretar un p-value y saber cuándo NO usarlo
- Construir y evaluar un modelo de regresión lineal y uno logístico
- Leer una curva ROC y elegir un umbral de clasificación según el contexto clínico
- Identificar fuga de datos (data leakage) en un estudio predictivo
- Reflexionar sobre las limitaciones de modelar con datos sintéticos y muestras pequeñas
