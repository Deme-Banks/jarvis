"""
Example Plugin for JARVIS
"""
from plugins.plugin_system import Plugin
from typing import Dict, Optional


class ExamplePlugin(Plugin):
    """Example plugin that handles weather queries"""
    
    def get_name(self) -> str:
        return "Weather Plugin"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def handle_command(self, command: str, context: Dict) -> Optional[str]:
        """Handle weather-related commands"""
        command_lower = command.lower()
        
        if "weather" in command_lower:
            return "I don't have weather data configured, but I can help with cybersecurity testing!"
        
        return None
    
    def initialize(self):
        """Initialize plugin"""
        print("Weather Plugin initialized")
    
    def cleanup(self):
        """Cleanup plugin"""
        print("Weather Plugin cleaned up")
