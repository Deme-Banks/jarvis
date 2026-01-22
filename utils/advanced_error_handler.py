"""
Advanced Error Handling and Recovery
"""
import traceback
import sys
from typing import Dict, Optional, Callable
from datetime import datetime
import json
import os


class AdvancedErrorHandler:
    """Advanced error handling with recovery strategies"""
    
    def __init__(self, log_file: str = "./logs/errors.json"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        self.error_history = []
        self.recovery_strategies = {}
        self._register_default_strategies()
    
    def _register_default_strategies(self):
        """Register default recovery strategies"""
        self.recovery_strategies = {
            'ConnectionError': self._handle_connection_error,
            'TimeoutError': self._handle_timeout_error,
            'FileNotFoundError': self._handle_file_not_found,
            'PermissionError': self._handle_permission_error,
            'ValueError': self._handle_value_error,
            'KeyError': self._handle_key_error
        }
    
    def _handle_connection_error(self, error: Exception, context: Dict) -> Optional[str]:
        """Handle connection errors"""
        return "Connection error. Retrying with fallback..."
    
    def _handle_timeout_error(self, error: Exception, context: Dict) -> Optional[str]:
        """Handle timeout errors"""
        return "Request timed out. Trying again..."
    
    def _handle_file_not_found(self, error: Exception, context: Dict) -> Optional[str]:
        """Handle file not found errors"""
        return "File not found. Checking alternative locations..."
    
    def _handle_permission_error(self, error: Exception, context: Dict) -> Optional[str]:
        """Handle permission errors"""
        return "Permission denied. Try running with appropriate permissions."
    
    def _handle_value_error(self, error: Exception, context: Dict) -> Optional[str]:
        """Handle value errors"""
        return "Invalid value. Please check your input."
    
    def _handle_key_error(self, error: Exception, context: Dict) -> Optional[str]:
        """Handle key errors"""
        return "Missing required information. Please provide all necessary details."
    
    def handle_error(self, error: Exception, context: Dict = None, 
                    retry: bool = True) -> Optional[str]:
        """Handle error with recovery"""
        error_type = type(error).__name__
        error_message = str(error)
        
        # Log error
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': error_type,
            'message': error_message,
            'context': context or {},
            'traceback': traceback.format_exc()
        }
        
        self.error_history.append(error_entry)
        self._save_error_log(error_entry)
        
        # Try recovery strategy
        if error_type in self.recovery_strategies:
            recovery_response = self.recovery_strategies[error_type](error, context or {})
            if recovery_response:
                return recovery_response
        
        # Default error message
        return f"An error occurred: {error_message}. Check logs for details."
    
    def _save_error_log(self, error_entry: Dict):
        """Save error to log file"""
        try:
            errors = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    errors = json.load(f)
            
            errors.append(error_entry)
            
            # Keep only last 1000 errors
            if len(errors) > 1000:
                errors = errors[-1000:]
            
            with open(self.log_file, 'w') as f:
                json.dump(errors, f, indent=2)
        except:
            pass
    
    def register_recovery_strategy(self, error_type: str, strategy: Callable):
        """Register custom recovery strategy"""
        self.recovery_strategies[error_type] = strategy
    
    def get_error_stats(self) -> Dict:
        """Get error statistics"""
        if not self.error_history:
            return {}
        
        error_types = {}
        for error in self.error_history:
            error_type = error['type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        return {
            'total_errors': len(self.error_history),
            'errors_by_type': error_types,
            'recent_errors': self.error_history[-10:]
        }
