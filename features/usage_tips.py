"""
Usage Tips System - Contextual help and tips
"""
import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class UsageTips:
    """Usage tips and contextual help"""
    
    def __init__(self, tips_file: str = "data/tips.json"):
        self.tips_file = tips_file
        self.tips = self._load_tips()
        self.shown_tips = set()
    
    def _load_tips(self) -> List[Dict]:
        """Load tips from file"""
        default_tips = [
            {
                "id": "voice_shortcuts",
                "title": "Voice Shortcuts",
                "content": "Use shortcuts like 'kl' for 'create keylogger' or 'scan' for 'scan network'",
                "category": "voice",
                "trigger": ["first_command", "voice"]
            },
            {
                "id": "templates",
                "title": "Command Templates",
                "content": "Use templates to quickly create common commands. Try 'use template create_keylogger'",
                "category": "commands",
                "trigger": ["create", "malware"]
            },
            {
                "id": "ai_coding",
                "title": "AI Coding",
                "content": "JARVIS can generate, read, and build code. Try 'generate Python function to sort list'",
                "category": "ai",
                "trigger": ["code", "program", "generate"]
            },
            {
                "id": "workflows",
                "title": "Workflows",
                "content": "Create multi-step workflows for complex tasks. Say 'create workflow' to get started",
                "category": "automation",
                "trigger": ["workflow", "automate"]
            },
            {
                "id": "integrations",
                "title": "Integrations",
                "content": "JARVIS integrates with GitHub, Jira, Calendar, and more. Configure in settings.",
                "category": "integrations",
                "trigger": ["github", "jira", "calendar"]
            }
        ]
        
        if os.path.exists(self.tips_file):
            try:
                with open(self.tips_file, 'r') as f:
                    custom_tips = json.load(f)
                    default_tips.extend(custom_tips)
            except:
                pass
        
        return default_tips
    
    def get_tip(self, context: str = None, category: str = None) -> Optional[Dict]:
        """Get a relevant tip based on context"""
        available_tips = [
            tip for tip in self.tips
            if tip["id"] not in self.shown_tips and
            (not category or tip["category"] == category) and
            (not context or any(trigger in context.lower() for trigger in tip.get("trigger", [])))
        ]
        
        if available_tips:
            tip = available_tips[0]
            self.shown_tips.add(tip["id"])
            return tip
        
        return None
    
    def get_all_tips(self, category: str = None) -> List[Dict]:
        """Get all tips, optionally filtered by category"""
        if category:
            return [tip for tip in self.tips if tip["category"] == category]
        return self.tips
    
    def mark_tip_shown(self, tip_id: str):
        """Mark a tip as shown"""
        self.shown_tips.add(tip_id)
