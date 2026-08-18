"""Skill routing tests (no screenshots / no app launches)."""
import unittest

from core.skills import try_skill


class TestSkills(unittest.TestCase):
    def test_time(self):
        reply = try_skill("what time is it")
        self.assertIsNotNone(reply)
        self.assertIn("It's", reply)

    def test_identity(self):
        reply = try_skill("who are you")
        self.assertIn("J.A.R.V.I.S", reply)

    def test_stand_down(self):
        self.assertIn("Standing by", try_skill("stand down"))

    def test_coding_is_not_a_skill(self):
        self.assertIsNone(try_skill("write a python function that adds two numbers"))

    def test_helpful_is_not_help(self):
        self.assertIsNone(try_skill("write a helpful comment"))
