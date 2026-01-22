"""
Enhanced Cybersecurity Module Improvements
"""
import re
import json
import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import ipaddress


@dataclass
class AttackReport:
    """Structured attack report for VSOC"""
    timestamp: str
    attack_type: str
    target: str
    duration: float
    packets_sent: int
    success_rate: float
    detection_methods: List[str]
    recommendations: List[str]


class ImprovedNLP:
    """Enhanced Natural Language Processing for security commands"""
    
    @staticmethod
    def extract_target(text: str) -> Optional[Tuple[str, Optional[int]]]:
        """Extract IP address or hostname from text"""
        # IPv4 pattern
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ip_match = re.search(ip_pattern, text)
        if ip_match:
            ip = ip_match.group()
            # Try to extract port
            port_pattern = r':(\d{1,5})'
            port_match = re.search(port_pattern, text)
            port = int(port_match.group(1)) if port_match else None
            return (ip, port)
        
        # Hostname pattern
        hostname_pattern = r'\b([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
        hostname_match = re.search(hostname_pattern, text)
        if hostname_match:
            hostname = hostname_match.group()
            port_match = re.search(r':(\d{1,5})', text)
            port = int(port_match.group(1)) if port_match else None
            return (hostname, port)
        
        # Check for localhost
        if 'localhost' in text.lower():
            port_match = re.search(r':(\d{1,5})', text)
            port = int(port_match.group(1)) if port_match else 80
            return ('127.0.0.1', port)
        
        return None
    
    @staticmethod
    def extract_duration(text: str) -> int:
        """Extract duration in seconds from text"""
        # Look for numbers followed by time units
        patterns = [
            (r'(\d+)\s*(?:second|sec)', 1),
            (r'(\d+)\s*(?:minute|min)', 60),
            (r'(\d+)\s*(?:hour|hr)', 3600),
        ]
        
        for pattern, multiplier in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return int(match.group(1)) * multiplier
        
        # Default duration
        return 10
    
    @staticmethod
    def extract_intensity(text: str) -> int:
        """Extract attack intensity/threads from text"""
        intensity_keywords = {
            'light': 5,
            'low': 5,
            'medium': 20,
            'moderate': 20,
            'high': 50,
            'heavy': 50,
            'extreme': 100
        }
        
        text_lower = text.lower()
        for keyword, value in intensity_keywords.items():
            if keyword in text_lower:
                return value
        
        # Extract number if mentioned
        num_match = re.search(r'(\d+)\s*(?:thread|connection|worker)', text.lower())
        if num_match:
            return int(num_match.group(1))
        
        return 10  # Default


class VSOCReporter:
    """VSOC integration and reporting"""
    
    def __init__(self, report_dir: str = "./vsoc_reports"):
        import os
        self.report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)
    
    def generate_report(self, attack_data: Dict) -> AttackReport:
        """Generate structured attack report"""
        report = AttackReport(
            timestamp=datetime.datetime.now().isoformat(),
            attack_type=attack_data.get('type', 'unknown'),
            target=attack_data.get('target', 'unknown'),
            duration=attack_data.get('duration', 0),
            packets_sent=attack_data.get('packets_sent', 0),
            success_rate=attack_data.get('success_rate', 0.0),
            detection_methods=self._suggest_detection_methods(attack_data),
            recommendations=self._generate_recommendations(attack_data)
        )
        
        # Save report
        self._save_report(report)
        
        return report
    
    def _suggest_detection_methods(self, attack_data: Dict) -> List[str]:
        """Suggest detection methods based on attack type"""
        attack_type = attack_data.get('type', '').lower()
        
        detection_map = {
            'tcp': ['SYN flood detection', 'Connection rate monitoring', 'Firewall logs'],
            'udp': ['UDP flood detection', 'Bandwidth monitoring', 'Packet analysis'],
            'http': ['Web server logs', 'Rate limiting alerts', 'Application monitoring'],
            'slowloris': ['Connection timeout monitoring', 'HTTP header analysis', 'Server resource monitoring']
        }
        
        for key, methods in detection_map.items():
            if key in attack_type:
                return methods
        
        return ['Network monitoring', 'Log analysis', 'Anomaly detection']
    
    def _generate_recommendations(self, attack_data: Dict) -> List[str]:
        """Generate defensive recommendations"""
        recommendations = [
            "Implement rate limiting",
            "Configure firewall rules",
            "Enable DDoS protection",
            "Monitor network traffic",
            "Set up alerting thresholds"
        ]
        
        attack_type = attack_data.get('type', '').lower()
        if 'tcp' in attack_type or 'syn' in attack_type:
            recommendations.append("Enable SYN cookies")
            recommendations.append("Reduce SYN timeout")
        
        if 'http' in attack_type:
            recommendations.append("Use CDN for DDoS mitigation")
            recommendations.append("Implement CAPTCHA")
        
        return recommendations
    
    def _save_report(self, report: AttackReport):
        """Save report to file"""
        filename = f"{self.report_dir}/attack_{report.timestamp.replace(':', '-')}.json"
        with open(filename, 'w') as f:
            json.dump(asdict(report), f, indent=2)
    
    def export_summary(self, reports: List[AttackReport]) -> str:
        """Export summary of all attacks"""
        summary = {
            "total_attacks": len(reports),
            "attack_types": {},
            "total_packets": sum(r.packets_sent for r in reports),
            "attacks": [asdict(r) for r in reports]
        }
        
        for report in reports:
            attack_type = report.attack_type
            summary["attack_types"][attack_type] = summary["attack_types"].get(attack_type, 0) + 1
        
        filename = f"{self.report_dir}/summary_{datetime.datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return filename


