"""Jarvis crew: one voice, specialist models backstage (no live Ollama)."""
import unittest
from unittest.mock import MagicMock

from core.crew import (
    JarvisCrew,
    classify,
    pick_role,
    strip_think,
)


class TestClassify(unittest.TestCase):
    def test_chat_stays_with_jarvis(self):
        self.assertIsNone(classify("what time is the meeting"))

    def test_code_goes_to_coder(self):
        self.assertEqual(classify("write a python function"), "coder")

    def test_math_goes_to_reasoner(self):
        self.assertEqual(classify("calculate the probability step by step"), "reasoner")


class TestStripThink(unittest.TestCase):
    def test_drops_r1_scratchpad(self):
        raw = "<think>secret scratch</think>\nAnswer: 42"
        self.assertEqual(strip_think(raw), "Answer: 42")


class TestPickRole(unittest.TestCase):
    def test_coder_prefers_7b(self):
        installed = ["llama3.2:latest", "qwen2.5-coder:7b", "qwen2.5-coder:3b"]
        self.assertEqual(pick_role("coder", installed), "qwen2.5-coder:7b")

    def test_reasoner_offline_when_missing(self):
        self.assertIsNone(pick_role("reasoner", ["qwen2.5-coder:7b"]))


class TestCrewReply(unittest.TestCase):
    def test_chat_uses_conductor_only(self):
        llm = MagicMock()
        llm.list_models.return_value = ["qwen2.5-coder:7b"]
        llm.model_name = "qwen2.5-coder:7b"
        llm.complete.return_value = "Of course, sir."
        crew = JarvisCrew(llm)
        reply = crew.reply("how are you")
        self.assertEqual(reply, "Of course, sir.")
        self.assertEqual(llm.complete.call_count, 1)
        kwargs = llm.complete.call_args.kwargs
        self.assertEqual(kwargs["model"], "qwen2.5-coder:7b")
        self.assertIn("J.A.R.V.I.S", kwargs["system_prompt"])

    def test_reasoner_then_jarvis_when_both_installed(self):
        llm = MagicMock()
        llm.list_models.return_value = ["qwen2.5-coder:7b", "deepseek-r1:8b"]
        llm.model_name = "qwen2.5-coder:7b"
        llm.complete.side_effect = [
            "<think>scratch</think>\nThe answer is 4.",
            "Four, sir.",
        ]
        crew = JarvisCrew(llm)
        reply = crew.reply("calculate 2 plus 2")
        self.assertEqual(reply, "Four, sir.")
        self.assertEqual(llm.complete.call_count, 2)
        first = llm.complete.call_args_list[0]
        second = llm.complete.call_args_list[1]
        self.assertEqual(first.kwargs["model"], "deepseek-r1:8b")
        self.assertEqual(second.kwargs["model"], "qwen2.5-coder:7b")

    def test_roster_says_jarvis_is_the_voice(self):
        llm = MagicMock()
        llm.list_models.return_value = ["qwen2.5-coder:7b"]
        llm.model_name = "qwen2.5-coder:7b"
        text = JarvisCrew(llm).roster_text()
        self.assertIn("I am JARVIS", text)
        self.assertIn("not separate assistants", text)
        self.assertIn("coder", text.lower())

    def test_prefer_switches_conductor(self):
        llm = MagicMock()
        llm.list_models.return_value = ["qwen2.5-coder:7b", "qwen3:8b"]
        llm.model_name = "qwen2.5-coder:7b"
        llm.context = []
        crew = JarvisCrew(llm)
        msg = crew.prefer("qwen3:8b")
        self.assertEqual(llm.model_name, "qwen3:8b")
        self.assertEqual(crew.preferred_conductor, "qwen3:8b")
        self.assertIn("qwen3:8b", msg)
        missing = crew.prefer("mistral:7b")
        self.assertIn("not installed", missing)


if __name__ == "__main__":
    unittest.main()
