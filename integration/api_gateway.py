"""
API Gateway - Manage all API integrations
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime
import requests


class APIGateway:
    """API Gateway for managing all integrations"""
    
    def __init__(self, config_file: str = "config/api_gateway.json"):
        self.config_file = config_file
        self.apis = self._load_apis()
        self.rate_limits = {}
        self.request_logs = []
    
    def _load_apis(self) -> Dict:
        """Load API configurations"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def register_api(self, name: str, base_url: str, auth_type: str = "bearer",
                    api_key: Optional[str] = None, rate_limit: Optional[Dict] = None) -> Dict:
        """Register an API"""
        self.apis[name] = {
            "base_url": base_url,
            "auth_type": auth_type,
            "api_key": api_key or os.getenv(f"{name.upper()}_API_KEY"),
            "rate_limit": rate_limit or {"requests_per_minute": 60},
            "registered": datetime.now().isoformat()
        }
        
        self._save_apis()
        return {"success": True, "api": name}
    
    def _save_apis(self):
        """Save API configurations"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.apis, f, indent=2)
    
    def make_request(self, api_name: str, endpoint: str, method: str = "GET",
                    data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict:
        """Make API request through gateway"""
        if api_name not in self.apis:
            return {"error": f"API '{api_name}' not registered"}
        
        api_config = self.apis[api_name]
        
        # Check rate limit
        if not self._check_rate_limit(api_name):
            return {"error": "Rate limit exceeded"}
        
        # Build request
        url = f"{api_config['base_url']}/{endpoint.lstrip('/')}"
        request_headers = headers or {}
        
        # Add authentication
        if api_config['auth_type'] == "bearer" and api_config.get('api_key'):
            request_headers["Authorization"] = f"Bearer {api_config['api_key']}"
        elif api_config['auth_type'] == "api_key" and api_config.get('api_key'):
            request_headers["X-API-Key"] = api_config['api_key']
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=request_headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, headers=request_headers, json=data, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=request_headers, json=data, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=request_headers, timeout=10)
            else:
                return {"error": f"Unsupported method: {method}"}
            
            # Log request
            self._log_request(api_name, endpoint, method, response.status_code)
            
            response.raise_for_status()
            
            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json() if response.content else {},
                "api": api_name
            }
        except Exception as e:
            return {"error": str(e), "api": api_name}
    
    def _check_rate_limit(self, api_name: str) -> bool:
        """Check if API is within rate limit"""
        if api_name not in self.rate_limits:
            self.rate_limits[api_name] = {
                "requests": [],
                "limit": self.apis[api_name].get("rate_limit", {}).get("requests_per_minute", 60)
            }
        
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        # Remove old requests
        self.rate_limits[api_name]["requests"] = [
            req_time for req_time in self.rate_limits[api_name]["requests"]
            if req_time > minute_ago
        ]
        
        # Check limit
        if len(self.rate_limits[api_name]["requests"]) >= self.rate_limits[api_name]["limit"]:
            return False
        
        # Add current request
        self.rate_limits[api_name]["requests"].append(now)
        return True
    
    def _log_request(self, api_name: str, endpoint: str, method: str, status_code: int):
        """Log API request"""
        self.request_logs.append({
            "timestamp": datetime.now().isoformat(),
            "api": api_name,
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code
        })
        
        # Keep only last 1000 logs
        if len(self.request_logs) > 1000:
            self.request_logs = self.request_logs[-1000:]
    
    def get_api_stats(self, api_name: Optional[str] = None) -> Dict:
        """Get API usage statistics"""
        if api_name:
            api_logs = [log for log in self.request_logs if log["api"] == api_name]
        else:
            api_logs = self.request_logs
        
        stats = {
            "total_requests": len(api_logs),
            "successful": len([log for log in api_logs if 200 <= log["status_code"] < 300]),
            "failed": len([log for log in api_logs if log["status_code"] >= 400]),
            "by_method": defaultdict(int),
            "by_endpoint": defaultdict(int)
        }
        
        for log in api_logs:
            stats["by_method"][log["method"]] += 1
            stats["by_endpoint"][log["endpoint"]] += 1
        
        return stats
