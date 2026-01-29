# Laboratorio 1.1 — Veracidad y Missing Values

En datos reales de hospital, **no todo está completo**: hay campos faltantes, errores de dedo y registros incompletos.
A esto (en el marco de Big Data) se le llama **Veracidad**: el reto de confiar en datos ruidosos, incompletos o inconsistentes.

En este laboratorio harás una mini-auditoría de calidad (veracidad y missing values).

---

## 🎯 Objetivos de aprendizaje

### Parte clínica / datos (Veracidad)

- Entender por qué en RWD existen **missing values**
- Insertar datos “sucios” (NULL, errores)
- Medir missing values con consultas SQL simples

### Parte técnica / proceso (GitHub)

- Trabajar con **fork por grupo**
- Usar **branch por laboratorio**
- Configurar `origin` (fork) y `upstream` (curso)
- Mantener **una sola carpeta local** (sin re-clonar)
- Crear **un PR** como entrega oficial

---

## 👥 Reglas del laboratorio (para evitar caos)

> [!IMPORTANT]
> Estas reglas son **parte de la evaluación**.

### Regla 1 — Fork por grupo (no individual)

- **Cada grupo debe tener UN fork** del repo del curso.
- Si ya hiciste un fork individual, **no lo uses** para entregar.

### Regla 2 — Un branch por laboratorio

El branch del grupo para este lab debe llamarse **exactamente**:

```
lab1.1-veracity/grupo-<N>
```

Ejemplos:

- `lab1.1-veracity/grupo-1`
- `lab1.1-veracity/grupo-8`

### Regla 3 — Un “integrador” por grupo

- **Una persona** hace `commit`, `push` y el PR (integrador).
- Los otros 2 ayudan, revisan, y proponen cambios.
- Esto evita conflictos y “pisarse” commits.

> [!NOTE]
> Esto es un esquema real de equipos: una persona integra, las otras revisan.

### Regla 4 — No vuelvas a clonar

Usa la **misma carpeta local** donde ya tienes el repo.
No crees 10 folders.

---

# Parte A — GitHub: dejar tu PC “en limpio” y bien configurada

## 1) Verifica dónde estás parado (local)

En la carpeta del repo (la raíz), corre:

```powershell
git status
git remote -v
```

### ¿Qué estamos buscando?

- `origin` debe apuntar al **fork del grupo**
- `upstream` debe apuntar al **repo del curso**

Ejemplo esperado:

```text
origin    https://github.com/GRUPO-X/healthdatalab.git (fetch)
origin    https://github.com/GRUPO-X/healthdatalab.git (push)
upstream  https://github.com/uvg-analisis-de-datos-biomedicos/healthdatalab.git (fetch)
upstream  https://github.com/uvg-analisis-de-datos-biomedicos/healthdatalab.git (push)
```

---

## 2) Si NO tienes `upstream`, agrégalo (una vez)

```powershell
git remote add upstream https://github.com/uvg-analisis-de-datos-biomedicos/healthdatalab.git
```

Luego verifica:

```powershell
git remote -v
```

---

## 3) Si tu `origin` NO es el fork del grupo, corrígelo

> [!WARNING]
> Este paso es el que “arregla clones sucios” sin re-clonar.

1. Borra el origin actual (no borra tus archivos):

```powershell
git remote remove origin
```

2. Agrega el origin correcto (fork del grupo):

```powershell
git remote add origin https://github.com/<ORG_O_USUARIO_DEL_GRUPO>/healthdatalab.git
```

3. Verifica:

```powershell
git remote -v
```

---

## 🔁 Ritual obligatorio: “sincronizar antes de empezar”

Esto se hará en **todos** los labs.

```powershell
git checkout main
git pull upstream main
git push origin main
```

> [!TIP]
> Si esto funciona, significa: “estoy al día con el curso y mi fork también”.

---

## 4) Crear el branch del laboratorio (solo integrador)

```powershell
git checkout -b lab1.1-veracity/grupo-<N>
```

Ejemplo:

```powershell
git checkout -b lab1.1-veracity/grupo-4
```

Verifica:

```powershell
git status
```

Debe decir:

```text
On branch lab1.1-veracity/grupo-4
```

---

# Parte B — Veracidad: Missing Values en una tabla de pacientes

> [!IMPORTANT]
> Este lab asume que ya tienes el entorno del Lab 00 funcionando (Docker + Postgres + Jupyter).

## 5) Levantar servicios

Desde la carpeta del lab (ajusta la ruta a tu repo):

```powershell
cd labs/lab-1-ehr-capture
docker compose up -d
docker ps
```

---

## 6) Crear un script SQL de actualización (datos “imperfectos”)

Crea este archivo:

```
sql/003_veracity_update.sql
```

Contenido (cópialo tal cual):

