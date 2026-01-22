"""
Cache Optimizer - Improve caching strategies
"""
import time
import hashlib
import json
from typing import Any, Optional, Dict
from collections import OrderedDict
import threading


class LRUCache:
    """LRU Cache with TTL"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.max_size = max_size
        self.ttl = ttl
        self.cache: OrderedDict = OrderedDict()
        self.timestamps: Dict[str, float] = {}
        self.lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        with self.lock:
            if key in self.cache:
                # Check TTL
                if time.time() - self.timestamps[key] > self.ttl:
                    del self.cache[key]
                    del self.timestamps[key]
                    return None
                
                # Move to end (most recently used)
                self.cache.move_to_end(key)
                return self.cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """Set value in cache"""
        with self.lock:
            # Remove oldest if at capacity
            if len(self.cache) >= self.max_size and key not in self.cache:
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
                del self.timestamps[oldest_key]
            
            self.cache[key] = value
            self.timestamps[key] = time.time()
            self.cache.move_to_end(key)
    
    def clear(self):
        """Clear cache"""
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()
    
    def size(self) -> int:
        """Get cache size"""
        return len(self.cache)


class SmartCache:
    """Smart caching with multiple strategies"""
    
    def __init__(self):
        self.lru_cache = LRUCache(max_size=1000, ttl=3600)
        self.semantic_cache: Dict[str, Any] = {}
    
    def _generate_key(self, data: Any) -> str:
        """Generate cache key"""
        if isinstance(data, str):
            return hashlib.md5(data.encode()).hexdigest()
        return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()
    
    def get(self, key: Any) -> Optional[Any]:
        """Get from cache"""
        cache_key = self._generate_key(key)
        return self.lru_cache.get(cache_key)
    
    def set(self, key: Any, value: Any):
        """Set in cache"""
        cache_key = self._generate_key(key)
        self.lru_cache.set(cache_key, value)
    
    def get_semantic(self, query: str) -> Optional[Any]:
        """Get semantically similar cached result"""
        query_lower = query.lower()
        for cached_query, result in self.semantic_cache.items():
            # Simple similarity check (in production, use embeddings)
            if query_lower in cached_query or cached_query in query_lower:
                return result
        return None
    
    def set_semantic(self, query: str, result: Any):
        """Set semantically cached result"""
        self.semantic_cache[query.lower()] = result
        # Limit semantic cache size
        if len(self.semantic_cache) > 100:
            oldest = next(iter(self.semantic_cache))
            del self.semantic_cache[oldest]
