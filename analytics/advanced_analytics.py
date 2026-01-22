"""
Advanced Analytics - Deep insights and predictions
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import statistics


class AdvancedAnalytics:
    """Advanced analytics and insights"""
    
    def __init__(self, data_file: str = "data/analytics.json"):
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load analytics data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {"events": [], "metrics": {}}
        return {"events": [], "metrics": {}}
    
    def _save_data(self):
        """Save analytics data"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def track_event(self, event_type: str, event_data: Dict):
        """Track an event"""
        event = {
            "type": event_type,
            "data": event_data,
            "timestamp": datetime.now().isoformat()
        }
        
        self.data["events"].append(event)
        self._save_data()
    
    def analyze_usage_patterns(self, days: int = 7) -> Dict:
        """Analyze usage patterns"""
        cutoff = datetime.now() - timedelta(days=days)
        recent_events = [
            e for e in self.data["events"]
            if datetime.fromisoformat(e["timestamp"]) >= cutoff
        ]
        
        # Time patterns
        hour_counts = Counter()
        day_counts = Counter()
        
        for event in recent_events:
            dt = datetime.fromisoformat(event["timestamp"])
            hour_counts[dt.hour] += 1
            day_counts[dt.strftime("%A")] += 1
        
        # Event type patterns
        event_type_counts = Counter(e["type"] for e in recent_events)
        
        return {
            "period_days": days,
            "total_events": len(recent_events),
            "hourly_distribution": dict(hour_counts),
            "daily_distribution": dict(day_counts),
            "event_types": dict(event_type_counts),
            "peak_hour": hour_counts.most_common(1)[0][0] if hour_counts else None,
            "peak_day": day_counts.most_common(1)[0][0] if day_counts else None
        }
    
    def predict_next_action(self, recent_actions: List[str]) -> Optional[str]:
        """Predict next likely action"""
        if len(recent_actions) < 2:
            return None
        
        # Analyze patterns
        patterns = defaultdict(list)
        for i in range(len(recent_actions) - 1):
            current = recent_actions[i]
            next_action = recent_actions[i + 1]
            patterns[current].append(next_action)
        
        # Get most likely next action
        last_action = recent_actions[-1]
        if last_action in patterns:
            next_actions = patterns[last_action]
            most_common = Counter(next_actions).most_common(1)
            if most_common:
                return most_common[0][0]
        
        return None
    
    def generate_insights(self) -> List[Dict]:
        """Generate actionable insights"""
        insights = []
        
        # Analyze patterns
        patterns = self.analyze_usage_patterns()
        
        # Peak usage insight
        if patterns.get("peak_hour") is not None:
            insights.append({
                "type": "usage_pattern",
                "title": "Peak Usage Time",
                "message": f"Most active during hour {patterns['peak_hour']}:00",
                "recommendation": f"Consider scheduling important tasks around {patterns['peak_hour']}:00"
            })
        
        # Event type insight
        if patterns.get("event_types"):
            most_common = max(patterns["event_types"].items(), key=lambda x: x[1])
            insights.append({
                "type": "activity_focus",
                "title": "Most Common Activity",
                "message": f"Most frequent activity: {most_common[0]} ({most_common[1]} times)",
                "recommendation": f"Consider creating shortcuts for {most_common[0]}"
            })
        
        return insights
    
    def calculate_metrics(self) -> Dict:
        """Calculate key metrics"""
        events = self.data.get("events", [])
        
        if not events:
            return {"error": "No data available"}
        
        # Time-based metrics
        timestamps = [datetime.fromisoformat(e["timestamp"]) for e in events]
        time_diffs = [
            (timestamps[i+1] - timestamps[i]).total_seconds()
            for i in range(len(timestamps) - 1)
        ]
        
        return {
            "total_events": len(events),
            "avg_time_between_events": statistics.mean(time_diffs) if time_diffs else 0,
            "events_per_day": len(events) / max(1, (timestamps[-1] - timestamps[0]).days) if len(timestamps) > 1 else 0,
            "unique_event_types": len(set(e["type"] for e in events)),
            "date_range": {
                "start": timestamps[0].isoformat() if timestamps else None,
                "end": timestamps[-1].isoformat() if timestamps else None
            }
        }
