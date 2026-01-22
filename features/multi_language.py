"""
Multi-Language Support
"""
from typing import Dict, List, Optional
import os
import json


class MultiLanguageSupport:
    """Multi-language support for JARVIS"""
    
    def __init__(self, language: str = "en"):
        self.language = language
        self.translations = self._load_translations()
        self.supported_languages = ['en', 'es', 'fr', 'de', 'it', 'pt', 'zh', 'ja', 'ko', 'ru']
    
    def _load_translations(self) -> Dict:
        """Load translations"""
        translations = {
            'en': {
                'wake_word': 'jarvis',
                'greeting': 'Hello, I am JARVIS. How can I help you?',
                'listening': 'Listening...',
                'processing': 'Processing...',
                'error': 'I encountered an error.',
                'unknown_command': "I don't understand that command.",
                'help': 'I can help with malware creation, code generation, network testing, and more.'
            },
            'es': {
                'wake_word': 'jarvis',
                'greeting': 'Hola, soy JARVIS. ¿Cómo puedo ayudarte?',
                'listening': 'Escuchando...',
                'processing': 'Procesando...',
                'error': 'Encontré un error.',
                'unknown_command': 'No entiendo ese comando.',
                'help': 'Puedo ayudar con creación de malware, generación de código, pruebas de red y más.'
            },
            'fr': {
                'wake_word': 'jarvis',
                'greeting': 'Bonjour, je suis JARVIS. Comment puis-je vous aider?',
                'listening': 'Écoute...',
                'processing': 'Traitement...',
                'error': "J'ai rencontré une erreur.",
                'unknown_command': "Je ne comprends pas cette commande.",
                'help': 'Je peux aider avec la création de malware, la génération de code, les tests réseau et plus encore.'
            }
        }
        
        # Load from file if exists
        trans_file = f"./config/translations_{self.language}.json"
        if os.path.exists(trans_file):
            try:
                with open(trans_file, 'r') as f:
                    file_trans = json.load(f)
                    if self.language in translations:
                        translations[self.language].update(file_trans)
                    else:
                        translations[self.language] = file_trans
            except:
                pass
        
        return translations
    
    def translate(self, key: str, default: str = None) -> str:
        """Translate key to current language"""
        if self.language in self.translations:
            return self.translations[self.language].get(key, default or key)
        return default or key
    
    def set_language(self, language: str):
        """Set language"""
        if language in self.supported_languages:
            self.language = language
            self.translations = self._load_translations()
            return True
        return False
    
    def detect_language(self, text: str) -> str:
        """Detect language from text (simplified)"""
        # Simple keyword-based detection
        text_lower = text.lower()
        
        # Spanish indicators
        if any(word in text_lower for word in ['hola', 'gracias', 'por favor', 'español']):
            return 'es'
        
        # French indicators
        if any(word in text_lower for word in ['bonjour', 'merci', 's\'il vous plaît', 'français']):
            return 'fr'
        
        # Default to English
        return 'en'
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return self.supported_languages
