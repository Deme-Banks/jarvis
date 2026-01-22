"""
GPU Acceleration for JARVIS
"""
import os
from typing import Optional, Dict, List
import subprocess


class GPUAccelerator:
    """GPU acceleration utilities"""
    
    def __init__(self):
        self.gpu_available = self._check_gpu()
        self.gpu_info = self._get_gpu_info()
    
    def _check_gpu(self) -> bool:
        """Check if GPU is available"""
        # Check for CUDA
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return True
        except:
            pass
        
        # Check for ROCm (AMD)
        try:
            result = subprocess.run(['rocm-smi'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return True
        except:
            pass
        
        return False
    
    def _get_gpu_info(self) -> Dict:
        """Get GPU information"""
        info = {
            'available': False,
            'type': None,
            'name': None,
            'memory': None
        }
        
        if not self.gpu_available:
            return info
        
        # Try NVIDIA
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader'], 
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if lines:
                    parts = lines[0].split(',')
                    info['available'] = True
                    info['type'] = 'NVIDIA'
                    info['name'] = parts[0].strip()
                    info['memory'] = parts[1].strip() if len(parts) > 1 else None
        except:
            pass
        
        # Try AMD
        if not info['available']:
            try:
                result = subprocess.run(['rocm-smi', '--showid'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    info['available'] = True
                    info['type'] = 'AMD'
            except:
                pass
        
        return info
    
    def get_optimization_suggestions(self) -> List[str]:
        """Get GPU optimization suggestions"""
        suggestions = []
        
        if not self.gpu_available:
            suggestions.append("No GPU detected. Consider using CPU-optimized models.")
            return suggestions
        
        if self.gpu_info['type'] == 'NVIDIA':
            suggestions.append("Use CUDA for LLM inference")
            suggestions.append("Enable TensorRT for faster inference")
            suggestions.append("Use GPU-accelerated audio processing")
            suggestions.append("Consider model quantization (INT8) for faster inference")
        
        elif self.gpu_info['type'] == 'AMD':
            suggestions.append("Use ROCm for LLM inference")
            suggestions.append("Enable GPU-accelerated processing")
        
        return suggestions
    
    def is_available(self) -> bool:
        """Check if GPU is available"""
        return self.gpu_available
    
    def get_info(self) -> Dict:
        """Get GPU information"""
        return self.gpu_info
