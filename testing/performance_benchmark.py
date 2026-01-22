"""
Performance Benchmarking Suite - Measure and validate optimizations
"""
import time
import tracemalloc
import statistics
from typing import Dict, List, Optional
from datetime import datetime
from utils.performance_profiler import PerformanceProfiler
from agents.orchestrator_pi import PiOrchestrator


class PerformanceBenchmark:
    """Performance benchmarking suite"""
    
    def __init__(self):
        self.profiler = PerformanceProfiler()
        self.results: Dict[str, List[float]] = {}
        self.memory_results: Dict[str, List[int]] = {}
    
    def benchmark_startup(self, iterations: int = 5) -> Dict:
        """Benchmark startup time"""
        times = []
        memory_usage = []
        
        for i in range(iterations):
            tracemalloc.start()
            start_time = time.perf_counter()
            
            # Measure orchestrator initialization
            orchestrator = PiOrchestrator()
            
            end_time = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            times.append(end_time - start_time)
            memory_usage.append(peak / 1024 / 1024)  # MB
        
        return {
            "metric": "startup_time",
            "iterations": iterations,
            "avg_time": statistics.mean(times),
            "min_time": min(times),
            "max_time": max(times),
            "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
            "avg_memory": statistics.mean(memory_usage),
            "times": times,
            "memory": memory_usage
        }
    
    def benchmark_response_time(self, orchestrator: PiOrchestrator, 
                               commands: List[str], iterations: int = 10) -> Dict:
        """Benchmark response time for commands"""
        results = {}
        
        for command in commands:
            times = []
            for i in range(iterations):
                start_time = time.perf_counter()
                orchestrator.process(command)
                end_time = time.perf_counter()
                times.append(end_time - start_time)
            
            results[command] = {
                "avg_time": statistics.mean(times),
                "min_time": min(times),
                "max_time": max(times),
                "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
                "times": times
            }
        
        return {
            "metric": "response_time",
            "commands": results,
            "overall_avg": statistics.mean([r["avg_time"] for r in results.values()])
        }
    
    def benchmark_cache_hit_rate(self, orchestrator: PiOrchestrator,
                                commands: List[str], iterations: int = 20) -> Dict:
        """Benchmark cache hit rate"""
        hits = 0
        misses = 0
        
        # First run (misses)
        for command in commands:
            orchestrator.process(command)
            misses += 1
        
        # Second run (should be hits)
        for command in commands:
            start_time = time.perf_counter()
            orchestrator.process(command)
            end_time = time.perf_counter()
            
            # If response is very fast, likely cached
            if (end_time - start_time) < 0.1:
                hits += 1
            else:
                misses += 1
        
        hit_rate = hits / (hits + misses) if (hits + misses) > 0 else 0
        
        return {
            "metric": "cache_hit_rate",
            "hits": hits,
            "misses": misses,
            "hit_rate": hit_rate,
            "total_requests": hits + misses
        }
    
    def run_full_benchmark(self) -> Dict:
        """Run full benchmark suite"""
        print("Running performance benchmarks...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "startup": self.benchmark_startup(),
            "cache": None,
            "response": None
        }
        
        # Response time benchmark
        orchestrator = PiOrchestrator()
        test_commands = [
            "create keylogger",
            "scan network",
            "get system information",
            "show performance metrics"
        ]
        
        results["response"] = self.benchmark_response_time(orchestrator, test_commands)
        results["cache"] = self.benchmark_cache_hit_rate(orchestrator, test_commands)
        
        return results
    
    def generate_report(self, results: Dict) -> str:
        """Generate benchmark report"""
        report = f"""
=== JARVIS Performance Benchmark Report ===
Generated: {results['timestamp']}

STARTUP TIME:
  Average: {results['startup']['avg_time']:.4f}s
  Min: {results['startup']['min_time']:.4f}s
  Max: {results['startup']['max_time']:.4f}s
  Memory: {results['startup']['avg_memory']:.2f} MB

RESPONSE TIME:
  Overall Average: {results['response']['overall_avg']:.4f}s
"""
        for cmd, data in results['response']['commands'].items():
            report += f"  {cmd}: {data['avg_time']:.4f}s (min: {data['min_time']:.4f}s, max: {data['max_time']:.4f}s)\n"
        
        report += f"""
CACHE PERFORMANCE:
  Hit Rate: {results['cache']['hit_rate']*100:.2f}%
  Hits: {results['cache']['hits']}
  Misses: {results['cache']['misses']}

=== End of Report ===
"""
        return report
