"""
Enhanced Error Handling with Recovery
"""
import traceback
import logging
from typing import Optional, Callable, Dict, Any
from datetime import datetime
import json
import os


class ErrorHandler:
    """Enhanced error handling with recovery"""
    
    def __init__(self, log_file: str = "./logs/errors.log"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("JARVIS")
        
        # Error recovery strategies
        self.recovery_strategies: Dict[str, Callable] = {}
        self.error_counts: Dict[str, int] = {}
    
    def register_recovery(self, error_type: str, strategy: Callable):
        """Register recovery strategy for error type"""
        self.recovery_strategies[error_type] = strategy
    
    def handle_error(self, error: Exception, context: Optional[Dict] = None,
                    retry: bool = True) -> Optional[Any]:
        """Handle error with recovery"""
        error_type = type(error).__name__
        error_msg = str(error)
        
        # Log error
        self.logger.error(
            f"Error: {error_type} - {error_msg}",
            exc_info=True,
            extra={"context": context}
        )
        
        # Save to error log
        self._save_error_log(error_type, error_msg, context)
        
        # Increment error count
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Try recovery if available
        if retry and error_type in self.recovery_strategies:
            try:
                return self.recovery_strategies[error_type](error, context)
            except Exception as recovery_error:
                self.logger.error(f"Recovery failed: {recovery_error}")
        
        return None
    
    def _save_error_log(self, error_type: str, error_msg: str, context: Optional[Dict]):
        """Save error to log file"""
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "error_message": error_msg,
            "context": context or {},
            "traceback": traceback.format_exc()
        }
        
        try:
            log_entries = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    try:
                        log_entries = json.load(f)
                    except:
                        pass
            
            log_entries.append(error_entry)
            
            # Keep last 1000 errors
            if len(log_entries) > 1000:
                log_entries = log_entries[-1000:]
            
            with open(self.log_file, 'w') as f:
                json.dump(log_entries, f, indent=2)
        except:
            pass
    
    def get_error_stats(self) -> Dict:
        """Get error statistics"""
        return {
            "total_errors": sum(self.error_counts.values()),
            "error_types": dict(self.error_counts),
            "log_file": self.log_file
        }
    
    def clear_errors(self):
        """Clear error counts"""
        self.error_counts.clear()


# Global error handler
_error_handler = ErrorHandler()


def handle_error(error: Exception, context: Optional[Dict] = None, retry: bool = True):
    """Global error handler"""
    return _error_handler.handle_error(error, context, retry)


def get_error_handler() -> ErrorHandler:
    """Get global error handler"""
    return _error_handler
