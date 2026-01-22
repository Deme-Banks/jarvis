"""
Tests for Cache System
"""
import unittest
import os
import tempfile
from optimization.cache import ResponseCache


class TestResponseCache(unittest.TestCase):
    """Test response cache"""
    
    def setUp(self):
        self.cache_dir = tempfile.mkdtemp()
        self.cache = ResponseCache(capacity=10, cache_dir=self.cache_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.cache_dir, ignore_errors=True)
    
    def test_cache_set_get(self):
        """Test setting and getting from cache"""
        self.cache.set("test query", "test response", {})
        result = self.cache.get("test query", {})
        self.assertEqual(result, "test response")
    
    def test_cache_miss(self):
        """Test cache miss"""
        result = self.cache.get("nonexistent", {})
        self.assertIsNone(result)
    
    def test_cache_capacity(self):
        """Test cache capacity limit"""
        for i in range(15):
            self.cache.set(f"query{i}", f"response{i}", {})
        
        # First 5 should be evicted
        self.assertIsNone(self.cache.get("query0", {}))
        self.assertIsNotNone(self.cache.get("query14", {}))
