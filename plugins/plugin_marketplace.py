"""
Plugin Marketplace - Community plugins system
"""
import os
import json
import importlib
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class PluginMarketplace:
    """Plugin marketplace and management system"""
    
    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = plugins_dir
        self.plugins = {}
        self.marketplace_url = "https://plugins.jarvis.ai"  # Example
        os.makedirs(plugins_dir, exist_ok=True)
    
    def load_plugin(self, plugin_name: str) -> Dict:
        """Load a plugin"""
        plugin_path = os.path.join(self.plugins_dir, plugin_name)
        
        if not os.path.exists(plugin_path):
            return {"error": f"Plugin '{plugin_name}' not found"}
        
        try:
            # Load plugin manifest
            manifest_path = os.path.join(plugin_path, "manifest.json")
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
            else:
                return {"error": "Plugin manifest not found"}
            
            # Load plugin module
            plugin_module = importlib.import_module(f"plugins.{plugin_name}.plugin")
            
            self.plugins[plugin_name] = {
                "manifest": manifest,
                "module": plugin_module,
                "loaded": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "plugin": plugin_name,
                "version": manifest.get("version"),
                "description": manifest.get("description")
            }
        except Exception as e:
            return {"error": str(e)}
    
    def list_plugins(self) -> List[Dict]:
        """List all available plugins"""
        plugins = []
        
        if os.path.exists(self.plugins_dir):
            for item in os.listdir(self.plugins_dir):
                plugin_path = os.path.join(self.plugins_dir, item)
                if os.path.isdir(plugin_path):
                    manifest_path = os.path.join(plugin_path, "manifest.json")
                    if os.path.exists(manifest_path):
                        try:
                            with open(manifest_path, 'r') as f:
                                manifest = json.load(f)
                            plugins.append({
                                "name": item,
                                "version": manifest.get("version"),
                                "description": manifest.get("description"),
                                "author": manifest.get("author"),
                                "loaded": item in self.plugins
                            })
                        except:
                            pass
        
        return plugins
    
    def create_plugin_template(self, plugin_name: str, description: str,
                              author: str = "Unknown") -> Dict:
        """Create a plugin template"""
        plugin_path = os.path.join(self.plugins_dir, plugin_name)
        os.makedirs(plugin_path, exist_ok=True)
        
        # Create manifest
        manifest = {
            "name": plugin_name,
            "version": "1.0.0",
            "description": description,
            "author": author,
            "created": datetime.now().isoformat(),
            "commands": [],
            "hooks": []
        }
        
        manifest_path = os.path.join(plugin_path, "manifest.json")
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        # Create plugin.py template
        plugin_code = f'''"""
{plugin_name} Plugin
{description}
"""
from typing import Dict, Any

class {plugin_name.title().replace('_', '')}Plugin:
    """{description}"""
    
    def __init__(self):
        self.name = "{plugin_name}"
        self.version = "1.0.0"
    
    def execute(self, command: str, params: Dict[str, Any] = None) -> Dict:
        """Execute plugin command"""
        return {{
            "success": True,
            "message": "Plugin executed",
            "command": command
        }}
    
    def handle_hook(self, hook_name: str, data: Dict[str, Any]) -> Dict:
        """Handle system hook"""
        return {{
            "success": True,
            "hook": hook_name
        }}
'''
        
        plugin_file = os.path.join(plugin_path, "plugin.py")
        with open(plugin_file, 'w') as f:
            f.write(plugin_code)
        
        # Create README
        readme = f'''# {plugin_name}

{description}

## Installation

Copy this plugin to the plugins directory.

## Usage

The plugin will be automatically loaded by JARVIS.

## Commands

(Add your plugin commands here)

## Hooks

(Add your plugin hooks here)
'''
        
        readme_file = os.path.join(plugin_path, "README.md")
        with open(readme_file, 'w') as f:
            f.write(readme)
        
        return {
            "success": True,
            "plugin_path": plugin_path,
            "manifest": manifest_path
        }
    
    def search_marketplace(self, query: str) -> List[Dict]:
        """Search plugin marketplace"""
        # This would connect to a real marketplace API
        # For now, return example results
        return [
            {
                "name": "github-integration",
                "description": "GitHub integration plugin",
                "downloads": 150,
                "rating": 4.5
            },
            {
                "name": "weather-plugin",
                "description": "Weather information plugin",
                "downloads": 89,
                "rating": 4.2
            }
        ]
    
    def install_from_marketplace(self, plugin_name: str) -> Dict:
        """Install plugin from marketplace"""
        # This would download from marketplace
        return {
            "success": True,
            "plugin": plugin_name,
            "message": "Plugin installed from marketplace"
        }
