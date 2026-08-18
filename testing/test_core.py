"""Tests for shared core (no live Ollama required)."""
import unittest

from optimization.precomputed import get_precomputed
from ai_coding.code_brain import is_coding_request


class TestPrecomputed(unittest.TestCase):
    def test_hello_is_greeting(self):
        text = get_precomputed("hello")
        self.assertIsNotNone(text)
        self.assertIn("JARVIS", text)

    def test_this_is_not_a_greeting(self):
        self.assertIsNone(get_precomputed("explain this later"))

    def test_hi_inside_this_does_not_match(self):
        self.assertIsNone(get_precomputed("this"))


class TestCodingStillSeparate(unittest.TestCase):
    def test_write_function_is_coding(self):
        self.assertTrue(is_coding_request("write a python function"))


if __name__ == "__main__":
    unittest.main()
