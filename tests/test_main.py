import unittest

from backend.main import validate_finding


class TestTervaValidation(unittest.TestCase):

    def test_valid_finding(self):
        finding = {
            "title": "Possible SQL Injection",
            "source": "Sample Security Scanner",
            "asset": "Local Training Application",
            "description": "Possible SQL injection detected."
        }

        result = validate_finding(finding)

        self.assertTrue(result["valid"])
        self.assertEqual(result["missing_fields"], [])

    def test_missing_description(self):
        finding = {
            "title": "Possible SQL Injection",
            "source": "Sample Security Scanner",
            "asset": "Local Training Application"
        }

        result = validate_finding(finding)

        self.assertFalse(result["valid"])
        self.assertEqual(result["missing_fields"], ["description"])


if __name__ == "__main__":
    unittest.main()