"""Tests for shared core (no live Ollama required)."""
import unittest
from unittest.mock import MagicMock

from optimization.precomputed import get_precomputed
from ai_coding.code_brain import is_coding_request
from core.models import catalog_text, resolve_alias, switch_runtime


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


class TestLocalModelCatalog(unittest.TestCase):
    def test_catalog_text_marks_installed(self):
        text = catalog_text(installed=["qwen2.5-coder:7b"])
        self.assertTrue(
            "I am JARVIS" in text or "Open-weight models we can run locally" in text
        )
        coder = next(line for line in text.splitlines() if "qwen2.5-coder:7b" in line)
        qwen3 = next(line for line in text.splitlines() if "qwen3:8b" in line)
        self.assertTrue("[ready]" in coder or "[installed]" in coder)
        self.assertIn("[not pulled]", qwen3)
        self.assertIn("use qwen3", text)

    def test_resolve_alias(self):
        self.assertEqual(resolve_alias("use qwen3"), "qwen3:8b")
        self.assertEqual(resolve_alias("use deepseek"), "deepseek-r1:8b")
        self.assertEqual(resolve_alias("use mistral"), "mistral:7b")
        self.assertEqual(resolve_alias("use coder"), "qwen2.5-coder:7b")
        self.assertEqual(resolve_alias("use glm4"), "glm4:9b")
        self.assertIsNone(resolve_alias("hello there"))

    def test_switch_runtime_uses_list_models(self):
        import config_pi as config

        llm = MagicMock()
        llm.list_models.return_value = ["qwen2.5-coder:7b", "qwen3:8b"]
        llm.model_name = "qwen2.5-coder:7b"
        llm.context = [{"role": "user", "content": "hi"}]
        previous = config.PiConfig.LOCAL_MODEL_NAME
        try:
            msg = switch_runtime(llm, "qwen3:8b")
            self.assertEqual(llm.model_name, "qwen3:8b")
            self.assertEqual(llm.context, [])
            self.assertIn("qwen3:8b", msg)
            missing = switch_runtime(llm, "mistral:7b")
            self.assertIn("not installed", missing)
            self.assertIn("ollama pull mistral:7b", missing)
        finally:
            config.PiConfig.LOCAL_MODEL_NAME = previous


if __name__ == "__main__":
    unittest.main()
