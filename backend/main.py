
"""
TERVA - Threat Evidence & Risk Verification Architecture
Version: 0.1.0

First component: Evidence Validation
"""

from datetime import datetime, timezone


def validate_finding(finding):
    """Check whether a security finding has required information."""

    required_fields = [
        "title",
        "source",
        "asset",
        "description"
    ]

    missing_fields = []

    for field in required_fields:
        if not finding.get(field):
            missing_fields.append(field)

    if missing_fields:
        return {
            "valid": False,
            "missing_fields": missing_fields
        }

    return {
        "valid": True,
        "missing_fields": []
    }


def create_evidence_record(finding):
    """Create a structured evidence record."""

    validation = validate_finding(finding)

    if not validation["valid"]:
        print("Finding validation failed.")
        print("Missing fields:", validation["missing_fields"])
        return None

    evidence = {
        "id": "TERVA-EVD-001",
        "title": finding["title"],
        "source": finding["source"],
        "asset": finding["asset"],
        "description": finding["description"],
        "status": "UNVERIFIED",
        "collected_at": datetime.now(timezone.utc).isoformat()
    }

    return evidence


def main():
    print("=" * 45)
    print("       TERVA EVIDENCE ENGINE v0.1")
    print("=" * 45)

    sample_finding = {
    "title": "Possible SQL Injection",
    "source": "Sample Security Scanner",
    "asset": "Local Training Application",
    "description": "A scanner reported a possible SQL injection."
}

    evidence = create_evidence_record(sample_finding)

    if evidence:
        print("\nEvidence successfully created:\n")

        for key, value in evidence.items():
            print(f"{key}: {value}")

    print("\nTERVA execution completed.")


if __name__ == "__main__":
    main()
