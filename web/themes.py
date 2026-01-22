"""
Theme System - Dark/Light/Custom Themes
"""
import json
import os
from typing import Dict, Optional


class ThemeManager:
    """Theme management for JARVIS UI"""
    
    def __init__(self, themes_file: str = "config/themes.json"):
        self.themes_file = themes_file
        self.themes = self._load_themes()
    
    def _load_themes(self) -> Dict:
        """Load themes from file"""
        default_themes = {
            "dark": {
                "name": "Dark",
                "background": "#1a1a1a",
                "foreground": "#ffffff",
                "primary": "#007bff",
                "secondary": "#6c757d",
                "accent": "#28a745",
                "error": "#dc3545",
                "warning": "#ffc107"
            },
            "light": {
                "name": "Light",
                "background": "#ffffff",
                "foreground": "#000000",
                "primary": "#007bff",
                "secondary": "#6c757d",
                "accent": "#28a745",
                "error": "#dc3545",
                "warning": "#ffc107"
            },
            "cyber": {
                "name": "Cyber",
                "background": "#0a0e27",
                "foreground": "#00ff41",
                "primary": "#00ff41",
                "secondary": "#008f11",
                "accent": "#ff0080",
                "error": "#ff0000",
                "warning": "#ffff00"
            }
        }
        
        if os.path.exists(self.themes_file):
            try:
                with open(self.themes_file, 'r') as f:
                    custom_themes = json.load(f)
                    default_themes.update(custom_themes)
            except:
                pass
        
        return default_themes
    
    def get_theme(self, theme_name: str) -> Optional[Dict]:
        """Get theme by name"""
        return self.themes.get(theme_name)
    
    def create_custom_theme(self, name: str, colors: Dict) -> str:
        """Create a custom theme"""
        self.themes[name] = {
            "name": name,
            **colors
        }
        
        os.makedirs(os.path.dirname(self.themes_file), exist_ok=True)
        with open(self.themes_file, 'w') as f:
            json.dump(self.themes, f, indent=2)
        
        return f"Theme '{name}' created successfully."
    
    def list_themes(self) -> List[str]:
        """List available themes"""
        return list(self.themes.keys())
    
    def get_theme_css(self, theme_name: str) -> str:
        """Generate CSS for theme"""
        theme = self.get_theme(theme_name)
        if not theme:
            theme = self.get_theme("dark")
        
        return f"""
        :root {{
            --bg-color: {theme['background']};
            --fg-color: {theme['foreground']};
            --primary-color: {theme['primary']};
            --secondary-color: {theme['secondary']};
            --accent-color: {theme['accent']};
            --error-color: {theme['error']};
            --warning-color: {theme['warning']};
        }}
        
        body {{
            background-color: var(--bg-color);
            color: var(--fg-color);
        }}
        
        .btn-primary {{
            background-color: var(--primary-color);
            color: var(--fg-color);
        }}
        
        .card {{
            background-color: var(--bg-color);
            border: 1px solid var(--secondary-color);
        }}
        """
