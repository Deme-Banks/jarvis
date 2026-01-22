"""
Network Traffic Analyzer
WARNING: For authorized testing and educational purposes only.
"""
import os
import tempfile
import json
from typing import Dict, List, Optional
from datetime import datetime


class NetworkAnalyzer:
    """Network traffic analysis tool"""
    
    def create_network_analyzer(self, analysis_types: List[str] = None,
                               capture_duration: int = 60) -> Dict:
        """Create network traffic analyzer"""
        analysis_types = analysis_types or ['packet_capture', 'traffic_analysis', 'protocol_analysis']
        
        code = f'''"""
Educational Network Traffic Analyzer - FOR AUTHORIZED TESTING ONLY
WARNING: Use only in isolated VMs. Illegal without authorization.
"""
import socket
import subprocess
import json
import platform
from datetime import datetime
from collections import defaultdict

def capture_packets(duration=60):
    """Capture network packets"""
    captured_data = {{
        'packets': [],
        'protocols': defaultdict(int),
        'connections': defaultdict(int),
        'start_time': datetime.now().isoformat()
    }}
    
    try:
        if platform.system() == 'Windows':
            # Use netsh trace (requires admin)
            print("Starting packet capture (Windows)...")
            # Note: Full packet capture requires admin and specialized tools
            # This is a simplified version
            result = subprocess.run(['netstat', '-an'], 
                                  capture_output=True, text=True, timeout=duration)
            captured_data['netstat_output'] = result.stdout
        else:
            # Use tcpdump (requires root)
            print("Starting packet capture (Linux/Mac)...")
            # Note: Full packet capture requires root and tcpdump
            # This is a simplified version
            result = subprocess.run(['netstat', '-an'], 
                                  capture_output=True, text=True, timeout=duration)
            captured_data['netstat_output'] = result.stdout
    except Exception as e:
        captured_data['error'] = str(e)
    
    return captured_data

def analyze_traffic():
    """Analyze network traffic patterns"""
    analysis = {{
        'active_connections': [],
        'listening_ports': [],
        'established_connections': [],
        'foreign_addresses': []
    }}
    
    try:
        if platform.system() == 'Windows':
            result = subprocess.run(['netstat', '-an'], 
                                  capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(['netstat', '-an'], 
                                  capture_output=True, text=True, timeout=10)
        
        for line in result.stdout.split('\\n'):
            if 'LISTENING' in line or 'LISTEN' in line:
                parts = line.split()
                if len(parts) >= 2:
                    analysis['listening_ports'].append(parts[1])
            elif 'ESTABLISHED' in line or 'ESTAB' in line:
                parts = line.split()
                if len(parts) >= 2:
                    local_addr = parts[1]
                    remote_addr = parts[2] if len(parts) > 2 else None
                    analysis['established_connections'].append({{
                        'local': local_addr,
                        'remote': remote_addr
                    }})
                    if remote_addr:
                        analysis['foreign_addresses'].append(remote_addr)
    except Exception as e:
        analysis['error'] = str(e)
    
    return analysis

def analyze_protocols():
    """Analyze network protocols"""
    protocol_stats = defaultdict(int)
    
    try:
        if platform.system() == 'Windows':
            result = subprocess.run(['netstat', '-s'], 
                                  capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(['netstat', '-s'], 
                                  capture_output=True, text=True, timeout=10)
        
        # Parse protocol statistics
        for line in result.stdout.split('\\n'):
            if 'TCP' in line:
                protocol_stats['TCP'] += 1
            elif 'UDP' in line:
                protocol_stats['UDP'] += 1
            elif 'ICMP' in line:
                protocol_stats['ICMP'] += 1
    except Exception as e:
        protocol_stats['error'] = str(e)
    
    return dict(protocol_stats)

def detect_suspicious_activity():
    """Detect suspicious network activity"""
    suspicious = {{
        'unusual_ports': [],
        'foreign_connections': [],
        'high_connection_count': False
    }}
    
    try:
        analysis = analyze_traffic()
        
        # Check for unusual ports
        common_ports = [80, 443, 22, 21, 25, 53, 3389, 8080]
        for port_str in analysis.get('listening_ports', []):
            try:
                port = int(port_str.split(':')[-1])
                if port not in common_ports and port > 1024:
                    suspicious['unusual_ports'].append(port)
            except:
                pass
        
        # Check foreign connections
        foreign_addrs = analysis.get('foreign_addresses', [])
        if len(foreign_addrs) > 10:
            suspicious['high_connection_count'] = True
            suspicious['foreign_connections'] = list(set(foreign_addrs))[:10]
    except Exception as e:
        suspicious['error'] = str(e)
    
    return suspicious

# Main execution
analysis_types = {analysis_types}
capture_duration = {capture_duration}

results = {{
    'timestamp': datetime.now().isoformat(),
    'capture_duration': capture_duration
}}

if 'packet_capture' in analysis_types:
    print("Capturing packets...")
    results['packet_capture'] = capture_packets(capture_duration)

if 'traffic_analysis' in analysis_types:
    print("Analyzing traffic...")
    results['traffic_analysis'] = analyze_traffic()

if 'protocol_analysis' in analysis_types:
    print("Analyzing protocols...")
    results['protocol_analysis'] = analyze_protocols()

if 'suspicious_activity' in analysis_types:
    print("Detecting suspicious activity...")
    results['suspicious_activity'] = detect_suspicious_activity()

# Save results
with open('network_analysis.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

print("\\nNetwork analysis saved to network_analysis.json")
'''
        
        filepath = os.path.join(
            tempfile.gettempdir(),
            f"network_analyzer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        )
        
        with open(filepath, 'w') as f:
            f.write(code)
        
        return {
            'type': 'network_analyzer',
            'file': filepath,
            'analysis_types': analysis_types,
            'capture_duration': capture_duration,
            'warning': 'Educational only. Use in isolated VM. Illegal without authorization.'
        }
