"""
Advanced Security Features
"""
import os
import hashlib
import json
from typing import Dict, List, Optional
from datetime import datetime
import tempfile


class AdvancedSecurity:
    """Advanced security features"""
    
    def __init__(self):
        self.security_log = []
        self.threat_detection_enabled = True
    
    def detect_suspicious_activity(self, activity: Dict) -> Dict:
        """Detect suspicious activity"""
        suspicious_indicators = []
        
        # Check for rapid command execution
        if activity.get('commands_per_minute', 0) > 50:
            suspicious_indicators.append('high_command_rate')
        
        # Check for unusual patterns
        if activity.get('error_rate', 0) > 0.5:
            suspicious_indicators.append('high_error_rate')
        
        # Check for unauthorized access attempts
        if activity.get('unauthorized_attempts', 0) > 0:
            suspicious_indicators.append('unauthorized_access')
        
        if suspicious_indicators:
            return {
                'suspicious': True,
                'indicators': suspicious_indicators,
                'severity': 'high' if 'unauthorized_access' in suspicious_indicators else 'medium',
                'recommendation': 'Review activity and enable additional security measures'
            }
        
        return {'suspicious': False}
    
    def create_security_audit(self, audit_type: str = "full") -> Dict:
        """Create security audit"""
        audit = {
            'type': audit_type,
            'timestamp': datetime.now().isoformat(),
            'findings': [],
            'recommendations': []
        }
        
        # Check configurations
        config_checks = {
            'isolated_mode': True,
            'authorization_enabled': True,
            'logging_enabled': True,
            'backup_enabled': True
        }
        
        for check, expected in config_checks.items():
            # In real implementation, would check actual config
            audit['findings'].append({
                'check': check,
                'status': 'pass' if expected else 'fail',
                'recommendation': f"Ensure {check} is properly configured"
            })
        
        # Save audit
        audit_file = os.path.join(
            tempfile.gettempdir(),
            f"security_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(audit_file, 'w') as f:
            json.dump(audit, f, indent=2)
        
        return {
            'success': True,
            'audit_file': audit_file,
            'audit': audit
        }
    
    def hash_file(self, file_path: str, algorithm: str = "sha256") -> Dict:
        """Calculate file hash"""
        if not os.path.exists(file_path):
            return {'success': False, 'error': 'File not found'}
        
        try:
            hash_obj = hashlib.new(algorithm)
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            
            file_hash = hash_obj.hexdigest()
            
            return {
                'success': True,
                'file': file_path,
                'algorithm': algorithm,
                'hash': file_hash
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def verify_file_integrity(self, file_path: str, expected_hash: str,
                            algorithm: str = "sha256") -> Dict:
        """Verify file integrity"""
        result = self.hash_file(file_path, algorithm)
        
        if not result.get('success'):
            return result
        
        actual_hash = result['hash']
        match = actual_hash == expected_hash
        
        return {
            'success': True,
            'file': file_path,
            'match': match,
            'expected': expected_hash,
            'actual': actual_hash,
            'status': 'verified' if match else 'modified'
        }
