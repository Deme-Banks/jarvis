"""Unit tests for coding detection and self-edit safety (no LLM required)."""
import unittest

from ai_coding.code_brain import is_coding_request
from ai_coding.self_editor import PROJECT_ROOT, _is_allowed, is_edit_request


class TestCodingDetection(unittest.TestCase):
    def test_plain_chat_is_not_coding(self):
        self.assertFalse(is_coding_request("what time is it"))

    def test_write_function_is_coding(self):
        self.assertTrue(is_coding_request("write a python function that adds two numbers"))

    def test_explain_file_is_coding(self):
        self.assertTrue(is_coding_request("explain run_jarvis.py"))

    def test_traceback_is_coding(self):
        self.assertTrue(is_coding_request("debug this TypeError in my script"))

    def test_edit_hints(self):
        self.assertTrue(is_edit_request("edit your code and add a comment"))
        self.assertTrue(is_coding_request("change jarvis to greet me"))


class TestSelfEditSafety(unittest.TestCase):
    def test_env_blocked(self):
        ok, reason = _is_allowed(PROJECT_ROOT / ".env")
        self.assertFalse(ok)
        self.assertTrue(reason)

    def test_venv_blocked(self):
        ok, _ = _is_allowed(PROJECT_ROOT / "venv" / "lib" / "fake.py")
        self.assertFalse(ok)

    def test_python_source_allowed(self):
        ok, reason = _is_allowed(PROJECT_ROOT / "run_jarvis.py")
        self.assertTrue(ok, reason)


if __name__ == "__main__":
    unittest.main()
