"""
Refactored Orchestrator - Optimized version
"""
import os
from typing import Dict, Optional, Any
from utils.lazy_loader import LazyLoader
from utils.cache_optimizer import SmartCache
from utils.async_optimizer import AsyncOptimizer
from utils.performance_profiler import PerformanceProfiler


class OptimizedOrchestrator:
    """Optimized orchestrator with lazy loading and caching"""
    
    def __init__(self, prefer_cloud: bool = False):
        self.prefer_cloud = prefer_cloud
        
        # Lazy load components
        self._orchestrator = None
        self._cybersec = None
        self._ai_coding = None
        
        # Optimized caching
        self.cache = SmartCache()
        
        # Async optimizer
        self.async_optimizer = AsyncOptimizer()
        
        # Performance profiler
        self.profiler = PerformanceProfiler()
    
    @property
    def orchestrator(self):
        """Lazy load orchestrator"""
        if self._orchestrator is None:
            module = LazyLoader.get("orchestrator")
            self._orchestrator = module.PiOrchestrator(prefer_cloud=self.prefer_cloud)
        return self._orchestrator
    
    @property
    def cybersec(self):
        """Lazy load cybersecurity"""
        if self._cybersec is None:
            module = LazyLoader.get("cybersecurity")
            self._cybersec = module.EnhancedSecurityIntegration()
        return self._cybersec
    
    @property
    def ai_coding(self):
        """Lazy load AI coding"""
        if self._ai_coding is None:
            module = LazyLoader.get("ai_coding")
            self._ai_coding = module.AICodeGenerator()
        return self._ai_coding
    
    def process(self, user_request: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process user request with caching"""
        # Check cache first
        cached_result = self.cache.get(user_request)
        if cached_result:
            return cached_result
        
        # Check semantic cache
        semantic_result = self.cache.get_semantic(user_request)
        if semantic_result:
            return semantic_result
        
        # Profile the operation
        @self.profiler.profile_function
        def _process():
            # Route to appropriate handler
            if self._is_security_request(user_request):
                return self.cybersec.handle_security_request(user_request)
            elif self._is_coding_request(user_request):
                return self.ai_coding.generate_code(user_request)
            else:
                return self.orchestrator.process(user_request, context)
        
        result = _process()
        
        # Cache the result
        self.cache.set(user_request, result)
        self.cache.set_semantic(user_request, result)
        
        return result
    
    def _is_security_request(self, request: str) -> bool:
        """Check if request is security-related"""
        security_keywords = [
            "keylogger", "malware", "ddos", "scan", "exploit",
            "payload", "virus", "hack", "crack", "brute force"
        ]
        return any(keyword in request.lower() for keyword in security_keywords)
    
    def _is_coding_request(self, request: str) -> bool:
        """Check if request is coding-related"""
        coding_keywords = [
            "code", "program", "function", "class", "script",
            "generate code", "write code", "create function"
        ]
        return any(keyword in request.lower() for keyword in coding_keywords)
    
    def get_performance_report(self) -> str:
        """Get performance report"""
        return self.profiler.generate_report()
