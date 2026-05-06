# Proyecto Fase 2 — Ejemplo de referencia

> ⚠️ **Esto es inspiración, no plantilla.** No copies este caso para tu proyecto;
> úsalo para entender el **piso esperado** en estructura, reproducibilidad y
> trazabilidad clínica. Tu proyecto tiene otra pregunta clínica, otros datos,
> y debe ser tuyo.

## Caso del ejemplo

**Pregunta clínica.** ¿Qué pacientes en consulta cardiológica tienen riesgo
elevado de enfermedad coronaria?

**Decisión que el modelo informa.** Priorización para estudios diagnósticos
invasivos (cateterismo). El modelo NO decide a quién enviar — ordena la lista
para que el cardiólogo revise primero los casos de mayor riesgo.

**Dataset.** UCI Heart Disease (Cleveland, n=303, Detrano et al. 1989).
Tema deliberadamente fuera del scope típico de los proyectos del curso para
que sirva como referencia **de forma**, no de contenido.

## Resultados

| Métrica | Valor |
|---|---|
| AUC cross-validation (5-fold) | 0.901 ± 0.047 |
| AUC test (hold-out, n=75) | 0.914 |
| Sensibilidad | 80.0% |
| Especificidad | 87.5% |
| Modelo | Regresión logística regularizada |
| N tras curación | 297 (de 303 — se descartaron 6 con datos faltantes) |

Detalle completo en [notebooks/dashboard.ipynb](notebooks/dashboard.ipynb).

## Arquitectura: notebook delgado, módulos gordos

El notebook se lee como un **dashboard ejecutivo**: solo importa funciones
del paquete `src/`, las llama, y narra los resultados. Toda la lógica vive
en módulos `.py` testables. Esto es importante porque:

- Notebooks grandes son imposibles de revisar y reproducir.
- La lógica en módulos se puede testear (`tests/`), reusar y versionar bien.
- Los gráficos se rinden cuando el notebook los muestra, no cuando la
  función los crea — se puede cambiar el orden o suprimir sin reorganizar.

```
proyecto/
├── README.md                 ← este archivo
├── docker-compose.yml        ← mismo stack que los labs (jupyter/scipy-notebook)
├── requirements.txt
├── Makefile                  ← orquestación: `make all` desde cero a HTML
├── .gitignore                ← db/, processed/, html, checkpoints
├── data/
│   ├── README.md             ← procedencia, licencia, diccionario
│   └── raw/heart.csv         ← dataset UCI commiteado (público, 20KB)
├── db/                       ← SQLite generada (gitignored)
├── src/
│   ├── ingest.py             ← CSV → SQLite (raw_patients)
│   ├── curate.py             ← raw_patients → curated_patients
│   ├── eda.py                ← funciones que retornan Figure
│   ├── model.py              ← pipeline de regresión logística
│   └── validate.py           ← CV, ROC, métricas clínicas
├── notebooks/
│   └── dashboard.ipynb       ← orquesta todo, narra los resultados
└── tests/
    └── test_curate.py        ← smoke tests de curación
```

## Cómo correrlo

### Opción 1: Docker (recomendado, igual que los labs)

```bash
docker compose up
```

Abre http://localhost:8888 → `notebooks/dashboard.ipynb` → Run All.

### Opción 2: Pipeline completo automatizado (Makefile)

```bash
make all      # setup + ingest + curate + tests + render HTML
```

`make all` deja `notebooks/dashboard.html` listo para abrir.

> **El Makefile es un complemento, no un reemplazo.** Los labs usan
> `docker-compose` y eso aprendiste. Este proyecto muestra que puedes
> sumar herramientas (orquestación con Make, tests con pytest) cuando el
> proyecto crece. No estás obligado a usar Make — pero tampoco estás
> obligado a quedarte solo con lo que vimos en clase.

### Opción 3: Pipeline paso a paso

```bash
make ingest   # data/raw/heart.csv → db/heart.db (raw_patients)
make curate   # raw_patients → curated_patients
make test     # pytest
make render   # ejecuta el notebook y genera HTML
```

## Reproducibilidad

- `make all` desde un repo recién clonado debe producir el HTML sin
  intervención manual.
- La base SQLite (`db/heart.db`) **no** se commitea: es regenerable. Esto
  garantiza que cualquier resultado se reconstruye desde el CSV crudo.
- Versiones pinneadas en `requirements.txt`.

## Lo que este ejemplo intenta enseñar

1. **Trazabilidad clínica.** Cada decisión técnica está atada a una
   pregunta clínica concreta y un costo de error explícito.
2. **Honestidad metodológica.** Excluir `num` para evitar leakage,
   reportar sensibilidad/especificidad (no solo accuracy), documentar
   limitaciones reales.
3. **Reproducibilidad.** De CSV a HTML con un comando, sin estado mágico
   en notebooks.
4. **Estructura.** Notebook como dashboard, lógica en módulos, tests
   sobre lo que importa.

## Lo que este ejemplo NO intenta enseñar

- Modelos sofisticados. La regresión logística está justificada por N=297.
  En tu proyecto, el modelo correcto depende de tu pregunta y tu dataset.
- Visualización exhaustiva. Los gráficos del notebook responden preguntas
  específicas; no es un tour de seaborn.
- Despliegue. Esto es un análisis reproducible, no un sistema en producción.
