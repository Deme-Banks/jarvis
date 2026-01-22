"""
AI-Powered Code Builder and Compiler
"""
import os
import subprocess
import tempfile
from typing import Dict, List, Optional, Any
from datetime import datetime
import platform


class AICodeBuilder:
    """AI-powered code building and compilation"""
    
    def __init__(self):
        self.system = platform.system()
        self.build_cache = {}
    
    def build_code(self, filepath: str, language: str = None,
                  output_name: str = None,
                  options: Dict = None) -> Dict:
        """Build/compile code"""
        if not os.path.exists(filepath):
            return {
                'success': False,
                'error': f'File not found: {filepath}'
            }
        
        language = language or self._detect_language(filepath)
        options = options or {}
        
        if language == 'python':
            return self._build_python(filepath, options)
        elif language == 'javascript':
            return self._build_javascript(filepath, options)
        elif language == 'java':
            return self._build_java(filepath, output_name, options)
        elif language in ['c', 'cpp']:
            return self._build_cpp(filepath, output_name, options)
        elif language == 'go':
            return self._build_go(filepath, output_name, options)
        elif language == 'rust':
            return self._build_rust(filepath, output_name, options)
        else:
            return {
                'success': False,
                'error': f'Unsupported language: {language}'
            }
    
    def _build_python(self, filepath: str, options: Dict) -> Dict:
        """Build Python (check syntax, create executable)"""
        # Check syntax
        try:
            result = subprocess.run(
                ['python', '-m', 'py_compile', filepath],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': result.stderr,
                    'syntax_check': False
                }
            
            # Create executable (pyinstaller if available)
            if options.get('create_executable', False):
                return self._create_python_executable(filepath, options)
            
            return {
                'success': True,
                'syntax_check': True,
                'message': 'Python code is valid'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_python_executable(self, filepath: str, options: Dict) -> Dict:
        """Create Python executable using PyInstaller"""
        try:
            # Check if PyInstaller is available
            result = subprocess.run(
                ['pyinstaller', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': 'PyInstaller not installed. Install with: pip install pyinstaller'
                }
            
            # Build executable
            output_dir = options.get('output_dir', os.path.dirname(filepath))
            onefile = '--onefile' if options.get('onefile', True) else ''
            
            cmd = ['pyinstaller', onefile, '--distpath', output_dir, filepath]
            cmd = [c for c in cmd if c]  # Remove empty strings
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                exe_name = os.path.splitext(os.path.basename(filepath))[0]
                if self.system == 'Windows':
                    exe_path = os.path.join(output_dir, f'{exe_name}.exe')
                else:
                    exe_path = os.path.join(output_dir, exe_name)
                
                return {
                    'success': True,
                    'executable': exe_path,
                    'message': 'Executable created successfully'
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _build_javascript(self, filepath: str, options: Dict) -> Dict:
        """Build JavaScript (bundle, minify)"""
        # Check if Node.js is available
        try:
            result = subprocess.run(
                ['node', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': 'Node.js not installed'
                }
            
            # Syntax check
            result = subprocess.run(
                ['node', '--check', filepath],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': result.stderr,
                    'syntax_check': False
                }
            
            return {
                'success': True,
                'syntax_check': True,
                'message': 'JavaScript code is valid'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _build_java(self, filepath: str, output_name: str, options: Dict) -> Dict:
        """Build Java code"""
        try:
            # Check if javac is available
            result = subprocess.run(
                ['javac', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': 'Java compiler (javac) not found'
                }
            
            # Compile
            output_dir = options.get('output_dir', os.path.dirname(filepath))
            cmd = ['javac', '-d', output_dir, filepath]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                class_name = os.path.splitext(os.path.basename(filepath))[0]
                class_file = os.path.join(output_dir, f'{class_name}.class')
                
                return {
                    'success': True,
                    'class_file': class_file,
                    'message': 'Java code compiled successfully'
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _build_cpp(self, filepath: str, output_name: str, options: Dict) -> Dict:
        """Build C/C++ code"""
        try:
            # Determine compiler
            compiler = 'g++' if filepath.endswith('.cpp') else 'gcc'
            
            # Check if compiler is available
            result = subprocess.run(
                [compiler, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': f'{compiler} not found'
                }
            
            # Compile
            output_dir = options.get('output_dir', os.path.dirname(filepath))
            if not output_name:
                output_name = os.path.splitext(os.path.basename(filepath))[0]
            
            if self.system == 'Windows':
                output_name += '.exe'
            
            output_path = os.path.join(output_dir, output_name)
            
            cmd = [compiler, '-o', output_path, filepath]
            if options.get('optimize', False):
                cmd.insert(-2, '-O2')
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'executable': output_path,
                    'message': 'C/C++ code compiled successfully'
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _build_go(self, filepath: str, output_name: str, options: Dict) -> Dict:
        """Build Go code"""
        try:
            # Check if go is available
            result = subprocess.run(
                ['go', 'version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': 'Go compiler not found'
                }
            
            # Build
            output_dir = options.get('output_dir', os.path.dirname(filepath))
            if not output_name:
                output_name = os.path.splitext(os.path.basename(filepath))[0]
            
            output_path = os.path.join(output_dir, output_name)
            
            cmd = ['go', 'build', '-o', output_path, filepath]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'executable': output_path,
                    'message': 'Go code built successfully'
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _build_rust(self, filepath: str, output_name: str, options: Dict) -> Dict:
        """Build Rust code"""
        try:
            # Check if rustc is available
            result = subprocess.run(
                ['rustc', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': 'Rust compiler not found'
                }
            
            # Build
            output_dir = options.get('output_dir', os.path.dirname(filepath))
            if not output_name:
                output_name = os.path.splitext(os.path.basename(filepath))[0]
            
            if self.system == 'Windows':
                output_name += '.exe'
            
            output_path = os.path.join(output_dir, output_name)
            
            cmd = ['rustc', '-o', output_path, filepath]
            if options.get('optimize', False):
                cmd.insert(-2, '-O')
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'executable': output_path,
                    'message': 'Rust code compiled successfully'
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _detect_language(self, filepath: str) -> str:
        """Detect programming language from file extension"""
        ext = os.path.splitext(filepath)[1].lower()
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust'
        }
        return language_map.get(ext, 'unknown')
    
    def run_code(self, filepath: str, language: str = None,
                args: List[str] = None) -> Dict:
        """Run code"""
        language = language or self._detect_language(filepath)
        args = args or []
        
        if language == 'python':
            cmd = ['python', filepath] + args
        elif language == 'javascript':
            cmd = ['node', filepath] + args
        elif language == 'java':
            # Run compiled class
            class_name = os.path.splitext(os.path.basename(filepath))[0]
            cmd = ['java', class_name] + args
        else:
            # Try to run as executable
            cmd = [filepath] + args
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
