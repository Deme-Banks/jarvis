"""
Streaming LLM Responses for Real-time Output
"""
from typing import Generator, Optional, Callable
from llm.local_llm import LocalLLM
import config_pi as config


class StreamingLLM:
    """Streaming LLM for word-by-word responses"""
    
    def __init__(self, llm: Optional[LocalLLM] = None):
        self.llm = llm or LocalLLM()
    
    def stream_chat(self, message: str, system_prompt: Optional[str] = None) -> Generator[str, None, None]:
        """Stream chat response word by word"""
        try:
            # Use LLM's streaming capability
            for chunk in self.llm.stream_chat(message, system_prompt):
                yield chunk
        except Exception as e:
            # Fallback to non-streaming
            response = self.llm.chat(message, system_prompt)
            # Simulate streaming by yielding words
            words = response.split()
            for word in words:
                yield word + " "
    
    def stream_with_callback(self, message: str, callback: Callable[[str], None], 
                            system_prompt: Optional[str] = None) -> str:
        """Stream response with callback for each chunk"""
        full_response = ""
        for chunk in self.stream_chat(message, system_prompt):
            full_response += chunk
            callback(chunk)
        return full_response
