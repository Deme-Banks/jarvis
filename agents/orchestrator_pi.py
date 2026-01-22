"""
Raspberry Pi Optimized Orchestrator (Local LLM)
"""
from typing import List, Dict, Optional, Any
from llm.local_llm import LocalLLM
from prompts.orchestrator import ORCHESTRATOR_PROMPT
from prompts.specialists import (
    VOICE_UX_PROMPT,
    AUTOMATION_ENGINEER_PROMPT,
    PRODUCTIVITY_CHIEF_PROMPT,
    SECURITY_PRIVACY_PROMPT,
    CREATIVE_DIRECTOR_PROMPT,
    RESEARCH_ANALYST_PROMPT
)
import config_pi as config


class PiOrchestrator:
    """Lightweight orchestrator for Raspberry Pi using local LLM"""
    
    def __init__(self, local_llm: Optional[LocalLLM] = None):
        self.llm = local_llm or LocalLLM()
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
        # For Pi, use direct orchestrator response (faster)
        # Only use agents if explicitly enabled and needed
        
        agent_names = self._determine_agents(user_request)
        
        if not agent_names:
            # Direct response
            return self.llm.chat(
                user_request,
                system_prompt=ORCHESTRATOR_PROMPT
            )
        
        # Collect agent responses (sequential for Pi)
        agent_responses = {}
        for agent_name in agent_names:
            agent_responses[agent_name] = self._call_agent(agent_name, user_request)
        
        # Synthesize
        synthesis = f"""User: {user_request}

Agent insights:
{chr(10).join(f"{name}: {resp}" for name, resp in agent_responses.items() if resp)}

Provide a concise voice-optimized response."""
        
        return self.llm.chat(
            synthesis,
            system_prompt=ORCHESTRATOR_PROMPT
        )
