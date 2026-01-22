"""
Raspberry Pi Optimized Orchestrator (Local LLM)
"""
from typing import List, Dict, Optional, Any
from llm.local_llm import LocalLLM
from llm.cloud_llm import CloudLLMManager, OpenAILLM, GeminiLLM
from prompts.orchestrator import ORCHESTRATOR_PROMPT
from optimization.cache import ResponseCache
from optimization.precomputed import get_precomputed
import config_pi as config
from prompts.specialists import (
    VOICE_UX_PROMPT,
    AUTOMATION_ENGINEER_PROMPT,
    PRODUCTIVITY_CHIEF_PROMPT,
    SECURITY_PRIVACY_PROMPT,
    CREATIVE_DIRECTOR_PROMPT,
    RESEARCH_ANALYST_PROMPT
)
from ai_coding import AICodeGenerator, AICodeReader, AICodeBuilder
import config_pi as config


class PiOrchestrator:
    """Lightweight orchestrator for Raspberry Pi using local LLM + Cloud LLM"""
    
    def __init__(self, local_llm: Optional[LocalLLM] = None, 
                 cloud_llm: Optional[CloudLLMManager] = None,
                 prefer_cloud: bool = False):
        self.local_llm = local_llm or LocalLLM()
        self.cloud_manager = cloud_llm or CloudLLMManager()
        self.prefer_cloud = prefer_cloud
        
        # Auto-setup cloud LLMs if available
        if not self.cloud_manager.list_providers():
            self.cloud_manager.auto_setup()
        
        # Determine which LLM to use
        if self.prefer_cloud and self.cloud_manager.list_providers():
            try:
                self.llm = self.cloud_manager.get_provider()
            except:
                self.llm = self.local_llm
        elif self.local_llm.check_available():
            self.llm = self.local_llm
        elif self.cloud_manager.list_providers():
            try:
                self.llm = self.cloud_manager.get_provider()
            except:
                self.llm = self.local_llm
        else:
            self.llm = self.local_llm  # Fallback
        
        # Initialize AI coding tools
        self.code_generator = AICodeGenerator(self.llm)
        self.code_reader = AICodeReader(self.llm)
        self.code_builder = AICodeBuilder()
        
        # Initialize cache if enabled
        self.cache = None
        if config.PiConfig.ENABLE_RESPONSE_CACHE:
            self.cache = ResponseCache(
                max_size=config.PiConfig.CACHE_SIZE,
                ttl=config.PiConfig.CACHE_TTL
            )
        
        self.agents = {
            "voice_ux": VOICE_UX_PROMPT,
            "automation_engineer": AUTOMATION_ENGINEER_PROMPT,
            "productivity_chief": PRODUCTIVITY_CHIEF_PROMPT,
            "security_privacy": SECURITY_PRIVACY_PROMPT,
            "creative_director": CREATIVE_DIRECTOR_PROMPT,
            "research_analyst": RESEARCH_ANALYST_PROMPT
        }
    
    def _call_agent(self, agent_name: str, task: str) -> str:
        """Call a specialist agent (simplified for Pi)"""
        if not config.PiConfig.ENABLE_ALL_AGENTS:
            # Skip agent delegation for performance
            return ""
        
        agent_prompt = self.agents.get(agent_name)
        if not agent_prompt:
            return ""
        
        try:
            return self.llm.chat(
                task,
                system_prompt=agent_prompt
            )
        except Exception as e:
            return f"Agent error: {str(e)}"
    
    def _determine_agents(self, user_request: str) -> List[str]:
        """Determine which agents to consult"""
        if not config.PiConfig.ENABLE_ALL_AGENTS:
            return []
        
        request_lower = user_request.lower()
        selected_agents = []
        
        # Simple keyword routing
        if any(word in request_lower for word in ["speak", "voice", "say"]):
            selected_agents.append("voice_ux")
        if any(word in request_lower for word in ["automate", "script", "code"]):
            selected_agents.append("automation_engineer")
        if any(word in request_lower for word in ["plan", "schedule", "task"]):
            selected_agents.append("productivity_chief")
        
        return selected_agents[:config.PiConfig.MAX_CONCURRENT_AGENTS]
    
    def process(self, user_request: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process user request (optimized for Pi)"""
        # Check for coding requests first
        coding_response = self._handle_coding_request(user_request)
        if coding_response:
            return coding_response
        
        # Check pre-computed responses first (fastest)
        if config.PiConfig.USE_PRECOMPUTED:
            precomputed = get_precomputed(user_request)
            if precomputed:
                return precomputed
        
        # Check cache
        if self.cache:
            cached = self.cache.get(user_request, context)
            if cached:
                return cached
        
        # For Pi, use direct orchestrator response (faster)
        # Only use agents if explicitly enabled and needed
        
        agent_names = self._determine_agents(user_request)
        
        if not agent_names:
            # Direct response
            response = self.llm.chat(
                user_request,
                system_prompt=ORCHESTRATOR_PROMPT
            )
            
            # Cache response
            if self.cache:
                self.cache.set(user_request, response, context)
            
            return response
        
        # Collect agent responses (sequential for Pi)
        agent_responses = {}
        for agent_name in agent_names:
            agent_responses[agent_name] = self._call_agent(agent_name, user_request)
        
        # Synthesize
        synthesis = f"""User: {user_request}

Agent insights:
{chr(10).join(f"{name}: {resp}" for name, resp in agent_responses.items() if resp)}

Provide a concise voice-optimized response."""
        
        response = self.llm.chat(
            synthesis,
            system_prompt=ORCHESTRATOR_PROMPT
        )
        
        # Cache response
        if self.cache:
            self.cache.set(user_request, response, context)
        
        return response