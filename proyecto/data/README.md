# Datos del proyecto-ejemplo

## `raw/heart.csv`

**Fuente.** UCI Machine Learning Repository — *Heart Disease* (procesado Cleveland).
URL: https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data

**Citación obligatoria.**
Detrano R, Janosi A, Steinbrunn W, et al. *International application of a
new probability algorithm for the diagnosis of coronary artery disease.*
American Journal of Cardiology 1989; 64:304-310.

**Licencia.** Dominio público (UCI Repository, citación requerida).

**Tamaño.** 303 pacientes × 14 columnas. ~20 KB. Commiteado en el repo
para reproducibilidad inmediata; en proyectos con datos grandes o
sensibles esto NO se hace — se documenta la procedencia y se baja por
script.

## Diccionario de datos

| Columna | Tipo | Descripción |
|---|---|---|
| `age` | numérica | Edad en años |
| `sex` | binaria | 1 = masculino, 0 = femenino |
| `cp` | categórica | Tipo de dolor de pecho: 1=angina típica, 2=atípica, 3=no anginoso, 4=asintomático |
| `trestbps` | numérica | Presión arterial sistólica en reposo (mmHg) |
| `chol` | numérica | Colesterol sérico (mg/dl) |
| `fbs` | binaria | Glucemia en ayunas > 120 mg/dl (1 = sí) |
| `restecg` | categórica | ECG en reposo: 0=normal, 1=anomalía ST-T, 2=hipertrofia VI |
| `thalach` | numérica | Frecuencia cardiaca máxima alcanzada en prueba de esfuerzo |
| `exang` | binaria | Angina inducida por ejercicio (1 = sí) |
| `oldpeak` | numérica | Depresión del ST inducida por ejercicio vs. reposo |
| `slope` | categórica | Pendiente del segmento ST en ejercicio: 1=ascendente, 2=plana, 3=descendente |
| `ca` | categórica | Número de vasos principales coloreados por fluoroscopía (0-3) |
| `thal` | categórica | Talasemia: 3=normal, 6=defecto fijo, 7=defecto reversible |
| `num` | objetivo original | Severidad de enfermedad coronaria (0-4) |

**Faltantes.** Codificados como `?` en el CSV. Hay 6 filas con faltantes
(4 en `ca`, 2 en `thal`). El módulo `src/curate.py` documenta la decisión
de descartarlas.

**Target del modelo.** Se deriva en `src/curate.py` como
`target = 1 if num > 0 else 0`. El binario es suficiente para la decisión
clínica de priorización para cateterismo. La columna `num` se conserva
en `raw_patients` pero se excluye explícitamente como feature en
`src/model.py` (data leakage).

## `processed/`

Esta carpeta queda vacía en el repo. Si necesitas materializar versiones
intermedias de los datos (p.ej. para un análisis costoso), guárdalas aquí
y agrega al `.gitignore` (ya está). El estándar del proyecto es que la
única fuente de verdad para análisis es la base SQLite en `db/heart.db`,
generada desde `raw/heart.csv`.
