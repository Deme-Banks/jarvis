"""
Orchestrator Agent - Routes tasks to specialist agents
"""
from typing import List, Dict, Optional, Any
from openai import OpenAI
from prompts.orchestrator import ORCHESTRATOR_PROMPT
from prompts.specialists import (
    VOICE_UX_PROMPT,
    AUTOMATION_ENGINEER_PROMPT,
    PRODUCTIVITY_CHIEF_PROMPT,
    SECURITY_PRIVACY_PROMPT,
    CREATIVE_DIRECTOR_PROMPT,
    RESEARCH_ANALYST_PROMPT
)
import config


class Orchestrator:
    """Manages multi-agent system and routes tasks"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or config.Config.OPENAI_API_KEY)
        self.model = config.Config.DEFAULT_MODEL
        
        # Agent registry
        self.agents = {
            "voice_ux": VOICE_UX_PROMPT,
            "automation_engineer": AUTOMATION_ENGINEER_PROMPT,
            "productivity_chief": PRODUCTIVITY_CHIEF_PROMPT,
            "security_privacy": SECURITY_PRIVACY_PROMPT,
            "creative_director": CREATIVE_DIRECTOR_PROMPT,
            "research_analyst": RESEARCH_ANALYST_PROMPT
        }
    
    def _call_agent(self, agent_name: str, task: str, context: Optional[str] = None) -> str:
        """Call a specialist agent"""
        agent_prompt = self.agents.get(agent_name)
        if not agent_prompt:
            return f"Agent {agent_name} not found."
        
        full_prompt = f"{agent_prompt}\n\nTask: {task}"
        if context:
            full_prompt += f"\n\nContext: {context}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": agent_prompt},
                    {"role": "user", "content": task}
                ],
                temperature=config.Config.TEMPERATURE,
                max_tokens=config.Config.MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling {agent_name}: {str(e)}"
    
    def _determine_agents(self, user_request: str) -> List[str]:
        """Determine which agents to consult based on user request"""
        request_lower = user_request.lower()
        selected_agents = []
        
        # Simple keyword-based routing (can be enhanced with LLM)
        if any(word in request_lower for word in ["speak", "voice", "say", "tell", "pronounce"]):
            selected_agents.append("voice_ux")
        
        if any(word in request_lower for word in ["automate", "script", "api", "integrate", "code"]):
            selected_agents.append("automation_engineer")
        
        if any(word in request_lower for word in ["plan", "schedule", "prioritize", "task", "workflow"]):
            selected_agents.append("productivity_chief")
        
        if any(word in request_lower for word in ["security", "privacy", "safe", "secure", "protect"]):
            selected_agents.append("security_privacy")
        
        if any(word in request_lower for word in ["name", "brand", "creative", "tone", "style"]):
            selected_agents.append("creative_director")
        
        if any(word in request_lower for word in ["research", "fact", "verify", "check", "find"]):
            selected_agents.append("research_analyst")
        
        # Default: use orchestrator directly if no specific agent needed
        if not selected_agents:
            return []
        
        return selected_agents
    
    def process(self, user_request: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Process user request through multi-agent system
        
        Returns: Final response optimized for voice
        """
        # Determine which agents to consult
        agent_names = self._determine_agents(user_request)
        
        if not agent_names:
            # Direct orchestrator response
            return self._direct_response(user_request, context)
        
        # Collect responses from agents
        agent_responses = {}
        for agent_name in agent_names:
            agent_responses[agent_name] = self._call_agent(
                agent_name,
                user_request,
                str(context) if context else None
            )
        
        # Orchestrator synthesizes responses
        synthesis_prompt = f"""User request: {user_request}

Agent responses:
{chr(10).join(f"{name}: {response}" for name, response in agent_responses.items())}

Synthesize these into a single, concise voice-optimized response.
Format: (1) direct answer, (2) next step, (3) one question if needed."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": ORCHESTRATOR_PROMPT},
                    {"role": "user", "content": synthesis_prompt}
                ],
                temperature=config.Config.TEMPERATURE,
                max_tokens=config.Config.MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error processing request: {str(e)}"
    
    def _direct_response(self, user_request: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Direct response from orchestrator without agent delegation"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": ORCHESTRATOR_PROMPT},
                    {"role": "user", "content": user_request}
                ],
                temperature=config.Config.TEMPERATURE,
                max_tokens=config.Config.MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
