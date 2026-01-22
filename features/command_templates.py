"""
Command Templates - Pre-filled command structures
"""
import json
import os
from typing import Dict, List, Optional


class CommandTemplates:
    """Command templates for common tasks"""
    
    def __init__(self, templates_file: str = "config/templates.json"):
        self.templates_file = templates_file
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Load templates from file"""
        default_templates = {
            "create_keylogger": {
                "template": "create keylogger for {os} with {persistence} persistence and {obfuscation} obfuscation",
                "params": ["os", "persistence", "obfuscation"],
                "defaults": {"os": "windows", "persistence": "startup", "obfuscation": "base64"}
            },
            "network_scan": {
                "template": "scan network {target} with {scan_type} scan",
                "params": ["target", "scan_type"],
                "defaults": {"target": "192.168.1.0/24", "scan_type": "tcp"}
            },
            "create_malware": {
                "template": "create {malware_type} with {features}",
                "params": ["malware_type", "features"],
                "defaults": {"malware_type": "keylogger", "features": "persistence"}
            },
            "deploy_payload": {
                "template": "deploy {payload_type} to usb {drive}",
                "params": ["payload_type", "drive"],
                "defaults": {"payload_type": "keylogger", "drive": "auto"}
            }
        }
        
        if os.path.exists(self.templates_file):
            try:
                with open(self.templates_file, 'r') as f:
                    custom_templates = json.load(f)
                    default_templates.update(custom_templates)
            except:
                pass
        
        return default_templates
    
    def get_template(self, template_name: str) -> Optional[Dict]:
        """Get template by name"""
        return self.templates.get(template_name)
    
    def fill_template(self, template_name: str, **kwargs) -> str:
        """Fill template with values"""
        template = self.get_template(template_name)
        if not template:
            return f"Template '{template_name}' not found."
        
        # Merge defaults with provided values
        params = {**template.get("defaults", {}), **kwargs}
        
        # Fill template
        try:
            return template["template"].format(**params)
        except KeyError as e:
            return f"Missing parameter: {e}"
    
    def create_template(self, name: str, template: str, 
                       params: List[str], defaults: Dict) -> str:
        """Create a new template"""
        self.templates[name] = {
            "template": template,
            "params": params,
            "defaults": defaults
        }
        
        os.makedirs(os.path.dirname(self.templates_file), exist_ok=True)
        with open(self.templates_file, 'w') as f:
            json.dump(self.templates, f, indent=2)
        
        return f"Template '{name}' created successfully."
