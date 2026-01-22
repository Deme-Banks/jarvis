"""
Async Optimizer - Optimize async operations
"""
import asyncio
from typing import List, Callable, Any, Coroutine
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import functools


class AsyncOptimizer:
    """Optimize async operations"""
    
    def __init__(self, max_workers: int = 10):
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        self.process_pool = ProcessPoolExecutor(max_workers=max_workers)
    
    async def run_parallel(self, coroutines: List[Coroutine]) -> List[Any]:
        """Run multiple coroutines in parallel"""
        return await asyncio.gather(*coroutines)
    
    async def run_batch(self, tasks: List[Callable], batch_size: int = 5) -> List[Any]:
        """Run tasks in batches"""
        results = []
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            batch_results = await asyncio.gather(*[self._run_task(task) for task in batch])
            results.extend(batch_results)
        return results
    
    async def _run_task(self, task: Callable) -> Any:
        """Run a single task"""
        if asyncio.iscoroutinefunction(task):
            return await task()
        else:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self.thread_pool, task)
    
    def to_async(self, func: Callable):
        """Convert sync function to async"""
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self.thread_pool, functools.partial(func, *args, **kwargs))
        return wrapper
    
    def shutdown(self):
        """Shutdown thread and process pools"""
        self.thread_pool.shutdown(wait=True)
        self.process_pool.shutdown(wait=True)


def async_cache(ttl: int = 300):
    """Cache async function results"""
    cache = {}
    
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = str(args) + str(kwargs)
            if cache_key in cache:
                result, timestamp = cache[cache_key]
                if time.time() - timestamp < ttl:
                    return result
            
            result = await func(*args, **kwargs)
            cache[cache_key] = (result, time.time())
            return result
        return wrapper
    return decorator
