-- Lab 02: Terminología y Semántica
-- 005_apply_mappings.sql
-- "Codifica" el EHR: escribe system + code + display en tablas clínicas

-- 1) Diagnoses: diagnosis_text → ICD-10
UPDATE diagnoses d
SET
  code_system  = s.system_uri,
  code         = c.code,
  code_display = c.display
FROM map_diagnosis_text_to_concept m
JOIN terminology_concepts c ON c.concept_id = m.concept_id
JOIN terminology_systems  s ON s.system_id  = c.system_id
WHERE d.diagnosis_text = m.diagnosis_text;

-- 2) Lab items: label/unit → LOINC
UPDATE d_labitems li
SET
  code_system  = s.system_uri,
  code         = c.code,
  code_display = c.display
FROM map_labitem_to_concept m
JOIN terminology_concepts c ON c.concept_id = m.concept_id
JOIN terminology_systems  s ON s.system_id  = c.system_id
WHERE li.label = m.label
  AND (li.unit = m.unit OR (li.unit IS NULL AND m.unit IS NULL));

-- 3) Chequeos rápidos (para que el notebook pueda mostrar “antes vs después”)
--    A) ¿Cuántos diagnósticos quedaron sin código?
--       (esto no imprime nada por sí solo; es útil para que lo copies al notebook)
-- SELECT COUNT(*) AS uncoded_diagnoses FROM diagnoses WHERE code IS NULL;

--    B) ¿Cuántos labitems quedaron sin código?
-- SELECT COUNT(*) AS uncoded_labitems FROM d_labitems WHERE code IS NULL;

-- 4) Views opcionales (si te gusta dejarlo "listo para dashboard")
CREATE OR REPLACE VIEW v_diagnoses_coded AS
SELECT
  d.diagnosis_id,
  d.hadm_id,
  d.diagnosis_text,
  d.code_system,
  d.code,
  d.code_display
FROM diagnoses d;

CREATE OR REPLACE VIEW v_labitems_coded AS
SELECT
  li.labitem_id,
  li.label,
  li.unit,
  li.code_system,
  li.code,
  li.code_display
FROM d_labitems li;
