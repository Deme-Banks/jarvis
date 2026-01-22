"""
Advanced Analytics and Insights
"""
from typing import Dict, List, Optional
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import json
import os


class AdvancedAnalytics:
    """Advanced analytics and insights"""
    
    def __init__(self, data_file: str = "./memory/analytics.json"):
        self.data_file = data_file
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load analytics data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {
                    'sessions': [],
                    'commands': [],
                    'features_used': [],
                    'errors': [],
                    'performance': []
                }
        return {
            'sessions': [],
            'commands': [],
            'features_used': [],
            'errors': [],
            'performance': []
        }
    
    def _save_data(self):
        """Save analytics data"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def predict_next_action(self, recent_commands: List[str]) -> List[str]:
        """Predict next likely actions"""
        if not recent_commands:
            return ["create a keylogger", "analyze network", "generate code"]
        
        # Analyze patterns
        last_command = recent_commands[-1].lower()
        
        # Common follow-up patterns
        patterns = {
            'create': ['deploy', 'test', 'analyze'],
            'analyze': ['fix', 'improve', 'test'],
            'test': ['deploy', 'create', 'analyze'],
            'deploy': ['test', 'monitor', 'verify']
        }
        
        suggestions = []
        for keyword, follow_ups in patterns.items():
            if keyword in last_command:
                suggestions.extend(follow_ups)
        
        return suggestions[:5] if suggestions else ["create", "analyze", "test"]
    
    def detect_anomalies(self) -> List[Dict]:
        """Detect anomalies in usage"""
        anomalies = []
        
        # Check for unusual error rates
        recent_errors = [e for e in self.data.get('errors', []) 
                        if datetime.fromisoformat(e['timestamp']) > datetime.now() - timedelta(hours=24)]
        
        if len(recent_errors) > 50:  # Threshold
            anomalies.append({
                'type': 'high_error_rate',
                'message': f'Unusually high error rate: {len(recent_errors)} errors in 24h',
                'severity': 'warning'
            })
        
        # Check for unusual command patterns
        recent_commands = [c for c in self.data.get('commands', [])
                         if datetime.fromisoformat(c['timestamp']) > datetime.now() - timedelta(hours=1)]
        
        if len(recent_commands) > 100:  # Threshold
            anomalies.append({
                'type': 'high_activity',
                'message': f'Unusually high activity: {len(recent_commands)} commands in 1h',
                'severity': 'info'
            })
        
        return anomalies
    
    def get_trends(self, days: int = 7) -> Dict:
        """Get usage trends"""
        cutoff = datetime.now() - timedelta(days=days)
        
        recent_commands = [
            c for c in self.data.get('commands', [])
            if datetime.fromisoformat(c['timestamp']) > cutoff
        ]
        
        # Group by day
        daily_counts = defaultdict(int)
        for cmd in recent_commands:
            date = datetime.fromisoformat(cmd['timestamp']).date()
            daily_counts[str(date)] += 1
        
        # Calculate trend
        if len(daily_counts) >= 2:
            dates = sorted(daily_counts.keys())
            recent_avg = sum(daily_counts[d] for d in dates[-3:]) / 3
            older_avg = sum(daily_counts[d] for d in dates[:3]) / 3 if len(dates) >= 6 else recent_avg
            
            trend = "increasing" if recent_avg > older_avg else "decreasing" if recent_avg < older_avg else "stable"
        else:
            trend = "insufficient_data"
        
        return {
            'period_days': days,
            'total_commands': len(recent_commands),
            'daily_average': len(recent_commands) / days if days > 0 else 0,
            'daily_counts': dict(daily_counts),
            'trend': trend
        }
    
    def get_recommendations(self) -> List[str]:
        """Get personalized recommendations"""
        recommendations = []
        
        # Analyze usage patterns
        commands = [c['command'] for c in self.data.get('commands', [])]
        
        # Check if user uses certain features
        if not any('workflow' in c.lower() for c in commands[-20:]):
            recommendations.append("Try creating workflows to automate repetitive tasks")
        
        if not any('schedule' in c.lower() for c in commands[-20:]):
            recommendations.append("Use scheduled tasks for regular security checks")
        
        if not any('ai generate' in c.lower() for c in commands[-20:]):
            recommendations.append("Try AI-powered code generation for faster development")
        
        # Performance recommendations
        perf_data = self.data.get('performance', [])
        if perf_data:
            avg_time = sum(p.get('response_time', 0) for p in perf_data[-10:]) / len(perf_data[-10:])
            if avg_time > 5.0:
                recommendations.append("Consider enabling GPU acceleration for faster responses")
        
        return recommendations[:5]
    
    def generate_report(self, period_days: int = 7) -> Dict:
        """Generate comprehensive analytics report"""
        cutoff = datetime.now() - timedelta(days=period_days)
        
        recent_data = {
            'commands': [c for c in self.data.get('commands', [])
                        if datetime.fromisoformat(c['timestamp']) > cutoff],
            'errors': [e for e in self.data.get('errors', [])
                      if datetime.fromisoformat(e['timestamp']) > cutoff],
            'sessions': [s for s in self.data.get('sessions', [])
                        if datetime.fromisoformat(s['timestamp']) > cutoff]
        }
        
        # Calculate metrics
        total_commands = len(recent_data['commands'])
        successful = sum(1 for c in recent_data['commands'] if c.get('success', False))
        success_rate = (successful / total_commands * 100) if total_commands > 0 else 0
        
        # Most used features
        features = Counter([f['feature'] for f in self.data.get('features_used', [])
                           if datetime.fromisoformat(f['timestamp']) > cutoff])
        
        # Most common commands
        commands = Counter([c['command'][:50] for c in recent_data['commands']])
        
        return {
            'period': f'{period_days} days',
            'total_commands': total_commands,
            'success_rate': f'{success_rate:.1f}%',
            'total_errors': len(recent_data['errors']),
            'total_sessions': len(recent_data['sessions']),
            'top_features': dict(features.most_common(5)),
            'top_commands': dict(commands.most_common(5)),
            'trends': self.get_trends(period_days),
            'anomalies': self.detect_anomalies(),
            'recommendations': self.get_recommendations()
        }
