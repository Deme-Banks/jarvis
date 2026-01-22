"""
Enhanced API Gateway - Centralized API management
"""
import os
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from utils.cache_optimizer import SmartCache
from utils.performance_profiler import PerformanceProfiler


class EnhancedAPIGateway:
    """Enhanced API gateway with rate limiting, analytics, and routing"""
    
    def __init__(self):
        self.cache = SmartCache()
        self.profiler = PerformanceProfiler()
        self.rate_limits: Dict[str, Dict] = {}
        self.api_keys: Dict[str, Dict] = {}
        self.routes: Dict[str, Dict] = {}
        self.analytics: Dict[str, List] = defaultdict(list)
    
    def register_route(self, route: str, handler: callable,
                      rate_limit: int = 100, methods: List[str] = None) -> Dict:
        """Register an API route"""
        self.routes[route] = {
            "handler": handler,
            "rate_limit": rate_limit,
            "methods": methods or ["GET", "POST"],
            "registered": datetime.now().isoformat()
        }
        return {"success": True, "route": route}
    
    def register_api_key(self, api_key: str, user_id: str,
                        rate_limit: int = 100, permissions: List[str] = None) -> Dict:
        """Register an API key"""
        self.api_keys[api_key] = {
            "user_id": user_id,
            "rate_limit": rate_limit,
            "permissions": permissions or [],
            "created": datetime.now().isoformat(),
            "requests_count": 0,
            "last_request": None
        }
        return {"success": True, "api_key": api_key}
    
    def check_rate_limit(self, api_key: str) -> Dict:
        """Check if API key is within rate limit"""
        if api_key not in self.api_keys:
            return {"allowed": False, "error": "Invalid API key"}
        
        key_info = self.api_keys[api_key]
        rate_limit = key_info["rate_limit"]
        
        # Reset counter if new minute
        now = datetime.now()
        last_request = key_info.get("last_request")
        if last_request:
            last_time = datetime.fromisoformat(last_request)
            if (now - last_time).total_seconds() > 60:
                key_info["requests_count"] = 0
        
        if key_info["requests_count"] >= rate_limit:
            return {
                "allowed": False,
                "error": "Rate limit exceeded",
                "limit": rate_limit,
                "used": key_info["requests_count"]
            }
        
        # Increment counter
        key_info["requests_count"] += 1
        key_info["last_request"] = now.isoformat()
        
        return {"allowed": True, "remaining": rate_limit - key_info["requests_count"]}
    
    def route_request(self, route: str, method: str, api_key: str,
                     params: Dict = None) -> Dict:
        """Route API request"""
        # Check rate limit
        rate_check = self.check_rate_limit(api_key)
        if not rate_check.get("allowed"):
            return rate_check
        
        # Check route exists
        if route not in self.routes:
            return {"error": f"Route '{route}' not found"}
        
        route_info = self.routes[route]
        if method not in route_info["methods"]:
            return {"error": f"Method '{method}' not allowed"}
        
        # Log analytics
        self.analytics[route].append({
            "timestamp": datetime.now().isoformat(),
            "method": method,
            "api_key": api_key[:8] + "...",  # Partial key for privacy
            "params": params
        })
        
        # Execute handler
        try:
            handler = route_info["handler"]
            result = handler(params or {})
            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_analytics(self, route: Optional[str] = None) -> Dict:
        """Get API analytics"""
        if route:
            return {"route": route, "requests": self.analytics.get(route, [])}
        else:
            return {
                "all_routes": {
                    r: len(requests) for r, requests in self.analytics.items()
                },
                "total_requests": sum(len(r) for r in self.analytics.values())
            }
