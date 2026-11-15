
"""
TERVA - Threat Evidence & Risk Verification Architecture

Module: Evidence Validator
Purpose: Validate the structure and quality of security evidence.
"""

from datetime import datetime


REQUIRED_FIELDS = [
    "title",
    "source",
    "asset",
    "description",
    "collected_at",
]


def validate_evidence(evidence):
    """Validate a security evidence record."""

    if not isinstance(evidence, dict):
        return {
            "valid": False,
            "missing_fields": [],
            "errors": ["Evidence must be a dictionary"],
        }

    missing_fields = []
    errors = []

    # 1. Check required fields.
    for field in REQUIRED_FIELDS:
        value = evidence.get(field)

        if value is None or (
            isinstance(value, str) and not value.strip()
        ):
            missing_fields.append(field)

    # 2. Validate timestamp format.
    timestamp = evidence.get("collected_at")

    if timestamp and isinstance(timestamp, str):
        try:
            datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            errors.append("Invalid evidence timestamp")

    elif timestamp is not None and not isinstance(timestamp, str):
        errors.append("Timestamp must be a string")

    # 3. Validate evidence source.
    source = evidence.get("source")

    if source is not None and not isinstance(source, str):
        errors.append("Evidence source must be a string")

    # 4. Final validation result.
    valid = not missing_fields and not errors

    return {
        "valid": valid,
        "missing_fields": missing_fields,
        "errors": errors,
    }
