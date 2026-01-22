"""
Plugin Marketplace - Discovery and installation system
"""
import os
import json
import requests
from typing import Dict, List, Optional
from plugins.plugin_system import PluginSystem


class PluginMarketplace:
    """Plugin marketplace for JARVIS"""
    
    def __init__(self, marketplace_url: str = "https://marketplace.jarvis.ai",
                 plugins_dir: str = "plugins"):
        self.marketplace_url = marketplace_url
        self.plugins_dir = plugins_dir
        self.plugin_system = PluginSystem(plugins_dir)
        self.local_plugins: Dict[str, Dict] = {}
    
    def search_plugins(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """Search for plugins in marketplace"""
        # In production, would query marketplace API
        # For now, return mock results
        return [
            {
                "id": "github_integration",
                "name": "GitHub Integration",
                "description": "Enhanced GitHub integration",
                "author": "JARVIS Team",
                "version": "1.0.0",
                "downloads": 1000,
                "rating": 4.5,
                "category": "integration"
            },
            {
                "id": "custom_voice",
                "name": "Custom Voice",
                "description": "Custom voice profiles",
                "author": "Community",
                "version": "0.9.0",
                "downloads": 500,
                "rating": 4.0,
                "category": "voice"
            }
        ]
    
    def install_plugin(self, plugin_id: str) -> Dict:
        """Install a plugin from marketplace"""
        try:
            # In production, would download from marketplace
            # For now, simulate installation
            plugin_info = {
                "id": plugin_id,
                "name": f"Plugin {plugin_id}",
                "version": "1.0.0",
                "author": "Marketplace",
                "description": "Installed from marketplace"
            }
            
            # Register plugin
            self.plugin_system.register_plugin(
                plugin_id=plugin_id,
                name=plugin_info["name"],
                version=plugin_info["version"],
                author=plugin_info["author"],
                description=plugin_info["description"],
                entry_point=f"plugins.{plugin_id}"
            )
            
            # Load plugin
            self.plugin_system.load_plugin(plugin_id)
            
            return {
                "success": True,
                "plugin_id": plugin_id,
                "message": f"Plugin '{plugin_id}' installed successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def uninstall_plugin(self, plugin_id: str) -> Dict:
        """Uninstall a plugin"""
        try:
            if plugin_id in self.plugin_system.plugins:
                del self.plugin_system.plugins[plugin_id]
                if plugin_id in self.plugin_system.loaded_plugins:
                    del self.plugin_system.loaded_plugins[plugin_id]
                self.plugin_system._save_plugins()
                return {"success": True, "plugin_id": plugin_id}
            return {"success": False, "error": "Plugin not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_featured_plugins(self) -> List[Dict]:
        """Get featured plugins"""
        return self.search_plugins("", category="featured")
    
    def get_popular_plugins(self) -> List[Dict]:
        """Get popular plugins"""
        return sorted(
            self.search_plugins(""),
            key=lambda x: x.get("downloads", 0),
            reverse=True
        )[:10]
    
    def rate_plugin(self, plugin_id: str, rating: int) -> Dict:
        """Rate a plugin (1-5 stars)"""
        # In production, would submit to marketplace API
        return {
            "success": True,
            "plugin_id": plugin_id,
            "rating": rating
        }
