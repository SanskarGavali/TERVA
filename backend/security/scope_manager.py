
"""
TERVA - Threat Evidence & Risk Verification Architecture

Module: Scope Manager
Purpose: Check whether a target is explicitly included
in an approved security engagement.
"""


def is_target_in_scope(target, allowed_targets):
    """
    Check whether a target is explicitly allowed.

    Returns True if the target is in the allowlist.
    Otherwise, returns False.
    """

    if not target or not allowed_targets:
        return False

    if not isinstance(target, str):
        return False

    if not isinstance(allowed_targets, list):
        return False

    target = target.strip()

    if not target:
        return False

    allowed_targets = [
        item.strip()
        for item in allowed_targets
        if isinstance(item, str)
    ]

    return target in allowed_targets
