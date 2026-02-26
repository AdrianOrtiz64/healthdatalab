-- Lab 02: Terminología y Semántica
-- 004_seed_terminology.sql
-- Carga un "mini ICD-10" y un "mini LOINC" + mapeos desde el EHR local

-- 1) Sistemas
INSERT INTO terminology_systems (system_name, system_uri, description)
VALUES
  ('ICD-10', 'http://hl7.org/fhir/sid/icd-10', 'Diagnósticos (mini demo)'),
  ('LOINC',  'http://loinc.org',              'Laboratorios (mini demo)')
ON CONFLICT (system_name) DO NOTHING;

-- Helpers: IDs de sistemas
-- (Postgres: lo resolvemos con subqueries en cada insert)

-- 2) Conceptos ICD-10 (mini)
INSERT INTO terminology_concepts (system_id, code, display, version, concept_type)
VALUES
  ((SELECT system_id FROM terminology_systems WHERE system_name='ICD-10'), 'I10',    'Essential (primary) hypertension', 'ICD-10', 'diagnosis'),
  ((SELECT system_id FROM terminology_systems WHERE system_name='ICD-10'), 'R07.9',  'Chest pain, unspecified',         'ICD-10', 'diagnosis'),
  ((SELECT system_id FROM terminology_systems WHERE system_name='ICD-10'), 'Z09',    'Follow-up exam after treatment',  'ICD-10', 'diagnosis'),
  ((SELECT system_id FROM terminology_systems WHERE system_name='ICD-10'), 'A41.9',  'Sepsis, unspecified organism',    'ICD-10', 'diagnosis'),
  ((SELECT system_id FROM terminology_systems WHERE system_name='ICD-10'), 'N17.9',  'Acute kidney failure, unspecified','ICD-10', 'diagnosis'),
  ((SELECT system_id FROM terminology_systems WHERE system_name='ICD-10'), 'J45.901','Unspecified asthma with exacerbation','ICD-10', 'diagnosis'),
  ((SELECT system_id FROM terminology_systems WHERE system_name='ICD-10'), 'J18.9',  'Pneumonia, unspecified organism', 'ICD-10', 'diagnosis'),
  ((SELECT system_id FROM terminology_systems WHERE system_name='ICD-10'), 'T14.90', 'Injury, unspecified, initial encounter', 'ICD-10', 'diagnosis'),
  ((SELECT system_id FROM terminology_systems WHERE system_name='ICD-10'), 'N39.0',  'Urinary tract infection, site not specified','ICD-10', 'diagnosis'),
  ((SELECT system_id FROM terminology_systems WHERE system_name='ICD-10'), 'E86.0',  'Dehydration',                    'ICD-10', 'diagnosis'),
  ((SELECT system_id FROM terminology_systems WHERE system_name='ICD-10'), 'I50.9',  'Heart failure, unspecified',      'ICD-10', 'diagnosis'),
  ((SELECT system_id FROM terminology_systems WHERE system_name='ICD-10'), 'K35.80', 'Acute appendicitis without perforation, abscess, or gangrene', 'ICD-10', 'diagnosis')
ON CONFLICT (system_id, code) DO NOTHING;

-- 3) Conceptos LOINC (mini)
INSERT INTO terminology_concepts (system_id, code, display, version, concept_type)
VALUES
  ((SELECT system_id FROM terminology_systems WHERE system_name='LOINC'), '2160-0', 'Creatinine [Mass/volume] in Serum or Plasma', 'LOINC', 'lab'),
  ((SELECT system_id FROM terminology_systems WHERE system_name='LOINC'), '718-7',  'Hemoglobin [Mass/volume] in Blood',           'LOINC', 'lab'),
  ((SELECT system_id FROM terminology_systems WHERE system_name='LOINC'), '6690-2', 'Leukocytes [#/volume] in Blood',              'LOINC', 'lab'),
  ((SELECT system_id FROM terminology_systems WHERE system_name='LOINC'), '777-3',  'Platelets [#/volume] in Blood',               'LOINC', 'lab'),
  ((SELECT system_id FROM terminology_systems WHERE system_name='LOINC'), '2524-7', 'Lactate [Moles/volume] in Blood',             'LOINC', 'lab')
ON CONFLICT (system_id, code) DO NOTHING;

