"""Jarvis identity: canon plus living memory (no live Ollama)."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import core.identity as identity


class TestIdentity(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "identity.json"
        self.patcher = patch.object(identity, "IDENTITY_PATH", self.path)
        self.patcher.start()

    def tearDown(self) -> None:
        self.patcher.stop()
        self.tmp.cleanup()

    def test_who_am_i_is_jarvis(self):
        text = identity.who_am_i()
        self.assertIn("J.A.R.V.I.S", text)
        self.assertNotIn("language model", text.lower())

    def test_learns_name(self):
        reply = identity.handle_turn("my name is Deme")
        self.assertIsNotNone(reply)
        self.assertIn("Deme", reply or "")
        self.assertIn("Deme", identity.who_am_i())
        self.assertIn("Deme", identity.greeting())

    def test_remember_and_recall(self):
        identity.handle_turn("remember I work nights")
        about = identity.handle_turn("what do you know about me")
        self.assertIn("nights", about or "")

    def test_forget(self):
        identity.handle_turn("remember I like espresso")
        identity.handle_turn("forget espresso")
        about = identity.about_user()
        self.assertNotIn("espresso", about)

    def test_live_prompt_includes_canon_and_memory(self):
        identity.handle_turn("call me Banks")
        prompt = identity.live_prompt()
        self.assertIn("one intelligence", prompt)
        self.assertIn("Banks", prompt)
        self.assertIn("LIVING MEMORY", prompt)

    def test_hello_stays_in_character(self):
        text = identity.canned_reply("hello")
        self.assertIn("JARVIS", text or "")


if __name__ == "__main__":
    unittest.main()
