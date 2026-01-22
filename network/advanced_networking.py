"""
Advanced Networking Capabilities
"""
import socket
import subprocess
import platform
from typing import Dict, List, Optional, Tuple
import ipaddress
import threading
import time


class AdvancedNetworking:
    """Advanced networking utilities"""
    
    def __init__(self):
        self.system = platform.system()
    
    def scan_port(self, host: str, port: int, timeout: float = 1.0) -> bool:
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def scan_ports(self, host: str, ports: List[int], 
                  timeout: float = 1.0, max_threads: int = 100) -> Dict[int, bool]:
        """Scan multiple ports"""
        results = {}
        lock = threading.Lock()
        
        def scan_port_thread(port):
            is_open = self.scan_port(host, port, timeout)
            with lock:
                results[port] = is_open
        
        threads = []
        for port in ports:
            while threading.active_count() >= max_threads:
                time.sleep(0.1)
            
            thread = threading.Thread(target=scan_port_thread, args=(port,))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        return results
    
    def scan_network(self, network: str, ports: List[int] = [22, 80, 443, 3389]) -> Dict:
        """Scan network for open ports"""
        try:
            network_obj = ipaddress.ip_network(network, strict=False)
            results = {}
            
            for ip in network_obj.hosts():
                ip_str = str(ip)
                port_results = self.scan_ports(ip_str, ports)
                open_ports = [p for p, is_open in port_results.items() if is_open]
                if open_ports:
                    results[ip_str] = open_ports
            
            return {
                'network': network,
                'scanned_hosts': len(list(network_obj.hosts())),
                'hosts_with_open_ports': len(results),
                'results': results
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_local_network_info(self) -> Dict:
        """Get local network information"""
        info = {
            'hostname': socket.gethostname(),
            'local_ip': None,
            'interfaces': []
        }
        
        try:
            # Get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            info['local_ip'] = s.getsockname()[0]
            s.close()
        except:
            pass
        
        # Get network interfaces (platform-specific)
        if self.system == "Windows":
            try:
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                info['interfaces'] = result.stdout
            except:
                pass
        else:
            try:
                result = subprocess.run(['ifconfig'], capture_output=True, text=True)
                info['interfaces'] = result.stdout
            except:
                pass
        
        return info
    
    def test_connectivity(self, host: str, port: int = 80, timeout: float = 5.0) -> Dict:
        """Test connectivity to host"""
        start_time = time.time()
        is_reachable = self.scan_port(host, port, timeout)
        response_time = time.time() - start_time
        
        return {
            'host': host,
            'port': port,
            'reachable': is_reachable,
            'response_time': response_time
        }
    
    def get_route_table(self) -> Dict:
        """Get routing table"""
        if self.system == "Windows":
            try:
                result = subprocess.run(['route', 'print'], capture_output=True, text=True)
                return {'routes': result.stdout}
            except:
                return {'error': 'Failed to get routes'}
        else:
            try:
                result = subprocess.run(['route', '-n'], capture_output=True, text=True)
                return {'routes': result.stdout}
            except:
                return {'error': 'Failed to get routes'}
