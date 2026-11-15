
"""
TERVA - Threat Evidence & Risk Verification Architecture

Module: Engagement
Purpose: Define and validate an authorised security engagement.
"""

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class Engagement:
    engagement_id: str
    owner: str
    authorization_reference: str
    allowed_targets: list[str]
    permitted_actions: list[str]
    start_date: datetime
    expiry_date: datetime
    status: str = "PENDING"


def validate_engagement(engagement):
    """Validate engagement details and its active period."""

    required_fields = [
        "engagement_id",
        "owner",
        "authorization_reference",
        "allowed_targets",
        "permitted_actions",
        "start_date",
        "expiry_date"
    ]

    missing_fields = []

    for field in required_fields:
        value = getattr(engagement, field, None)

        if value is None or value == "":
            missing_fields.append(field)

    if missing_fields:
        return {
            "valid": False,
            "reason": "Missing required fields",
            "missing_fields": missing_fields
        }

    if not isinstance(engagement.start_date, datetime):
        return {
            "valid": False,
            "reason": "Invalid start date",
            "missing_fields": []
        }

    if not isinstance(engagement.expiry_date, datetime):
        return {
            "valid": False,
            "reason": "Invalid expiry date",
            "missing_fields": []
        }

    if not engagement.allowed_targets:
        return {
            "valid": False,
            "reason": "No allowed targets configured",
            "missing_fields": []
        }

    if not engagement.permitted_actions:
        return {
            "valid": False,
            "reason": "No permitted actions configured",
            "missing_fields": []
        }

    if engagement.start_date.tzinfo is None:
        return {
            "valid": False,
            "reason": "Start date must include timezone",
            "missing_fields": []
        }

    if engagement.expiry_date.tzinfo is None:
        return {
            "valid": False,
            "reason": "Expiry date must include timezone",
            "missing_fields": []
        }

    if engagement.expiry_date <= engagement.start_date:
        return {
            "valid": False,
            "reason": "Expiry date must be after start date",
            "missing_fields": []
        }

    now = datetime.now(timezone.utc)

    if engagement.start_date > now:
        return {
            "valid": False,
            "reason": "Engagement has not started",
            "missing_fields": []
        }

    if engagement.expiry_date <= now:
        return {
            "valid": False,
            "reason": "Engagement has expired",
            "missing_fields": []
        }

    if engagement.status != "ACTIVE":
        return {
            "valid": False,
            "reason": "Engagement is not active",
            "missing_fields": []
        }

    return {
        "valid": True,
        "reason": "Engagement is currently valid",
        "missing_fields": []
    }
