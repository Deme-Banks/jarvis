"""
Cybersecurity Module Integration with JARVIS
"""
from agents.orchestrator_pi import PiOrchestrator
from cybersecurity.malware_lab import MalwareLab, SecurityTools
from cybersecurity.ddos_tester import DDoSTester, StressTester
from prompts.specialists import SECURITY_PRIVACY_PROMPT
import config_pi as config


class CybersecurityOrchestrator:
    """
    Cybersecurity testing orchestrator for VSOC.
    
    Integrates malware analysis, DDoS testing, and security tools
    with the JARVIS voice interface.
    """
    
    def __init__(self, base_orchestrator: Optional[PiOrchestrator] = None):
        self.base_orchestrator = base_orchestrator
        self.malware_lab = MalwareLab(isolated_mode=True)
        self.ddos_tester = DDoSTester(max_threads=10)
        self.security_tools = SecurityTools()
    
    def handle_security_request(self, request: str) -> str:
        """Route security-related requests"""
        request_lower = request.lower()
        
        # Malware creation requests
        if any(word in request_lower for word in ["create virus", "make malware", "payload", "keylogger", "reverse shell"]):
            return self._handle_malware_creation(request)
        
        # DDoS testing requests
        if any(word in request_lower for word in ["ddos", "flood", "stress test", "attack"]):
            return self._handle_ddos_test(request)
        
        # Security scanning
        if any(word in request_lower for word in ["scan", "nmap", "vulnerability"]):
            return self._handle_scanning(request)
        
        # General security advice
        return self._handle_general_security(request)
    
    def _handle_malware_creation(self, request: str) -> str:
        """Handle malware creation requests"""
        request_lower = request.lower()
        
        if "keylogger" in request_lower:
            payload = self.malware_lab.create_educational_payload("keylogger")
            return f"Created educational keylogger in isolated sandbox: {payload['file']}. {payload['warning']}"
        
        elif "reverse shell" in request_lower or "backdoor" in request_lower:
            payload = self.malware_lab.create_educational_payload("reverse_shell")
            return f"Created educational reverse shell: {payload['file']}. {payload['warning']} Use listener: {payload['listener']}"
        
        elif "encrypt" in request_lower or "ransomware" in request_lower:
            payload = self.malware_lab.create_educational_payload("file_encryptor")
            return f"Created educational file encryptor: {payload['file']}. {payload['warning']}"
        
        elif "scanner" in request_lower or "network scan" in request_lower:
            payload = self.malware_lab.create_educational_payload("network_scanner")
            return f"Created network scanner: {payload['file']}. {payload['warning']}"
        
        return "Available payloads: keylogger, reverse_shell, file_encryptor, network_scanner. Specify which one."
    
    def _handle_ddos_test(self, request: str) -> str:
        """Handle DDoS testing requests"""
        # Extract target from request (simplified)
        # In production, use NLP to extract IP/URL
        
        if "localhost" in request.lower() or "127.0.0.1" in request:
            target = "127.0.0.1"
            port = 80
            
            if "tcp" in request.lower() or "syn" in request.lower():
                result = self.ddos_tester.tcp_flood(target, port, duration=5)
                return f"TCP flood test completed. {result['packets_sent']} packets sent. {result['warning']}"
            
            elif "udp" in request.lower():
                result = self.ddos_tester.udp_flood(target, port, duration=5)
                return f"UDP flood test completed. {result['packets_sent']} packets sent. {result['warning']}"
            
            elif "http" in request.lower() or "web" in request.lower():
                result = self.ddos_tester.http_flood(f"http://{target}", duration=5)
                return f"HTTP flood test completed. {result['requests_sent']} requests sent. {result['warning']}"
            
            elif "slowloris" in request.lower():
                result = self.ddos_tester.slowloris(target, duration=5)
                return f"Slowloris test completed. {result['connections']} connections. {result['warning']}"
        
        return "DDoS testing available. Specify: tcp, udp, http, or slowloris. Target must be localhost or authorized network."
    
    def _handle_scanning(self, request: str) -> str:
        """Handle security scanning requests"""
        tools = self.security_tools.check_tools()
        
        if tools.get("nmap"):
            if "localhost" in request.lower():
                cmd = self.security_tools.generate_nmap_scan("127.0.0.1", "basic")
                return f"Run: {cmd} (authorized networks only)"
            else:
                return "Nmap available. Specify target (localhost only for safety)."
        else:
            return "Nmap not installed. Install: sudo apt-get install nmap"
    
    def _handle_general_security(self, request: str) -> str:
        """Handle general security questions"""
        if self.base_orchestrator:
            return self.base_orchestrator.process(
                f"{SECURITY_PRIVACY_PROMPT}\n\nUser question: {request}"
            )
        return "Security module ready. Available: malware creation, DDoS testing, scanning."
