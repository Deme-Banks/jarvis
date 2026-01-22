"""
Semantic Caching for Similar Queries
"""
import hashlib
import json
import os
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from collections import OrderedDict


class SemanticCache:
    """Semantic cache that matches similar queries"""
    
    def __init__(self, cache_dir: str = "./memory/semantic_cache", 
                 similarity_threshold: float = 0.8,
                 max_size: int = 1000):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.similarity_threshold = similarity_threshold
        self.max_size = max_size
        self.cache = OrderedDict()
        self._load_cache()
    
    def _load_cache(self):
        """Load cache from disk"""
        cache_file = os.path.join(self.cache_dir, "cache.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    for key, value in data.items():
                        self.cache[key] = value
            except:
                pass
    
    def _save_cache(self):
        """Save cache to disk"""
        cache_file = os.path.join(self.cache_dir, "cache.json")
        try:
            with open(cache_file, 'w') as f:
                json.dump(dict(self.cache), f, indent=2)
        except:
            pass
    
    def _simple_similarity(self, query1: str, query2: str) -> float:
        """Simple similarity calculation (word overlap)"""
        words1 = set(query1.lower().split())
        words2 = set(query2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _get_key(self, query: str) -> str:
        """Get cache key from query"""
        # Normalize query
        normalized = ' '.join(query.lower().split())
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def get(self, query: str) -> Optional[str]:
        """Get cached response for similar query"""
        # First, try exact match
        key = self._get_key(query)
        if key in self.cache:
            entry = self.cache[key]
            # Check expiration
            if datetime.now() < datetime.fromisoformat(entry['expires']):
                # Move to end (LRU)
                self.cache.move_to_end(key)
                return entry['response']
            else:
                del self.cache[key]
        
        # Try semantic match
        query_lower = query.lower()
        best_match = None
        best_similarity = 0.0
        
        for cached_key, entry in self.cache.items():
            if datetime.now() >= datetime.fromisoformat(entry['expires']):
                continue
            
            similarity = self._simple_similarity(query_lower, entry['query'])
            if similarity > best_similarity and similarity >= self.similarity_threshold:
                best_similarity = similarity
                best_match = entry
        
        if best_match:
            return best_match['response']
        
        return None
    
    def set(self, query: str, response: str, ttl: int = 3600):
        """Cache response with TTL"""
        key = self._get_key(query)
        
        # Remove if exists
        if key in self.cache:
            del self.cache[key]
        
        # Add new entry
        expires = (datetime.now() + timedelta(seconds=ttl)).isoformat()
        self.cache[key] = {
            'query': query,
            'response': response,
            'expires': expires,
            'created': datetime.now().isoformat()
        }
        
        # Enforce max size (LRU)
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
        
        # Save periodically
        if len(self.cache) % 10 == 0:
            self._save_cache()
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total = len(self.cache)
        expired = sum(1 for e in self.cache.values() 
                     if datetime.now() >= datetime.fromisoformat(e['expires']))
        
        return {
            'total_entries': total,
            'active_entries': total - expired,
            'expired_entries': expired,
            'max_size': self.max_size,
            'similarity_threshold': self.similarity_threshold
        }
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self._save_cache()
