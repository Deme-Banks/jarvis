"""
Pre-computed replies for short, exact-ish greetings only.

Substring matching is avoided so "hi" does not fire inside "this".
"""
from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional


class PrecomputedResponses:
    def __init__(self):
        self.responses = self._load_responses()

    def _load_responses(self) -> Dict[str, str]:
        return {
            "greeting": "Hello. I'm JARVIS. I can talk, write code, and edit files in this project when you ask.",
            "goodbye": "Goodbye. Call if you need me.",
            "thanks": "You're welcome.",
            "what can you do": "I can talk, write code, check this PC, search the web, open apps, take screenshots, and take notes. Say Jarvis, then the command.",
            "help": "Try: what time is it, system status, screenshot, open notepad, search Python, or write a function.",
            "status": "All systems operational. Ready for commands.",
            "who are you": "J.A.R.V.I.S. — Just A Rather Very Intelligent System. Online, and at your service.",
            "capabilities": "Chat, coding, system status, weather, web search, allowlisted apps, screenshots, notes, and voice.",
            "time": self._get_time_response(),
            "who are you": "J.A.R.V.I.S. — Just A Rather Very Intelligent System. Online, and at your service.",
            "capabilities": "Chat, coding, system status, weather, web search, allowlisted apps, screenshots, notes, and voice.",
            "learning": "I keep recent conversation context in this session. For code, name the file you want explained.",
        }

    def _get_time_response(self) -> str:
        now = datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')} on {now.strftime('%B %d, %Y')}."

    def get(self, query: str) -> Optional[str]:
        query_lower = query.lower().strip().rstrip("!?.,")
        if query_lower in self.responses:
            return self.responses[query_lower]

        exact = {
            "hello": "greeting",
            "hi": "greeting",
            "hey": "greeting",
            "hi jarvis": "greeting",
            "hello jarvis": "greeting",
            "bye": "goodbye",
            "goodbye": "goodbye",
            "thanks": "thanks",
            "thank you": "thanks",
            "help": "help",
            "what time is it": "time",
            "what time": "time",
            "who are you": "who are you",
            "what can you do": "what can you do",
        }
        if query_lower in exact:
            key = exact[query_lower]
            if key == "time":
                return self._get_time_response()
            return self.responses.get(key)
        return None


_precomputed = PrecomputedResponses()


def get_precomputed(query: str) -> Optional[str]:
    return _precomputed.get(query)
