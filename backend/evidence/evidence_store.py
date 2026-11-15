
"""
TERVA - Threat Evidence & Risk Verification Architecture

Module: Evidence Store
Purpose: Persist and retrieve evidence records using SQLite.
"""

import json
import sqlite3

from contextlib import contextmanager
from pathlib import Path


# Database configuration
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_FILE = (
    PROJECT_ROOT / "backend" / "data" / "terva_evidence.db"
)


@contextmanager
def get_connection():
    """Create and safely close a SQLite database connection."""

    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def initialize_store():
    """Create the evidence table if it does not exist."""

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS evidence (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                source TEXT NOT NULL,
                asset TEXT NOT NULL,
                description TEXT NOT NULL,
                collected_at TEXT NOT NULL,
                status TEXT NOT NULL,
                evidence_json TEXT NOT NULL
            )
        """)


def save_evidence(evidence):
    """Validate and permanently save an evidence record."""

    from backend.evidence.validator import validate_evidence

    validation = validate_evidence(evidence)

    if not validation["valid"]:
        return {
            "success": False,
            "reason": "Evidence validation failed",
            "validation": validation,
        }

    evidence_id = evidence.get("id")

    if not isinstance(evidence_id, str) or not evidence_id.strip():
        return {
            "success": False,
            "reason": "Evidence ID is missing or invalid",
        }

    try:
        with get_connection() as connection:
            connection.execute("""
                INSERT INTO evidence (
                    id,
                    title,
                    source,
                    asset,
                    description,
                    collected_at,
                    status,
                    evidence_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                evidence_id,
                evidence["title"],
                evidence["source"],
                evidence["asset"],
                evidence["description"],
                evidence["collected_at"],
                evidence.get("status", "UNVERIFIED"),
                json.dumps(evidence),
            ))

        return {
            "success": True,
            "evidence_id": evidence_id,
        }

    except sqlite3.IntegrityError:
        return {
            "success": False,
            "reason": "Evidence ID already exists",
        }


def get_evidence(evidence_id):
    """Retrieve one evidence record by its ID."""

    with get_connection() as connection:
        row = connection.execute(
            "SELECT evidence_json FROM evidence WHERE id = ?",
            (evidence_id,),
        ).fetchone()

    if row is None:
        return None

    return json.loads(row["evidence_json"])


def list_evidence():
    """Retrieve all stored evidence records."""

    with get_connection() as connection:
        rows = connection.execute("""
            SELECT evidence_json
            FROM evidence
            ORDER BY collected_at DESC
        """).fetchall()

    return [
        json.loads(row["evidence_json"])
        for row in rows
    ]


# Initialize the main database
initialize_store()
