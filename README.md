# Health Data Lab

## BE3006: Análisis de Datos Biomédicos - Ciclo 1, 2026 🏥📊

Bienvenido a la organización de GitHub para el curso **BE3006** de la Universidad del Valle de Guatemala. Este espacio está diseñado para centralizar el aprendizaje práctico y el desarrollo del proyecto integrador, centrado en una pregunta fundamental: **¿Cómo hacer que los datos acompañen decisiones clínicas reales a lo largo del trayecto del paciente (_Patient Journey_)?**.

## 🌟 Visión del Curso

El objetivo central es **convertir observaciones clínicas en datos sistémicos, reutilizables y comparables** para mejorar la toma de decisiones. Acompañaremos al paciente desde su primer síntoma hasta el análisis de sus resultados poblacionales, optimizando el ciclo: **Observar → Medir → Analizar**.

## 🛠️ Stack Tecnológico

Para "domar la complejidad de los datos de salud", utilizaremos herramientas estándar de la industria:

- **Infraestructura:** Docker & Docker Compose (para entornos reproducibles de grado regulatorio).
- **Base de Datos:** PostgreSQL & SQL (Modelado relacional y OMOP).
- **Lenguajes:** Python (pandas, numpy, matplotlib, scikit-learn).
- **Entornos:** Jupyter Notebooks para análisis exploratorio (EDA).
- **Visualización:** Grafana para dashboards operativos.
- **Imágenes:** Procesamiento de metadatos y datos DICOM.

---

## 🧪 Laboratorios

Los laboratorios están diseñados para construir, pieza a pieza, las capacidades necesarias para el proyecto final.

| Lab      | Título                        | Competencia              | Herramienta Clave          |
| :------- | :---------------------------- | :----------------------- | :------------------------- |
| **L0**   | **Setup del Entorno**         | Gobernanza               | Docker + Git               |
| **L1**   | **Captura en el EHR**         | Modelos de Datos         | PostgreSQL (Mini-MIMIC)    |
| **L1.1** | **Veracidad de los datos**    | Auditoría de Calidad     | PostgreSQL                 |
| **L2**   | **Terminología y Semántica**  | Estándares Clínicos      | ICD-10, SNOMED CT, LOINC   |
| **L3**   | **Interoperabilidad FHIR**    | Interoperabilidad        | FHIR R4, Python            |
| **L3.1** | **Datos Sintéticos**          | Datos Sintéticos en Salud| Synthea, Python            |
| **L4**   | **Curación de Datos RWD**     | Preparación              | Python + Pandas            |
| **L5**   | **EDA Clínico**               | Estadística clínica      | Seaborn + Matplotlib       |
| **L6**   | **Modelado Estadístico**      | Modelado estadístico     | Statsmodels + Scikit-learn |
| **L7**   | **Imágenes como Datos**       | Imágenes y señales       | DICOM + Matplotlib         |
| **L8**   | **Predicción Clínica**        | Machine Learning         | Scikit-learn               |
| **L9**   | **Visual Analytics**          | Toma de Decisiones       | Grafana Dashboard          |

---

## 📈 Metodología de Trabajo

Este repositorio sigue una metodología de **Aprendizaje basado en proyectos e investigación**:

1.  **Exploración (Issues):** Identificación de problemas de calidad de datos y discrepancias semánticas.
2.  **Discusión (Discussions):** Debate sobre dilemas éticos, privacidad (GDPR/HIPAA) y gobernanza.
3.  **Colaboración (Pull Requests):** Entrega de laboratorios mediante revisiones de código cruzadas para asegurar la **reproducibilidad**.
4.  **Wiki:**

## 📂 Estructura del Repositorio

- `/labs`: Enunciados y archivos base para las prácticas del curso.
- `/resources`: Lecturas complementarias de _Fundamentals of Clinical Data Science_ y _Machine Learning in Medicine_.
- `/proyecto`: **Ejemplo de referencia** del proyecto integrador Fase 2 (no es plantilla — es inspiración). Pipeline end-to-end con dataset clínico real, notebook tipo dashboard y módulos `.py` testeables. Ver [proyecto/README.md](proyecto/README.md).

---

## Reglas

- Nunca trabajar en main
- Una rama por lab: labXX/grupo-YY
- Solo editar tu carpeta submissions/grupo-YY
- Entrega = PR a main

---

## 📚 Bibliografía Guía

- **Nguyen, A.** (2022). _Hands-On Healthcare Data_. O’Reilly Media..
- **Kubben, P., et al.** (2019). _Fundamentals of Clinical Data Science_. Springer..
- **Cleophas, T. J., & Zwinderman, A. H.** (2015). _Machine Learning in Medicine_. Springer..

---

**Docente:** M.Sc. Miguel Godoy – [mgodoy@uvg.edu.gt](mailto:mgodoy@uvg.edu.gt).
**UVG - 2026** | _Espacio de exploración y creación en conjunto_.
