"""Pipeline modular del proyecto-ejemplo Fase 2.

Cada módulo corresponde a una etapa del flujo end-to-end:

- ingest:   CSV crudo -> SQLite (raw_patients)
- curate:   raw_patients -> curated_patients (tipos, faltantes, target binario)
- eda:      figuras matplotlib que responden preguntas clínicas concretas
- model:    pipeline de regresión logística + tabla de coeficientes
- validate: cross-validation, ROC, métricas clínicas (sensibilidad/especificidad)
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw" / "heart.csv"
DB_PATH = PROJECT_ROOT / "db" / "heart.db"
