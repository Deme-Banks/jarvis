"""
LLM-Powered Learning - Uses AI to learn and improve
"""
from typing import Dict, List, Optional
from learning.memory import MemorySystem
from llm.local_llm import LocalLLM


class LLMLearner:
    """Uses LLM to learn patterns and improve responses"""
    
    def __init__(self, memory: MemorySystem, llm: LocalLLM):
        self.memory = memory
        self.llm = llm
    
    def learn_from_conversations(self, limit: int = 50):
        """Analyze conversations and learn patterns using LLM"""
        if not self.memory.conversations:
            return {}
        
        recent_convs = self.memory.conversations[-limit:]
        
        # Create learning prompt
        prompt = f"""Analyze these conversations and extract learning insights:

Conversations:
{self._format_conversations(recent_convs)}

Extract:
1. User preferences (response style, topics, etc.)
2. Common patterns in requests
3. Successful response patterns
4. Areas for improvement

Return as structured insights."""
        
        try:
            response = self.llm.chat(prompt, system_prompt="You are a learning analysis system.")
            
            # Extract insights
            insights = self._parse_insights(response)
            
            # Apply insights to memory
            self._apply_insights(insights)
            
            return insights
        except Exception as e:
            print(f"LLM learning error: {e}")
            return {}
    
    def _format_conversations(self, conversations: List[Dict]) -> str:
        """Format conversations for LLM"""
        formatted = []
        for conv in conversations:
            formatted.append(f"User: {conv['user']}")
            formatted.append(f"Assistant: {conv['assistant']}")
            formatted.append("---")
        return "\n".join(formatted)
    
    def _parse_insights(self, llm_response: str) -> Dict:
        """Parse insights from LLM response"""
        insights = {
            "preferences": {},
            "patterns": [],
            "improvements": []
        }
        
        # Simple parsing (can be enhanced)
        lines = llm_response.split("\n")
        current_section = None
        
        for line in lines:
            if "preference" in line.lower():
                current_section = "preferences"
            elif "pattern" in line.lower():
                current_section = "patterns"
            elif "improvement" in line.lower():
                current_section = "improvements"
            elif line.strip() and current_section:
                insights[current_section].append(line.strip())
        
        return insights
    
    def _apply_insights(self, insights: Dict):
        """Apply learned insights to memory"""
        # Apply preferences
        for pref in insights.get("preferences", []):
            if ":" in pref:
                key, value = pref.split(":", 1)
                self.memory.learn_preference(key.strip(), value.strip())
    
    def improve_response(self, user_input: str, base_response: str) -> str:
        """Use LLM to improve response based on learned patterns"""
        # Get context
        context = self.memory.get_recent_context(5)
        preferences = self.memory.preferences
        
        prompt = f"""Improve this response based on learned patterns:

User input: {user_input}
Base response: {base_response}

User preferences: {preferences}
Recent context: {self._format_conversations(context)}

Improve the response to be more helpful, personalized, and aligned with user preferences."""
        
        try:
            improved = self.llm.chat(prompt, system_prompt="You improve responses based on learned patterns.")
            return improved
        except:
            return base_response
    
    def generate_personalized_response(self, user_input: str, 
                                     base_response: str) -> str:
        """Generate personalized response using learned patterns"""
        user_style = self.memory.analyze_user_style()
        knowledge = self._get_relevant_knowledge(user_input)
        
        prompt = f"""Generate a personalized response:

User input: {user_input}
Base response: {base_response}

User communication style: {user_style}
Relevant knowledge: {knowledge}

Make the response personalized and context-aware."""
        
        try:
            personalized = self.llm.chat(
                prompt, 
                system_prompt="You generate personalized, context-aware responses."
            )
            return personalized
        except:
            return base_response
    
    def _get_relevant_knowledge(self, user_input: str) -> List[str]:
        """Get relevant knowledge for user input"""
        keywords = [word for word in user_input.lower().split() if len(word) > 4]
        relevant = []
        
        for keyword in keywords:
            knowledge = self.memory.get_knowledge(keyword)
            if knowledge:
                relevant.extend([k["information"] for k in knowledge[:2]])
        
        return relevant
