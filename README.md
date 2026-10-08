# FHIR Patient Summary App

Pulls synthetic Patient records from the public HAPI FHIR sandbox (https://hapi.fhir.org/baseR4), maps them into a SQLite table, and reports records with missing fields. Uses synthetic data only; no real patient data.

## Run

    pip install -r requirements.txt
    python fetch_patients.py --count 20

Creates `patients.db` in the current folder.

## Files

- `fetch_patients.py` - fetches Patient resources, maps them to flat rows, validates required fields, writes to SQL
- `schema.sql` - target table
- `frontend/` - TODO: one-screen React summary view (not started)

## Status

- [x] Fetch and map Patient resources
- [x] Missing-field validation
- [x] Load rows into SQLite
- [ ] React summary screen
