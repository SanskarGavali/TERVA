
"""
TERVA - Threat Evidence & Risk Verification Architecture

Module: Audit Logger
Purpose: Record permission decisions for future review.
"""

import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUDIT_FILE = PROJECT_ROOT / "backend" / "data" / "audit_log.jsonl"


def record_event(engagement_id, target, action, decision, reason):
    """Record one security decision in an audit log."""

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engagement_id": engagement_id,
        "target": target,
        "action": action,
        "decision": decision,
        "reason": reason,
    }

    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with AUDIT_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event) + "\n")

    return event
