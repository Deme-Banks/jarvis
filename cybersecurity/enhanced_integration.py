"""
Enhanced Cybersecurity Integration with Improvements
"""
from typing import Optional, Dict
from agents.orchestrator_pi import PiOrchestrator
from cybersecurity.enhanced_ddos import EnhancedDDoSTester
from cybersecurity.enhanced_malware import EnhancedMalwareLab
from cybersecurity.improvements import ImprovedNLP, EnhancedAuthorization, VSOCReporter
from prompts.specialists import SECURITY_PRIVACY_PROMPT
import config_pi as config


class EnhancedCybersecurityOrchestrator:
    """Enhanced cybersecurity orchestrator with improved features"""
    
    def __init__(self, base_orchestrator: Optional[PiOrchestrator] = None):
        self.base_orchestrator = base_orchestrator
        self.malware_lab = EnhancedMalwareLab(isolated_mode=True)
        self.ddos_tester = EnhancedDDoSTester(max_threads=50)
        self.nlp = ImprovedNLP()
        self.authorization = EnhancedAuthorization()
        self.reporter = VSOCReporter()
    
    def handle_security_request(self, request: str) -> str:
        """Enhanced request handling with NLP"""
        request_lower = request.lower()
        
        # Malware creation
        if any(word in request_lower for word in ["create", "make", "generate", "payload", "malware", "virus"]):
            return self._handle_enhanced_malware(request)
        
        # DDoS testing
        if any(word in request_lower for word in ["ddos", "flood", "attack", "stress", "test"]):
            return self._handle_enhanced_ddos(request)
        
        # Reporting
        if any(word in request_lower for word in ["report", "summary", "stats", "results"]):
            return self._handle_reporting(request)
        
        # Authorization
        if any(word in request_lower for word in ["authorize", "whitelist", "permission"]):
            return self._handle_authorization(request)
        
        # Scanning
        if any(word in request_lower for word in ["scan", "nmap", "vulnerability"]):
            return self._handle_scanning(request)
        
        # General security
        return self._handle_general_security(request)
    
    def _handle_enhanced_malware(self, request: str) -> str:
        """Handle malware creation with options"""
        request_lower = request.lower()
        
        # Determine payload type
        payload_type = None
        if "keylogger" in request_lower:
            payload_type = "keylogger"
        elif "reverse" in request_lower or "shell" in request_lower:
            payload_type = "reverse_shell"
        elif "encrypt" in request_lower or "ransom" in request_lower:
            payload_type = "file_encryptor"
        
        if not payload_type:
            return "Specify payload type: keylogger, reverse_shell, or file_encryptor"
        
        # Check for obfuscation
        obfuscation = None
        if "obfuscate" in request_lower or "obfuscated" in request_lower:
            obfuscation = "base64" if "base64" in request_lower else "compression"
        
        if obfuscation:
            payload = self.malware_lab.create_obfuscated_payload(payload_type, obfuscation)
            return f"Created obfuscated {payload_type} with {obfuscation}: {payload['file']}. {payload['warning']}"
        elif "polymorphic" in request_lower:
            payload = self.malware_lab.create_polymorphic_payload(payload_type)
            return f"Created polymorphic {payload_type}: {payload['file']}. {payload['warning']}"
        else:
            # Use enhanced malware lab
            payload = self.malware_lab.create_obfuscated_payload(payload_type, "none")
            return f"Created {payload_type}: {payload['file']}. {payload['warning']}"
    
    def _handle_enhanced_ddos(self, request: str) -> str:
        """Handle DDoS with natural language parsing"""
        try:
            # Parse command
            attack_config = self.ddos_tester.parse_attack_command(request)
            
            # Check authorization
            is_auth, message = self.authorization.is_authorized(attack_config["target"])
            if not is_auth:
                return f"Authorization failed: {message}"
            
            # Execute attack
            attack_type = attack_config["type"]
            target = attack_config["target"]
            port = attack_config["port"]
            duration = attack_config["duration"]
            threads = attack_config["intensity"]
            
            if attack_type == "tcp":
                result = self.ddos_tester.advanced_tcp_flood(target, port, duration, threads)
            elif attack_type == "udp":
                result = self.ddos_tester.udp_flood(target, port, duration)
            elif attack_type == "http":
                url = f"http://{target}:{port}" if port != 80 else f"http://{target}"
                if "post" in request.lower():
                    result = self.ddos_tester.http_post_flood(url, duration, threads)
                else:
                    result = self.ddos_tester.http_flood(url, duration)
            elif attack_type == "slowloris":
                result = self.ddos_tester.slowloris(target, port, duration)
            elif attack_type == "icmp":
                result = self.ddos_tester.icmp_flood(target, duration, threads)
            else:
                result = self.ddos_tester.advanced_tcp_flood(target, port, duration, threads)
            
            # Format response
            response = f"{result['type']} completed. "
            if 'packets_sent' in result:
                response += f"{result['packets_sent']} packets sent. "
            if 'packets_per_second' in result:
                response += f"Rate: {result['packets_per_second']:.2f} pps. "
            if 'report' in result:
                response += f"Report saved to VSOC. "
            response += result.get('warning', '')
            
            return response
            
        except ValueError as e:
            return f"Error parsing command: {str(e)}. Specify target, duration, and attack type."
        except Exception as e:
            return f"Attack error: {str(e)}"
    
    def _handle_reporting(self, request: str) -> str:
        """Handle reporting requests"""
        import os
        import glob
        
        report_files = glob.glob("./vsoc_reports/*.json")
        if not report_files:
            return "No attack reports found."
        
        count = len(report_files)
        latest = max(report_files, key=os.path.getctime)
        
        return f"Found {count} attack reports. Latest: {os.path.basename(latest)}. Check ./vsoc_reports/ for details."
    
    def _handle_authorization(self, request: str) -> str:
        """Handle authorization requests"""
        target_info = self.nlp.extract_target(request)
        if target_info:
            target, _ = target_info
            self.authorization.add_target(target, "User request")
            return f"Added {target} to authorized targets."
        return "Could not extract target. Specify IP or hostname."
    
    def _handle_scanning(self, request: str) -> str:
        """Handle scanning requests"""
        from cybersecurity.security_agent import SecurityTools
        tools = SecurityTools()
        available = tools.check_tools()
        
        if available.get("nmap"):
            target_info = self.nlp.extract_target(request)
            if target_info:
                target, port = target_info
                cmd = tools.generate_nmap_scan(target, "basic")
                return f"Run: {cmd} (authorized networks only)"
            return "Nmap available. Specify target."
        return "Install nmap: sudo apt-get install nmap"
    
    def _handle_general_security(self, request: str) -> str:
        """Handle general security questions"""
        if self.base_orchestrator:
            return self.base_orchestrator.process(
                f"{SECURITY_PRIVACY_PROMPT}\n\nUser question: {request}"
            )
        return "Security module ready. Available: malware creation, DDoS testing, scanning, reporting."
