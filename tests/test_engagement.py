
import unittest
from datetime import datetime, timedelta, timezone

from backend.security.engagement import (
    Engagement,
    validate_engagement
)


class TestEngagementValidation(unittest.TestCase):

    def create_engagement(self, **overrides):
        now = datetime.now(timezone.utc)

        data = {
            "engagement_id": "TERVA-ENG-001",
            "owner": "Training Lab",
            "authorization_reference": "AUTH-001",
            "allowed_targets": ["192.168.1.10"],
            "permitted_actions": ["metadata_review"],
            "start_date": now - timedelta(hours=1),
            "expiry_date": now + timedelta(days=1),
            "status": "ACTIVE"
        }

        data.update(overrides)

        return Engagement(**data)

    def test_valid_active_engagement(self):
        engagement = self.create_engagement()
        result = validate_engagement(engagement)

        self.assertTrue(result["valid"])

    def test_missing_authorization(self):
        engagement = self.create_engagement(
            authorization_reference=""
        )
        result = validate_engagement(engagement)

        self.assertFalse(result["valid"])

    def test_empty_allowed_targets(self):
        engagement = self.create_engagement(
            allowed_targets=[]
        )
        result = validate_engagement(engagement)

        self.assertFalse(result["valid"])

    def test_expired_engagement(self):
        engagement = self.create_engagement(
            expiry_date=datetime.now(timezone.utc) - timedelta(days=1)
        )
        result = validate_engagement(engagement)

        self.assertFalse(result["valid"])

    def test_pending_engagement(self):
        engagement = self.create_engagement(status="PENDING")
        result = validate_engagement(engagement)

        self.assertFalse(result["valid"])


if __name__ == "__main__":
    unittest.main()
