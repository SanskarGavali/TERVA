
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from backend.audit import audit_logger


class TestAuditLogger(unittest.TestCase):

    def test_record_event(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "audit_log.jsonl"

            with patch.object(audit_logger, "AUDIT_FILE", test_file):
                event = audit_logger.record_event(
                    "TERVA-ENG-001",
                    "example.com",
                    "metadata_review",
                    "ALLOW",
                    "Permission checks passed"
                )

                self.assertTrue(test_file.exists())

                with test_file.open(encoding="utf-8") as file:
                    saved_event = json.loads(file.readline())

                self.assertEqual(
                    saved_event["engagement_id"],
                    "TERVA-ENG-001"
                )

                self.assertEqual(saved_event["decision"], "ALLOW")
                self.assertIn("timestamp", event)

    def test_multiple_events_are_appended(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "audit_log.jsonl"

            with patch.object(audit_logger, "AUDIT_FILE", test_file):
                for decision in ["ALLOW", "DENY"]:
                    audit_logger.record_event(
                        "TERVA-ENG-001",
                        "example.com",
                        "metadata_review",
                        decision,
                        "Test event"
                    )

                with test_file.open(encoding="utf-8") as file:
                    records = file.readlines()

                self.assertEqual(len(records), 2)


if __name__ == "__main__":
    unittest.main()
