"""Análisis exploratorio. Cada función responde UNA pregunta clínica concreta.

Convención: las funciones retornan un objeto Figure de matplotlib. NO llaman
a plt.show() — eso es responsabilidad del notebook. Esto las hace testeables,
embebibles en reports HTML, y permite cambiar el orden sin reorganizar plt.

Paleta acotada: dos colores por gráfico (#5AA2AE teal, #156082 azul oscuro).
Si un gráfico requiere más colores, repensar la pregunta.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

PALETTE = ["#5AA2AE", "#156082"]
TEAL, NAVY = PALETTE


def _setup_style() -> None:
    sns.set_style("whitegrid")
    sns.set_context("notebook")


def plot_target_balance(df: pd.DataFrame) -> Figure:
    """Pregunta: ¿qué tan balanceado está el outcome?
    Importa porque modelos sobre clases muy desbalanceadas requieren tratamiento
    especial (umbrales, class_weight, sampling)."""
    _setup_style()
    fig, ax = plt.subplots(figsize=(5, 3.5))
    counts = df["target"].value_counts().sort_index()
    ax.bar(["Sin enfermedad", "Con enfermedad"], counts.values, color=PALETTE)
    for i, v in enumerate(counts.values):
        ax.text(i, v + 2, f"{v}\n({v / len(df):.0%})", ha="center", fontsize=10)
    ax.set_ylabel("Pacientes")
    ax.set_title("Distribución del outcome")
    ax.set_ylim(0, max(counts.values) * 1.15)
    fig.tight_layout()
    return fig


def plot_age_by_target(df: pd.DataFrame) -> Figure:
    """Pregunta: ¿la edad separa pacientes con vs. sin enfermedad coronaria?"""
    _setup_style()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(
        data=df, x="target", y="age", ax=ax,
        palette=PALETTE, hue="target", legend=False,
    )
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Sin enfermedad", "Con enfermedad"])
    ax.set_xlabel("")
    ax.set_ylabel("Edad (años)")
    ax.set_title("Edad por estado de enfermedad coronaria")
    fig.tight_layout()
    return fig


def plot_chest_pain_by_target(df: pd.DataFrame) -> Figure:
    """Pregunta: ¿el tipo de dolor de pecho discrimina?
    cp: 1=angina típica, 2=atípica, 3=no anginoso, 4=asintomático."""
    _setup_style()
    fig, ax = plt.subplots(figsize=(7, 4))
    cp_labels = {1: "Angina típica", 2: "Atípica", 3: "No anginoso", 4: "Asintomático"}
    ct = pd.crosstab(df["cp"].map(cp_labels), df["target"], normalize="index")
    ct.columns = ["Sin enfermedad", "Con enfermedad"]
    ct.plot(kind="bar", ax=ax, color=PALETTE, width=0.7)
    ax.set_ylabel("Proporción")
    ax.set_xlabel("Tipo de dolor de pecho")
    ax.set_title("Tasa de enfermedad por tipo de dolor de pecho")
    ax.legend(loc="upper left")
    plt.setp(ax.get_xticklabels(), rotation=15, ha="right")
    fig.tight_layout()
    return fig


def plot_thalach_vs_age(df: pd.DataFrame) -> Figure:
    """Pregunta: ¿cómo se relaciona la frecuencia cardiaca máxima alcanzada
    en stress test (thalach) con la edad, separando por outcome?"""
    _setup_style()
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    for label, color in zip([0, 1], PALETTE):
        sub = df[df["target"] == label]
        ax.scatter(
            sub["age"], sub["thalach"],
            color=color, alpha=0.6, s=35,
            label="Sin enfermedad" if label == 0 else "Con enfermedad",
        )
    ax.set_xlabel("Edad (años)")
    ax.set_ylabel("Frecuencia cardiaca máxima (thalach)")
    ax.set_title("Capacidad funcional vs. edad")
    ax.legend()
    fig.tight_layout()
    return fig


def plot_correlations(df: pd.DataFrame) -> Figure:
    """Pregunta: ¿qué features numéricas están correlacionadas con el outcome?
    Ojo: correlación lineal, no captura interacciones."""
    _setup_style()
    numeric = df[["age", "trestbps", "chol", "thalach", "oldpeak", "target"]]
    corr = numeric.corr()
    fig, ax = plt.subplots(figsize=(6, 5))
    cmap = sns.blend_palette([TEAL, "white", NAVY], as_cmap=True)
    sns.heatmap(
        corr, annot=True, fmt=".2f", cmap=cmap,
        vmin=-1, vmax=1, center=0, square=True, ax=ax,
        cbar_kws={"shrink": 0.8},
    )
    ax.set_title("Correlación de Pearson (numéricas)")
    fig.tight_layout()
    return fig


def descriptive_table(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla 1 estilo paper: media (sd) por grupo para variables numéricas,
    n (%) para categóricas. Sin tests estadísticos en este nivel — la
    validación cuantitativa va en validate.py."""
    rows = []
    for col in ["age", "trestbps", "chol", "thalach", "oldpeak"]:
        for grp, sub in df.groupby("target"):
            rows.append({
                "variable": col,
                "grupo": "Con enfermedad" if grp == 1 else "Sin enfermedad",
                "resumen": f"{sub[col].mean():.1f} ± {sub[col].std():.1f}",
            })
    table = pd.DataFrame(rows)
    return table.pivot(index="variable", columns="grupo", values="resumen")
