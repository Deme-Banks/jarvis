"""
Voice Feedback and Learning System
"""
from typing import Dict, List, Optional
from datetime import datetime
import json
import os


class VoiceFeedback:
    """Voice feedback and learning system"""
    
    def __init__(self, feedback_file: str = "./memory/feedback.json"):
        self.feedback_file = feedback_file
        os.makedirs(os.path.dirname(feedback_file), exist_ok=True)
        self.feedback_history = []
        self.learned_preferences = {}
        self._load_feedback()
    
    def _load_feedback(self):
        """Load feedback history"""
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r') as f:
                    data = json.load(f)
                    self.feedback_history = data.get('history', [])
                    self.learned_preferences = data.get('preferences', {})
            except:
                pass
    
    def _save_feedback(self):
        """Save feedback"""
        with open(self.feedback_file, 'w') as f:
            json.dump({
                'history': self.feedback_history,
                'preferences': self.learned_preferences
            }, f, indent=2)
    
    def record_feedback(self, command: str, response: str, rating: int,
                       comment: Optional[str] = None) -> Dict:
        """Record user feedback"""
        feedback = {
            'command': command,
            'response': response,
            'rating': rating,  # 1-5
            'comment': comment,
            'timestamp': datetime.now().isoformat()
        }
        
        self.feedback_history.append(feedback)
        
        # Learn from feedback
        if rating >= 4:
            # Positive feedback - learn what worked
            self._learn_positive(command, response)
        elif rating <= 2:
            # Negative feedback - learn what didn't work
            self._learn_negative(command, response)
        
        self._save_feedback()
        
        return {'success': True, 'feedback': feedback}
    
    def _learn_positive(self, command: str, response: str):
        """Learn from positive feedback"""
        # Extract patterns from successful interactions
        command_lower = command.lower()
        
        # Learn preferred response style
        if 'concise' in response.lower() or len(response) < 100:
            self.learned_preferences['response_style'] = 'concise'
        elif 'detailed' in response.lower() or len(response) > 500:
            self.learned_preferences['response_style'] = 'detailed'
    
    def _learn_negative(self, command: str, response: str):
        """Learn from negative feedback"""
        # Track what didn't work
        if 'command' not in self.learned_preferences:
            self.learned_preferences['command'] = {}
        
        command_lower = command.lower()
        if command_lower not in self.learned_preferences['command']:
            self.learned_preferences['command'][command_lower] = {
                'failures': 0,
                'successes': 0
            }
        
        self.learned_preferences['command'][command_lower]['failures'] += 1
    
    def get_learned_preferences(self) -> Dict:
        """Get learned preferences"""
        return dict(self.learned_preferences)
    
    def get_feedback_stats(self) -> Dict:
        """Get feedback statistics"""
        if not self.feedback_history:
            return {}
        
        ratings = [f['rating'] for f in self.feedback_history]
        avg_rating = sum(ratings) / len(ratings)
        
        return {
            'total_feedback': len(self.feedback_history),
            'average_rating': avg_rating,
            'positive_count': sum(1 for r in ratings if r >= 4),
            'negative_count': sum(1 for r in ratings if r <= 2)
        }
