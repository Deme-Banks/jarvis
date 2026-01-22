"""
API Gateway - Manage all API integrations
"""
import os
import requests
from typing import Dict, List, Optional
from datetime import datetime
import json


class APIGateway:
    """API Gateway for managing all integrations"""
    
    def __init__(self, config_file: str = "config/api_gateway.json"):
        self.config_file = config_file
        self.apis = self._load_apis()
        self.rate_limits = {}
        self.usage_stats = {}
    
    def _load_apis(self) -> Dict:
        """Load API configurations"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def register_api(self, name: str, base_url: str, auth_type: str,
                    auth_config: Dict, rate_limit: Optional[Dict] = None) -> Dict:
        """Register an API"""
        self.apis[name] = {
            "base_url": base_url,
            "auth_type": auth_type,  # bearer, api_key, oauth, etc.
            "auth_config": auth_config,
            "rate_limit": rate_limit or {},
            "registered": datetime.now().isoformat()
        }
        
        self._save_apis()
        return {"success": True, "api": name}
    
    def _save_apis(self):
        """Save API configurations"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.apis, f, indent=2)
    
    def call_api(self, api_name: str, endpoint: str, method: str = "GET",
                 data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """Call an API endpoint"""
        if api_name not in self.apis:
            return {"error": f"API '{api_name}' not registered"}
        
        api_config = self.apis[api_name]
        url = f"{api_config['base_url']}{endpoint}"
        
        # Prepare headers
        headers = self._prepare_headers(api_config)
        
        # Check rate limits
        if not self._check_rate_limit(api_name):
            return {"error": "Rate limit exceeded"}
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data, params=params, timeout=10)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                return {"error": f"Unsupported method: {method}"}
            
            response.raise_for_status()
            
            # Update usage stats
            self._update_usage(api_name)
            
            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json() if response.content else None,
                "response": response.text
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _prepare_headers(self, api_config: Dict) -> Dict:
        """Prepare headers with authentication"""
        headers = {"Content-Type": "application/json"}
        
        auth_type = api_config.get("auth_type")
        auth_config = api_config.get("auth_config", {})
        
        if auth_type == "bearer":
            headers["Authorization"] = f"Bearer {auth_config.get('token')}"
        elif auth_type == "api_key":
            if auth_config.get("header"):
                headers[auth_config["header"]] = auth_config.get("key")
            else:
                headers["X-API-Key"] = auth_config.get("key")
        elif auth_type == "basic":
            import base64
            credentials = f"{auth_config.get('username')}:{auth_config.get('password')}"
            encoded = base64.b64encode(credentials.encode()).decode()
            headers["Authorization"] = f"Basic {encoded}"
        
        return headers
    
    def _check_rate_limit(self, api_name: str) -> bool:
        """Check if API call is within rate limit"""
        if api_name not in self.apis:
            return True
        
        rate_limit = self.apis[api_name].get("rate_limit", {})
        if not rate_limit:
            return True
        
        # Simplified rate limiting
        # In production, would use more sophisticated tracking
        return True
    
    def _update_usage(self, api_name: str):
        """Update API usage statistics"""
        if api_name not in self.usage_stats:
            self.usage_stats[api_name] = {"calls": 0, "errors": 0}
        
        self.usage_stats[api_name]["calls"] += 1
    
    def list_apis(self) -> List[str]:
        """List all registered APIs"""
        return list(self.apis.keys())
    
    def get_api_stats(self, api_name: str) -> Dict:
        """Get statistics for an API"""
        return {
            "api": api_name,
            "config": self.apis.get(api_name, {}),
            "usage": self.usage_stats.get(api_name, {})
        }
