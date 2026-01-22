"""
Advanced Voice Command Processing
"""
import re
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


class AdvancedVoiceCommands:
    """Advanced voice command processing"""
    
    def __init__(self):
        self.command_patterns = self._load_patterns()
        self.context_stack = []
    
    def _load_patterns(self) -> Dict:
        """Load command patterns"""
        return {
            'create': [
                r'create\s+(?:a\s+)?(\w+)',
                r'make\s+(?:a\s+)?(\w+)',
                r'generate\s+(?:a\s+)?(\w+)',
                r'build\s+(?:a\s+)?(\w+)'
            ],
            'analyze': [
                r'analyze\s+(?:the\s+)?(\w+)',
                r'read\s+(?:the\s+)?(\w+)',
                r'review\s+(?:the\s+)?(\w+)',
                r'examine\s+(?:the\s+)?(\w+)'
            ],
            'test': [
                r'test\s+(?:the\s+)?(\w+)',
                r'run\s+(?:a\s+)?(\w+)',
                r'execute\s+(?:the\s+)?(\w+)'
            ],
            'deploy': [
                r'deploy\s+(?:the\s+)?(\w+)',
                r'send\s+(?:the\s+)?(\w+)',
                r'install\s+(?:the\s+)?(\w+)'
            ]
        }
    
    def parse_command(self, command: str) -> Dict:
        """Parse command with advanced pattern matching"""
        command_lower = command.lower()
        
        parsed = {
            'action': None,
            'object': None,
            'parameters': {},
            'modifiers': [],
            'confidence': 0.0
        }
        
        # Match action patterns
        for action, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, command_lower)
                if match:
                    parsed['action'] = action
                    parsed['object'] = match.group(1)
                    parsed['confidence'] += 0.4
                    break
            if parsed['action']:
                break
        
        # Extract parameters
        # IP addresses
        ip_match = re.search(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', command)
        if ip_match:
            parsed['parameters']['ip'] = ip_match.group(1)
            parsed['confidence'] += 0.2
        
        # Ports
        port_match = re.search(r'port\s+(\d+)', command_lower)
        if port_match:
            parsed['parameters']['port'] = int(port_match.group(1))
            parsed['confidence'] += 0.1
        
        # URLs
        url_match = re.search(r'https?://[^\s]+', command)
        if url_match:
            parsed['parameters']['url'] = url_match.group()
            parsed['confidence'] += 0.1
        
        # File paths
        path_match = re.search(r'[A-Za-z]:\\[^\s]+|/[^\s]+|[\w\.-]+\.\w+', command)
        if path_match:
            parsed['parameters']['path'] = path_match.group()
            parsed['confidence'] += 0.1
        
        # Modifiers
        modifiers = {
            'obfuscated': 'obfuscation',
            'encrypted': 'encryption',
            'stealth': 'stealth',
            'persistent': 'persistence',
            'polymorphic': 'polymorphic'
        }
        
        for keyword, modifier in modifiers.items():
            if keyword in command_lower:
                parsed['modifiers'].append(modifier)
                parsed['confidence'] += 0.05
        
        return parsed
    
    def suggest_completion(self, partial_command: str, context: List[str] = None) -> List[str]:
        """Suggest command completion"""
        suggestions = []
        partial_lower = partial_command.lower()
        
        # Common completions
        if partial_lower.startswith('create'):
            suggestions.extend([
                'create a keylogger',
                'create a reverse shell',
                'create malware',
                'create code'
            ])
        elif partial_lower.startswith('analyze'):
            suggestions.extend([
                'analyze code',
                'analyze network',
                'analyze file'
            ])
        elif partial_lower.startswith('test'):
            suggestions.extend([
                'test connection',
                'test malware',
                'test network'
            ])
        
        # Filter by partial match
        suggestions = [s for s in suggestions if partial_lower in s.lower()]
        
        return suggestions[:5]
    
    def get_context_aware_response(self, command: str, recent_commands: List[str]) -> Optional[str]:
        """Get context-aware response"""
        if not recent_commands:
            return None
        
        # Check for follow-up questions
        command_lower = command.lower()
        
        if any(word in command_lower for word in ['what', 'how', 'why', 'when']):
            # This might be a follow-up
            last_command = recent_commands[-1].lower()
            
            if 'create' in last_command and 'keylogger' in last_command:
                if 'what' in command_lower:
                    return "A keylogger captures keystrokes. It's saved and ready to use."
            elif 'analyze' in last_command:
                if 'what' in command_lower:
                    return "The analysis is complete. Check the results above."
        
        return None
