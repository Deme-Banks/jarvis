"""
Plugin System for JARVIS
"""
import os
import importlib.util
from typing import Dict, List, Optional, Callable
from abc import ABC, abstractmethod


class Plugin(ABC):
    """Base plugin class"""
    
    @abstractmethod
    def get_name(self) -> str:
        """Get plugin name"""
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """Get plugin version"""
        pass
    
    @abstractmethod
    def handle_command(self, command: str, context: Dict) -> Optional[str]:
        """Handle command, return response or None"""
        pass
    
    def initialize(self):
        """Initialize plugin (optional)"""
        pass
    
    def cleanup(self):
        """Cleanup plugin (optional)"""
        pass


class PluginManager:
    """Manage plugins"""
    
    def __init__(self, plugin_dir: str = "./plugins"):
        self.plugin_dir = plugin_dir
        os.makedirs(plugin_dir, exist_ok=True)
        self.plugins: List[Plugin] = []
        self._load_plugins()
    
    def _load_plugins(self):
        """Load all plugins from directory"""
        if not os.path.exists(self.plugin_dir):
            return
        
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                try:
                    plugin = self._load_plugin(os.path.join(self.plugin_dir, filename))
                    if plugin:
                        plugin.initialize()
                        self.plugins.append(plugin)
                except Exception as e:
                    print(f"Failed to load plugin {filename}: {e}")
    
    def _load_plugin(self, filepath: str) -> Optional[Plugin]:
        """Load a single plugin"""
        spec = importlib.util.spec_from_file_location("plugin", filepath)
        if spec is None or spec.loader is None:
            return None
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Look for Plugin class
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) and 
                issubclass(attr, Plugin) and 
                attr != Plugin):
                return attr()
        
        return None
    
    def handle_command(self, command: str, context: Dict) -> Optional[str]:
        """Try to handle command with plugins"""
        for plugin in self.plugins:
            try:
                response = plugin.handle_command(command, context)
                if response:
                    return response
            except Exception as e:
                print(f"Plugin {plugin.get_name()} error: {e}")
        
        return None
    
    def list_plugins(self) -> List[Dict]:
        """List all loaded plugins"""
        return [
            {
                'name': plugin.get_name(),
                'version': plugin.get_version()
            }
            for plugin in self.plugins
        ]
    
    def unload_all(self):
        """Unload all plugins"""
        for plugin in self.plugins:
            try:
                plugin.cleanup()
            except:
                pass
        self.plugins.clear()
