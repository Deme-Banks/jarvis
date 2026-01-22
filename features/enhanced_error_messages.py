"""
Enhanced Error Messages - Contextual help and recovery
"""
from typing import Dict, Optional, List
import re


class EnhancedErrorMessages:
    """Enhanced error message system with contextual help"""
    
    def __init__(self):
        self.error_patterns = {
            "connection": {
                "patterns": [r"connection", r"network", r"timeout", r"unreachable"],
                "suggestions": [
                    "Check your internet connection",
                    "Verify the API endpoint is accessible",
                    "Try again in a few moments"
                ],
                "recovery": "Retry the operation"
            },
            "permission": {
                "patterns": [r"permission", r"access denied", r"unauthorized"],
                "suggestions": [
                    "Check file permissions",
                    "Run with administrator privileges if needed",
                    "Verify user has required access"
                ],
                "recovery": "Check permissions and try again"
            },
            "not found": {
                "patterns": [r"not found", r"does not exist", r"missing"],
                "suggestions": [
                    "Verify the file or path exists",
                    "Check the spelling of the path",
                    "Ensure the file hasn't been moved or deleted"
                ],
                "recovery": "Verify the path and try again"
            },
            "syntax": {
                "patterns": [r"syntax error", r"invalid syntax", r"parse error"],
                "suggestions": [
                    "Check for typos in your command",
                    "Verify command syntax",
                    "Review the command format"
                ],
                "recovery": "Correct the syntax and try again"
            },
            "api": {
                "patterns": [r"api key", r"authentication", r"invalid token"],
                "suggestions": [
                    "Check your API key is set correctly",
                    "Verify the API key is valid",
                    "Check API key permissions"
                ],
                "recovery": "Update API key in .env file"
            }
        }
    
    def enhance_error(self, error_message: str, context: Optional[Dict] = None) -> Dict:
        """Enhance error message with contextual help"""
        error_lower = error_message.lower()
        
        # Find matching error pattern
        matched_pattern = None
        for pattern_name, pattern_data in self.error_patterns.items():
            for pattern in pattern_data["patterns"]:
                if re.search(pattern, error_lower):
                    matched_pattern = pattern_data
                    break
            if matched_pattern:
                break
        
        enhanced = {
            "original_error": error_message,
            "context": context or {},
            "suggestions": matched_pattern["suggestions"] if matched_pattern else [
                "Review the error message",
                "Check system logs for more details",
                "Try the operation again"
            ],
            "recovery_action": matched_pattern.get("recovery", "Review and retry") if matched_pattern else "Review and retry",
            "helpful": True
        }
        
        return enhanced
    
    def format_error_message(self, error: Exception, context: Optional[Dict] = None) -> str:
        """Format error message for user"""
        enhanced = self.enhance_error(str(error), context)
        
        message = f"❌ Error: {enhanced['original_error']}\n\n"
        message += "💡 Suggestions:\n"
        for i, suggestion in enumerate(enhanced['suggestions'], 1):
            message += f"  {i}. {suggestion}\n"
        
        message += f"\n🔄 Recovery: {enhanced['recovery_action']}"
        
        return message
