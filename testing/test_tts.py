"""Spoken-form cleanup for Jarvis TTS (no network)."""
import unittest

from voice.tts_pi import spoken_form


class TestSpokenForm(unittest.TestCase):
    def test_strips_code_fences(self):
        text = "Here you go.\n```python\nprint(1)\n```\nDone."
        spoken = spoken_form(text)
        self.assertNotIn("print", spoken)
        self.assertIn("on screen", spoken)

    def test_strips_markdown(self):
        spoken = spoken_form("**Ready**, sir.")
        self.assertEqual(spoken, "Ready, sir.")

    def test_empty(self):
        self.assertEqual(spoken_form("   "), "")

    def test_truncates(self):
        spoken = spoken_form("word " * 200, limit=40)
        self.assertLessEqual(len(spoken), 42)


if __name__ == "__main__":
    unittest.main()
