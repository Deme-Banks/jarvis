"""
Webhook System - Event-driven integrations
"""
import os
import requests
import json
import hmac
import hashlib
from typing import Dict, List, Optional, Callable
from datetime import datetime
from refactoring.code_deduplication import CommonUtils


class WebhookSystem:
    """Webhook system for event-driven integrations"""
    
    def __init__(self, webhooks_file: str = "data/webhooks.json"):
        self.webhooks_file = webhooks_file
        self.webhooks: Dict[str, Dict] = {}
        self.event_handlers: Dict[str, List[Callable]] = {}
        self._load_webhooks()
    
    def register_webhook(self, webhook_id: str, url: str, 
                        events: List[str], secret: Optional[str] = None) -> Dict:
        """Register a webhook"""
        webhook = {
            "id": webhook_id,
            "url": url,
            "events": events,
            "secret": secret,
            "active": True,
            "created": datetime.now().isoformat(),
            "delivery_count": 0,
            "failure_count": 0
        }
        
        self.webhooks[webhook_id] = webhook
        self._save_webhooks()
        
        return {"success": True, "webhook_id": webhook_id}
    
    def trigger_event(self, event_type: str, payload: Dict) -> Dict:
        """Trigger an event and notify webhooks"""
        triggered = []
        failed = []
        
        for webhook_id, webhook in self.webhooks.items():
            if not webhook.get("active", True):
                continue
            
            if event_type not in webhook.get("events", []):
                continue
            
            # Send webhook
            result = self._send_webhook(webhook, event_type, payload)
            if result["success"]:
                triggered.append(webhook_id)
                webhook["delivery_count"] = webhook.get("delivery_count", 0) + 1
            else:
                failed.append(webhook_id)
                webhook["failure_count"] = webhook.get("failure_count", 0) + 1
        
        self._save_webhooks()
        
        return {
            "success": True,
            "event": event_type,
            "triggered": triggered,
            "failed": failed
        }
    
    def _send_webhook(self, webhook: Dict, event_type: str, payload: Dict) -> Dict:
        """Send webhook notification"""
        try:
            data = {
                "event": event_type,
                "payload": payload,
                "timestamp": datetime.now().isoformat()
            }
            
            headers = {"Content-Type": "application/json"}
            
            # Add signature if secret exists
            if webhook.get("secret"):
                signature = self._generate_signature(
                    json.dumps(data),
                    webhook["secret"]
                )
                headers["X-Webhook-Signature"] = signature
            
            response = requests.post(
                webhook["url"],
                json=data,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _generate_signature(self, payload: str, secret: str) -> str:
        """Generate webhook signature"""
        return hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def _load_webhooks(self):
        """Load webhooks from file"""
        self.webhooks = CommonUtils.safe_json_load(self.webhooks_file, {})
    
    def _save_webhooks(self):
        """Save webhooks to file"""
        CommonUtils.safe_json_save(self.webhooks_file, self.webhooks)
