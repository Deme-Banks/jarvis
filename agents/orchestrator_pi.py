"""
Raspberry Pi Optimized Orchestrator (Local LLM) - Optimized with lazy loading
"""
from typing import List, Dict, Optional, Any
from utils.lazy_loader import LazyLoader
from utils.cache_optimizer import SmartCache
from utils.performance_profiler import PerformanceProfiler
from prompts.orchestrator import ORCHESTRATOR_PROMPT
from optimization.precomputed import get_precomputed
import config_pi as config


class PiOrchestrator:
    """Lightweight orchestrator for Raspberry Pi using local LLM + Cloud LLM - Optimized"""
    
    def __init__(self, local_llm: Optional[Any] = None, 
                 cloud_llm: Optional[Any] = None,
                 prefer_cloud: bool = False):
        self.prefer_cloud = prefer_cloud
        
        # Lazy load components - don't initialize until needed
        self._local_llm = local_llm
        self._cloud_manager = cloud_llm
        self._ai_selector = None
        self._llm = None
        self._code_generator = None
        self._code_reader = None
        self._code_builder = None
        self._vision_analyzer = None
        self._document_analyzer = None
        self._web_search = None
        
        # Use optimized SmartCache instead of ResponseCache
        self.cache = SmartCache() if config.PiConfig.ENABLE_RESPONSE_CACHE else None
        
        # Performance profiler
        self.profiler = PerformanceProfiler()
        
        # Lazy load prompts only when needed
        self._prompts_loaded = False
        self._agents = None
    
    @property
    def local_llm(self):
        """Lazy load local LLM"""
        if self._local_llm is None:
            llm_module = LazyLoader.get("local_llm")
            self._local_llm = llm_module.LocalLLM()
        return self._local_llm
    
    @property
    def cloud_manager(self):
        """Lazy load cloud LLM manager"""
        if self._cloud_manager is None:
            llm_module = LazyLoader.get("cloud_llm")
            self._cloud_manager = llm_module.CloudLLMManager()
            if not self._cloud_manager.list_providers():
                self._cloud_manager.auto_setup()
        return self._cloud_manager
    
    @property
    def ai_selector(self):
        """Lazy load AI selector"""
        if self._ai_selector is None:
            selector_module = LazyLoader.get("smart_ai_selector")
            self._ai_selector = selector_module.SmartAISelector()
        return self._ai_selector
    
    @property
    def llm(self):
        """Lazy load LLM"""
        if self._llm is None:
            if self.prefer_cloud and self.cloud_manager.list_providers():
                try:
                    self._llm = self.cloud_manager.get_provider()
                except:
                    self._llm = self.local_llm
            elif self.local_llm.check_available():
                self._llm = self.local_llm
            elif self.cloud_manager.list_providers():
                try:
                    self._llm = self.cloud_manager.get_provider()
                except:
                    self._llm = self.local_llm
            else:
                self._llm = self.local_llm
        return self._llm
    
    @property
    def code_generator(self):
        """Lazy load code generator"""
        if self._code_generator is None:
            coding_module = LazyLoader.get("ai_code_generator")
            self._code_generator = coding_module.AICodeGenerator(self.llm)
        return self._code_generator
    
    @property
    def code_reader(self):
        """Lazy load code reader"""
        if self._code_reader is None:
            coding_module = LazyLoader.get("ai_code_reader")
            self._code_reader = coding_module.AICodeReader(self.llm)
        return self._code_reader
    
    @property
    def code_builder(self):
        """Lazy load code builder"""
        if self._code_builder is None:
            coding_module = LazyLoader.get("ai_code_builder")
            self._code_builder = coding_module.AICodeBuilder()
        return self._code_builder
    
    @property
    def vision_analyzer(self):
        """Lazy load vision analyzer"""
        if self._vision_analyzer is None:
            vision_module = LazyLoader.get("vision_analysis")
            self._vision_analyzer = vision_module.VisionAnalyzer(self.llm)
        return self._vision_analyzer
    
    @property
    def document_analyzer(self):
        """Lazy load document analyzer"""
        if self._document_analyzer is None:
            doc_module = LazyLoader.get("document_analyzer")
            self._document_analyzer = doc_module.DocumentAnalyzer(self.llm)
        return self._document_analyzer
    
    @property
    def web_search(self):
        """Lazy load web search"""
        if self._web_search is None:
            web_module = LazyLoader.get("web_search")
            self._web_search = web_module.WebSearch()
        return self._web_search
    
    @property
    def agents(self):
        """Lazy load agent prompts"""
        if not self._prompts_loaded:
            prompts_module = LazyLoader.get("specialists")
            self._agents = {
                "voice_ux": prompts_module.VOICE_UX_PROMPT,
                "automation_engineer": prompts_module.AUTOMATION_ENGINEER_PROMPT,
                "productivity_chief": prompts_module.PRODUCTIVITY_CHIEF_PROMPT,
                "security_privacy": prompts_module.SECURITY_PRIVACY_PROMPT,
                "creative_director": prompts_module.CREATIVE_DIRECTOR_PROMPT,
                "research_analyst": prompts_module.RESEARCH_ANALYST_PROMPT
            }
            self._prompts_loaded = True
        return self._agents
    
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
            # Use Smart AI Selector to get the best response
            orchestrator_prompt = LazyLoader.get("orchestrator_prompt").ORCHESTRATOR_PROMPT
            result = self.ai_selector.get_best_response(
                user_request,
                system_prompt=orchestrator_prompt,
                context=context
            )
            
            if result.get("success"):
                response = result["response"]
                provider_used = result.get("provider", "unknown")
                
                # Cache response with optimized cache
                if self.cache:
                    self.cache.set(user_request, response)
                    # Also cache semantically
                    self.cache.set_semantic(user_request, response)
                
                # Optionally include provider info in response (for transparency)
                # For voice responses, we'll just return the response
                return response
            else:
                # Fallback to direct LLM call if selector fails
                orchestrator_prompt = LazyLoader.get("orchestrator_prompt").ORCHESTRATOR_PROMPT
                response = self.llm.chat(
                    user_request,
                    system_prompt=orchestrator_prompt
                )
                
                if self.cache:
                    self.cache.set(user_request, response)
                    self.cache.set_semantic(user_request, response)
                
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
        
        # Use Smart AI Selector for synthesis too
        orchestrator_prompt = LazyLoader.get("orchestrator_prompt").ORCHESTRATOR_PROMPT
        result = self.ai_selector.get_best_response(
            synthesis,
            system_prompt=orchestrator_prompt,
            context=context
        )
        
        if result.get("success"):
            response = result["response"]
        else:
            # Fallback
            orchestrator_prompt = LazyLoader.get("orchestrator_prompt").ORCHESTRATOR_PROMPT
            response = self.llm.chat(
                synthesis,
                system_prompt=orchestrator_prompt
            )
        
        # Cache response with optimized cache
        if self.cache:
            self.cache.set(user_request, response)
            self.cache.set_semantic(user_request, response)
        
        return response