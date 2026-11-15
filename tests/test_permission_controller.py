
import unittest
from datetime import datetime, timedelta, timezone

from backend.security.engagement import Engagement
from backend.security.permission_controller import evaluate_request


class TestPermissionController(unittest.TestCase):

    def create_engagement(self, **overrides):
        now = datetime.now(timezone.utc)

        data = {
            "engagement_id": "TERVA-ENG-001",
            "owner": "My Training Lab",
            "authorization_reference": "AUTH-001",
            "allowed_targets": ["example.com"],
            "permitted_actions": ["metadata_review"],
            "start_date": now - timedelta(hours=1),
            "expiry_date": now + timedelta(days=1),
            "status": "ACTIVE",
        }

        data.update(overrides)

        return Engagement(**data)

    def test_valid_request(self):
        engagement = self.create_engagement()

        result = evaluate_request(
            engagement, "example.com", "metadata_review"
        )

        self.assertEqual(result["decision"], "ALLOW")

    def test_out_of_scope_target(self):
        engagement = self.create_engagement()

        result = evaluate_request(
            engagement, "other-example.com", "metadata_review"
        )

        self.assertEqual(result["decision"], "DENY")

    def test_unpermitted_action(self):
        engagement = self.create_engagement()

        result = evaluate_request(
            engagement, "example.com", "network_scan"
        )

        self.assertEqual(result["decision"], "DENY")

    def test_expired_engagement(self):
        engagement = self.create_engagement(
            expiry_date=datetime.now(timezone.utc) - timedelta(days=1)
        )

        result = evaluate_request(
            engagement, "example.com", "metadata_review"
        )

        self.assertEqual(result["decision"], "DENY")

    def test_unsupported_automatic_action(self):
        engagement = self.create_engagement(
            permitted_actions=["exploit_validation"]
        )

        result = evaluate_request(
            engagement, "example.com", "exploit_validation"
        )

        self.assertEqual(result["decision"], "DENY")


if __name__ == "__main__":
    unittest.main()
