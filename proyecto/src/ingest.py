"""Ingesta del CSV crudo de UCI Heart Disease (Cleveland) a SQLite.

Idempotente: correrlo dos veces produce el mismo estado final. La tabla
`raw_patients` se reescribe entera; no acumula filas duplicadas.

El CSV en data/raw/heart.csv viene del UCI ML Repository, dataset
"Heart Disease" (procesado Cleveland, n=303). Detrano et al. 1989.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from . import DATA_RAW, DB_PATH

RAW_TABLE = "raw_patients"


def load_raw_csv(path: Path = DATA_RAW) -> pd.DataFrame:
    """Lee el CSV crudo. Mantiene `?` como string — la conversion a NaN
    es responsabilidad de curate.py, no de ingest. Aquí no transformamos:
    solo cargamos."""
    if not path.exists():
        raise FileNotFoundError(
            f"No se encuentra {path}. El CSV debe vivir en data/raw/heart.csv. "
            "Ver data/README.md para procedencia."
        )
    return pd.read_csv(path, dtype=str)


def write_to_sqlite(df: pd.DataFrame, db_path: Path = DB_PATH) -> None:
    """Reescribe la tabla raw_patients. Idempotente."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        df.to_sql(RAW_TABLE, conn, if_exists="replace", index=False)


def populate_db(csv_path: Path = DATA_RAW, db_path: Path = DB_PATH) -> int:
    """Pipeline de ingest. Retorna número de filas escritas."""
    df = load_raw_csv(csv_path)
    write_to_sqlite(df, db_path)
    return len(df)


def table_summary(db_path: Path = DB_PATH, table: str = RAW_TABLE) -> dict:
    """Resumen rápido para mostrar en el notebook (filas, columnas, primer registro)."""
    with sqlite3.connect(db_path) as conn:
        row_count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        columns = [r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    return {"table": table, "rows": row_count, "columns": columns}


if __name__ == "__main__":
    n = populate_db()
    print(f"[ingest] {n} filas escritas en {DB_PATH} (tabla {RAW_TABLE})")
