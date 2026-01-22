"""
Smart AI Selector - Automatically choose the best AI provider
"""
import os
from typing import Dict, Optional, List
from llm.cloud_llm import OpenAILLM, GeminiLLM, CloudLLMManager
from llm.local_llm import LocalLLM


class SmartAISelector:
    """Intelligently selects the best AI provider for each query"""
    
    def __init__(self):
        self.openai = OpenAILLM() if os.getenv("OPENAI_API_KEY") else None
        self.gemini = GeminiLLM() if os.getenv("GEMINI_API_KEY") else None
        self.local_llm = LocalLLM()
        self.preferences = {
            "image_generation": "openai",  # DALL-E is best for images
            "code_generation": "gemini",   # Gemini is good for code
            "general_chat": "auto",         # Auto-select
            "vision_analysis": "openai",   # GPT-4 Vision is advanced
            "fast_response": "gemini",      # Gemini is often faster
            "complex_reasoning": "openai",  # GPT-4 is better for complex tasks
        }
        self.usage_stats = {
            "openai": {"calls": 0, "success": 0, "errors": 0},
            "gemini": {"calls": 0, "success": 0, "errors": 0},
            "local": {"calls": 0, "success": 0, "errors": 0}
        }
    
    def _detect_query_type(self, query: str) -> str:
        """Detect the type of query"""
        query_lower = query.lower()
        
        # Image generation
        if any(word in query_lower for word in ["generate image", "create image", "make image", "draw", "picture"]):
            return "image_generation"
        
        # Code generation
        if any(word in query_lower for word in ["generate code", "write code", "create code", "program", "function", "script"]):
            return "code_generation"
        
        # Vision analysis
        if any(word in query_lower for word in ["analyze image", "what's in this image", "describe image", "see in image"]):
            return "vision_analysis"
        
        # Complex reasoning
        if any(word in query_lower for word in ["explain", "why", "how does", "analyze", "compare", "evaluate"]):
            return "complex_reasoning"
        
        # Fast/simple queries
        if len(query.split()) < 10:
            return "fast_response"
        
        return "general_chat"
    
    def _select_best_provider(self, query_type: str, query: str) -> Optional[object]:
        """Select the best AI provider for the query"""
        preference = self.preferences.get(query_type, "auto")
        
        # Check availability
        available_providers = []
        if self.openai and self.openai.check_available():
            available_providers.append(("openai", self.openai))
        if self.gemini and self.gemini.check_available():
            available_providers.append(("gemini", self.gemini))
        if self.local_llm.check_available():
            available_providers.append(("local", self.local_llm))
        
        if not available_providers:
            return None
        
        # If preference is set and available, use it
        if preference != "auto":
            for name, provider in available_providers:
                if name == preference:
                    return provider
        
        # Auto-select based on query characteristics
        if query_type == "image_generation":
            # OpenAI DALL-E for images
            for name, provider in available_providers:
                if name == "openai":
                    return provider
        
        if query_type == "code_generation":
            # Prefer Gemini for code
            for name, provider in available_providers:
                if name == "gemini":
                    return provider
        
        if query_type == "vision_analysis":
            # Prefer OpenAI GPT-4 Vision
            for name, provider in available_providers:
                if name == "openai":
                    return provider
        
        if query_type == "complex_reasoning":
            # Prefer OpenAI GPT-4 for complex reasoning
            for name, provider in available_providers:
                if name == "openai":
                    return provider
        
        # Default: prefer cloud over local, OpenAI over Gemini for general queries
        for name, provider in available_providers:
            if name == "openai":
                return provider
        for name, provider in available_providers:
            if name == "gemini":
                return provider
        for name, provider in available_providers:
            if name == "local":
                return provider
        
        return available_providers[0][1] if available_providers else None
    
    def get_best_response(self, query: str, system_prompt: Optional[str] = None,
                         context: Optional[List[Dict]] = None,
                         compare: bool = False) -> Dict:
        """Get the best response from the optimal AI provider"""
        query_type = self._detect_query_type(query)
        provider = self._select_best_provider(query_type, query)
        
        if not provider:
            return {
                "error": "No AI provider available",
                "query": query
            }
        
        provider_name = "unknown"
        if provider == self.openai:
            provider_name = "openai"
        elif provider == self.gemini:
            provider_name = "gemini"
        elif provider == self.local_llm:
            provider_name = "local"
        
        # If compare mode, try both and pick best
        if compare and query_type == "general_chat":
            return self._compare_and_select(query, system_prompt, context)
        
        try:
            # Get response
            response = provider.chat(query, system_prompt=system_prompt, context=context)
            
            # Update stats
            self.usage_stats[provider_name]["calls"] += 1
            self.usage_stats[provider_name]["success"] += 1
            
            return {
                "response": response,
                "provider": provider_name,
                "query_type": query_type,
                "success": True
            }
        except Exception as e:
            # Update error stats
            self.usage_stats[provider_name]["calls"] += 1
            self.usage_stats[provider_name]["errors"] += 1
            
            # Try fallback
            return self._try_fallback(query, system_prompt, context, provider_name)
    
    def _compare_and_select(self, query: str, system_prompt: Optional[str] = None,
                           context: Optional[List[Dict]] = None) -> Dict:
        """Compare responses from multiple providers and select best"""
        responses = []
        
        # Try OpenAI
        if self.openai and self.openai.check_available():
            try:
                openai_response = self.openai.chat(query, system_prompt, context)
                responses.append({
                    "provider": "openai",
                    "response": openai_response,
                    "length": len(openai_response),
                    "quality_score": self._score_response(openai_response)
                })
            except:
                pass
        
        # Try Gemini
        if self.gemini and self.gemini.check_available():
            try:
                gemini_response = self.gemini.chat(query, system_prompt, context)
                responses.append({
                    "provider": "gemini",
                    "response": gemini_response,
                    "length": len(gemini_response),
                    "quality_score": self._score_response(gemini_response)
                })
            except:
                pass
        
        if not responses:
            return {"error": "No providers available"}
        
        # Select best response (highest quality score)
        best = max(responses, key=lambda x: x["quality_score"])
        
        return {
            "response": best["response"],
            "provider": best["provider"],
            "compared": True,
            "all_responses": responses,
            "success": True
        }
    
    def _score_response(self, response: str) -> float:
        """Score response quality (simple heuristic)"""
        score = 0.0
        
        # Length score (not too short, not too long)
        length = len(response)
        if 50 <= length <= 2000:
            score += 0.3
        elif length > 2000:
            score += 0.2
        
        # Completeness (has multiple sentences)
        sentences = response.count('.') + response.count('!') + response.count('?')
        if sentences >= 2:
            score += 0.3
        
        # Detail (has specific information)
        if any(word in response.lower() for word in ["because", "example", "specifically", "details"]):
            score += 0.2
        
        # Clarity (not too many errors)
        if response.count('error') == 0 and response.count('Error') == 0:
            score += 0.2
        
        return score
    
    def _try_fallback(self, query: str, system_prompt: Optional[str] = None,
                     context: Optional[List[Dict]] = None,
                     failed_provider: str = None) -> Dict:
        """Try fallback providers if primary fails"""
        fallback_order = ["openai", "gemini", "local"]
        
        if failed_provider:
            fallback_order = [p for p in fallback_order if p != failed_provider]
        
        for provider_name in fallback_order:
            provider = None
            if provider_name == "openai" and self.openai:
                provider = self.openai
            elif provider_name == "gemini" and self.gemini:
                provider = self.gemini
            elif provider_name == "local":
                provider = self.local_llm
            
            if provider and provider.check_available():
                try:
                    response = provider.chat(query, system_prompt, context)
                    return {
                        "response": response,
                        "provider": provider_name,
                        "fallback": True,
                        "original_provider": failed_provider,
                        "success": True
                    }
                except:
                    continue
        
        return {
            "error": "All AI providers failed",
            "query": query
        }
    
    def get_stats(self) -> Dict:
        """Get usage statistics"""
        return {
            "usage": self.usage_stats,
            "preferences": self.preferences,
            "available": {
                "openai": self.openai.check_available() if self.openai else False,
                "gemini": self.gemini.check_available() if self.gemini else False,
                "local": self.local_llm.check_available()
            }
        }
