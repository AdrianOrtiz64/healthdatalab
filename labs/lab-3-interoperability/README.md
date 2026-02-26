# Lab 3 — Interoperabilidad: De SQL a FHIR

En los labs anteriores:

- Construimos un EHR relacional (patients, admissions, diagnoses, labevents)
- Normalizamos su semántica con ICD-10 y LOINC (el "terminology server")

Ahora el paso final:

> Los datos existen y están codificados. ¿Cómo los **intercambiamos** con otro sistema?

---

## 🎯 Objetivo del laboratorio

Convertir datos clínicos relacionales a **FHIR** (Fast Healthcare Interoperability Resources), el estándar HL7 que usan hospitales, gobiernos y aplicaciones de salud para intercambiar información clínica.

Vamos a:

- Construir el EHR y el servidor de terminología directamente desde el notebook
- Mapear cada tabla SQL a su recurso FHIR equivalente
- Ensamblar un Bundle FHIR listo para intercambio
- Consultar la especificación oficial de HL7 FHIR

---

## 🧱 Qué vamos a construir

```
patients       →  Patient
admissions     →  Encounter
diagnoses      →  Condition
labevents      →  Observation
(todos)        →  Bundle
```

---

## 📊 Qué aprenderás

- Por qué los códigos (ICD-10, LOINC) son prerequisito para la interoperabilidad
- Cómo se estructura un recurso FHIR y cómo se referencian entre sí
- La diferencia entre un Bundle `collection` y uno `transaction`
- Cómo filtrar datos para un destinatario específico (registro epidemiológico)

---

## 🧭 Flujo de trabajo

Sigue el flujo definido en `course_setup.md`.

1. Actualiza `main`
2. Crea tu branch:

```bash
git checkout -b lab03-interoperability/grupo-N
```

3. Trabaja únicamente en ese branch
4. Haz commits durante el proceso
5. Entrega con Pull Request

---

## 📓 Importante

Este laboratorio se guía completamente desde el notebook:

```
notebooks/Lab03_Interoperabilidad_FHIR.ipynb
```

**No necesitas correr ningún script SQL manualmente.** El notebook ejecuta los scripts en orden y muestra el estado de la base de datos después de cada paso.

Las instrucciones y ejercicios están dentro del notebook.

---

## ✅ Antes de empezar

Verifica:

```bash
git branch
git remote -v
docker compose up -d
```

- No estás en `main`
- Tienes `origin` y `upstream`
- Docker está corriendo (db + jupyter)

---

## 🧠 Resultado esperado

Al final deberías poder:

- Explicar qué tabla SQL corresponde a qué recurso FHIR
- Construir un Bundle FHIR válido para una admisión clínica
- Explicar por qué un diagnóstico sin código ICD-10 es menos interoperable
- Consultar la especificación FHIR para entender la estructura de cada recurso
