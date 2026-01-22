"""
Workflow Templates - Pre-built automation workflows
"""
from typing import Dict, List
from datetime import datetime
from refactoring.code_deduplication import CommonUtils


class WorkflowTemplates:
    """Pre-built workflow templates"""
    
    def __init__(self):
        self.templates: Dict[str, Dict] = {
            "security_audit": {
                "name": "Security Audit",
                "steps": [
                    {"action": "scan_network", "params": {"target": "auto"}},
                    {"action": "check_vulnerabilities", "params": {}},
                    {"action": "analyze_logs", "params": {"days": 7}},
                    {"action": "generate_report", "params": {"format": "pdf"}}
                ],
                "schedule": "weekly"
            },
            "backup_workflow": {
                "name": "Automated Backup",
                "steps": [
                    {"action": "backup_data", "params": {"source": "data/"}},
                    {"action": "verify_backup", "params": {}},
                    {"action": "clean_old_backups", "params": {"keep_days": 30}},
                    {"action": "notify", "params": {"message": "Backup complete"}}
                ],
                "schedule": "daily"
            },
            "performance_monitoring": {
                "name": "Performance Monitoring",
                "steps": [
                    {"action": "get_system_info", "params": {}},
                    {"action": "check_resources", "params": {}},
                    {"action": "analyze_performance", "params": {}},
                    {"action": "alert_if_needed", "params": {"threshold": 80}}
                ],
                "schedule": "hourly"
            }
        }
    
    def get_template(self, template_id: str) -> Dict:
        """Get a workflow template"""
        return self.templates.get(template_id, {})
    
    def list_templates(self) -> List[Dict]:
        """List all templates"""
        return [
            {"id": tid, **template}
            for tid, template in self.templates.items()
        ]
    
    def create_from_template(self, template_id: str, 
                           workflow_name: str, custom_params: Dict = None) -> Dict:
        """Create workflow from template"""
        template = self.get_template(template_id)
        if not template:
            return {"error": f"Template '{template_id}' not found"}
        
        workflow = {
            "name": workflow_name,
            "steps": template["steps"].copy(),
            "created": datetime.now().isoformat()
        }
        
        # Apply custom parameters
        if custom_params:
            for step in workflow["steps"]:
                step["params"].update(custom_params.get(step["action"], {}))
        
        return {"success": True, "workflow": workflow}
