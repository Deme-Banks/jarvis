"""
Safe Code Execution Sandbox
"""
import os
import subprocess
import tempfile
import sys
from typing import Dict, Optional
from contextlib import redirect_stdout, redirect_stderr
import io


class CodeExecutor:
    """Safe code execution sandbox"""
    
    def __init__(self, timeout: int = 30, memory_limit: int = 512):
        self.timeout = timeout
        self.memory_limit = memory_limit  # MB
        self.allowed_modules = [
            'math', 'datetime', 'json', 'os', 'sys', 'random',
            'string', 'collections', 'itertools', 'functools'
        ]
        self.blocked_modules = [
            'subprocess', 'socket', 'urllib', 'requests',
            'pickle', 'eval', 'exec', '__import__'
        ]
    
    def execute_python(self, code: str, inputs: Optional[Dict] = None) -> Dict:
        """Execute Python code safely"""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Capture output
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            # Execute with timeout
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=tempfile.gettempdir()
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'execution_time': 0  # Would measure actual time
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Execution timeout',
                'timeout': self.timeout
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            # Cleanup
            try:
                os.unlink(temp_file)
            except:
                pass
    
    def validate_code(self, code: str) -> Dict:
        """Validate code before execution"""
        issues = []
        
        # Check for blocked modules
        for blocked in self.blocked_modules:
            if f'import {blocked}' in code or f'from {blocked}' in code:
                issues.append(f'Blocked module: {blocked}')
        
        # Check for dangerous functions
        dangerous = ['eval', 'exec', '__import__', 'compile']
        for func in dangerous:
            if func in code:
                issues.append(f'Dangerous function: {func}')
        
        # Check for file system access
        if 'open(' in code and '../' in code:
            issues.append('Potential path traversal')
        
        return {
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def execute_safe(self, code: str, language: str = "python") -> Dict:
        """Execute code with safety checks"""
        # Validate first
        validation = self.validate_code(code)
        if not validation['valid']:
            return {
                'success': False,
                'error': 'Code validation failed',
                'issues': validation['issues']
            }
        
        if language == "python":
            return self.execute_python(code)
        else:
            return {
                'success': False,
                'error': f'Language {language} not supported'
            }
