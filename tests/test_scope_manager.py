
import unittest

from backend.security.scope_manager import is_target_in_scope


class TestScopeManager(unittest.TestCase):

    def test_allowed_target(self):
        allowed = ["192.168.1.10", "example.com"]

        result = is_target_in_scope("192.168.1.10", allowed)

        self.assertTrue(result)

    def test_disallowed_target(self):
        allowed = ["192.168.1.10"]

        result = is_target_in_scope("example.com", allowed)

        self.assertFalse(result)

    def test_empty_target(self):
        result = is_target_in_scope("", ["example.com"])

        self.assertFalse(result)

    def test_empty_allowlist(self):
        result = is_target_in_scope("example.com", [])

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
