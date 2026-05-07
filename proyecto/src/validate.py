"""Validación clínica: cross-validation, ROC, métricas de utilidad clínica.

Reporta sensibilidad, especificidad, AUC, matriz de confusión — NO solo
accuracy. En un dataset desbalanceado o con costos asimétricos (no es lo
mismo perder un caso que sobrediagnosticar), accuracy esconde lo que importa.

Umbral por defecto = 0.5 para mantener el ejemplo simple. En un caso real
el umbral se elige según la utilidad clínica (curva de Youden, costo del
falso negativo, etc.). Documentar la decisión donde se toma.
"""

from __future__ import annotations

from typing import Dict, Tuple

import numpy as np
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from sklearn.metrics import (
    auc,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score

from .model import TrainedModel, build_pipeline, prepare_features

PALETTE = ["#5AA2AE", "#156082"]
TEAL, NAVY = PALETTE


def cross_validate_auc(
    df: pd.DataFrame, n_splits: int = 5, seed: int = 42
) -> Dict[str, float]:
    """Stratified K-fold CV sobre AUC. Hacemos CV sobre el dataset completo
    porque CV es la estimación de generalización, no el test set final."""
    X, y = prepare_features(df)
    pipe = build_pipeline()
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    scores = cross_val_score(pipe, X, y, scoring="roc_auc", cv=cv)
    return {
        "auc_mean": float(scores.mean()),
        "auc_std": float(scores.std()),
        "auc_folds": scores.tolist(),
    }


def evaluate(model: TrainedModel, threshold: float = 0.5) -> Tuple[Dict, Figure]:
    """Evaluación holística sobre el test set. Retorna métricas + ROC.

    Threshold default 0.5: razonable cuando los costos clínicos de FP y FN
    son comparables. Para priorización de cateterismo (FN = paciente con
    enfermedad enviado a casa) probablemente convenga bajar el umbral —
    decisión que el equipo clínico debe tomar, no el modelo."""
    proba = model.pipeline.predict_proba(model.X_test)[:, 1]
    y_pred = (proba >= threshold).astype(int)
    y_true = model.y_test.values

    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    sensitivity = tp / (tp + fn) if (tp + fn) else float("nan")
    specificity = tn / (tn + fp) if (tn + fp) else float("nan")
    ppv = tp / (tp + fp) if (tp + fp) else float("nan")
    npv = tn / (tn + fn) if (tn + fn) else float("nan")
    accuracy = (tp + tn) / cm.sum()
    auc_test = roc_auc_score(y_true, proba)

    metrics = {
        "auc_test": float(auc_test),
        "accuracy": float(accuracy),
        "sensitivity": float(sensitivity),
        "specificity": float(specificity),
        "ppv": float(ppv),
        "npv": float(npv),
        "threshold": threshold,
        "confusion_matrix": cm.tolist(),
        "n_test": int(cm.sum()),
    }

    fig = _plot_roc(y_true, proba, auc_test)
    return metrics, fig


def _plot_roc(y_true: np.ndarray, proba: np.ndarray, auc_value: float) -> Figure:
    fpr, tpr, _ = roc_curve(y_true, proba)
    fig, ax = plt.subplots(figsize=(5.5, 5))
    ax.plot(fpr, tpr, color=NAVY, lw=2.2, label=f"AUC = {auc_value:.3f}")
    ax.plot([0, 1], [0, 1], color=TEAL, lw=1, linestyle="--", label="Azar")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.01)
    ax.set_xlabel("1 − Especificidad (FPR)")
    ax.set_ylabel("Sensibilidad (TPR)")
    ax.set_title("Curva ROC — test set")
    ax.legend(loc="lower right")
    fig.tight_layout()
    return fig


def plot_confusion_matrix(metrics: Dict) -> Figure:
    """Render legible de la matriz de confusión con etiquetas clínicas."""
    cm = np.array(metrics["confusion_matrix"])
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, cmap="Blues")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    labels = ["Sin enfermedad", "Con enfermedad"]
    ax.set_xticks([0, 1], labels=labels)
    ax.set_yticks([0, 1], labels=labels)
    ax.set_xlabel("Predicción")
    ax.set_ylabel("Real")
    ax.set_title(f"Matriz de confusión (umbral={metrics['threshold']:.2f})")
    for i in range(2):
        for j in range(2):
            color = "white" if cm[i, j] > cm.max() / 2 else "black"
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                    color=color, fontsize=14, fontweight="bold")
    fig.tight_layout()
    return fig


def format_metrics(metrics: Dict) -> pd.DataFrame:
    """Tabla legible para mostrar en el notebook."""
    return pd.DataFrame([
        ("AUC (test)", f"{metrics['auc_test']:.3f}"),
        ("Accuracy", f"{metrics['accuracy']:.1%}"),
        ("Sensibilidad", f"{metrics['sensitivity']:.1%}"),
        ("Especificidad", f"{metrics['specificity']:.1%}"),
        ("VPP", f"{metrics['ppv']:.1%}"),
        ("VPN", f"{metrics['npv']:.1%}"),
        ("Umbral", f"{metrics['threshold']:.2f}"),
        ("N test", str(metrics["n_test"])),
    ], columns=["Métrica", "Valor"])
