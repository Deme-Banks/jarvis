"""
Advanced Obfuscation Techniques
WARNING: For authorized testing and educational purposes only.
"""
import base64
import zlib
import random
import string
from typing import Dict, Optional
import ast
import re


class AdvancedObfuscator:
    """Advanced code obfuscation techniques"""
    
    def __init__(self):
        pass
    
    def control_flow_obfuscation(self, code: str) -> str:
        """Obfuscate control flow"""
        # Add dummy conditions
        obfuscated = code
        
        # Replace if statements with obfuscated versions
        pattern = r'if\s+([^:]+):'
        def obfuscate_condition(match):
            condition = match.group(1)
            dummy_var = ''.join(random.choices(string.ascii_lowercase, k=8))
            return f'if ({dummy_var} := {random.randint(0, 1)}) or ({condition}):'
        
        obfuscated = re.sub(pattern, obfuscate_condition, obfuscated)
        
        return obfuscated
    
    def api_hashing(self, code: str) -> str:
        """Hash API calls"""
        # Find common API calls
        api_calls = {
            'socket': 'hash_socket',
            'subprocess': 'hash_subprocess',
            'os': 'hash_os'
        }
        
        obfuscated = code
        for api, hash_name in api_calls.items():
            # Simple hash (in real implementation, use proper hashing)
            hash_value = hash(api) % 10000
            obfuscated = obfuscated.replace(f'import {api}', f'# {api} -> {hash_value}')
        
        return obfuscated
    
    def dynamic_loading(self, code: str) -> str:
        """Convert to dynamic loading"""
        # Encode code
        encoded = base64.b64encode(code.encode()).decode()
        
        dynamic_code = f'''
import base64
import importlib

# Encoded payload
payload = "{encoded}"

# Decode and execute
decoded = base64.b64decode(payload).decode()
exec(decoded)
'''
        return dynamic_code
    
    def multi_layer_obfuscation(self, code: str, layers: int = 3) -> str:
        """Apply multiple obfuscation layers"""
        obfuscated = code
        
        for i in range(layers):
            # Layer 1: Compress
            if i == 0:
                compressed = zlib.compress(obfuscated.encode())
                encoded = base64.b64encode(compressed).decode()
                obfuscated = f'''
import zlib, base64
exec(zlib.decompress(base64.b64decode("{encoded}")).decode())
'''
            # Layer 2: Encrypt
            elif i == 1:
                key = ''.join(random.choices(string.ascii_letters, k=16))
                encrypted = bytearray()
                for j, byte in enumerate(obfuscated.encode()):
                    encrypted.append(byte ^ ord(key[j % len(key)]))
                encoded = base64.b64encode(encrypted).decode()
                obfuscated = f'''
import base64
key = "{key}"
encrypted = "{encoded}"
decrypted = bytearray()
for i, byte in enumerate(base64.b64decode(encrypted)):
    decrypted.append(byte ^ ord(key[i % len(key)]))
exec(decrypted.decode())
'''
            # Layer 3: Add junk
            else:
                obfuscated = self._add_junk_code(obfuscated)
        
        return obfuscated
    
    def _add_junk_code(self, code: str) -> str:
        """Add junk code"""
        lines = code.split('\n')
        junk_lines = []
        
        for _ in range(random.randint(3, 7)):
            var = ''.join(random.choices(string.ascii_lowercase, k=8))
            junk_lines.append(f"{var} = {random.randint(0, 1000)}")
            junk_lines.append(f"if {var} > 9999: pass")
        
        # Insert at random positions
        for junk in junk_lines:
            pos = random.randint(0, len(lines))
            lines.insert(pos, junk)
        
        return '\n'.join(lines)
    
    def create_fully_obfuscated(self, payload_path: str) -> Dict:
        """Create fully obfuscated payload"""
        with open(payload_path, 'r') as f:
            code = f.read()
        
        # Apply all obfuscation techniques
        obfuscated = self.multi_layer_obfuscation(code, layers=3)
        obfuscated = self.control_flow_obfuscation(obfuscated)
        obfuscated = self.api_hashing(obfuscated)
        
        # Save
        import os
        obfuscated_path = os.path.join(
            os.path.dirname(payload_path),
            f"fully_obfuscated_{os.path.basename(payload_path)}"
        )
        
        with open(obfuscated_path, 'w') as f:
            f.write(obfuscated)
        
        return {
            "type": "fully_obfuscated",
            "original": payload_path,
            "obfuscated": obfuscated_path,
            "layers": 3,
            "warning": "Educational only. Use in isolated VM. Illegal without authorization."
        }
