"""
Quick Actions for Common Tasks
"""
from typing import Dict, List, Optional
from datetime import datetime
import os


class QuickActions:
    """Quick action shortcuts"""
    
    def __init__(self):
        self.actions = self._load_actions()
    
    def _load_actions(self) -> Dict:
        """Load quick actions"""
        return {
            'security_check': {
                'name': 'Security Check',
                'commands': [
                    'scan network 192.168.1.0/24',
                    'check system health',
                    'analyze recent logs'
                ]
            },
            'daily_setup': {
                'name': 'Daily Setup',
                'commands': [
                    'check system status',
                    'show recent commands',
                    'get recommendations'
                ]
            },
            'malware_test': {
                'name': 'Malware Test',
                'commands': [
                    'create a keylogger',
                    'test on localhost',
                    'generate report'
                ]
            },
            'code_session': {
                'name': 'Code Session',
                'commands': [
                    'generate code for calculator',
                    'analyze code',
                    'build and test'
                ]
            }
        }
    
    def execute_action(self, action_name: str) -> Dict:
        """Execute a quick action"""
        if action_name not in self.actions:
            return {
                'success': False,
                'error': f'Action {action_name} not found'
            }
        
        action = self.actions[action_name]
        return {
            'success': True,
            'name': action['name'],
            'commands': action['commands'],
            'message': f"Quick action '{action['name']}' ready. Commands: {', '.join(action['commands'])}"
        }
    
    def list_actions(self) -> List[Dict]:
        """List all quick actions"""
        return [
            {
                'name': name,
                'display_name': action['name'],
                'commands': action['commands']
            }
            for name, action in self.actions.items()
        ]
    
    def create_custom_action(self, name: str, display_name: str, commands: List[str]) -> bool:
        """Create custom quick action"""
        self.actions[name] = {
            'name': display_name,
            'commands': commands
        }
        return True
