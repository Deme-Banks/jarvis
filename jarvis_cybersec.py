"""
JARVIS with Cybersecurity Testing Capabilities
WARNING: For authorized testing and educational purposes only.
"""
import sys
from jarvis_pi import JarvisPi
from cybersecurity.enhanced_integration import EnhancedCybersecurityOrchestrator
from agents.orchestrator_pi import PiOrchestrator
from llm.local_llm import LocalLLM
import config_pi as config


class JarvisCybersec(JarvisPi):
    """JARVIS with integrated cybersecurity testing capabilities"""
    
    def __init__(self):
        super().__init__()
        self.cybersec_orchestrator = EnhancedCybersecurityOrchestrator(self.orchestrator)
        
        print("=" * 60)
        print("JARVIS CYBERSECURITY MODE")
        print("=" * 60)
        print("WARNING: For authorized testing and educational purposes only.")
        print("Only use on networks you own or have explicit authorization to test.")
        print("Unauthorized use is illegal and unethical.")
        print("=" * 60)
    
    def _process_audio(self, audio_data: bytes):
        """Process audio with cybersecurity capabilities"""
        # Transcribe
        text = self.stt.transcribe(audio_data)
        if not text or len(text.strip()) < 2:
            return
        
        print(f"You: {text}")
        
        # Check if it's a security-related request
        text_lower = text.lower()
        is_security_request = any(word in text_lower for word in [
            "virus", "malware", "ddos", "attack", "hack", "exploit",
            "keylogger", "reverse shell", "scan", "vulnerability",
            "penetration", "pentest", "security test"
        ])
        
        if is_security_request:
            # Route to cybersecurity module
            response = self.cybersec_orchestrator.handle_security_request(text)
        else:
            # Normal JARVIS processing
            response = self.orchestrator.process(
                text,
                context={"memory": self.context_memory[-5:]}
            )
        
        # Update memory
        self.context_memory.append({"user": text, "assistant": response})
        if len(self.context_memory) > config.PiConfig.CONTEXT_MEMORY_SIZE:
            self.context_memory = self.context_memory[-config.PiConfig.CONTEXT_MEMORY_SIZE:]
        
        print(f"JARVIS: {response}")
        
        # Speak response
        self._speak(response)


def main():
    """Main entry point"""
    print("\n" + "=" * 60)
    print("JARVIS CYBERSECURITY TESTING MODULE")
    print("=" * 60)
    print("\nWARNINGS:")
    print("1. For authorized testing and educational purposes ONLY")
    print("2. Only test networks you own or have written authorization")
    print("3. Use in isolated VMs and test environments")
    print("4. Unauthorized use is ILLEGAL (Computer Fraud and Abuse Act)")
    print("5. You are responsible for your actions")
    print("\n" + "=" * 60)
    
    response = input("\nDo you understand and agree to use this responsibly? (yes/no): ")
    if response.lower() != "yes":
        print("Exiting. Use responsibly.")
        sys.exit(0)
    
    jarvis = JarvisCybersec()
    jarvis.start()


if __name__ == "__main__":
    main()
