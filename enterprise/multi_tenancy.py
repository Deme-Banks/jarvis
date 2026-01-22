"""
Multi-Tenancy Support - Multiple Organizations
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime


class MultiTenancyManager:
    """Multi-tenancy management"""
    
    def __init__(self, tenants_file: str = "data/tenants.json"):
        self.tenants_file = tenants_file
        self.tenants: Dict[str, Dict] = self._load_tenants()
    
    def _load_tenants(self) -> Dict:
        """Load tenants from file"""
        if os.path.exists(self.tenants_file):
            try:
                with open(self.tenants_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_tenants(self):
        """Save tenants to file"""
        os.makedirs(os.path.dirname(self.tenants_file), exist_ok=True)
        with open(self.tenants_file, 'w') as f:
            json.dump(self.tenants, f, indent=2)
    
    def create_tenant(self, tenant_id: str, name: str, 
                     config: Optional[Dict] = None) -> Dict:
        """Create a new tenant"""
        if tenant_id in self.tenants:
            return {"error": f"Tenant '{tenant_id}' already exists"}
        
        self.tenants[tenant_id] = {
            "id": tenant_id,
            "name": name,
            "created": datetime.now().isoformat(),
            "config": config or {},
            "users": [],
            "resources": {}
        }
        
        self._save_tenants()
        return {"success": True, "tenant_id": tenant_id}
    
    def get_tenant(self, tenant_id: str) -> Optional[Dict]:
        """Get tenant information"""
        return self.tenants.get(tenant_id)
    
    def add_user_to_tenant(self, tenant_id: str, user_id: str, 
                           role: str = "user") -> Dict:
        """Add user to tenant"""
        if tenant_id not in self.tenants:
            return {"error": f"Tenant '{tenant_id}' not found"}
        
        user = {
            "user_id": user_id,
            "role": role,
            "added": datetime.now().isoformat()
        }
        
        self.tenants[tenant_id]["users"].append(user)
        self._save_tenants()
        return {"success": True, "user": user}
    
    def get_tenant_resources(self, tenant_id: str) -> Dict:
        """Get tenant resources"""
        if tenant_id not in self.tenants:
            return {"error": f"Tenant '{tenant_id}' not found"}
        
        return self.tenants[tenant_id].get("resources", {})
    
    def set_tenant_resource(self, tenant_id: str, resource_type: str,
                           resource_id: str, data: Dict) -> Dict:
        """Set tenant resource"""
        if tenant_id not in self.tenants:
            return {"error": f"Tenant '{tenant_id}' not found"}
        
        if "resources" not in self.tenants[tenant_id]:
            self.tenants[tenant_id]["resources"] = {}
        
        if resource_type not in self.tenants[tenant_id]["resources"]:
            self.tenants[tenant_id]["resources"][resource_type] = {}
        
        self.tenants[tenant_id]["resources"][resource_type][resource_id] = data
        self._save_tenants()
        return {"success": True}
    
    def list_tenants(self) -> List[Dict]:
        """List all tenants"""
        return [
            {
                "id": tenant["id"],
                "name": tenant["name"],
                "user_count": len(tenant.get("users", []))
            }
            for tenant in self.tenants.values()
        ]
    
    def delete_tenant(self, tenant_id: str) -> Dict:
        """Delete a tenant"""
        if tenant_id not in self.tenants:
            return {"error": f"Tenant '{tenant_id}' not found"}
        
        del self.tenants[tenant_id]
        self._save_tenants()
        return {"success": True, "message": f"Tenant '{tenant_id}' deleted"}
