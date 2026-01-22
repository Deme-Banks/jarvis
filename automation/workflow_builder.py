"""
Workflow Builder - Visual workflow creation
"""
import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime


class WorkflowBuilder:
    """Visual workflow builder"""
    
    def __init__(self, workflows_file: str = "data/workflows.json"):
        self.workflows_file = workflows_file
        self.workflows = self._load_workflows()
    
    def _load_workflows(self) -> Dict:
        """Load workflows"""
        if os.path.exists(self.workflows_file):
            try:
                with open(self.workflows_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_workflows(self):
        """Save workflows"""
        os.makedirs(os.path.dirname(self.workflows_file), exist_ok=True)
        with open(self.workflows_file, 'w') as f:
            json.dump(self.workflows, f, indent=2)
    
    def create_workflow(self, name: str, steps: List[Dict],
                       triggers: Optional[List[str]] = None,
                       schedule: Optional[str] = None) -> Dict:
        """Create a workflow"""
        workflow = {
            "name": name,
            "steps": steps,
            "triggers": triggers or [],
            "schedule": schedule,
            "created": datetime.now().isoformat(),
            "enabled": True,
            "execution_count": 0,
            "last_execution": None
        }
        
        self.workflows[name] = workflow
        self._save_workflows()
        
        return {"success": True, "workflow": name}
    
    def add_step(self, workflow_name: str, step: Dict, position: Optional[int] = None) -> Dict:
        """Add a step to workflow"""
        if workflow_name not in self.workflows:
            return {"error": f"Workflow '{workflow_name}' not found"}
        
        if position is not None:
            self.workflows[workflow_name]["steps"].insert(position, step)
        else:
            self.workflows[workflow_name]["steps"].append(step)
        
        self._save_workflows()
        return {"success": True, "workflow": workflow_name, "steps": len(self.workflows[workflow_name]["steps"])}
    
    def get_workflow_visualization(self, workflow_name: str) -> str:
        """Get workflow visualization (ASCII art)"""
        if workflow_name not in self.workflows:
            return f"Workflow '{workflow_name}' not found"
        
        workflow = self.workflows[workflow_name]
        visualization = f"Workflow: {workflow_name}\n"
        visualization += "=" * 50 + "\n\n"
        
        for i, step in enumerate(workflow["steps"], 1):
            step_type = step.get("type", "unknown")
            action = step.get("action", "")
            visualization += f"Step {i}: [{step_type}] {action}\n"
            if i < len(workflow["steps"]):
                visualization += "    ↓\n"
        
        return visualization
    
    def validate_workflow(self, workflow_name: str) -> Dict:
        """Validate workflow structure"""
        if workflow_name not in self.workflows:
            return {"error": f"Workflow '{workflow_name}' not found"}
        
        workflow = self.workflows[workflow_name]
        errors = []
        warnings = []
        
        # Check for steps
        if not workflow.get("steps"):
            errors.append("Workflow has no steps")
        
        # Validate each step
        for i, step in enumerate(workflow.get("steps", []), 1):
            if "type" not in step:
                errors.append(f"Step {i}: Missing 'type'")
            if "action" not in step:
                errors.append(f"Step {i}: Missing 'action'")
        
        # Check for triggers or schedule
        if not workflow.get("triggers") and not workflow.get("schedule"):
            warnings.append("Workflow has no triggers or schedule")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
