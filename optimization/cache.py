"""
Response Caching System for Performance
"""
import hashlib
import json
import os
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


class ResponseCache:
    """Fast response caching system"""
    
    def __init__(self, cache_dir: str = "./cache", max_size: int = 1000, ttl: int = 3600):
        self.cache_dir = cache_dir
        self.max_size = max_size
        self.ttl = ttl  # Time to live in seconds
        os.makedirs(cache_dir, exist_ok=True)
        self.cache_file = os.path.join(cache_dir, "response_cache.json")
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """Load cache from disk"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """Save cache to disk"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except:
            pass
    
    def _generate_key(self, query: str, context: Optional[Dict] = None) -> str:
        """Generate cache key from query and context"""
        cache_string = query.lower().strip()
        if context:
            cache_string += json.dumps(context, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get(self, query: str, context: Optional[Dict] = None) -> Optional[str]:
        """Get cached response"""
        key = self._generate_key(query, context)
        
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        
        # Check if expired
        if datetime.now().isoformat() > entry.get("expires_at", ""):
            del self.cache[key]
            return None
        
        # Update access time
        entry["last_accessed"] = datetime.now().isoformat()
        entry["access_count"] = entry.get("access_count", 0) + 1
        
        return entry["response"]
    
    def set(self, query: str, response: str, context: Optional[Dict] = None):
        """Cache a response"""
        key = self._generate_key(query, context)
        
        # Clean old entries if cache is full
        if len(self.cache) >= self.max_size:
            self._clean_old_entries()
        
        expires_at = (datetime.now() + timedelta(seconds=self.ttl)).isoformat()
        
        self.cache[key] = {
            "query": query,
            "response": response,
            "created_at": datetime.now().isoformat(),
            "expires_at": expires_at,
            "last_accessed": datetime.now().isoformat(),
            "access_count": 1,
            "context": context
        }
        
        # Save periodically (every 10 entries)
        if len(self.cache) % 10 == 0:
            self._save_cache()
    
    def _clean_old_entries(self):
        """Remove old or least-used entries"""
        now = datetime.now()
        
        # Remove expired entries first
        expired_keys = [
            key for key, entry in self.cache.items()
            if now.isoformat() > entry.get("expires_at", "")
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        # If still full, remove least accessed
        if len(self.cache) >= self.max_size:
            sorted_entries = sorted(
                self.cache.items(),
                key=lambda x: x[1].get("access_count", 0)
            )
            
            # Remove bottom 10%
            remove_count = max(1, len(self.cache) // 10)
            for key, _ in sorted_entries[:remove_count]:
                del self.cache[key]
    
    def clear(self):
        """Clear entire cache"""
        self.cache = {}
        self._save_cache()
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total_entries = len(self.cache)
        total_accesses = sum(entry.get("access_count", 0) for entry in self.cache.values())
        
        return {
            "total_entries": total_entries,
            "max_size": self.max_size,
            "total_accesses": total_accesses,
            "hit_rate": total_accesses / max(total_entries, 1),
            "cache_file": self.cache_file
        }
