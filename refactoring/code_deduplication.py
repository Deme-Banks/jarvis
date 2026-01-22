"""
Code Deduplication - Extract common patterns
"""
from typing import Dict, Any, Optional, List
import json
import os


class CommonUtils:
    """Common utilities extracted from duplicated code"""
    
    @staticmethod
    def safe_json_load(file_path: str, default: Any = None) -> Any:
        """Safely load JSON file"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return default if default is not None else {}
    
    @staticmethod
    def safe_json_save(file_path: str, data: Any) -> bool:
        """Safely save JSON file"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return False
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """Validate API key format"""
        if not api_key or len(api_key) < 10:
            return False
        return True
    
    @staticmethod
    def format_error(error: Exception, context: Optional[Dict] = None) -> Dict:
        """Format error consistently"""
        return {
            "error": str(error),
            "type": type(error).__name__,
            "context": context or {}
        }
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename[:255]  # Limit length


class ResponseFormatter:
    """Consistent response formatting"""
    
    @staticmethod
    def success(message: str, data: Any = None) -> Dict:
        """Format success response"""
        response = {
            "success": True,
            "message": message
        }
        if data is not None:
            response["data"] = data
        return response
    
    @staticmethod
    def error(message: str, error: Optional[Exception] = None) -> Dict:
        """Format error response"""
        response = {
            "success": False,
            "message": message
        }
        if error:
            response["error"] = str(error)
            response["error_type"] = type(error).__name__
        return response
