"""
AI-Powered Code Generator
"""
import os
import tempfile
from typing import Dict, List, Optional, Any
from datetime import datetime
from llm.cloud_llm import CloudLLMManager, OpenAILLM, GeminiLLM
from llm.local_llm import LocalLLM
import json


class AICodeGenerator:
    """AI-powered code generation"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self._setup_llm()
    
    def _setup_llm(self):
        """Setup LLM for code generation"""
        if self.llm is None:
            # Try cloud LLMs first
            manager = CloudLLMManager()
            manager.auto_setup()
            
            if manager.list_providers():
                self.llm = manager.get_provider()
            else:
                # Fallback to local
                local_llm = LocalLLM()
                if local_llm.check_available():
                    self.llm = local_llm
    
    def generate_code(self, description: str, language: str = "python",
                     requirements: List[str] = None, 
                     style: str = "clean") -> Dict:
        """Generate code from description"""
        requirements = requirements or []
        
        prompt = f"""Generate {language} code based on this description:

{description}

Requirements:
{chr(10).join(f"- {req}" for req in requirements)}

Code style: {style}

Provide only the code, no explanations. Make it production-ready and well-commented."""
        
        try:
            code = self.llm.chat(prompt, system_prompt="You are an expert software engineer. Generate clean, efficient, production-ready code.")
            
            # Clean up code (remove markdown if present)
            if "```" in code:
                lines = code.split('\n')
                code_lines = []
                in_code = False
                for line in lines:
                    if line.strip().startswith("```"):
                        in_code = not in_code
                        continue
                    if in_code:
                        code_lines.append(line)
                code = '\n'.join(code_lines)
            
            # Save to file
            filepath = os.path.join(
                tempfile.gettempdir(),
                f"generated_{language}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{self._get_extension(language)}"
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            
            return {
                'success': True,
                'file': filepath,
                'code': code,
                'language': language,
                'description': description
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'description': description
            }
    
    def generate_from_voice(self, voice_command: str) -> Dict:
        """Generate code from voice command"""
        command_lower = voice_command.lower()
        
        # Extract language
        language = "python"
        for lang in ["python", "javascript", "java", "cpp", "c++", "c", "go", "rust", "ruby", "php", "swift", "kotlin"]:
            if lang in command_lower:
                language = lang
                break
        
        # Extract requirements
        requirements = []
        if "with" in command_lower:
            # Extract features after "with"
            parts = command_lower.split("with")
            if len(parts) > 1:
                features = parts[1].strip().split("and")
                requirements = [f.strip() for f in features]
        
        # Use the command as description
        description = voice_command
        
        return self.generate_code(description, language, requirements)
    
    def generate_function(self, function_name: str, description: str,
                         parameters: List[str] = None,
                         return_type: str = None,
                         language: str = "python") -> Dict:
        """Generate a specific function"""
        params_str = ", ".join(parameters) if parameters else ""
        return_str = f" -> {return_type}" if return_type else ""
        
        prompt = f"""Generate a {language} function:

Function name: {function_name}
Parameters: {params_str}
Return type: {return_type or 'auto'}
Description: {description}

Provide only the function code, well-commented."""
        
        try:
            code = self.llm.chat(prompt, system_prompt="You are an expert software engineer. Generate clean, efficient functions.")
            
            # Save to file
            filepath = os.path.join(
                tempfile.gettempdir(),
                f"{function_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{self._get_extension(language)}"
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            
            return {
                'success': True,
                'file': filepath,
                'code': code,
                'function_name': function_name
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_class(self, class_name: str, description: str,
                      methods: List[str] = None,
                      language: str = "python") -> Dict:
        """Generate a class"""
        methods_str = "\n".join(f"- {m}" for m in methods) if methods else ""
        
        prompt = f"""Generate a {language} class:

Class name: {class_name}
Description: {description}
Methods:
{methods_str}

Provide only the class code, well-commented and production-ready."""
        
        try:
            code = self.llm.chat(prompt, system_prompt="You are an expert software engineer. Generate clean, efficient classes.")
            
            filepath = os.path.join(
                tempfile.gettempdir(),
                f"{class_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{self._get_extension(language)}"
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            
            return {
                'success': True,
                'file': filepath,
                'code': code,
                'class_name': class_name
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_extension(self, language: str) -> str:
        """Get file extension for language"""
        extensions = {
            'python': 'py',
            'javascript': 'js',
            'java': 'java',
            'cpp': 'cpp',
            'c++': 'cpp',
            'c': 'c',
            'go': 'go',
            'rust': 'rs',
            'ruby': 'rb',
            'php': 'php',
            'swift': 'swift',
            'kotlin': 'kt'
        }
        return extensions.get(language.lower(), 'txt')
