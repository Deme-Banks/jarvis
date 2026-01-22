"""
Jira Integration - Create tickets, update status, search
"""
import os
import requests
from typing import Dict, List, Optional
from datetime import datetime


class JiraIntegration:
    """Jira integration for JARVIS"""
    
    def __init__(self, url: Optional[str] = None, 
                 email: Optional[str] = None,
                 api_token: Optional[str] = None):
        self.url = url or os.getenv("JIRA_URL")
        self.email = email or os.getenv("JIRA_EMAIL")
        self.api_token = api_token or os.getenv("JIRA_API_TOKEN")
        
        if self.url and self.email and self.api_token:
            self.auth = (self.email, self.api_token)
        else:
            self.auth = None
    
    def create_issue(self, project_key: str, summary: str,
                    description: str, issue_type: str = "Task",
                    priority: Optional[str] = None) -> Dict:
        """Create a Jira issue"""
        if not self.auth:
            return {"error": "Jira credentials not configured"}
        
        try:
            url = f"{self.url}/rest/api/3/issue"
            data = {
                "fields": {
                    "project": {"key": project_key},
                    "summary": summary,
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": description
                                    }
                                ]
                            }
                        ]
                    },
                    "issuetype": {"name": issue_type}
                }
            }
            
            if priority:
                data["fields"]["priority"] = {"name": priority}
            
            response = requests.post(url, json=data, auth=self.auth, timeout=10)
            response.raise_for_status()
            
            issue = response.json()
            return {
                "success": True,
                "key": issue["key"],
                "id": issue["id"],
                "url": f"{self.url}/browse/{issue['key']}"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def update_issue_status(self, issue_key: str, status: str) -> Dict:
        """Update issue status"""
        if not self.auth:
            return {"error": "Jira credentials not configured"}
        
        try:
            # Get available transitions
            url = f"{self.url}/rest/api/3/issue/{issue_key}/transitions"
            response = requests.get(url, auth=self.auth, timeout=10)
            response.raise_for_status()
            
            transitions = response.json()["transitions"]
            transition_id = None
            for transition in transitions:
                if transition["to"]["name"].lower() == status.lower():
                    transition_id = transition["id"]
                    break
            
            if not transition_id:
                return {"error": f"Status '{status}' not available"}
            
            # Execute transition
            url = f"{self.url}/rest/api/3/issue/{issue_key}/transitions"
            data = {"transition": {"id": transition_id}}
            
            response = requests.post(url, json=data, auth=self.auth, timeout=10)
            response.raise_for_status()
            
            return {
                "success": True,
                "issue_key": issue_key,
                "new_status": status
            }
        except Exception as e:
            return {"error": str(e)}
    
    def search_issues(self, jql: str, max_results: int = 50) -> List[Dict]:
        """Search issues using JQL"""
        if not self.auth:
            return []
        
        try:
            url = f"{self.url}/rest/api/3/search"
            params = {
                "jql": jql,
                "maxResults": max_results
            }
            
            response = requests.get(url, params=params, auth=self.auth, timeout=10)
            response.raise_for_status()
            
            results = response.json()
            issues = []
            for issue in results.get("issues", []):
                issues.append({
                    "key": issue["key"],
                    "summary": issue["fields"]["summary"],
                    "status": issue["fields"]["status"]["name"],
                    "url": f"{self.url}/browse/{issue['key']}"
                })
            
            return issues
        except Exception as e:
            return [{"error": str(e)}]
