
"""
TERVA - Threat Evidence & Risk Verification Architecture

Module: Permission Controller
Purpose: Evaluate requests and automatically record decisions.
"""

from backend.security.engagement import validate_engagement
from backend.security.scope_manager import is_target_in_scope
from backend.audit.audit_logger import record_event


SAFE_AUTOMATIC_ACTIONS = {
    "metadata_review",
    "passive_analysis",
    "report_generation",
}


def _finish_decision(engagement, target, action, decision, reason):
    """Record a decision before returning it."""

    engagement_id = getattr(
        engagement, "engagement_id", "UNKNOWN"
    )

    try:
        record_event(
            engagement_id=str(engagement_id),
            target=str(target),
            action=str(action),
            decision=decision,
            reason=reason,
        )

    except Exception:
        # Fail closed: never allow an operation if its
        # audit record cannot be written.
        return {
            "decision": "DENY",
            "reason": "Audit logging failed; request denied",
            "audit_recorded": False,
        }

    return {
        "decision": decision,
        "reason": reason,
        "audit_recorded": True,
    }


def evaluate_request(engagement, target, action):
    """
    Evaluate a security request.

    This function checks permissions and records the result.
    It does not execute security operations.
    """

    # 1. Validate the engagement.
    validation = validate_engagement(engagement)

    if not validation["valid"]:
        return _finish_decision(
            engagement,
            target,
            action,
            "DENY",
            validation["reason"],
        )

    # 2. Check target scope.
    if not is_target_in_scope(target, engagement.allowed_targets):
        return _finish_decision(
            engagement,
            target,
            action,
            "DENY",
            "Target is outside the approved scope",
        )

    # 3. Validate action format.
    if not isinstance(action, str) or not action.strip():
        return _finish_decision(
            engagement,
            target,
            action,
            "DENY",
            "Invalid action",
        )

    action = action.strip()

    # 4. Check engagement permissions.
    if action not in engagement.permitted_actions:
        return _finish_decision(
            engagement,
            target,
            action,
            "DENY",
            "Action is not permitted by the engagement",
        )

    # 5. Check automatic execution policy.
    if action not in SAFE_AUTOMATIC_ACTIONS:
        return _finish_decision(
            engagement,
            target,
            action,
            "DENY",
            "Action is not enabled for automatic execution",
        )

    # 6. All checks passed.
    return _finish_decision(
        engagement,
        target,
        action,
        "ALLOW",
        "Target and action passed all permission checks",
    )
