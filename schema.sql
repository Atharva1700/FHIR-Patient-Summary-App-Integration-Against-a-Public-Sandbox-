CREATE TABLE IF NOT EXISTS patient_summary (
    patient_id   TEXT PRIMARY KEY,
    family_name  TEXT,
    given_name   TEXT,
    birth_date   TEXT,
    gender       TEXT,
    missing      TEXT  -- comma-separated list of required fields that were absent
);
