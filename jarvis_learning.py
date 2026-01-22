"""
JARVIS with Self-Learning Capabilities
"""
import sys
from jarvis_pi import JarvisPi
from learning.memory import MemorySystem
from learning.feedback_loop import FeedbackLoop
from llm.local_llm import LocalLLM
import config_pi as config


class JarvisLearning(JarvisPi):
    """JARVIS with self-learning capabilities"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize learning system
        self.memory = MemorySystem()
        self.feedback_loop = FeedbackLoop(self.memory, self.llm)
        
        print("=" * 60)
        print("JARVIS LEARNING MODE ENABLED")
        print("=" * 60)
        print("JARVIS will learn from every interaction")
        print("Preferences, patterns, and knowledge will be saved")
        print("=" * 60)
    
    def _process_audio(self, audio_data: bytes):
        """Process audio with learning"""
        # Transcribe
        text = self.stt.transcribe(audio_data)
        if not text or len(text.strip()) < 2:
            return
        
        print(f"You: {text}")
        
        # Check for learning-related commands
        text_lower = text.lower()
        if "what have you learned" in text_lower or "learning stats" in text_lower:
            stats = self.feedback_loop.get_learning_stats()
            response = f"I've learned from {stats['total_interactions']} interactions. "
            response += f"I know {stats['learned_preferences']} preferences and "
            response += f"{stats['knowledge_topics']} topics. "
            response += "Would you like more details?"
        elif "forget everything" in text_lower or "reset learning" in text_lower:
            confirm = input("Are you sure you want to reset all learning? (yes/no): ")
            if confirm.lower() == "yes":
                self.feedback_loop.reset_learning()
                response = "All learning data has been reset."
            else:
                response = "Reset cancelled."
        else:
            # Normal processing
            response = self.orchestrator.process(
                text,
                context={
                    "memory": self.context_memory[-5:],
                    "learned_preferences": self.memory.preferences,
                    "knowledge": self.memory.get_recent_context(3)
                }
            )
            
            # Improve response using learned patterns
            response = self.feedback_loop.improve_next_response(text, response)
            
            # Learn from interaction
            self.feedback_loop.process_interaction(text, response)
        
        # Update memory
        self.context_memory.append({"user": text, "assistant": response})
        if len(self.context_memory) > config.PiConfig.CONTEXT_MEMORY_SIZE:
            self.context_memory = self.context_memory[-config.PiConfig.CONTEXT_MEMORY_SIZE:]
        
        print(f"JARVIS: {response}")
        
        # Speak response
        self._speak(response)
    
    def get_learning_report(self) -> str:
        """Get learning report"""
        stats = self.feedback_loop.get_learning_stats()
        
        report = f"""
JARVIS Learning Report
======================
Total Interactions: {stats['total_interactions']}
Learned Preferences: {stats['learned_preferences']}
Knowledge Topics: {stats['knowledge_topics']}
Learned Patterns: {stats['learned_patterns']}
Improvements Made: {stats['improvement_count']}

User Communication Style:
- Average message length: {stats['user_style'].get('avg_message_length', 0):.1f} chars
- Question ratio: {stats['user_style'].get('question_ratio', 0):.1%}
- Command ratio: {stats['user_style'].get('command_ratio', 0):.1%}
"""
        return report


def main():
    """Main entry point"""
    print("\n" + "=" * 60)
    print("JARVIS SELF-LEARNING MODE")
    print("=" * 60)
    print("\nJARVIS will:")
    print("- Learn your preferences and communication style")
    print("- Remember important information")
    print("- Improve responses based on past interactions")
    print("- Build a knowledge base over time")
    print("\n" + "=" * 60)
    
    jarvis = JarvisLearning()
    jarvis.start()


if __name__ == "__main__":
    main()