```sql
-- Lab 1.1: Veracity / Missing Values
-- Insertamos datos "reales": campos faltantes y errores de dedo.

-- A) 3 pacientes "sucios" (missing + typo)
INSERT INTO patients (external_id, full_name, sex, date_of_birth) VALUES
('MRN-9001', 'Paciente Sin Fecha', 'F', NULL),            -- Missing DOB
('MRN-9002', 'Paciente Sin Nombre', 'M', '1990-01-01'),   -- Nombre vacío (lo simulamos después)
('MRN-9003', 'Paciente Ciudad Typo', 'M', '1985-09-10');  -- Ciudad con typo (simulada en admissions o diagnóstico)

-- B) Si tu tabla patients no tiene "full_name" nullable o quieres simular missing:
-- actualizamos a NULL un nombre (para simular realidad)
UPDATE patients
SET full_name = NULL
WHERE external_id = 'MRN-9002';

-- C) Simulamos un error de dedo en texto clínico (diagnosis)
-- Creamos una admisión para MRN-9003 y le ponemos un texto con typo
-- (Esto asume que subject_id de MRN-9003 existe. Si falla, revisa el Troubleshooting)
INSERT INTO admissions (subject_id, admittime, dischtime, admission_type, hospital_expire_flag)
SELECT subject_id, '2101-10-01 08:00', '2101-10-02 12:00', 'Emergency', false
FROM patients
WHERE external_id = 'MRN-9003';

INSERT INTO diagnoses (hadm_id, diagnosis_text)
SELECT a.hadm_id, 'Guateeeemala referral note'
FROM admissions a
JOIN patients p ON p.subject_id = a.subject_id
WHERE p.external_id = 'MRN-9003'
ORDER BY a.hadm_id DESC
LIMIT 1;
```

---

## 7) Ejecutar el SQL (Windows PowerShell)

```powershell
Get-Content .\sql\003_veracity_update.sql | docker compose exec -T db psql -U uvg_user -d health_data
```

✅ Debes ver `INSERT` y `UPDATE`.

---

## 🔵 CHECKPOINT 1 (commit obligatorio): “Datos imperfectos insertados”

```powershell
git add sql/003_veracity_update.sql
git commit -m "Checkpoint 1: veracity data inserted (missing + typos)"
```

---

# Parte C — Auditoría rápida en Jupyter (SQL básico, guiado)

Abre `connection_test.ipynb` (el mismo del entorno) y ejecuta **una celda por tarea**.

> [!IMPORTANT]
> Si una consulta falla, no sigas. Corrige primero.

## 8.1 Ver ejemplos de registros “sucios”

```python
pd.read_sql("""
SELECT subject_id, external_id, full_name, sex, date_of_birth
FROM patients
WHERE external_id LIKE 'MRN-9%'
ORDER BY external_id;
""", engine)
```

---

## 8.2 Contar cuántos pacientes tienen fecha de nacimiento faltante

**Tu consulta debe devolver un número.**

Pista: usa `COUNT(*)` y `WHERE date_of_birth IS NULL`.

Escribe algo así (completa tú el SQL):

```python
query = """
SELECT COUNT(*) AS n_missing_dob
FROM patients
WHERE date_of_birth IS NULL;
"""
pd.read_sql(query, engine)
```

---

## 8.3 Contar cuántos pacientes tienen nombre faltante

Pista: `full_name IS NULL`.

---

## 8.4 Encontrar textos con posibles errores de dedo (typos)

Ejemplo: buscar “Guate” en diagnósticos:

Pista: `LIKE '%Guate%'`.

---

## 🔵 CHECKPOINT 2 (commit obligatorio): “Auditoría de missing values”

```powershell
git add *.ipynb
git commit -m "Checkpoint 2: missing value audit queries"
```

---

# Parte D — Reflexión corta (en el PR)

Responde en la descripción del PR:

1. ¿Por qué en datos reales hay campos `NULL`? Da 2 causas.
2. Si un hospital tiene 40% de `date_of_birth` faltante, ¿qué impacto tiene en un modelo de riesgo?
3. ¿Qué es más peligroso: un `NULL` o un typo (“Guateeeemala”)? ¿por qué?

---

# ✅ Entrega (Pull Request)

## 9) Push del branch del grupo (integrador)

```powershell
git push -u origin lab1.1-veracity/grupo-<N>
```

## 10) Crear PR en GitHub

- Base: `main`
- Compare: `lab1.1-veracity/grupo-<N>`
- **NO hacer merge**

Título:

```
Lab 1.1 – Veracity – Grupo <N>
```

En la descripción incluye:

- Qué hiciste (missing + auditoría)
- Respuestas de reflexión

---

# Troubleshooting (lo que más pasa en clase)

## A) “Estoy en el branch incorrecto”

```powershell
git branch
```

El branch actual tiene un `*`.

Cámbiate:

```powershell
git checkout lab1.1-veracity/grupo-<N>
```

---

## B) “No veo el lab nuevo / carpetas no aparecen”

Te falta sincronizar con upstream:

```powershell
git checkout main
git pull upstream main
```

---

## C) “No tengo permisos / 403 al hacer push”

Estás intentando empujar al repo del curso (upstream) o a un fork que no es tuyo.

Revisa `origin`:

```powershell
git remote -v
```

`origin` debe ser el fork del grupo.

---

## D) “Ya tengo cambios raros localmente / carpeta sucia”

No reclones. Guarda tus cambios y vuelve a tu branch.

```powershell
git status
```

Si dice que hay cambios que no quieres:

```powershell
git restore .
```

Si son cambios que sí quieres conservar, dile al integrador que los replique o los copies.

---

# ✅ Checklist final

- [ ] `origin` apunta al fork del grupo
- [ ] `upstream` apunta al repo del curso
- [ ] Branch: `lab1.1-veracity/grupo-<N>`
- [ ] Script SQL ejecutado
- [ ] Queries en Jupyter funcionando
- [ ] 2 commits (checkpoint 1 y 2)
- [ ] PR abierto correctamente
