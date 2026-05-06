"""Curación de raw_patients -> curated_patients.

Decisiones explícitas (también documentadas en el notebook):

1. Faltantes ('?') en `ca` (4 filas) y `thal` (2 filas) -> drop. N pasa de 303 a 297.
   Justificación: <2% de las filas, sin patrón sistemico observable; la
   imputación introduce ruido que en un dataset de 303 pacientes no
   compensa la información perdida. Documentar la decisión es lo importante.

2. Target binario: `target = 1 if num > 0 else 0`. La variable original `num`
   codifica severidad (0-4). Para la decisión clínica de priorización
   ("¿enviar a cateterismo?") un binario es suficiente y honesto sobre la
   resolución del modelo en un dataset chico. La columna `num` se
   conserva en raw_patients pero NO debe usarse como feature (data leakage).

3. Tipos: todas las features numéricas a float; sex/fbs/exang a int (0/1);
   cp/restecg/slope/ca/thal/target a int categóricos.

Idempotente: reescribe la tabla curated_patients de cero cada vez.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from . import DB_PATH
from .ingest import RAW_TABLE

CURATED_TABLE = "curated_patients"

NUMERIC_COLS = ["age", "trestbps", "chol", "thalach", "oldpeak"]
BINARY_COLS = ["sex", "fbs", "exang"]
CATEGORICAL_COLS = ["cp", "restecg", "slope", "ca", "thal"]


def read_raw(db_path: Path = DB_PATH) -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql(f"SELECT * FROM {RAW_TABLE}", conn)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica las tres decisiones documentadas arriba. No muta el input."""
    out = df.replace("?", np.nan).copy()

    for col in NUMERIC_COLS:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    for col in BINARY_COLS + CATEGORICAL_COLS + ["num"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    before = len(out)
    out = out.dropna().reset_index(drop=True)
    dropped = before - len(out)

    out["target"] = (out["num"] > 0).astype(int)

    for col in BINARY_COLS + CATEGORICAL_COLS:
        out[col] = out[col].astype(int)
    out["num"] = out["num"].astype(int)

    out.attrs["dropped_rows"] = dropped
    return out


def write_curated(df: pd.DataFrame, db_path: Path = DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        df.to_sql(CURATED_TABLE, conn, if_exists="replace", index=False)


def curate(db_path: Path = DB_PATH) -> dict:
    """Pipeline de curación. Retorna metadata sobre lo que pasó."""
    raw = read_raw(db_path)
    cleaned = clean(raw)
    write_curated(cleaned, db_path)
    return {
        "raw_rows": len(raw),
        "curated_rows": len(cleaned),
        "dropped_rows": cleaned.attrs.get("dropped_rows", 0),
        "positive_rate": float(cleaned["target"].mean()),
    }


def read_curated(db_path: Path = DB_PATH) -> pd.DataFrame:
    """Helper para que eda/model/validate no toquen SQL."""
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql(f"SELECT * FROM {CURATED_TABLE}", conn)


if __name__ == "__main__":
    summary = curate()
    print(
        f"[curate] {summary['raw_rows']} -> {summary['curated_rows']} "
        f"(drop {summary['dropped_rows']}). Tasa de positivos: "
        f"{summary['positive_rate']:.1%}"
    )
