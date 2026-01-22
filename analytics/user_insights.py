"""
User Insights - Advanced user behavior analysis
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from utils.cache_optimizer import SmartCache
from utils.performance_profiler import PerformanceProfiler


class UserInsights:
    """Advanced user behavior insights"""
    
    def __init__(self):
        self.cache = SmartCache()
        self.profiler = PerformanceProfiler()
        self.command_history: List[Dict] = []
        self.user_patterns: Dict[str, Dict] = {}
    
    def analyze_usage_patterns(self, user_id: str, days: int = 30) -> Dict:
        """Analyze user usage patterns"""
        cutoff_date = datetime.now() - timedelta(days=days)
        user_commands = [
            cmd for cmd in self.command_history
            if cmd.get("user_id") == user_id
            and datetime.fromisoformat(cmd.get("timestamp", "")) > cutoff_date
        ]
        
        # Most used commands
        command_counts = Counter(cmd.get("command") for cmd in user_commands)
        top_commands = command_counts.most_common(10)
        
        # Time patterns
        hour_counts = Counter(
            datetime.fromisoformat(cmd.get("timestamp", "")).hour
            for cmd in user_commands
        )
        peak_hours = hour_counts.most_common(5)
        
        # Day patterns
        day_counts = Counter(
            datetime.fromisoformat(cmd.get("timestamp", "")).weekday()
            for cmd in user_commands
        )
        
        return {
            "user_id": user_id,
            "period_days": days,
            "total_commands": len(user_commands),
            "top_commands": [{"command": cmd, "count": count} for cmd, count in top_commands],
            "peak_hours": [{"hour": hour, "count": count} for hour, count in peak_hours],
            "day_distribution": dict(day_counts)
        }
    
    def predict_next_command(self, user_id: str, context: Dict = None) -> List[str]:
        """Predict next likely commands"""
        patterns = self.user_patterns.get(user_id, {})
        
        # Get recent commands
        recent = [
            cmd for cmd in self.command_history
            if cmd.get("user_id") == user_id
        ][-5:]
        
        # Simple prediction based on patterns
        predictions = []
        if recent:
            last_command = recent[-1].get("command", "")
            # In production, would use ML model
            predictions = [
                f"repeat {last_command}",
                "show results",
                "get system information"
            ]
        
        return predictions
    
    def get_productivity_score(self, user_id: str) -> Dict:
        """Calculate user productivity score"""
        user_commands = [
            cmd for cmd in self.command_history
            if cmd.get("user_id") == user_id
        ]
        
        if not user_commands:
            return {"score": 0, "level": "beginner"}
        
        # Calculate score based on various factors
        total_commands = len(user_commands)
        unique_commands = len(set(cmd.get("command") for cmd in user_commands))
        success_rate = sum(1 for cmd in user_commands if cmd.get("success")) / total_commands
        
        score = (total_commands * 0.3) + (unique_commands * 0.4) + (success_rate * 100 * 0.3)
        
        if score > 80:
            level = "expert"
        elif score > 50:
            level = "advanced"
        elif score > 20:
            level = "intermediate"
        else:
            level = "beginner"
        
        return {
            "user_id": user_id,
            "score": round(score, 2),
            "level": level,
            "total_commands": total_commands,
            "unique_commands": unique_commands,
            "success_rate": round(success_rate, 2)
        }
