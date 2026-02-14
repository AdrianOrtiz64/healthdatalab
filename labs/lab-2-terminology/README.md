# 🧪 Lab 2 — Terminología y Semántica

En los labs anteriores:

- Creamos tablas
- Insertamos datos
- Detectamos errores y valores faltantes

Ahora vamos a resolver otro problema:

> Los datos existen, pero no están estandarizados.

---

## 🎯 Objetivo del laboratorio

Trabajar con un **modelo clínico codificado**.

Vamos a:

- Crear un mini “terminology service”
- Mapear diagnósticos y laboratorios a códigos estándar simulados
- Comparar analítica antes y después de codificar
- Entender por qué los códigos importan

---

## 🧱 Qué vamos a construir

Dentro del mismo entorno PostgreSQL:

1. Tablas clínicas (ya existentes)
   - `patients`
   - `admissions`
   - `diagnoses`
   - `labevents`
   - `d_labitems`

2. Nuevas tablas de terminología:
   - `icd10_codes`
   - `loinc_codes`
   - `diagnosis_code_map`
   - `labitem_code_map`

No usaremos APIs externas.
Simularemos un **mini terminology server relacional**.

---

## 📊 Qué aprenderás

- Diferencia entre texto libre y código estructurado
- Qué significa “normalizar semánticamente”
- Cómo cambia la analítica cuando usamos códigos

---

## 🧭 Flujo de trabajo

Sigue exactamente el flujo definido en `course_setup.md`.

Resumen mínimo:

1. Actualiza `main`
2. Crea tu branch:

```bash
git checkout -b lab2-terminology/grupo-N
```

3. Trabaja únicamente en ese branch
4. Haz commits durante el proceso
5. Entrega con Pull Request

---

## 📓 Importante

Este laboratorio se guía desde el notebook:

```
lab2-terminology.ipynb
```

Las instrucciones están dentro del notebook.
Debes ejecutarlo paso a paso.

No modifiques la estructura general.
Sí puedes agregar celdas para explorar.

---

## ✅ Antes de empezar

Verifica:

```bash
git branch
git remote -v
```

- No estás en `main`
- Tienes `origin` y `upstream`
- Estás en la carpeta correcta
- Docker está corriendo

---

## 🧠 Resultado esperado

Al final deberías poder:

- Agrupar diagnósticos por código
- Agrupar laboratorios por código
- Mostrar diferencias en resultados antes y después de codificar
- Explicar qué problema resuelve la terminología

---
