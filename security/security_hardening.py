"""
Security Hardening - Advanced security measures
"""
import os
import hashlib
import secrets
import base64
from typing import Dict, List, Optional
from datetime import datetime


class SecurityHardening:
    """Security hardening utilities"""
    
    def generate_secure_password(self, length: int = 16,
                                 include_special: bool = True) -> str:
        """Generate secure password"""
        import string
        
        chars = string.ascii_letters + string.digits
        if include_special:
            chars += string.punctuation
        
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    def hash_password(self, password: str, algorithm: str = "sha256") -> str:
        """Hash password"""
        if algorithm == "sha256":
            return hashlib.sha256(password.encode()).hexdigest()
        elif algorithm == "bcrypt":
            try:
                import bcrypt
                return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            except ImportError:
                return hashlib.sha256(password.encode()).hexdigest()
        else:
            return hashlib.sha256(password.encode()).hexdigest()
    
    def generate_api_key(self, length: int = 32) -> str:
        """Generate secure API key"""
        return secrets.token_urlsafe(length)
    
    def encrypt_file(self, file_path: str, key: str) -> Dict:
        """Encrypt a file"""
        try:
            from cryptography.fernet import Fernet
            
            # Generate key from password
            key_hash = hashlib.sha256(key.encode()).digest()
            fernet_key = base64.urlsafe_b64encode(key_hash)
            fernet = Fernet(fernet_key)
            
            # Read and encrypt
            with open(file_path, 'rb') as f:
                data = f.read()
            
            encrypted = fernet.encrypt(data)
            
            # Write encrypted file
            encrypted_path = file_path + ".encrypted"
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted)
            
            return {"success": True, "encrypted_file": encrypted_path}
        except ImportError:
            return {"error": "cryptography not installed. Install with: pip install cryptography"}
        except Exception as e:
            return {"error": str(e)}
    
    def check_file_permissions(self, file_path: str) -> Dict:
        """Check file permissions"""
        import stat
        
        if not os.path.exists(file_path):
            return {"error": "File not found"}
        
        file_stat = os.stat(file_path)
        permissions = stat.filemode(file_stat.st_mode)
        
        return {
            "file": file_path,
            "permissions": permissions,
            "readable": os.access(file_path, os.R_OK),
            "writable": os.access(file_path, os.W_OK),
            "executable": os.access(file_path, os.X_OK)
        }
    
    def secure_delete(self, file_path: str, passes: int = 3) -> Dict:
        """Securely delete a file"""
        if not os.path.exists(file_path):
            return {"error": "File not found"}
        
        try:
            file_size = os.path.getsize(file_path)
            
            with open(file_path, 'ba+') as f:
                for _ in range(passes):
                    f.seek(0)
                    f.write(os.urandom(file_size))
            
            os.remove(file_path)
            return {"success": True, "file": file_path}
        except Exception as e:
            return {"error": str(e)}
    
    def generate_certificate(self, common_name: str, days: int = 365) -> Dict:
        """Generate self-signed certificate"""
        try:
            from cryptography import x509
            from cryptography.x509.oid import NameOID
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.asymmetric import rsa
            from cryptography.hazmat.primitives import serialization
            from datetime import timedelta
            
            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            
            # Create certificate
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "State"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "City"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Organization"),
                x509.NameAttribute(NameOID.COMMON_NAME, common_name),
            ])
            
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.utcnow()
            ).not_valid_after(
                datetime.utcnow() + timedelta(days=days)
            ).add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName(common_name),
                ]),
                critical=False,
            ).sign(private_key, hashes.SHA256())
            
            # Save certificate and key
            cert_path = f"{common_name}.crt"
            key_path = f"{common_name}.key"
            
            with open(cert_path, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            
            with open(key_path, "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            
            return {
                "success": True,
                "certificate": cert_path,
                "private_key": key_path
            }
        except ImportError:
            return {"error": "cryptography not installed. Install with: pip install cryptography"}
        except Exception as e:
            return {"error": str(e)}
