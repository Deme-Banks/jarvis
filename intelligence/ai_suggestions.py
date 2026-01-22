"""
AI-Powered Proactive Suggestions
"""
from typing import Dict, List, Optional
from datetime import datetime
from llm.cloud_llm import CloudLLMManager, OpenAILLM, GeminiLLM
from llm.local_llm import LocalLLM


class AISuggestions:
    """AI-powered proactive suggestions"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self._setup_llm()
        self.context_history = []
    
    def _setup_llm(self):
        """Setup LLM for suggestions"""
        if self.llm is None:
            manager = CloudLLMManager()
            manager.auto_setup()
            
            if manager.list_providers():
                self.llm = manager.get_provider()
            else:
                local_llm = LocalLLM()
                if local_llm.check_available():
                    self.llm = local_llm
    
    def get_proactive_suggestions(self, context: Dict) -> List[str]:
        """Get proactive suggestions based on context"""
        recent_commands = context.get('recent_commands', [])
        time_of_day = context.get('time_of_day', 'afternoon')
        current_task = context.get('current_task')
        
        prompt = f"""Based on this context, suggest 3-5 helpful actions the user might want to take:

Recent commands: {recent_commands[-5:] if recent_commands else 'None'}
Time of day: {time_of_day}
Current task: {current_task or 'None'}

Provide practical, actionable suggestions relevant to cybersecurity testing and automation.
Format as a simple list, one per line."""
        
        try:
            suggestions_text = self.llm.chat(
                prompt,
                system_prompt="You are a helpful assistant providing proactive suggestions."
            )
            
            # Parse suggestions
            suggestions = [s.strip() for s in suggestions_text.split('\n') if s.strip() and not s.strip().startswith('-')]
            suggestions = [s.lstrip('- ').lstrip('* ') for s in suggestions]  # Remove bullets
            
            return suggestions[:5]
        except:
            # Fallback suggestions
            return [
                "Create a security test workflow",
                "Run system health check",
                "Review recent commands",
                "Generate a security report"
            ]
    
    def suggest_optimization(self, performance_data: Dict) -> List[str]:
        """Suggest optimizations based on performance"""
        suggestions = []
        
        avg_response_time = performance_data.get('avg_response_time', 0)
        if avg_response_time > 5.0:
            suggestions.append("Enable GPU acceleration for faster responses")
            suggestions.append("Use model quantization to reduce response time")
        
        cache_hit_rate = performance_data.get('cache_hit_rate', 0)
        if cache_hit_rate < 0.3:
            suggestions.append("Increase cache size for better performance")
        
        memory_usage = performance_data.get('memory_usage', 0)
        if memory_usage > 80:
            suggestions.append("Reduce cache size to free memory")
            suggestions.append("Disable unused agents")
        
        return suggestions
    
    def suggest_security_improvements(self, security_data: Dict) -> List[str]:
        """Suggest security improvements"""
        suggestions = []
        
        # Analyze security practices
        if security_data.get('isolated_mode', True):
            suggestions.append("Good: Isolated mode is enabled")
        else:
            suggestions.append("Enable isolated mode for safer testing")
        
        if not security_data.get('backup_recent', False):
            suggestions.append("Create a backup of your work")
        
        if security_data.get('error_rate', 0) > 0.1:
            suggestions.append("Review error logs for security issues")
        
        return suggestions
