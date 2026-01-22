"""
Parallel Orchestrator for Faster Multi-Agent Processing
"""
from typing import List, Dict, Optional, Any
from agents.orchestrator_pi import PiOrchestrator
from optimization.parallel_processing import ParallelProcessor
from prompts.orchestrator import ORCHESTRATOR_PROMPT
from prompts.specialists import (
    VOICE_UX_PROMPT,
    AUTOMATION_ENGINEER_PROMPT,
    PRODUCTIVITY_CHIEF_PROMPT,
    SECURITY_PRIVACY_PROMPT,
    CREATIVE_DIRECTOR_PROMPT,
    RESEARCH_ANALYST_PROMPT
)
from llm.local_llm import LocalLLM
import config_pi as config


class ParallelOrchestrator(PiOrchestrator):
    """Orchestrator with parallel agent processing"""
    
    def __init__(self, local_llm: Optional[LocalLLM] = None):
        super().__init__(local_llm)
        self.parallel_processor = ParallelProcessor(
            max_workers=config.PiConfig.MAX_CONCURRENT_AGENTS
        )
    
    def _call_agents_parallel(self, agent_names: List[str], task: str) -> Dict[str, str]:
        """Call multiple agents in parallel"""
        if not config.PiConfig.ENABLE_ALL_AGENTS:
            return {}
        
        # Create agent functions
        agent_functions = []
        for agent_name in agent_names:
            agent_prompt = self.agents.get(agent_name)
            if agent_prompt:
                def create_agent_func(name, prompt):
                    def agent_func(request):
                        return self.llm.chat(request, system_prompt=prompt)
                    return agent_func
                
                agent_functions.append({
                    'func': create_agent_func(agent_name, agent_prompt),
                    'args': (task,)
                })
        
        # Process in parallel
        results = self.parallel_processor.process_parallel(agent_functions)
        
        # Build response dict
        agent_responses = {}
        for i, result in enumerate(results):
            if result['success']:
                agent_name = agent_names[i]
                agent_responses[agent_name] = result['result']
        
        return agent_responses
    
    def process(self, user_request: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process with parallel agent execution"""
        # Check cache first (from parent)
        if config.PiConfig.USE_PRECOMPUTED:
            from optimization.precomputed import get_precomputed
            precomputed = get_precomputed(user_request)
            if precomputed:
                return precomputed
        
        if self.cache:
            cached = self.cache.get(user_request, context)
            if cached:
                return cached
        
        # Determine agents
        agent_names = self._determine_agents(user_request)
        
        if not agent_names:
            # Direct response
            response = self.llm.chat(
                user_request,
                system_prompt=ORCHESTRATOR_PROMPT
            )
            if self.cache:
                self.cache.set(user_request, response, context)
            return response
        
        # Process agents in parallel
        agent_responses = self._call_agents_parallel(agent_names, user_request)
        
        # Synthesize
        synthesis = f"""User: {user_request}

Agent insights:
{chr(10).join(f"{name}: {resp}" for name, resp in agent_responses.items() if resp)}

Provide a concise voice-optimized response."""
        
        response = self.llm.chat(
            synthesis,
            system_prompt=ORCHESTRATOR_PROMPT
        )
        
        if self.cache:
            self.cache.set(user_request, response, context)
        
        return response
