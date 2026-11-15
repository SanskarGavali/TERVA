
import unittest

from backend.evidence.collector import collect_evidence


class TestEvidenceCollector(unittest.TestCase):

    def test_valid_evidence_is_collected(self):
        result = collect_evidence(
            "Possible SQL Injection",
            "Sample Scanner",
            "Local Training App",
            "Sample security finding",
        )

        self.assertTrue(result["success"])
        self.assertTrue(result["validation"]["valid"])
        self.assertIsNotNone(result["evidence"])

    def test_missing_title_is_rejected(self):
        result = collect_evidence(
            "",
            "Sample Scanner",
            "Local Training App",
            "Sample security finding",
        )

        self.assertFalse(result["success"])
        self.assertIn("title", result["validation"]["missing_fields"])

    def test_invalid_source_type_is_rejected(self):
        result = collect_evidence(
            "Possible SQL Injection",
            123,
            "Local Training App",
            "Sample security finding",
        )

        self.assertFalse(result["success"])
        self.assertIn(
            "Evidence source must be a string",
            result["validation"]["errors"],
        )

    def test_evidence_ids_are_unique(self):
        first = collect_evidence(
            "Finding One", "Scanner", "Local App", "Description One"
        )
        second = collect_evidence(
            "Finding Two", "Scanner", "Local App", "Description Two"
        )

        first_id = first["evidence"]["id"]
        second_id = second["evidence"]["id"]

        self.assertNotEqual(first_id, second_id)
        self.assertTrue(first_id.startswith("TERVA-EVD-"))
        self.assertTrue(second_id.startswith("TERVA-EVD-"))


if __name__ == "__main__":
    unittest.main()
