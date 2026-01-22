"""
Parallel Processing for Multiple Agents
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Callable, Any, Optional
import time


class ParallelProcessor:
    """Parallel processing for multiple operations"""
    
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def process_parallel(self, tasks: List[Dict[str, Any]]) -> List[Dict]:
        """
        Process multiple tasks in parallel
        
        tasks: List of dicts with 'func' (callable) and 'args' (tuple)
        """
        results = []
        futures = {}
        
        # Submit all tasks
        for i, task in enumerate(tasks):
            func = task.get('func')
            args = task.get('args', ())
            kwargs = task.get('kwargs', {})
            future = self.executor.submit(func, *args, **kwargs)
            futures[future] = i
        
        # Collect results as they complete
        for future in as_completed(futures):
            task_index = futures[future]
            try:
                result = future.result()
                results.append({
                    'index': task_index,
                    'success': True,
                    'result': result
                })
            except Exception as e:
                results.append({
                    'index': task_index,
                    'success': False,
                    'error': str(e)
                })
        
        # Sort by original index
        results.sort(key=lambda x: x['index'])
        return results
    
    def process_agents_parallel(self, agents: List[Callable], 
                               user_request: str) -> List[Dict]:
        """Process multiple agents in parallel"""
        tasks = [
            {'func': agent, 'args': (user_request,)}
            for agent in agents
        ]
        return self.process_parallel(tasks)
    
    def map_parallel(self, func: Callable, items: List[Any]) -> List[Any]:
        """Apply function to items in parallel"""
        futures = [self.executor.submit(func, item) for item in items]
        return [future.result() for future in as_completed(futures)]
    
    def shutdown(self):
        """Shutdown executor"""
        self.executor.shutdown(wait=True)


class BatchProcessor:
    """Batch processing for efficiency"""
    
    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size
        self.batch = []
    
    def add(self, item: Any):
        """Add item to batch"""
        self.batch.append(item)
        if len(self.batch) >= self.batch_size:
            return self.flush()
        return None
    
    def flush(self) -> List[Any]:
        """Process and clear batch"""
        batch = self.batch.copy()
        self.batch.clear()
        return batch
    
    def process_batch(self, items: List[Any], processor: Callable) -> List[Any]:
        """Process items in batches"""
        results = []
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            batch_results = processor(batch)
            results.extend(batch_results)
        return results
