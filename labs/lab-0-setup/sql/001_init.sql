CREATE TABLE IF NOT EXISTS patient ( patient_id SERIAL PRIMARY KEY, sex TEXT CHECK (sex IN ('M','F','O')), birth_date DATE, city TEXT, has_chronic_condition BOOLEAN, created_at TIMESTAMP DEFAULT now() );

INSERT INTO patient (sex, birth_date, city, has_chronic_condition) VALUES ('F', '1990-05-12', 'Guatemala', true), ('M', '1984-11-03', 'Antigua', false), ('O', '2001-07-21', 'Quetzaltenango', true), ('F', '1975-02-18', 'Guatemala', false), ('M', '1998-09-30', 'Escuintla', false);
