"""Regresión logística con tratamiento explícito de variables categóricas.

Decisión: regresión logística como modelo principal.
- Coeficientes interpretables clínicamente (odds ratios).
- N=297 es chico — modelos flexibles (RF, gradient boosting) sobreajustan
  sin ganar AUC en este orden de magnitud.
- El curso valora pipeline simple bien validado sobre sofisticación injustificada.

Si quisieras agregar Random Forest, hazlo en una función nueva
`train_random_forest(...)` y compara honestamente vía CV en validate.py.
NO sustituyas la baseline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC_FEATURES = ["age", "trestbps", "chol", "thalach", "oldpeak"]
BINARY_FEATURES = ["sex", "fbs", "exang"]
CATEGORICAL_FEATURES = ["cp", "restecg", "slope", "ca", "thal"]
ALL_FEATURES = NUMERIC_FEATURES + BINARY_FEATURES + CATEGORICAL_FEATURES

# `num` es la severidad original (0-4). `target` se derivó de num. Si dejamos
# `num` como feature, el modelo lo usaría como cheat -> AUC artificialmente
# perfecto. Esto es data leakage: la respuesta correcta del examen filtrada
# en las preguntas. Excluir explícitamente.
LEAKY_COLUMNS = ["num", "target"]


@dataclass
class TrainedModel:
    pipeline: Pipeline
    feature_names: List[str]
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series


def prepare_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Separa X e y excluyendo columnas con leakage."""
    y = df["target"].copy()
    X = df.drop(columns=LEAKY_COLUMNS).copy()
    missing = [c for c in ALL_FEATURES if c not in X.columns]
    if missing:
        raise ValueError(f"Columnas esperadas faltantes en X: {missing}")
    return X[ALL_FEATURES], y


def build_pipeline() -> Pipeline:
    """Pipeline: scaling de numéricas, one-hot de categóricas, regresión logística.
    Mete todo dentro del Pipeline para que el preprocesamiento se ajuste solo
    en train y se aplique a test sin fugas."""
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("bin", "passthrough", BINARY_FEATURES),
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"),
             CATEGORICAL_FEATURES),
        ]
    )
    return Pipeline([
        ("prep", preprocessor),
        ("clf", LogisticRegression(max_iter=1000, solver="liblinear")),
    ])


def split_train_test(
    X: pd.DataFrame, y: pd.Series, test_size: float = 0.25, seed: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Stratified split — preserva la tasa de positivos en train y test."""
    return train_test_split(X, y, test_size=test_size, stratify=y, random_state=seed)


def train(df: pd.DataFrame, test_size: float = 0.25, seed: int = 42) -> TrainedModel:
    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = split_train_test(X, y, test_size, seed)
    pipe = build_pipeline()
    pipe.fit(X_train, y_train)
    feat_names = _expand_feature_names(pipe)
    return TrainedModel(pipe, feat_names, X_train, X_test, y_train, y_test)


def _expand_feature_names(pipe: Pipeline) -> List[str]:
    """Recupera los nombres expandidos tras one-hot encoding."""
    prep = pipe.named_steps["prep"]
    names: List[str] = []
    names.extend(NUMERIC_FEATURES)
    names.extend(BINARY_FEATURES)
    ohe: OneHotEncoder = prep.named_transformers_["cat"]
    cat_names = ohe.get_feature_names_out(CATEGORICAL_FEATURES)
    names.extend(cat_names.tolist())
    return names


def coefficient_table(model: TrainedModel) -> pd.DataFrame:
    """Coeficientes con su odds ratio (exp(coef)) ordenados por magnitud.
    Para variables estandarizadas, |coef| compara directamente la fuerza."""
    coefs = model.pipeline.named_steps["clf"].coef_.ravel()
    table = pd.DataFrame({
        "feature": model.feature_names,
        "coef": coefs,
        "odds_ratio": np.exp(coefs),
    })
    table["abs_coef"] = table["coef"].abs()
    return table.sort_values("abs_coef", ascending=False).drop(columns="abs_coef")
