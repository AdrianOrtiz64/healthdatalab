-- Patients: identidad longitudinal
CREATE TABLE IF NOT EXISTS patients (
  subject_id SERIAL PRIMARY KEY,
  external_id TEXT UNIQUE,
  full_name TEXT,
  sex CHAR(1) CHECK (sex IN ('M','F','O')),
  date_of_birth DATE,
  date_of_death DATE
);

-- Admissions: encuentros clínicos (eje del modelo)
CREATE TABLE IF NOT EXISTS admissions (
  hadm_id SERIAL PRIMARY KEY,
  subject_id INT REFERENCES patients(subject_id),
  admittime TIMESTAMP,
  dischtime TIMESTAMP,
  admission_type TEXT,
  hospital_expire_flag BOOLEAN
);

-- Diagnoses: diagnósticos por admisión
CREATE TABLE IF NOT EXISTS diagnoses (
  diagnosis_id SERIAL PRIMARY KEY,
  hadm_id INT REFERENCES admissions(hadm_id),
  diagnosis_text TEXT
);

-- Lab dictionary
CREATE TABLE IF NOT EXISTS d_labitems (
  labitem_id SERIAL PRIMARY KEY,
  label TEXT,
  unit TEXT
);

-- Lab events
CREATE TABLE IF NOT EXISTS labevents (
  labevent_id SERIAL PRIMARY KEY,
  hadm_id INT REFERENCES admissions(hadm_id),
  labitem_id INT REFERENCES d_labitems(labitem_id),
  charttime TIMESTAMP,
  value_num NUMERIC
);

-- Patients
INSERT INTO patients (external_id, full_name, sex, date_of_birth) VALUES
('MRN-0001', 'Ana Lopez',       'F', '1980-03-12'),
('MRN-0002', 'Carlos Perez',    'M', '1975-07-01'),
('MRN-0003', 'María Gomez',     'F', '1992-11-23'),
('MRN-0004', 'Jose Martinez',   'M', '1968-05-09'),
('MRN-0005', 'Alex Rivera',     'O', '2001-08-14'),
('MRN-0006', 'Lucía Herrera',   'F', '1988-02-02'),
('MRN-0007', 'Miguel Castillo', 'M', '1959-10-30'),
('MRN-0008', 'Sofia Morales',   'F', '1979-06-18');

-- Admissions
INSERT INTO admissions (subject_id, admittime, dischtime, admission_type, hospital_expire_flag) VALUES
-- Ana (2 admisiones)
(1, '2101-01-10 08:00', '2101-01-15 14:00', 'Emergency', false),
(1, '2102-06-01 10:00', '2102-06-05 09:00', 'Elective',  false),

-- Carlos (1 admisión con mortalidad)
(2, '2101-03-20 22:00', '2101-03-28 10:00', 'Emergency', true),

-- María (1 admisión)
(3, '2101-07-11 13:00', '2101-07-14 11:00', 'Urgent',    false),

-- José (1 admisión)
(4, '2101-09-02 06:00', '2101-09-10 15:00', 'Emergency', false),

-- Alex (1 admisión)
(5, '2101-12-18 19:00', '2101-12-22 08:00', 'Emergency', false),

-- Lucía (2 admisiones)
(6, '2101-02-05 09:30', '2101-02-08 10:00', 'Emergency', false),
(6, '2101-11-01 16:00', '2101-11-04 12:00', 'Urgent',    false),

-- Miguel (1 admisión)
(7, '2101-05-14 07:00', '2101-05-20 15:00', 'Emergency', false),

-- Sofía (1 admisión)
(8, '2101-08-21 20:00', '2101-08-24 09:00', 'Emergency', false);

-- Diagnoses
INSERT INTO diagnoses (hadm_id, diagnosis_text) VALUES
(1,  'Hypertension'),
(1,  'Chest pain'),
(2,  'Elective procedure follow-up'),
(3,  'Sepsis'),
(3,  'Acute Kidney Injury'),
(4,  'Asthma exacerbation'),
(5,  'Pneumonia'),
(6,  'Trauma'),
(7,  'Urinary tract infection'),
(8,  'Dehydration'),
(9,  'Heart failure'),
(10, 'Appendicitis');

-- Lab dictionary
INSERT INTO d_labitems (label, unit) VALUES
('Creatinine', 'mg/dL'),
('Hemoglobin', 'g/dL'),
('White Blood Cells', '10^9/L'),
('Platelets', '10^9/L'),
('Lactate', 'mmol/L');

-- Lab events
INSERT INTO labevents (hadm_id, labitem_id, charttime, value_num) VALUES
-- hadm 1 (Ana - Emergency)
(1, 1, '2101-01-11 06:00', 1.1),
(1, 1, '2101-01-13 06:00', 1.6),
(1, 2, '2101-01-11 06:00', 13.2),
(1, 3, '2101-01-11 06:00',  7.8),
(1, 4, '2101-01-11 06:00', 230),

-- hadm 2 (Ana - Elective)
(2, 2, '2102-06-02 07:00', 12.9),
(2, 3, '2102-06-02 07:00',  6.2),
(2, 4, '2102-06-02 07:00', 210),

-- hadm 3 (Carlos - Sepsis + AKI + death)
(3, 5, '2101-03-21 06:30', 3.8),
(3, 3, '2101-03-21 06:30', 18.4),
(3, 1, '2101-03-21 07:00', 2.5),
(3, 1, '2101-03-23 07:00', 3.1),
(3, 2, '2101-03-21 07:00', 10.4),
(3, 4, '2101-03-21 07:00', 120),

-- hadm 4 (María)
(4, 2, '2101-07-12 08:00', 11.5),
(4, 3, '2101-07-12 08:00',  9.1),
(4, 4, '2101-07-12 08:00', 250),

-- hadm 5 (José - Pneumonia)
(5, 3, '2101-09-03 06:30', 14.2),
(5, 2, '2101-09-03 06:30', 12.1),
(5, 5, '2101-09-03 06:30', 2.2),

-- hadm 6 (Alex - Trauma)
(6, 2, '2101-12-19 07:00', 10.8),
(6, 3, '2101-12-19 07:00', 12.5),
(6, 4, '2101-12-19 07:00', 180),

-- hadm 7 (Lucía - UTI)
(7, 1, '2101-02-06 06:00', 0.9),
(7, 3, '2101-02-06 06:00', 11.0),

-- hadm 8 (Lucía - Dehydration)
(8, 1, '2101-11-02 06:00', 1.4),
(8, 1, '2101-11-03 06:00', 1.1),
(8, 3, '2101-11-02 06:00',  8.4),

-- hadm 9 (Miguel - HF)
(9, 1, '2101-05-15 07:00', 1.8),
(9, 2, '2101-05-15 07:00', 12.7),
(9, 3, '2101-05-15 07:00', 10.2),
(9, 4, '2101-05-15 07:00', 160),

-- hadm 10 (Sofía - Appendicitis)
(10, 3, '2101-08-22 06:00', 13.0),
(10, 2, '2101-08-22 06:00', 12.9);