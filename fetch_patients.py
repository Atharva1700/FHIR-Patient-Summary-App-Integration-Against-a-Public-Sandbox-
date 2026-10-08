"""Fetch synthetic Patient resources from the HAPI FHIR sandbox and store a flat summary.

Usage:
    python fetch_patients.py --count 20 --db patients.db
"""
import argparse
import sqlite3
from pathlib import Path

import requests

FHIR_BASE = "https://hapi.fhir.org/baseR4"
REQUIRED = ("family_name", "given_name", "birth_date", "gender")
SCHEMA = Path(__file__).with_name("schema.sql")


def fetch_patients(count: int) -> list[dict]:
    resp = requests.get(
        f"{FHIR_BASE}/Patient", params={"_count": count, "_format": "json"}, timeout=30
    )
    resp.raise_for_status()
    bundle = resp.json()
    return [e["resource"] for e in bundle.get("entry", []) if "resource" in e]


def to_row(patient: dict) -> dict:
    name = (patient.get("name") or [{}])[0]
    row = {
        "patient_id": patient.get("id"),
        "family_name": name.get("family"),
        "given_name": " ".join(name.get("given", [])) or None,
        "birth_date": patient.get("birthDate"),
        "gender": patient.get("gender"),
    }
    row["missing"] = ",".join(f for f in REQUIRED if not row.get(f)) or None
    return row


def save(rows: list[dict], db_path: str) -> None:
    con = sqlite3.connect(db_path)
    con.executescript(SCHEMA.read_text())
    con.executemany(
        """INSERT OR REPLACE INTO patient_summary
           (patient_id, family_name, given_name, birth_date, gender, missing)
           VALUES (:patient_id, :family_name, :given_name, :birth_date, :gender, :missing)""",
        rows,
    )
    con.commit()
    con.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--db", default="patients.db")
    args = parser.parse_args()

    rows = [to_row(p) for p in fetch_patients(args.count)]
    save(rows, args.db)

    incomplete = [r for r in rows if r["missing"]]
    print(f"Stored {len(rows)} patients in {args.db}; {len(incomplete)} with missing fields.")
    for r in incomplete:
        print(f"  {r['patient_id']}: missing {r['missing']}")


if __name__ == "__main__":
    main()
