"""
Plugin System - Extensible plugin architecture
"""
import os
import json
import importlib
from typing import Dict, List, Optional, Any
from datetime import datetime
from refactoring.code_deduplication import CommonUtils


class PluginSystem:
    """Plugin system for JARVIS"""
    
    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = plugins_dir
        self.plugins: Dict[str, Dict] = {}
        self.loaded_plugins: Dict[str, Any] = {}
        os.makedirs(plugins_dir, exist_ok=True)
    
    def register_plugin(self, plugin_id: str, name: str, version: str,
                       author: str, description: str, entry_point: str,
                       commands: List[str] = None) -> Dict:
        """Register a plugin"""
        plugin = {
            "id": plugin_id,
            "name": name,
            "version": version,
            "author": author,
            "description": description,
            "entry_point": entry_point,
            "commands": commands or [],
            "enabled": True,
            "registered": datetime.now().isoformat()
        }
        
        self.plugins[plugin_id] = plugin
        self._save_plugins()
        
        return {"success": True, "plugin_id": plugin_id}
    
    def load_plugin(self, plugin_id: str) -> Dict:
        """Load a plugin"""
        if plugin_id not in self.plugins:
            return {"error": f"Plugin '{plugin_id}' not registered"}
        
        plugin = self.plugins[plugin_id]
        if not plugin.get("enabled", True):
            return {"error": f"Plugin '{plugin_id}' is disabled"}
        
        try:
            # Load plugin module
            entry_point = plugin["entry_point"]
            module = importlib.import_module(entry_point)
            
            # Initialize plugin
            if hasattr(module, 'initialize'):
                plugin_instance = module.initialize()
                self.loaded_plugins[plugin_id] = plugin_instance
            
            return {"success": True, "plugin_id": plugin_id}
        except Exception as e:
            return {"error": f"Failed to load plugin: {str(e)}"}
    
    def execute_plugin_command(self, plugin_id: str, command: str,
                              args: Dict = None) -> Dict:
        """Execute a plugin command"""
        if plugin_id not in self.loaded_plugins:
            return {"error": f"Plugin '{plugin_id}' not loaded"}
        
        plugin = self.loaded_plugins[plugin_id]
        
        if hasattr(plugin, 'execute'):
            try:
                result = plugin.execute(command, args or {})
                return {"success": True, "result": result}
            except Exception as e:
                return {"error": str(e)}
        
        return {"error": "Plugin does not support execution"}
    
    def list_plugins(self) -> List[Dict]:
        """List all registered plugins"""
        return [
            {
                "id": plugin_id,
                "name": plugin["name"],
                "version": plugin["version"],
                "enabled": plugin.get("enabled", True),
                "loaded": plugin_id in self.loaded_plugins
            }
            for plugin_id, plugin in self.plugins.items()
        ]
    
    def _save_plugins(self):
        """Save plugin registry"""
        registry_file = os.path.join(self.plugins_dir, "registry.json")
        CommonUtils.safe_json_save(registry_file, self.plugins)
    
    def _load_plugins(self):
        """Load plugin registry"""
        registry_file = os.path.join(self.plugins_dir, "registry.json")
        self.plugins = CommonUtils.safe_json_load(registry_file, {})


class PluginBase:
    """Base class for plugins"""
    
    def __init__(self, plugin_id: str, name: str):
        self.plugin_id = plugin_id
        self.name = name
    
    def initialize(self):
        """Initialize plugin"""
        return self
    
    def execute(self, command: str, args: Dict) -> Any:
        """Execute plugin command"""
        raise NotImplementedError
    
    def get_info(self) -> Dict:
        """Get plugin information"""
        return {
            "id": self.plugin_id,
            "name": self.name
        }
