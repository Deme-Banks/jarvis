"""
Alerting System for JARVIS
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from collections import deque


class AlertingSystem:
    """Alert and notification system"""
    
    def __init__(self, alerts_file: str = "./memory/alerts.json"):
        self.alerts_file = alerts_file
        os.makedirs(os.path.dirname(alerts_file), exist_ok=True)
        self.alerts = deque(maxlen=1000)
        self.alert_rules = []
        self._load_alerts()
    
    def _load_alerts(self):
        """Load alerts from file"""
        if os.path.exists(self.alerts_file):
            try:
                with open(self.alerts_file, 'r') as f:
                    data = json.load(f)
                    self.alerts = deque(data.get('alerts', []), maxlen=1000)
                    self.alert_rules = data.get('rules', [])
            except:
                pass
    
    def _save_alerts(self):
        """Save alerts to file"""
        try:
            with open(self.alerts_file, 'w') as f:
                json.dump({
                    'alerts': list(self.alerts),
                    'rules': self.alert_rules
                }, f, indent=2)
        except:
            pass
    
    def create_alert(self, level: str, message: str, source: str = "system",
                    metadata: Optional[Dict] = None) -> Dict:
        """Create an alert"""
        alert = {
            'level': level,  # info, warning, error, critical
            'message': message,
            'source': source,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {},
            'acknowledged': False
        }
        
        self.alerts.append(alert)
        self._save_alerts()
        
        # Check alert rules
        self._check_rules(alert)
        
        return alert
    
    def _check_rules(self, alert: Dict):
        """Check alert rules and trigger actions"""
        for rule in self.alert_rules:
            if self._matches_rule(alert, rule):
                self._execute_rule_action(alert, rule)
    
    def _matches_rule(self, alert: Dict, rule: Dict) -> bool:
        """Check if alert matches rule"""
        # Check level
        if rule.get('level') and alert['level'] != rule['level']:
            return False
        
        # Check source
        if rule.get('source') and alert['source'] != rule['source']:
            return False
        
        # Check keywords
        if rule.get('keywords'):
            message_lower = alert['message'].lower()
            if not any(kw.lower() in message_lower for kw in rule['keywords']):
                return False
        
        return True
    
    def _execute_rule_action(self, alert: Dict, rule: Dict):
        """Execute rule action"""
        action = rule.get('action')
        
        if action == 'notify':
            # Send notification (would integrate with notification services)
            pass
        elif action == 'log':
            # Log to file
            pass
        elif action == 'execute':
            # Execute command
            pass
    
    def add_alert_rule(self, name: str, level: Optional[str] = None,
                       source: Optional[str] = None,
                       keywords: Optional[List[str]] = None,
                       action: str = "notify") -> bool:
        """Add alert rule"""
        rule = {
            'name': name,
            'level': level,
            'source': source,
            'keywords': keywords or [],
            'action': action
        }
        
        self.alert_rules.append(rule)
        self._save_alerts()
        return True
    
    def get_alerts(self, level: Optional[str] = None, 
                  unacknowledged_only: bool = False,
                  limit: int = 50) -> List[Dict]:
        """Get alerts"""
        alerts = list(self.alerts)
        
        # Filter by level
        if level:
            alerts = [a for a in alerts if a['level'] == level]
        
        # Filter unacknowledged
        if unacknowledged_only:
            alerts = [a for a in alerts if not a['acknowledged']]
        
        # Sort by timestamp (newest first)
        alerts.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return alerts[:limit]
    
    def acknowledge_alert(self, alert_timestamp: str) -> bool:
        """Acknowledge an alert"""
        for alert in self.alerts:
            if alert['timestamp'] == alert_timestamp:
                alert['acknowledged'] = True
                self._save_alerts()
                return True
        return False
    
    def get_stats(self) -> Dict:
        """Get alert statistics"""
        total = len(self.alerts)
        levels = {}
        unacknowledged = 0
        
        for alert in self.alerts:
            level = alert['level']
            levels[level] = levels.get(level, 0) + 1
            if not alert['acknowledged']:
                unacknowledged += 1
        
        return {
            'total_alerts': total,
            'by_level': levels,
            'unacknowledged': unacknowledged,
            'rules': len(self.alert_rules)
        }