-- 4) Mapeo: diagnosis_text (local) → concepto ICD-10
-- Nota: aquí asumimos que tu diagnosis_text coincide exactamente con los strings del seed del Lab 1.
INSERT INTO map_diagnosis_text_to_concept (diagnosis_text, concept_id)
VALUES
  ('Hypertension', (SELECT concept_id FROM terminology_concepts c
                    JOIN terminology_systems s ON s.system_id=c.system_id
                    WHERE s.system_name='ICD-10' AND c.code='I10')),

  ('Chest pain', (SELECT concept_id FROM terminology_concepts c
                  JOIN terminology_systems s ON s.system_id=c.system_id
                  WHERE s.system_name='ICD-10' AND c.code='R07.9')),

  ('Elective procedure follow-up', (SELECT concept_id FROM terminology_concepts c
                                    JOIN terminology_systems s ON s.system_id=c.system_id
                                    WHERE s.system_name='ICD-10' AND c.code='Z09')),

  ('Sepsis', (SELECT concept_id FROM terminology_concepts c
              JOIN terminology_systems s ON s.system_id=c.system_id
              WHERE s.system_name='ICD-10' AND c.code='A41.9')),

  ('Acute Kidney Injury', (SELECT concept_id FROM terminology_concepts c
                           JOIN terminology_systems s ON s.system_id=c.system_id
                           WHERE s.system_name='ICD-10' AND c.code='N17.9')),

  ('Asthma exacerbation', (SELECT concept_id FROM terminology_concepts c
                           JOIN terminology_systems s ON s.system_id=c.system_id
                           WHERE s.system_name='ICD-10' AND c.code='J45.901')),

  ('Pneumonia', (SELECT concept_id FROM terminology_concepts c
                 JOIN terminology_systems s ON s.system_id=c.system_id
                 WHERE s.system_name='ICD-10' AND c.code='J18.9')),

  ('Trauma', (SELECT concept_id FROM terminology_concepts c
              JOIN terminology_systems s ON s.system_id=c.system_id
              WHERE s.system_name='ICD-10' AND c.code='T14.90')),

  ('Urinary tract infection', (SELECT concept_id FROM terminology_concepts c
                               JOIN terminology_systems s ON s.system_id=c.system_id
                               WHERE s.system_name='ICD-10' AND c.code='N39.0')),

  ('Dehydration', (SELECT concept_id FROM terminology_concepts c
                   JOIN terminology_systems s ON s.system_id=c.system_id
                   WHERE s.system_name='ICD-10' AND c.code='E86.0')),

  ('Heart failure', (SELECT concept_id FROM terminology_concepts c
                     JOIN terminology_systems s ON s.system_id=c.system_id
                     WHERE s.system_name='ICD-10' AND c.code='I50.9')),

  ('Appendicitis', (SELECT concept_id FROM terminology_concepts c
                    JOIN terminology_systems s ON s.system_id=c.system_id
                    WHERE s.system_name='ICD-10' AND c.code='K35.80'))
ON CONFLICT (diagnosis_text) DO NOTHING;

-- 5) Mapeo: d_labitems.label/unit (local) → concepto LOINC
INSERT INTO map_labitem_to_concept (label, unit, concept_id)
VALUES
  ('Creatinine', 'mg/dL', (SELECT concept_id FROM terminology_concepts c
                           JOIN terminology_systems s ON s.system_id=c.system_id
                           WHERE s.system_name='LOINC' AND c.code='2160-0')),

  ('Hemoglobin', 'g/dL', (SELECT concept_id FROM terminology_concepts c
                          JOIN terminology_systems s ON s.system_id=c.system_id
                          WHERE s.system_name='LOINC' AND c.code='718-7')),

  ('White Blood Cells', '10^9/L', (SELECT concept_id FROM terminology_concepts c
                                   JOIN terminology_systems s ON s.system_id=c.system_id
                                   WHERE s.system_name='LOINC' AND c.code='6690-2')),

  ('Platelets', '10^9/L', (SELECT concept_id FROM terminology_concepts c
                           JOIN terminology_systems s ON s.system_id=c.system_id
                           WHERE s.system_name='LOINC' AND c.code='777-3')),

  ('Lactate', 'mmol/L', (SELECT concept_id FROM terminology_concepts c
                         JOIN terminology_systems s ON s.system_id=c.system_id
                         WHERE s.system_name='LOINC' AND c.code='2524-7'))
ON CONFLICT (label, unit) DO NOTHING;
