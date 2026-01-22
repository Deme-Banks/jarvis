"""
Model Quantization for Faster Inference
"""
import os
import subprocess
from typing import Dict, Optional
import json


class ModelQuantizer:
    """Model quantization utilities"""
    
    def __init__(self):
        self.quantization_methods = ['int8', 'int4', 'fp16', 'fp8']
        self.supported_frameworks = self._check_frameworks()
    
    def _check_frameworks(self) -> Dict:
        """Check available quantization frameworks"""
        frameworks = {
            'onnx': False,
            'tensorrt': False,
            'llama_cpp': False,
            'ggml': False
        }
        
        # Check ONNX
        try:
            result = subprocess.run(['python', '-c', 'import onnx'], 
                                   capture_output=True, timeout=5)
            frameworks['onnx'] = result.returncode == 0
        except:
            pass
        
        # Check llama.cpp
        try:
            result = subprocess.run(['llama-cli', '--version'], 
                                   capture_output=True, timeout=5)
            frameworks['llama_cpp'] = result.returncode == 0
        except:
            pass
        
        return frameworks
    
    def get_quantization_suggestions(self, model_type: str = "llm") -> Dict:
        """Get quantization suggestions for model type"""
        suggestions = {
            'method': None,
            'framework': None,
            'expected_speedup': 1.0,
            'size_reduction': 0.0,
            'instructions': []
        }
        
        if model_type == "llm":
            # For LLMs, recommend INT8 or INT4
            if self.supported_frameworks.get('llama_cpp'):
                suggestions['method'] = 'int4'
                suggestions['framework'] = 'llama_cpp'
                suggestions['expected_speedup'] = 2.0
                suggestions['size_reduction'] = 0.75
                suggestions['instructions'] = [
                    "Convert model to GGML format",
                    "Use llama.cpp quantization: llama-cli quantize model.ggml model_q4_0.ggml q4_0",
                    "Load quantized model for faster inference"
                ]
            elif self.supported_frameworks.get('onnx'):
                suggestions['method'] = 'int8'
                suggestions['framework'] = 'onnx'
                suggestions['expected_speedup'] = 1.5
                suggestions['size_reduction'] = 0.5
                suggestions['instructions'] = [
                    "Convert model to ONNX format",
                    "Use ONNX quantization: python -m onnxruntime.quantization.quantize",
                    "Load quantized ONNX model"
                ]
        
        return suggestions
    
    def create_quantization_script(self, model_path: str, output_path: str, 
                                   method: str = "int8") -> Dict:
        """Create quantization script"""
        if method not in self.quantization_methods:
            return {'success': False, 'error': f'Unsupported method: {method}'}
        
        if method == 'int8':
            script = f'''"""
Model Quantization Script - INT8
Reduces model size by ~50% with minimal accuracy loss
"""
import subprocess
import os

model_path = "{model_path}"
output_path = "{output_path}"

# Quantization command (example for ONNX)
# python -m onnxruntime.quantization.quantize \\
#     --input {model_path} \\
#     --output {output_path} \\
#     --quantization_type QInt8

print(f"Quantizing {{model_path}} to {{output_path}}")
print("Method: INT8")
print("Expected: 50% size reduction, 1.5x speedup")
'''
        elif method == 'int4':
            script = f'''"""
Model Quantization Script - INT4
Reduces model size by ~75% with some accuracy loss
"""
import subprocess
import os

model_path = "{model_path}"
output_path = "{output_path}"

# Quantization command (example for llama.cpp)
# llama-cli quantize {model_path} {output_path} q4_0

print(f"Quantizing {{model_path}} to {{output_path}}")
print("Method: INT4")
print("Expected: 75% size reduction, 2x speedup")
'''
        else:
            script = f'''"""
Model Quantization Script - {method.upper()}
"""
import subprocess
import os

model_path = "{model_path}"
output_path = "{output_path}"

print(f"Quantizing {{model_path}} to {{output_path}}")
print("Method: {method.upper()}")
'''
        
        script_path = os.path.join(
            os.path.dirname(output_path),
            f"quantize_{method}_{os.path.basename(model_path)}.py"
        )
        
        with open(script_path, 'w') as f:
            f.write(script)
        
        return {
            'success': True,
            'script': script_path,
            'method': method,
            'model': model_path,
            'output': output_path
        }
