"""
Performance Profiler - Identify bottlenecks and optimize
"""
import time
import cProfile
import pstats
import functools
from typing import Dict, List, Optional
from collections import defaultdict
import tracemalloc


class PerformanceProfiler:
    """Performance profiling and optimization tools"""
    
    def __init__(self):
        self.profiler = cProfile.Profile()
        self.metrics: Dict[str, List[float]] = defaultdict(list)
        self.traces: Dict[str, float] = {}
        tracemalloc.start()
    
    def profile_function(self, func):
        """Decorator to profile a function"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            start_memory = tracemalloc.take_snapshot()
            
            result = func(*args, **kwargs)
            
            end_time = time.perf_counter()
            end_memory = tracemalloc.take_snapshot()
            
            duration = end_time - start_time
            memory_diff = end_memory.compare_to(start_memory, 'lineno')
            memory_used = sum(stat.size_diff for stat in memory_diff)
            
            self.metrics[func.__name__].append(duration)
            self.traces[func.__name__] = {
                "duration": duration,
                "memory": memory_used,
                "calls": 1
            }
            
            return result
        return wrapper
    
    def get_slowest_functions(self, limit: int = 10) -> List[Dict]:
        """Get slowest functions"""
        slowest = []
        for func_name, times in self.metrics.items():
            avg_time = sum(times) / len(times) if times else 0
            slowest.append({
                "function": func_name,
                "avg_time": avg_time,
                "total_calls": len(times),
                "total_time": sum(times)
            })
        
        return sorted(slowest, key=lambda x: x["avg_time"], reverse=True)[:limit]
    
    def get_memory_hogs(self, limit: int = 10) -> List[Dict]:
        """Get functions using most memory"""
        memory_hogs = []
        for func_name, trace in self.traces.items():
            memory_hogs.append({
                "function": func_name,
                "memory": trace.get("memory", 0),
                "duration": trace.get("duration", 0)
            })
        
        return sorted(memory_hogs, key=lambda x: x["memory"], reverse=True)[:limit]
    
    def generate_report(self) -> str:
        """Generate performance report"""
        report = "=== Performance Report ===\n\n"
        
        report += "Slowest Functions:\n"
        for func in self.get_slowest_functions(10):
            report += f"  {func['function']}: {func['avg_time']:.4f}s (called {func['total_calls']} times)\n"
        
        report += "\nMemory Hogs:\n"
        for func in self.get_memory_hogs(10):
            report += f"  {func['function']}: {func['memory'] / 1024 / 1024:.2f} MB\n"
        
        return report
