"""
CRM Integrations - Salesforce, HubSpot
"""
import os
import requests
from typing import Dict, List, Optional
from datetime import datetime


class SalesforceIntegration:
    """Salesforce integration"""
    
    def __init__(self, instance_url: Optional[str] = None,
                 access_token: Optional[str] = None):
        self.instance_url = instance_url or os.getenv("SALESFORCE_INSTANCE_URL")
        self.access_token = access_token or os.getenv("SALESFORCE_ACCESS_TOKEN")
        self.api_version = "v57.0"
    
    def create_lead(self, first_name: str, last_name: str,
                   email: str, company: str, **kwargs) -> Dict:
        """Create a lead in Salesforce"""
        if not self.instance_url or not self.access_token:
            return {"error": "Salesforce credentials not configured"}
        
        try:
            url = f"{self.instance_url}/services/data/v{self.api_version}/sobjects/Lead/"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            data = {
                "FirstName": first_name,
                "LastName": last_name,
                "Email": email,
                "Company": company,
                **kwargs
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "id": result.get("id"),
                "message": "Lead created successfully"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def query(self, soql: str) -> List[Dict]:
        """Execute SOQL query"""
        if not self.instance_url or not self.access_token:
            return [{"error": "Salesforce credentials not configured"}]
        
        try:
            url = f"{self.instance_url}/services/data/v{self.api_version}/query/"
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            params = {"q": soql}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return result.get("records", [])
        except Exception as e:
            return [{"error": str(e)}]


class HubSpotIntegration:
    """HubSpot integration"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("HUBSPOT_API_KEY")
        self.base_url = "https://api.hubapi.com"
    
    def create_contact(self, email: str, first_name: str = "",
                      last_name: str = "", **properties) -> Dict:
        """Create a contact in HubSpot"""
        if not self.api_key:
            return {"error": "HubSpot API key not configured"}
        
        try:
            url = f"{self.base_url}/crm/v3/objects/contacts"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "properties": {
                    "email": email,
                    "firstname": first_name,
                    "lastname": last_name,
                    **properties
                }
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "id": result.get("id"),
                "message": "Contact created successfully"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def create_deal(self, deal_name: str, amount: float,
                   pipeline_id: str, stage_id: str) -> Dict:
        """Create a deal in HubSpot"""
        if not self.api_key:
            return {"error": "HubSpot API key not configured"}
        
        try:
            url = f"{self.base_url}/crm/v3/objects/deals"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "properties": {
                    "dealname": deal_name,
                    "amount": str(amount),
                    "pipeline": pipeline_id,
                    "dealstage": stage_id
                }
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "id": result.get("id"),
                "message": "Deal created successfully"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_contacts(self, limit: int = 10) -> List[Dict]:
        """Get contacts from HubSpot"""
        if not self.api_key:
            return [{"error": "HubSpot API key not configured"}]
        
        try:
            url = f"{self.base_url}/crm/v3/objects/contacts"
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            params = {"limit": limit}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return [
                {
                    "id": item.get("id"),
                    "email": item.get("properties", {}).get("email"),
                    "name": f"{item.get('properties', {}).get('firstname', '')} {item.get('properties', {}).get('lastname', '')}".strip()
                }
                for item in result.get("results", [])
            ]
        except Exception as e:
            return [{"error": str(e)}]
