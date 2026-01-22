"""
Multi-Language Support
"""
import os
import json
from typing import Dict, Optional, List
try:
    from googletrans import Translator
    TRANSLATOR_AVAILABLE = True
except:
    TRANSLATOR_AVAILABLE = False


class MultiLanguageSupport:
    """Multi-language support for JARVIS"""
    
    def __init__(self, default_language: str = "en"):
        self.default_language = default_language
        self.current_language = default_language
        self.translator = Translator() if TRANSLATOR_AVAILABLE else None
        self.translations = self._load_translations()
    
    def _load_translations(self) -> Dict:
        """Load translations"""
        translations_file = "config/translations.json"
        if os.path.exists(translations_file):
            try:
                with open(translations_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def set_language(self, language_code: str):
        """Set current language"""
        self.current_language = language_code
        return {"success": True, "language": language_code}
    
    def detect_language(self, text: str) -> Dict:
        """Detect language of text"""
        if not TRANSLATOR_AVAILABLE or not self.translator:
            return {"error": "Translator not available. Install with: pip install googletrans==4.0.0rc1"}
        try:
            detected = self.translator.detect(text)
            return {
                "language": detected.lang,
                "confidence": detected.confidence
            }
        except Exception as e:
            return {"error": str(e)}
    
    def translate(self, text: str, target_language: Optional[str] = None,
                 source_language: Optional[str] = None) -> Dict:
        """Translate text"""
        if not TRANSLATOR_AVAILABLE or not self.translator:
            return {"error": "Translator not available. Install with: pip install googletrans==4.0.0rc1"}
        
        target = target_language or self.current_language
        
        try:
            result = self.translator.translate(
                text,
                dest=target,
                src=source_language
            )
            
            return {
                "success": True,
                "original": text,
                "translated": result.text,
                "source_language": result.src,
                "target_language": result.dest
            }
        except Exception as e:
            return {"error": str(e)}
    
    def translate_response(self, response: str) -> str:
        """Translate JARVIS response to current language"""
        if self.current_language == "en":
            return response
        
        translation = self.translate(response, self.current_language)
        if translation.get("success"):
            return translation["translated"]
        
        return response
    
    def get_supported_languages(self) -> List[Dict]:
        """Get list of supported languages"""
        languages = [
            {"code": "en", "name": "English"},
            {"code": "es", "name": "Spanish"},
            {"code": "fr", "name": "French"},
            {"code": "de", "name": "German"},
            {"code": "it", "name": "Italian"},
            {"code": "pt", "name": "Portuguese"},
            {"code": "ru", "name": "Russian"},
            {"code": "ja", "name": "Japanese"},
            {"code": "ko", "name": "Korean"},
            {"code": "zh", "name": "Chinese"}
        ]
        return languages
