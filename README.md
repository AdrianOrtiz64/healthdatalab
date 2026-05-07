# Health Data Lab

## BE3006: Análisis de Datos Biomédicos - Ciclo 1, 2026 🏥📊

Bienvenido a la organización de GitHub para el curso **BE3006** de la Universidad del Valle de Guatemala. Este espacio está diseñado para centralizar el aprendizaje práctico y el desarrollo del proyecto integrador, centrado en una pregunta fundamental: **¿Cómo hacer que los datos acompañen decisiones clínicas reales a lo largo del trayecto del paciente (_Patient Journey_)?**.

## 🌟 Visión del Curso

El objetivo central es **convertir observaciones clínicas en datos sistémicos, reutilizables y comparables** para mejorar la toma de decisiones. Acompañaremos al paciente desde su primer síntoma hasta el análisis de sus resultados poblacionales, optimizando el ciclo: **Observar → Medir → Analizar**.

## 🛠️ Stack Tecnológico

Para "domar la complejidad de los datos de salud", utilizaremos herramientas estándar de la industria:

- **Infraestructura:** Docker & Docker Compose (para entornos reproducibles de grado regulatorio).
- **Base de Datos:** PostgreSQL & SQL (Modelado relacional y OMOP).
- **Lenguajes:** Python (pandas, numpy, matplotlib, seaborn, scikit-learn, statsmodels).
- **Entornos:** Jupyter Notebooks para análisis exploratorio (EDA) y modelado.
- **Interoperabilidad:** FHIR R4, terminologías clínicas (ICD-10, SNOMED CT, LOINC).
- **Datos sintéticos:** Synthea para cohortes simuladas.
- **Imágenes:** pydicom para metadatos y datos DICOM.

---

## 🧪 Laboratorios

Los laboratorios están diseñados para construir, pieza a pieza, las capacidades necesarias para el proyecto final.

| Lab      | Título                                          | Competencia               | Herramienta Clave             |
| :------- | :---------------------------------------------- | :------------------------ | :---------------------------- |
| **L0**   | **Setup Reproducible**                          | Gobernanza                | Docker + Postgres + Jupyter   |
| **L1**   | **Captura en el EHR y Modelos de Datos**        | Modelos de Datos          | PostgreSQL (Mini-MIMIC)       |
| **L1.1** | **Veracidad y Missing Values**                  | Auditoría de Calidad      | PostgreSQL                    |
| **L2**   | **Terminología y Semántica**                    | Estándares Clínicos       | ICD-10, SNOMED CT, LOINC      |
| **L3**   | **Interoperabilidad: De SQL a FHIR**            | Interoperabilidad         | FHIR R4, Python               |
| **L3.1** | **Datos Sintéticos con Synthea**                | Datos Sintéticos en Salud | Synthea, Python               |
| **L4**   | **Modelado Estadístico**                        | Modelado estadístico      | Statsmodels + Scikit-learn    |
| **L5**   | **Exploración de Imágenes Médicas con DICOM**   | Imágenes y señales        | pydicom + Matplotlib          |
| **L6**   | **Machine Learning Supervisado**                | Machine Learning          | Scikit-learn                  |

> Próximos laboratorios del ciclo se agregarán a [labs/](labs/) conforme avance el curso. Cada lab vive en su propia carpeta con `README.md`, `docker-compose.yml`, `requirements.txt` y `notebooks/`.

---

## 📈 Metodología de Trabajo

Este repositorio sigue una metodología de **aprendizaje basado en proyectos**:

1. **Exploración (Issues):** Identificación de problemas de calidad de datos y discrepancias semánticas.
2. **Discusión (Discussions):** Debate sobre dilemas éticos, privacidad (GDPR/HIPAA) y gobernanza.
3. **Colaboración (Pull Requests):** Entrega de laboratorios mediante revisiones de código cruzadas para asegurar la **reproducibilidad**.

## 📂 Estructura del Repositorio

- [`labs/`](labs/) — Enunciados y archivos base de los laboratorios. Una carpeta por lab.
- [`proyecto/`](proyecto/) — **Ejemplo de referencia** del proyecto integrador Fase 2 (inspiración, no plantilla). Pipeline end-to-end con dataset clínico real, notebook tipo dashboard y módulos `.py` testeables. Ver [proyecto/README.md](proyecto/README.md).
- [`COURSE_SETUP.md`](COURSE_SETUP.md) — Flujo de trabajo con GitHub para grupos: forks, branches, pull requests. **Léelo antes del primer lab.**

---

## 🔑 Reglas del flujo de trabajo

- **Nunca trabajar en `main`.** Cada lab vive en su propio branch.
- **Un fork por grupo, un branch por lab, un PR por entrega** (`labX-nombre/grupo-N`).
- **El PR es la entrega oficial.** No se hace merge — el profesor revisa y califica.

Detalles completos en [COURSE_SETUP.md](COURSE_SETUP.md).

---

## 📚 Bibliografía Guía

- **Nguyen, A.** (2022). _Hands-On Healthcare Data_. O'Reilly Media.
- **Kubben, P., et al.** (2019). _Fundamentals of Clinical Data Science_. Springer.
- **Cleophas, T. J., & Zwinderman, A. H.** (2015). _Machine Learning in Medicine_. Springer.

---

**Docente:** M.Sc. Miguel Godoy — [mgodoy@uvg.edu.gt](mailto:mgodoy@uvg.edu.gt)
**UVG · 2026** | _Espacio de exploración y creación en conjunto._
