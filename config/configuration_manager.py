"""
Configuration Management System
"""
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigurationManager:
    """Manage JARVIS configuration"""
    
    def __init__(self, config_file: str = "./config/user_config.json"):
        self.config_file = config_file
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        self.config = self._load_config()
        self._apply_defaults()
    
    def _load_config(self) -> Dict:
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _apply_defaults(self):
        """Apply default configuration"""
        defaults = {
            'voice': {
                'wake_word': 'jarvis',
                'sensitivity': 0.5,
                'chunk_size': 256,
                'silence_threshold': 5
            },
            'llm': {
                'model': 'llama2',
                'temperature': 0.7,
                'max_tokens': 500
            },
            'features': {
                'enable_learning': True,
                'enable_analytics': True,
                'enable_plugins': True,
                'cache_enabled': True
            },
            'security': {
                'isolated_mode': True,
                'require_authorization': True
            }
        }
        
        for key, value in defaults.items():
            if key not in self.config:
                self.config[key] = value
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if sub_key not in self.config[key]:
                        self.config[key][sub_key] = sub_value
        
        self._save_config()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self._save_config()
    
    def reset(self):
        """Reset to defaults"""
        self.config = {}
        self._apply_defaults()
    
    def export(self, filepath: str):
        """Export configuration"""
        with open(filepath, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def import_config(self, filepath: str):
        """Import configuration"""
        with open(filepath, 'r') as f:
            imported = json.load(f)
        
        # Merge with existing
        self._merge_dict(self.config, imported)
        self._save_config()
    
    def _merge_dict(self, base: Dict, update: Dict):
        """Merge dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_dict(base[key], value)
            else:
                base[key] = value
