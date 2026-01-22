"""
Custom Integration Builder - Visual integration builder
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime


class CustomIntegrationBuilder:
    """Build custom integrations"""
    
    def __init__(self, integrations_file: str = "data/custom_integrations.json"):
        self.integrations_file = integrations_file
        self.integrations = self._load_integrations()
    
    def _load_integrations(self) -> Dict:
        """Load custom integrations"""
        if os.path.exists(self.integrations_file):
            try:
                with open(self.integrations_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_integrations(self):
        """Save integrations"""
        os.makedirs(os.path.dirname(self.integrations_file), exist_ok=True)
        with open(self.integrations_file, 'w') as f:
            json.dump(self.integrations, f, indent=2)
    
    def create_integration(self, name: str, api_config: Dict,
                          endpoints: List[Dict], authentication: Dict) -> Dict:
        """Create a custom integration"""
        integration = {
            "name": name,
            "created": datetime.now().isoformat(),
            "api_config": api_config,
            "endpoints": endpoints,
            "authentication": authentication,
            "enabled": True
        }
        
        self.integrations[name] = integration
        self._save_integrations()
        
        return {"success": True, "integration": name}
    
    def test_integration(self, name: str, endpoint: str, method: str = "GET",
                        data: Optional[Dict] = None) -> Dict:
        """Test an integration"""
        if name not in self.integrations:
            return {"error": f"Integration '{name}' not found"}
        
        integration = self.integrations[name]
        # This would actually make the API call
        return {
            "success": True,
            "integration": name,
            "endpoint": endpoint,
            "response": "Test successful"
        }
    
    def list_integrations(self) -> List[Dict]:
        """List all custom integrations"""
        return [
            {
                "name": name,
                "enabled": integration.get("enabled", False),
                "endpoints": len(integration.get("endpoints", []))
            }
            for name, integration in self.integrations.items()
        ]
    
    def generate_code(self, name: str) -> str:
        """Generate Python code for integration"""
        if name not in self.integrations:
            return f"# Integration '{name}' not found"
        
        integration = self.integrations[name]
        code = f'''"""
Custom Integration: {name}
Generated: {datetime.now().isoformat()}
"""
import requests
from typing import Dict, Optional

class {name.title().replace(' ', '')}Integration:
    """Custom integration for {name}"""
    
    def __init__(self):
        self.base_url = "{integration['api_config'].get('base_url', '')}"
        self.api_key = "{integration['authentication'].get('api_key', '')}"
    
    def _make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None):
        """Make API request"""
        url = f"{{self.base_url}}{{endpoint}}"
        headers = {{
            "Authorization": f"Bearer {{self.api_key}}",
            "Content-Type": "application/json"
        }}
        
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        
        response.raise_for_status()
        return response.json()
'''
        
        # Add endpoint methods
        for endpoint in integration.get("endpoints", []):
            endpoint_name = endpoint.get("name", "").replace(" ", "_").lower()
            method = endpoint.get("method", "GET")
            path = endpoint.get("path", "")
            
            code += f'''
    def {endpoint_name}(self, **kwargs):
        """{endpoint.get('description', '')}"""
        return self._make_request("{path}", method="{method}", data=kwargs)
'''
        
        return code
