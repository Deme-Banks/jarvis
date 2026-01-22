"""
Voice Enhancement Features
"""
import os
import re
from typing import Dict, List, Optional
from collections import deque


class VoiceEnhancements:
    """Enhanced voice features"""
    
    def __init__(self):
        self.command_suggestions = deque(maxlen=100)
        self.context_history = deque(maxlen=20)
    
    def suggest_commands(self, partial_command: str, context: List[str] = None) -> List[str]:
        """Suggest commands based on partial input"""
        suggestions = []
        partial_lower = partial_command.lower()
        
        # Common command patterns
        patterns = {
            'create': ['create a keylogger', 'create a reverse shell', 'create malware'],
            'generate': ['generate code', 'generate malware', 'generate report'],
            'analyze': ['analyze code', 'analyze network', 'analyze file'],
            'test': ['test connection', 'test malware', 'test network'],
            'build': ['build code', 'build malware', 'build project'],
            'scan': ['scan network', 'scan ports', 'scan files'],
            'deploy': ['deploy to USB', 'deploy malware', 'deploy payload']
        }
        
        # Find matching patterns
        for pattern, commands in patterns.items():
            if pattern in partial_lower:
                for cmd in commands:
                    if partial_lower in cmd.lower():
                        suggestions.append(cmd)
        
        # Add context-based suggestions
        if context:
            for ctx in context[-3:]:  # Last 3 commands
                if ctx.lower() not in [s.lower() for s in suggestions]:
                    suggestions.append(ctx)
        
        return suggestions[:5]  # Return top 5
    
    def detect_intent(self, command: str) -> Dict:
        """Detect user intent from command"""
        command_lower = command.lower()
        
        intent = {
            'action': None,
            'target': None,
            'parameters': {},
            'confidence': 0.0
        }
        
        # Action detection
        actions = {
            'create': ['create', 'make', 'generate', 'build'],
            'analyze': ['analyze', 'read', 'review', 'examine'],
            'test': ['test', 'run', 'execute', 'try'],
            'deploy': ['deploy', 'install', 'copy', 'send'],
            'scan': ['scan', 'check', 'inspect', 'probe']
        }
        
        for action, keywords in actions.items():
            if any(kw in command_lower for kw in keywords):
                intent['action'] = action
                intent['confidence'] += 0.3
                break
        
        # Target detection
        targets = {
            'malware': ['keylogger', 'trojan', 'virus', 'rat', 'malware', 'payload'],
            'code': ['code', 'script', 'program', 'function', 'class'],
            'network': ['network', 'port', 'ip', 'connection'],
            'file': ['file', 'document', 'apk', 'ipa', 'exe']
        }
        
        for target, keywords in targets.items():
            if any(kw in command_lower for kw in keywords):
                intent['target'] = target
                intent['confidence'] += 0.3
                break
        
        # Parameter extraction
        import re
        ip_match = re.search(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', command)
        if ip_match:
            intent['parameters']['ip'] = ip_match.group(1)
            intent['confidence'] += 0.2
        
        port_match = re.search(r'port\s+(\d+)', command_lower)
        if port_match:
            intent['parameters']['port'] = int(port_match.group(1))
            intent['confidence'] += 0.2
        
        return intent
    
    def get_contextual_help(self, command: str) -> str:
        """Get contextual help for command"""
        intent = self.detect_intent(command)
        
        help_texts = {
            'create': {
                'malware': 'To create malware, specify type: "create a keylogger" or "create a reverse shell"',
                'code': 'To create code, describe what you need: "create code for a calculator"',
                'default': 'Specify what to create: malware, code, or other'
            },
            'analyze': {
                'code': 'To analyze code, provide file path: "analyze code in script.py"',
                'network': 'To analyze network, specify target: "analyze network 192.168.1.0/24"',
                'default': 'Specify what to analyze: code, network, or file'
            },
            'test': {
                'default': 'Specify what to test: "test connection to 192.168.1.1" or "test malware"'
            }
        }
        
        action = intent.get('action')
        target = intent.get('target')
        
        if action and action in help_texts:
            if target and target in help_texts[action]:
                return help_texts[action][target]
            elif 'default' in help_texts[action]:
                return help_texts[action]['default']
        
        return "I can help with creating malware, analyzing code, testing networks, and more. Be more specific about what you need."
    
    def learn_from_feedback(self, command: str, success: bool, response: str):
        """Learn from user feedback"""
        self.command_suggestions.append({
            'command': command,
            'success': success,
            'response': response[:100]  # Truncate
        })
    
    def get_smart_suggestions(self, current_time: str = None, recent_commands: List[str] = None) -> List[str]:
        """Get smart command suggestions based on context"""
        suggestions = []
        
        # Time-based suggestions
        if current_time:
            hour = int(current_time.split(':')[0]) if ':' in current_time else 12
            if 9 <= hour <= 17:
                suggestions.append("What would you like to work on today?")
            elif hour >= 18:
                suggestions.append("Ready for some security testing?")
        
        # Context-based suggestions
        if recent_commands:
            last_cmd = recent_commands[-1].lower() if recent_commands else ""
            
            if 'create' in last_cmd:
                suggestions.append("Would you like to deploy what you created?")
            elif 'analyze' in last_cmd:
                suggestions.append("Want to test what you analyzed?")
            elif 'test' in last_cmd:
                suggestions.append("Ready to create something new?")
        
        # Default suggestions
        if not suggestions:
            suggestions = [
                "Create a keylogger",
                "Analyze network security",
                "Generate some code",
                "Test malware in isolated environment"
            ]
        
        return suggestions[:3]
