"""
Advanced Logging Configuration
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path


class JARVISLogger:
    """Configure logging for JARVIS"""
    
    def __init__(self, log_dir: str = "./logs", 
                 max_bytes: int = 10 * 1024 * 1024,  # 10MB
                 backup_count: int = 5):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        # Root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # Remove existing handlers
        root_logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        root_logger.addHandler(console_handler)
        
        # File handler (rotating)
        log_file = os.path.join(self.log_dir, 'jarvis.log')
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        root_logger.addHandler(file_handler)
        
        # Module-specific loggers
        self._setup_module_loggers()
    
    def _setup_module_loggers(self):
        """Setup loggers for specific modules"""
        modules = {
            'voice': logging.INFO,
            'agents': logging.INFO,
            'llm': logging.INFO,
            'cybersecurity': logging.WARNING,  # Less verbose for security
            'analytics': logging.INFO
        }
        
        for module, level in modules.items():
            logger = logging.getLogger(module)
            logger.setLevel(level)
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get logger for module"""
        return logging.getLogger(name)
