
"""
TERVA - Threat Evidence & Risk Verification Architecture

Module: Evidence Collector
Purpose: Create structured evidence records.
"""

from datetime import datetime, timezone
from uuid import uuid4

from backend.evidence.validator import validate_evidence


def collect_evidence(title, source, asset, description):
    """
    Create and validate a security evidence record.

    Returns the evidence record if valid.
    Otherwise, returns the validation errors.
    """

    evidence = {
        "id": f"TERVA-EVD-{uuid4().hex[:8].upper()}",
        "title": title,
        "source": source,
        "asset": asset,
        "description": description,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "status": "UNVERIFIED",
    }

    validation = validate_evidence(evidence)

    if not validation["valid"]:
        return {
            "success": False,
            "validation": validation,
            "evidence": None,
        }

    return {
        "success": True,
        "validation": validation,
        "evidence": evidence,
    }

