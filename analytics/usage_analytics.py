"""
Usage Analytics and Insights
"""
from typing import Dict, List, Optional
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import json
import os


class UsageAnalytics:
    """Analyze usage patterns and provide insights"""
    
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
                    'errors': []
                }
        return {
            'sessions': [],
            'commands': [],
            'features_used': [],
            'errors': []
        }
    
    def _save_data(self):
        """Save analytics data"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def record_session(self, duration: float, commands_count: int):
        """Record session"""
        self.data['sessions'].append({
            'timestamp': datetime.now().isoformat(),
            'duration': duration,
            'commands': commands_count
        })
        self._save_data()
    
    def record_command(self, command: str, success: bool, response_time: float):
        """Record command"""
        self.data['commands'].append({
            'timestamp': datetime.now().isoformat(),
            'command': command[:100],  # Truncate
            'success': success,
            'response_time': response_time
        })
        self._save_data()
    
    def record_feature(self, feature: str):
        """Record feature usage"""
        self.data['features_used'].append({
            'timestamp': datetime.now().isoformat(),
            'feature': feature
        })
        self._save_data()
    
    def record_error(self, error_type: str, error_message: str):
        """Record error"""
        self.data['errors'].append({
            'timestamp': datetime.now().isoformat(),
            'type': error_type,
            'message': error_message[:200]  # Truncate
        })
        self._save_data()
    
    def get_most_used_commands(self, limit: int = 10) -> List[Dict]:
        """Get most used commands"""
        commands = [c['command'] for c in self.data['commands']]
        counter = Counter(commands)
        
        return [
            {'command': cmd, 'count': count}
            for cmd, count in counter.most_common(limit)
        ]
    
    def get_feature_usage(self) -> Dict:
        """Get feature usage statistics"""
        features = [f['feature'] for f in self.data['features_used']]
        counter = Counter(features)
        
        return dict(counter)
    
    def get_success_rate(self) -> float:
        """Get success rate"""
        if not self.data['commands']:
            return 0.0
        
        successful = sum(1 for c in self.data['commands'] if c.get('success', False))
        return successful / len(self.data['commands'])
    
    def get_average_response_time(self) -> float:
        """Get average response time"""
        times = [c.get('response_time', 0) for c in self.data['commands'] if c.get('response_time')]
        if not times:
            return 0.0
        return sum(times) / len(times)
    
    def get_usage_by_hour(self) -> Dict:
        """Get usage by hour of day"""
        hour_counts = defaultdict(int)
        
        for command in self.data['commands']:
            timestamp = datetime.fromisoformat(command['timestamp'])
            hour = timestamp.hour
            hour_counts[hour] += 1
        
        return dict(hour_counts)
    
    def get_insights(self) -> Dict:
        """Get usage insights"""
        return {
            'total_commands': len(self.data['commands']),
            'total_sessions': len(self.data['sessions']),
            'success_rate': self.get_success_rate(),
            'avg_response_time': self.get_average_response_time(),
            'most_used_commands': self.get_most_used_commands(5),
            'feature_usage': self.get_feature_usage(),
            'usage_by_hour': self.get_usage_by_hour(),
            'total_errors': len(self.data['errors'])
        }
