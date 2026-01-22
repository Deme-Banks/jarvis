"""
Error Recovery - Advanced error handling and recovery
"""
import os
import json
import traceback
from typing import Dict, Optional, Callable
from datetime import datetime


class ErrorRecovery:
    """Advanced error recovery system"""
    
    def __init__(self, error_log_file: str = "logs/errors.jsonl"):
        self.error_log_file = error_log_file
        self.recovery_strategies = {}
        self.error_patterns = {}
        os.makedirs(os.path.dirname(error_log_file), exist_ok=True)
    
    def log_error(self, error: Exception, context: Dict = None):
        """Log error with context"""
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {}
        }
        
        with open(self.error_log_file, 'a') as f:
            f.write(json.dumps(error_entry) + '\n')
    
    def register_recovery_strategy(self, error_type: str, strategy: Callable):
        """Register recovery strategy for error type"""
        self.recovery_strategies[error_type] = strategy
    
    def attempt_recovery(self, error: Exception, context: Dict = None) -> Dict:
        """Attempt to recover from error"""
        error_type = type(error).__name__
        
        # Log error
        self.log_error(error, context)
        
        # Try recovery strategy
        if error_type in self.recovery_strategies:
            try:
                recovery_result = self.recovery_strategies[error_type](error, context)
                return {
                    "recovered": True,
                    "strategy": error_type,
                    "result": recovery_result
                }
            except Exception as e:
                return {
                    "recovered": False,
                    "error": f"Recovery failed: {str(e)}"
                }
        
        # Default recovery attempts
        return self._default_recovery(error, context)
    
    def _default_recovery(self, error: Exception, context: Dict) -> Dict:
        """Default recovery strategies"""
        error_type = type(error).__name__
        
        if error_type == "ConnectionError":
            return {
                "recovered": False,
                "suggestion": "Check network connectivity and retry"
            }
        elif error_type == "FileNotFoundError":
            return {
                "recovered": False,
                "suggestion": "Check file path and permissions"
            }
        elif error_type == "PermissionError":
            return {
                "recovered": False,
                "suggestion": "Check file permissions and user access"
            }
        elif error_type == "TimeoutError":
            return {
                "recovered": False,
                "suggestion": "Operation timed out, try again with longer timeout"
            }
        else:
            return {
                "recovered": False,
                "suggestion": "Review error logs for details"
            }
    
    def get_error_statistics(self) -> Dict:
        """Get error statistics"""
        errors = []
        
        if os.path.exists(self.error_log_file):
            with open(self.error_log_file, 'r') as f:
                for line in f:
                    try:
                        errors.append(json.loads(line))
                    except:
                        pass
        
        error_counts = {}
        for error in errors:
            error_type = error.get("error_type", "Unknown")
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        return {
            "total_errors": len(errors),
            "error_types": error_counts,
            "recent_errors": errors[-10:] if errors else []
        }
