"""
AI-Powered Code Reader and Analyzer
"""
import os
import ast
from typing import Dict, List, Optional, Any
from llm.cloud_llm import CloudLLMManager, OpenAILLM, GeminiLLM
from llm.local_llm import LocalLLM


class AICodeReader:
    """AI-powered code reading and analysis"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self._setup_llm()
    
    def _setup_llm(self):
        """Setup LLM for code analysis"""
        if self.llm is None:
            manager = CloudLLMManager()
            manager.auto_setup()
            
            if manager.list_providers():
                self.llm = manager.get_provider()
            else:
                local_llm = LocalLLM()
                if local_llm.check_available():
                    self.llm = local_llm
    
    def read_code(self, filepath: str) -> Dict:
        """Read and analyze code file"""
        if not os.path.exists(filepath):
            return {
                'success': False,
                'error': f'File not found: {filepath}'
            }
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Get file info
            language = self._detect_language(filepath)
            
            # Analyze with AI
            analysis = self.analyze_code(code, language)
            
            # Parse structure (for Python)
            structure = None
            if language == 'python':
                structure = self._parse_python_structure(code)
            
            return {
                'success': True,
                'file': filepath,
                'code': code,
                'language': language,
                'analysis': analysis,
                'structure': structure,
                'size': len(code),
                'lines': len(code.split('\n'))
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file': filepath
            }
    
    def analyze_code(self, code: str, language: str = "python") -> Dict:
        """Analyze code with AI"""
        prompt = f"""Analyze this {language} code and provide:

1. What the code does
2. Key functions/classes
3. Potential issues or bugs
4. Security concerns
5. Performance considerations
6. Suggestions for improvement

Code:
```{language}
{code}
```

Provide a comprehensive analysis."""
        
        try:
            analysis_text = self.llm.chat(
                prompt,
                system_prompt="You are an expert code reviewer. Provide detailed, actionable analysis."
            )
            
            return {
                'analysis': analysis_text,
                'language': language
            }
        except Exception as e:
            return {
                'error': str(e)
            }
    
    def explain_code(self, code: str, language: str = "python") -> str:
        """Explain what code does"""
        prompt = f"""Explain what this {language} code does in simple terms:

```{language}
{code}
```

Provide a clear, concise explanation."""
        
        try:
            explanation = self.llm.chat(
                prompt,
                system_prompt="You are a coding instructor. Explain code clearly and simply."
            )
            return explanation
        except Exception as e:
            return f"Error explaining code: {str(e)}"
    
    def find_bugs(self, code: str, language: str = "python") -> List[Dict]:
        """Find bugs in code"""
        prompt = f"""Find all bugs, errors, and potential issues in this {language} code:

```{language}
{code}
```

List each bug with:
- Location (line number if possible)
- Description
- Severity (critical, high, medium, low)
- Suggested fix

Provide a detailed bug report."""
        
        try:
            bug_report = self.llm.chat(
                prompt,
                system_prompt="You are a bug hunter. Find all issues in code."
            )
            
            # Parse bug report (simplified)
            bugs = []
            lines = bug_report.split('\n')
            current_bug = {}
            
            for line in lines:
                if 'bug' in line.lower() or 'issue' in line.lower():
                    if current_bug:
                        bugs.append(current_bug)
                    current_bug = {'description': line}
                elif 'severity' in line.lower():
                    current_bug['severity'] = line
                elif 'fix' in line.lower() or 'suggest' in line.lower():
                    current_bug['fix'] = line
            
            if current_bug:
                bugs.append(current_bug)
            
            return bugs if bugs else [{'description': bug_report}]
        except Exception as e:
            return [{'error': str(e)}]
    
    def suggest_improvements(self, code: str, language: str = "python") -> str:
        """Suggest code improvements"""
        prompt = f"""Suggest improvements for this {language} code:

```{language}
{code}
```

Focus on:
- Code quality
- Performance
- Best practices
- Security
- Maintainability

Provide actionable suggestions."""
        
        try:
            suggestions = self.llm.chat(
                prompt,
                system_prompt="You are a code quality expert. Provide actionable improvement suggestions."
            )
            return suggestions
        except Exception as e:
            return f"Error getting suggestions: {str(e)}"
    
    def refactor_code(self, code: str, language: str = "python",
                     improvements: List[str] = None) -> Dict:
        """Refactor code with AI"""
        improvements_str = "\n".join(f"- {imp}" for imp in improvements) if improvements else ""
        
        prompt = f"""Refactor this {language} code:

```{language}
{code}
```

Improvements to make:
{improvements_str}

Provide the refactored code with explanations of changes."""
        
        try:
            refactored = self.llm.chat(
                prompt,
                system_prompt="You are a refactoring expert. Improve code while maintaining functionality."
            )
            
            # Extract code if in markdown
            if "```" in refactored:
                lines = refactored.split('\n')
                code_lines = []
                in_code = False
                for line in lines:
                    if line.strip().startswith("```"):
                        in_code = not in_code
                        continue
                    if in_code:
                        code_lines.append(line)
                refactored_code = '\n'.join(code_lines)
            else:
                refactored_code = refactored
            
            return {
                'success': True,
                'refactored_code': refactored_code,
                'explanation': refactored
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
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin'
        }
        return language_map.get(ext, 'unknown')
    
    def _parse_python_structure(self, code: str) -> Dict:
        """Parse Python code structure"""
        try:
            tree = ast.parse(code)
            structure = {
                'functions': [],
                'classes': [],
                'imports': []
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    structure['functions'].append({
                        'name': node.name,
                        'line': node.lineno,
                        'args': [arg.arg for arg in node.args.args]
                    })
                elif isinstance(node, ast.ClassDef):
                    structure['classes'].append({
                        'name': node.name,
                        'line': node.lineno
                    })
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        structure['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        structure['imports'].append(node.module)
            
            return structure
        except:
            return {}
