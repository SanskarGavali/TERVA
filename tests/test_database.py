
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from backend.evidence.collector import collect_evidence
from backend.evidence import evidence_store


class TestEvidenceDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_directory.name) / "test_evidence.db"

        self.database_patch = patch.object(
            evidence_store,
            "DATABASE_FILE",
            self.database_path,
        )
        self.database_patch.start()

        evidence_store.initialize_store()

    def tearDown(self):
        self.database_patch.stop()
        self.temp_directory.cleanup()

    def create_sample_evidence(self):
        result = collect_evidence(
            "Possible SQL Injection",
            "Sample Scanner",
            "Local Training App",
            "Sample security finding",
        )
        return result["evidence"]

    def test_save_valid_evidence(self):
        evidence = self.create_sample_evidence()

        result = evidence_store.save_evidence(evidence)

        self.assertTrue(result["success"])
        self.assertEqual(result["evidence_id"], evidence["id"])

    def test_retrieve_saved_evidence(self):
        evidence = self.create_sample_evidence()
        evidence_store.save_evidence(evidence)

        retrieved = evidence_store.get_evidence(evidence["id"])

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["id"], evidence["id"])
        self.assertEqual(retrieved["title"], evidence["title"])

    def test_duplicate_evidence_id_is_rejected(self):
        evidence = self.create_sample_evidence()

        first_result = evidence_store.save_evidence(evidence)
        second_result = evidence_store.save_evidence(evidence)

        self.assertTrue(first_result["success"])
        self.assertFalse(second_result["success"])
        self.assertEqual(
            second_result["reason"],
            "Evidence ID already exists",
        )

    def test_invalid_evidence_is_rejected(self):
        invalid_evidence = {
            "id": "TERVA-EVD-INVALID",
            "title": "",
            "source": "Sample Scanner",
            "asset": "Local Training App",
            "description": "Sample finding",
            "collected_at": "2026-11-15T05:00:00+00:00",
        }

        result = evidence_store.save_evidence(invalid_evidence)

        self.assertFalse(result["success"])
        self.assertEqual(
            result["reason"],
            "Evidence validation failed",
        )

    def test_list_all_evidence(self):
        first = self.create_sample_evidence()
        second = self.create_sample_evidence()

        evidence_store.save_evidence(first)
        evidence_store.save_evidence(second)

        records = evidence_store.list_evidence()

        self.assertEqual(len(records), 2)

    def test_missing_evidence_returns_none(self):
        result = evidence_store.get_evidence("TERVA-EVD-NOTFOUND")

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
