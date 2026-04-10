-- Lab 02: Terminología y Semántica
-- 003_terminology_schema.sql
-- "Mini terminology server" en la misma DB

-- 1) Catálogo de sistemas de códigos (ICD-10, LOINC, etc.)
CREATE TABLE IF NOT EXISTS terminology_systems (
  system_id SERIAL PRIMARY KEY,
  system_name TEXT NOT NULL UNIQUE,      -- e.g., 'ICD-10', 'LOINC'
  system_uri  TEXT NOT NULL UNIQUE,      -- e.g., 'http://hl7.org/fhir/sid/icd-10'
  description TEXT
);

-- 2) Conceptos (códigos) dentro de un sistema
CREATE TABLE IF NOT EXISTS terminology_concepts (
  concept_id SERIAL PRIMARY KEY,
  system_id INT NOT NULL REFERENCES terminology_systems(system_id),
  code TEXT NOT NULL,
  display TEXT NOT NULL,
  version TEXT,
  concept_type TEXT,                     -- e.g., 'diagnosis', 'lab'
  UNIQUE (system_id, code)
);

-- 3) "Mapping tables" (puente desde texto local → concepto codificado)
--    A) Diagnóstico libre (diagnosis_text) → ICD-10
CREATE TABLE IF NOT EXISTS map_diagnosis_text_to_concept (
  diagnosis_text TEXT PRIMARY KEY,
  concept_id INT NOT NULL REFERENCES terminology_concepts(concept_id)
);

--    B) Label local de laboratorio (d_labitems.label + unit) → LOINC
CREATE TABLE IF NOT EXISTS map_labitem_to_concept (
  label TEXT NOT NULL,
  unit  TEXT,
  concept_id INT NOT NULL REFERENCES terminology_concepts(concept_id),
  PRIMARY KEY (label, unit)
);

-- 4) Preparar el EHR para guardar códigos (sin romper labs previos)
--    (esto NO borra nada; solo agrega columnas nuevas)
ALTER TABLE diagnoses
  ADD COLUMN IF NOT EXISTS code_system TEXT,
  ADD COLUMN IF NOT EXISTS code TEXT,
  ADD COLUMN IF NOT EXISTS code_display TEXT;

ALTER TABLE d_labitems
  ADD COLUMN IF NOT EXISTS code_system TEXT,
  ADD COLUMN IF NOT EXISTS code TEXT,
  ADD COLUMN IF NOT EXISTS code_display TEXT;

-- 5) Índices útiles para queries
CREATE INDEX IF NOT EXISTS idx_concepts_system_code ON terminology_concepts(system_id, code);
CREATE INDEX IF NOT EXISTS idx_diag_code ON diagnoses(code);
CREATE INDEX IF NOT EXISTS idx_labitems_code ON d_labitems(code);
