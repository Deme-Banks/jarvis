"""
Threat Intelligence Integration
"""
import os
import requests
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class ThreatIntelligence:
    """Threat intelligence feeds integration"""
    
    def __init__(self):
        self.feeds = {
            "alienvault": "https://otx.alienvault.com/api/v1/pulses/subscribed",
            "abuse_ch": "https://feeds.abuse.ch/urlhaus/recent/",
            "malware_bazaar": "https://mb-api.abuse.ch/api/v1/"
        }
    
    def get_recent_threats(self, feed: str = "alienvault",
                          limit: int = 10) -> List[Dict]:
        """Get recent threats from feed"""
        threats = []
        
        try:
            if feed == "alienvault":
                api_key = os.getenv("ALIENVAULT_API_KEY")
                if api_key:
                    url = f"{self.feeds[feed]}?limit={limit}"
                    headers = {"X-OTX-API-KEY": api_key}
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        for pulse in data.get("results", [])[:limit]:
                            threats.append({
                                "title": pulse.get("name"),
                                "description": pulse.get("description"),
                                "tags": pulse.get("tags", []),
                                "created": pulse.get("created")
                            })
            
            elif feed == "abuse_ch":
                response = requests.get(self.feeds[feed], timeout=10)
                if response.status_code == 200:
                    lines = response.text.split("\n")
                    for line in lines[:limit]:
                        if line and not line.startswith("#"):
                            parts = line.split(",")
                            if len(parts) >= 2:
                                threats.append({
                                    "url": parts[1],
                                    "status": parts[0],
                                    "date": parts[2] if len(parts) > 2 else ""
                                })
        
        except Exception as e:
            threats.append({"error": str(e)})
        
        return threats
    
    def check_ip_reputation(self, ip: str) -> Dict:
        """Check IP reputation"""
        reputation = {
            "ip": ip,
            "timestamp": datetime.now().isoformat(),
            "sources": {}
        }
        
        # Check multiple sources
        sources = {
            "abuseipdb": f"https://api.abuseipdb.com/api/v2/check",
            "virustotal": f"https://www.virustotal.com/vtapi/v2/ip-address/report"
        }
        
        for source, url in sources.items():
            try:
                api_key = os.getenv(f"{source.upper()}_API_KEY")
                if api_key:
                    if source == "abuseipdb":
                        params = {"ipAddress": ip, "maxAgeInDays": 90}
                        headers = {"Key": api_key}
                        response = requests.get(url, params=params, headers=headers, timeout=10)
                        if response.status_code == 200:
                            data = response.json()
                            reputation["sources"][source] = {
                                "abuse_confidence": data.get("data", {}).get("abuseConfidencePercentage"),
                                "is_public": data.get("data", {}).get("isPublic")
                            }
            except:
                pass
        
        return reputation
    
    def get_malware_samples(self, limit: int = 10) -> List[Dict]:
        """Get recent malware samples"""
        samples = []
        
        try:
            url = self.feeds["malware_bazaar"]
            data = {
                "query": "get_recent",
                "selector": "time",
                "limit": limit
            }
            
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                for sample in result.get("data", [])[:limit]:
                    samples.append({
                        "sha256": sample.get("sha256_hash"),
                        "file_type": sample.get("file_type"),
                        "first_seen": sample.get("first_seen"),
                        "tags": sample.get("tags", [])
                    })
        except Exception as e:
            samples.append({"error": str(e)})
        
        return samples
