"""
Async Operations for Non-blocking I/O
"""
import asyncio
import threading
from typing import Callable, Any, Optional
from concurrent.futures import ThreadPoolExecutor


class AsyncOperations:
    """Async operations manager"""
    
    def __init__(self, max_workers: int = 5):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.loop = None
        self.loop_thread = None
    
    def start_loop(self):
        """Start async event loop in background thread"""
        if self.loop is None:
            self.loop = asyncio.new_event_loop()
            self.loop_thread = threading.Thread(target=self._run_loop, daemon=True)
            self.loop_thread.start()
    
    def _run_loop(self):
        """Run event loop"""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
    
    def run_async(self, coro):
        """Run async coroutine"""
        if self.loop is None:
            self.start_loop()
        return asyncio.run_coroutine_threadsafe(coro, self.loop)
    
    def run_in_executor(self, func: Callable, *args, **kwargs):
        """Run function in thread pool"""
        return self.executor.submit(func, *args, **kwargs)
    
    def async_file_read(self, filepath: str) -> asyncio.Future:
        """Async file read"""
        async def read():
            with open(filepath, 'r') as f:
                return f.read()
        return self.run_async(read())
    
    def async_file_write(self, filepath: str, content: str) -> asyncio.Future:
        """Async file write"""
        async def write():
            with open(filepath, 'w') as f:
                f.write(content)
        return self.run_async(write())
    
    def async_http_request(self, url: str, method: str = "GET") -> asyncio.Future:
        """Async HTTP request"""
        async def request():
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url) as response:
                    return await response.text()
        return self.run_async(request())
    
    def shutdown(self):
        """Shutdown async operations"""
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        self.executor.shutdown(wait=True)


# Global async operations instance
_async_ops = AsyncOperations()


def get_async_ops() -> AsyncOperations:
    """Get global async operations instance"""
    return _async_ops
