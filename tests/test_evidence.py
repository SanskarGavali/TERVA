
import unittest
from datetime import datetime, timezone

from backend.evidence.validator import validate_evidence


class TestEvidenceValidator(unittest.TestCase):

    def create_evidence(self, **overrides):
        evidence = {
            "title": "Possible SQL Injection",
            "source": "Sample Security Scanner",
            "asset": "Local Training Application",
            "description": "A scanner reported possible SQL injection.",
            "collected_at": datetime.now(timezone.utc).isoformat(),
        }

        evidence.update(overrides)
        return evidence

    def test_valid_evidence(self):
        result = validate_evidence(self.create_evidence())

        self.assertTrue(result["valid"])
        self.assertEqual(result["missing_fields"], [])
        self.assertEqual(result["errors"], [])

    def test_missing_description(self):
        evidence = self.create_evidence(description="")

        result = validate_evidence(evidence)

        self.assertFalse(result["valid"])
        self.assertIn("description", result["missing_fields"])

    def test_missing_timestamp(self):
        evidence = self.create_evidence(collected_at="")

        result = validate_evidence(evidence)

        self.assertFalse(result["valid"])
        self.assertIn("collected_at", result["missing_fields"])

    def test_invalid_timestamp(self):
        evidence = self.create_evidence(collected_at="not-a-date")

        result = validate_evidence(evidence)

        self.assertFalse(result["valid"])
        self.assertIn("Invalid evidence timestamp", result["errors"])

    def test_invalid_evidence_type(self):
        result = validate_evidence("invalid evidence")

        self.assertFalse(result["valid"])
        self.assertIn(
            "Evidence must be a dictionary",
            result["errors"]
        )

    def test_invalid_source_type(self):
        evidence = self.create_evidence(source=123)

        result = validate_evidence(evidence)

        self.assertFalse(result["valid"])
        self.assertIn(
            "Evidence source must be a string",
            result["errors"]
        )


if __name__ == "__main__":
    unittest.main()
