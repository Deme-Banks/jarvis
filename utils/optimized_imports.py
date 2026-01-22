"""
Optimized Imports - Centralized import management
"""
# Register all modules for lazy loading
from utils.lazy_loader import LazyLoader

# LLM Modules
LazyLoader.register("local_llm", "llm.local_llm")
LazyLoader.register("cloud_llm", "llm.cloud_llm")
LazyLoader.register("smart_ai_selector", "llm.smart_ai_selector")

# AI Coding Modules
LazyLoader.register("ai_code_generator", "ai_coding")
LazyLoader.register("ai_code_reader", "ai_coding")
LazyLoader.register("ai_code_builder", "ai_coding")
LazyLoader.register("vision_analysis", "ai_coding.vision_analysis")
LazyLoader.register("document_analyzer", "ai_coding.document_analyzer")
LazyLoader.register("web_search", "ai_coding.web_search")

# Cybersecurity Modules
LazyLoader.register("enhanced_security", "cybersecurity.enhanced_integration")
LazyLoader.register("malware_lab", "cybersecurity.malware_lab")
LazyLoader.register("ddos_tester", "cybersecurity.ddos_tester")

# Voice Modules
LazyLoader.register("voice_interface", "voice.voice_interface_pi")
LazyLoader.register("stt", "voice.stt_pi")
LazyLoader.register("tts", "voice.tts_pi")

# Prompt Modules
LazyLoader.register("orchestrator_prompt", "prompts.orchestrator")
LazyLoader.register("specialists", "prompts.specialists")
