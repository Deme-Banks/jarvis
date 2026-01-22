"""
Document Analysis (PDF, Word, etc.)
"""
import os
from typing import Dict, Optional
from llm.cloud_llm import CloudLLMManager, OpenAILLM, GeminiLLM
from llm.local_llm import LocalLLM


class DocumentAnalyzer:
    """AI-powered document analysis"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self._setup_llm()
    
    def _setup_llm(self):
        """Setup LLM for document analysis"""
        if self.llm is None:
            manager = CloudLLMManager()
            manager.auto_setup()
            
            if manager.list_providers():
                self.llm = manager.get_provider()
            else:
                local_llm = LocalLLM()
                if local_llm.check_available():
                    self.llm = local_llm
    
    def analyze_pdf(self, pdf_path: str, analysis_type: str = "summary") -> Dict:
        """Analyze PDF document"""
        if not os.path.exists(pdf_path):
            return {'success': False, 'error': f'PDF not found: {pdf_path}'}
        
        # Extract text from PDF
        try:
            text = self._extract_pdf_text(pdf_path)
        except Exception as e:
            return {'success': False, 'error': f'Failed to extract text: {str(e)}'}
        
        # Analyze with AI
        if analysis_type == "summary":
            prompt = f"Summarize this document:\n\n{text[:4000]}"  # Limit length
        elif analysis_type == "key_points":
            prompt = f"Extract key points from this document:\n\n{text[:4000]}"
        elif analysis_type == "questions":
            prompt = f"Generate questions about this document:\n\n{text[:4000]}"
        else:
            prompt = f"Analyze this document: {analysis_type}\n\n{text[:4000]}"
        
        try:
            analysis = self.llm.chat(prompt, system_prompt="You are a document analysis expert.")
            
            return {
                'success': True,
                'analysis': analysis,
                'type': analysis_type,
                'text_length': len(text)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _extract_pdf_text(self, pdf_path: str) -> str:
        """Extract text from PDF"""
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except ImportError:
            # Fallback: try pdfplumber
            try:
                import pdfplumber
                with pdfplumber.open(pdf_path) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
                    return text
            except ImportError:
                raise ImportError("Install PyPDF2 or pdfplumber: pip install PyPDF2 pdfplumber")
    
    def analyze_word(self, docx_path: str, analysis_type: str = "summary") -> Dict:
        """Analyze Word document"""
        if not os.path.exists(docx_path):
            return {'success': False, 'error': f'Word document not found: {docx_path}'}
        
        # Extract text
        try:
            import docx
            doc = docx.Document(docx_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        except ImportError:
            return {'success': False, 'error': 'Install python-docx: pip install python-docx'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        
        # Analyze
        prompt = f"Analyze this document ({analysis_type}):\n\n{text[:4000]}"
        
        try:
            analysis = self.llm.chat(prompt)
            return {
                'success': True,
                'analysis': analysis,
                'type': analysis_type
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def analyze_text_file(self, file_path: str, analysis_type: str = "summary") -> Dict:
        """Analyze text file"""
        if not os.path.exists(file_path):
            return {'success': False, 'error': f'File not found: {file_path}'}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            return {'success': False, 'error': str(e)}
        
        prompt = f"Analyze this text file ({analysis_type}):\n\n{text[:4000]}"
        
        try:
            analysis = self.llm.chat(prompt)
            return {
                'success': True,
                'analysis': analysis,
                'type': analysis_type
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
