"""
Predictive Analytics - ML-based predictions
"""
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import Counter


class PredictiveAnalytics:
    """Predictive analytics for JARVIS"""
    
    def __init__(self):
        self.command_history = []
        self.patterns = {}
    
    def analyze_command_patterns(self, history: List[Dict]) -> Dict:
        """Analyze command patterns"""
        commands = [h.get("command", "") for h in history]
        command_counts = Counter(commands)
        
        # Find most common commands
        most_common = command_counts.most_common(10)
        
        # Find time patterns
        time_patterns = {}
        for h in history:
            hour = datetime.fromisoformat(h.get("timestamp", "")).hour
            time_patterns[hour] = time_patterns.get(hour, 0) + 1
        
        return {
            "most_common_commands": most_common,
            "time_patterns": time_patterns,
            "total_commands": len(commands)
        }
    
    def predict_next_command(self, recent_commands: List[str]) -> Optional[str]:
        """Predict next likely command"""
        if len(recent_commands) < 2:
            return None
        
        # Simple pattern matching
        last_command = recent_commands[-1]
        
        # Common patterns
        patterns = {
            "create keylogger": "deploy payload to usb",
            "scan network": "create report",
            "deploy payload": "add persistence",
            "create malware": "test malware"
        }
        
        return patterns.get(last_command.lower())
    
    def predict_usage_trends(self, history: List[Dict], days: int = 7) -> Dict:
        """Predict usage trends"""
        now = datetime.now()
        start_date = now - timedelta(days=days)
        
        recent_commands = [
            h for h in history
            if datetime.fromisoformat(h.get("timestamp", "")) >= start_date
        ]
        
        # Calculate trends
        daily_counts = {}
        for h in recent_commands:
            date = datetime.fromisoformat(h.get("timestamp", "")).date()
            daily_counts[date] = daily_counts.get(date, 0) + 1
        
        # Predict next day
        if len(daily_counts) >= 2:
            recent_days = sorted(daily_counts.items())[-3:]
            avg = sum(count for _, count in recent_days) / len(recent_days)
            predicted = int(avg)
        else:
            predicted = len(recent_commands) // days
        
        return {
            "historical_average": sum(daily_counts.values()) / len(daily_counts) if daily_counts else 0,
            "predicted_next_day": predicted,
            "trend": "increasing" if predicted > (sum(daily_counts.values()) / len(daily_counts) if daily_counts else 0) else "decreasing"
        }
    
    def detect_anomalies(self, history: List[Dict]) -> List[Dict]:
        """Detect anomalous behavior"""
        anomalies = []
        
        # Check for unusual command frequency
        commands = [h.get("command", "") for h in history]
        command_counts = Counter(commands)
        
        avg_count = sum(command_counts.values()) / len(command_counts) if command_counts else 0
        
        for command, count in command_counts.items():
            if count > avg_count * 3:  # 3x more than average
                anomalies.append({
                    "type": "unusual_frequency",
                    "command": command,
                    "count": count,
                    "average": avg_count
                })
        
        # Check for unusual time patterns
        night_commands = [
            h for h in history
            if 0 <= datetime.fromisoformat(h.get("timestamp", "")).hour < 6
        ]
        
        if len(night_commands) > len(history) * 0.2:  # More than 20% at night
            anomalies.append({
                "type": "unusual_time",
                "description": "High activity during night hours",
                "count": len(night_commands)
            })
        
        return anomalies
