"""Smoke tests de curación.

Pequeños y rápidos: cubren las invariantes que rompen el resto del pipeline
si fallan (target binario, sin NaN, drop de filas con '?'). No buscan ser
exhaustivos — son la red de seguridad que impide que un cambio en curate.py
pase desapercibido.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src import curate, ingest


@pytest.fixture
def fake_raw_df() -> pd.DataFrame:
    """Fixture mínimo: 6 filas, 2 con '?' que deben caer en curate."""
    return pd.DataFrame({
        "age": ["63", "45", "67", "52", "55", "70"],
        "sex": ["1", "0", "1", "1", "0", "1"],
        "cp": ["1", "3", "4", "2", "3", "4"],
        "trestbps": ["145", "120", "160", "138", "130", "150"],
        "chol": ["233", "200", "286", "223", "250", "300"],
        "fbs": ["1", "0", "0", "0", "0", "1"],
        "restecg": ["2", "0", "2", "0", "1", "2"],
        "thalach": ["150", "175", "108", "169", "160", "120"],
        "exang": ["0", "0", "1", "0", "0", "1"],
        "oldpeak": ["2.3", "0.0", "1.5", "0.0", "0.5", "2.0"],
        "slope": ["3", "1", "2", "1", "2", "3"],
        "ca": ["0", "0", "3", "?", "0", "2"],
        "thal": ["6", "3", "3", "3", "?", "7"],
        "num": ["0", "0", "2", "0", "1", "3"],
    })


@pytest.fixture
def temp_db(tmp_path: Path, fake_raw_df: pd.DataFrame) -> Path:
    db = tmp_path / "test.db"
    with sqlite3.connect(db) as conn:
        fake_raw_df.to_sql(ingest.RAW_TABLE, conn, index=False)
    return db


def test_clean_drops_rows_with_question_marks(fake_raw_df: pd.DataFrame) -> None:
    cleaned = curate.clean(fake_raw_df)
    assert len(cleaned) == 4, "Debió haber dropeado 2 filas con '?'"
    assert cleaned.attrs["dropped_rows"] == 2


def test_clean_target_is_binary(fake_raw_df: pd.DataFrame) -> None:
    cleaned = curate.clean(fake_raw_df)
    assert set(cleaned["target"].unique()).issubset({0, 1})
    assert cleaned["target"].dtype == np.int64 or cleaned["target"].dtype == int


def test_clean_target_derived_correctly(fake_raw_df: pd.DataFrame) -> None:
    cleaned = curate.clean(fake_raw_df)
    expected = (cleaned["num"] > 0).astype(int)
    assert (cleaned["target"] == expected).all()


def test_clean_no_nans(fake_raw_df: pd.DataFrame) -> None:
    cleaned = curate.clean(fake_raw_df)
    assert not cleaned.isnull().any().any(), "curate debe garantizar 0 NaN"


def test_clean_numeric_types(fake_raw_df: pd.DataFrame) -> None:
    cleaned = curate.clean(fake_raw_df)
    for col in curate.NUMERIC_COLS:
        assert pd.api.types.is_numeric_dtype(cleaned[col]), f"{col} debe ser numérico"


def test_curate_idempotent(temp_db: Path) -> None:
    """Correrlo dos veces debe producir el mismo curated_patients."""
    summary1 = curate.curate(temp_db)
    df1 = curate.read_curated(temp_db)
    summary2 = curate.curate(temp_db)
    df2 = curate.read_curated(temp_db)
    assert summary1 == summary2
    pd.testing.assert_frame_equal(df1, df2)


def test_ingest_idempotent(tmp_path: Path) -> None:
    """populate_db dos veces deja la tabla con el mismo contenido."""
    csv = tmp_path / "heart.csv"
    csv.write_text(
        "age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,"
        "slope,ca,thal,num\n"
        "63.0,1.0,1.0,145.0,233.0,1.0,2.0,150.0,0.0,2.3,3.0,0.0,6.0,0\n"
    )
    db = tmp_path / "x.db"
    n1 = ingest.populate_db(csv, db)
    n2 = ingest.populate_db(csv, db)
    assert n1 == n2 == 1
    summary = ingest.table_summary(db)
    assert summary["rows"] == 1
