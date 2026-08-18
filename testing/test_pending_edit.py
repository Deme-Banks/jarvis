"""Pending self-edit confirm, no LLM required."""
import unittest
from pathlib import Path

from ai_coding.self_editor import PROJECT_ROOT, PendingEdit, is_cancel, is_confirm


class TestConfirmWords(unittest.TestCase):
    def test_yes(self):
        self.assertTrue(is_confirm("apply"))
        self.assertTrue(is_confirm("yes"))
        self.assertTrue(is_cancel("cancel"))


class TestPendingWrite(unittest.TestCase):
    def test_commit_writes_then_stays_in_repo(self):
        target = PROJECT_ROOT / "data" / "_pending_test.txt"
        target.parent.mkdir(parents=True, exist_ok=True)
        pending = PendingEdit(
            action="write",
            rel="data/_pending_test.txt",
            target=target,
            old="",
            new="hello from pending edit\n",
            summary="test",
        )
        msg = pending.commit()
        self.assertIn("Applied", msg)
        self.assertEqual(target.read_text(encoding="utf-8"), "hello from pending edit\n")
        target.unlink(missing_ok=True)