class EnhancedAuthorization:
    """Improved authorization system"""
    
    def __init__(self, whitelist_file: str = "./authorized_targets.json"):
        self.whitelist_file = whitelist_file
        self.whitelist = self._load_whitelist()
    
    def _load_whitelist(self) -> List[str]:
        """Load authorized targets"""
        try:
            with open(self.whitelist_file, 'r') as f:
                data = json.load(f)
                return data.get('targets', ['127.0.0.1', 'localhost'])
        except:
            return ['127.0.0.1', 'localhost']
    
    def is_authorized(self, target: str) -> Tuple[bool, str]:
        """Check if target is authorized"""
        # Extract IP/hostname
        if '://' in target:
            from urllib.parse import urlparse
            target = urlparse(target).hostname or target
        
        # Check whitelist
        if target in self.whitelist:
            return True, "Authorized"
        
        # Check if localhost
        if target in ['127.0.0.1', 'localhost', '0.0.0.0']:
            return True, "Localhost (safe for testing)"
        
        # Check private IP ranges
        try:
            ip = ipaddress.ip_address(target)
            if ip.is_private:
                return False, "Private IP - requires explicit authorization"
        except:
            pass
        
        return False, "Not authorized - add to whitelist or get explicit permission"
    
    def add_target(self, target: str, reason: str = ""):
        """Add target to whitelist"""
        if target not in self.whitelist:
            self.whitelist.append(target)
            self._save_whitelist()
    
    def _save_whitelist(self):
        """Save whitelist to file"""
        data = {
            "targets": self.whitelist,
            "last_updated": datetime.datetime.now().isoformat()
        }
        with open(self.whitelist_file, 'w') as f:
            json.dump(data, f, indent=2)


class AttackMonitor:
    """Real-time attack monitoring"""
    
    def __init__(self):
        self.metrics = {
            "packets_per_second": [],
            "connections_active": 0,
            "errors": 0,
            "start_time": None
        }
    
    def start_monitoring(self):
        """Start monitoring session"""
        self.metrics["start_time"] = datetime.datetime.now()
    
    def record_packet(self):
        """Record packet sent"""
        self.metrics["packets_per_second"].append(datetime.datetime.now())
    
    def get_stats(self) -> Dict:
        """Get current statistics"""
        if not self.metrics["start_time"]:
            return {}
        
        elapsed = (datetime.datetime.now() - self.metrics["start_time"]).total_seconds()
        pps = len(self.metrics["packets_per_second"]) / elapsed if elapsed > 0 else 0
        
        return {
            "duration": elapsed,
            "packets_per_second": pps,
            "total_packets": len(self.metrics["packets_per_second"]),
            "active_connections": self.metrics["connections_active"],
            "errors": self.metrics["errors"]
        }
