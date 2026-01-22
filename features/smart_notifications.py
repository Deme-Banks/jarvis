"""
Smart Notification System
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import deque


class SmartNotifications:
    """Smart notification system"""
    
    def __init__(self, notifications_file: str = "./memory/notifications.json"):
        self.notifications_file = notifications_file
        os.makedirs(os.path.dirname(notifications_file), exist_ok=True)
        self.notifications = deque(maxlen=1000)
        self.preferences = self._load_preferences()
    
    def _load_preferences(self) -> Dict:
        """Load notification preferences"""
        if os.path.exists(self.notifications_file):
            try:
                with open(self.notifications_file, 'r') as f:
                    data = json.load(f)
                    return data.get('preferences', {
                        'enabled': True,
                        'types': ['info', 'warning', 'error'],
                        'quiet_hours': [22, 23, 0, 1, 2, 3, 4, 5, 6]
                    })
            except:
                return {
                    'enabled': True,
                    'types': ['info', 'warning', 'error'],
                    'quiet_hours': [22, 23, 0, 1, 2, 3, 4, 5, 6]
                }
        return {
            'enabled': True,
            'types': ['info', 'warning', 'error'],
            'quiet_hours': [22, 23, 0, 1, 2, 3, 4, 5, 6]
        }
    
    def send_notification(self, message: str, notification_type: str = "info",
                         priority: str = "normal") -> Dict:
        """Send notification"""
        if not self.preferences.get('enabled', True):
            return {'success': False, 'reason': 'notifications_disabled'}
        
        # Check quiet hours
        current_hour = datetime.now().hour
        if current_hour in self.preferences.get('quiet_hours', []):
            if priority != 'urgent':
                return {'success': False, 'reason': 'quiet_hours'}
        
        # Check type filter
        if notification_type not in self.preferences.get('types', []):
            return {'success': False, 'reason': 'type_filtered'}
        
        notification = {
            'message': message,
            'type': notification_type,
            'priority': priority,
            'timestamp': datetime.now().isoformat(),
            'read': False
        }
        
        self.notifications.append(notification)
        self._save_notifications()
        
        return {
            'success': True,
            'notification': notification
        }
    
    def get_unread_notifications(self, limit: int = 10) -> List[Dict]:
        """Get unread notifications"""
        unread = [n for n in self.notifications if not n.get('read', False)]
        return unread[-limit:]
    
    def mark_read(self, timestamp: str):
        """Mark notification as read"""
        for notification in self.notifications:
            if notification['timestamp'] == timestamp:
                notification['read'] = True
                self._save_notifications()
                break
    
    def _save_notifications(self):
        """Save notifications"""
        try:
            with open(self.notifications_file, 'w') as f:
                json.dump({
                    'notifications': list(self.notifications),
                    'preferences': self.preferences
                }, f, indent=2)
        except:
            pass
