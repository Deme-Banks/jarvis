"""
GitHub Integration - Commit, push, create issues, manage repos
"""
import os
import subprocess
import requests
import json
from typing import Dict, List, Optional
from datetime import datetime


class GitHubIntegration:
    """GitHub integration for JARVIS"""
    
    def __init__(self, token: Optional[str] = None):
        # Add optimized caching
        self.cache = SmartCache()
        self.profiler = PerformanceProfiler()
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        } if self.token else {}
    
    def commit_and_push(self, repo_path: str, message: str,
                       files: Optional[List[str]] = None) -> Dict:
        """Commit and push changes to GitHub"""
        try:
            os.chdir(repo_path)
            
            # Add files
            if files:
                for file in files:
                    subprocess.run(["git", "add", file], check=True)
            else:
                subprocess.run(["git", "add", "."], check=True)
            
            # Commit
            subprocess.run(["git", "commit", "-m", message], check=True)
            
            # Push
            result = subprocess.run(["git", "push"], capture_output=True, text=True, check=True)
            
            return {
                "success": True,
                "message": f"Committed and pushed: {message}",
                "output": result.stdout
            }
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": str(e),
                "output": e.stdout + e.stderr
            }
    
    def create_issue(self, owner: str, repo: str, title: str,
                    body: str, labels: Optional[List[str]] = None) -> Dict:
        """Create a GitHub issue"""
        if not self.token:
            return {"error": "GitHub token not configured"}
        
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/issues"
            data = {
                "title": title,
                "body": body,
                "labels": labels or []
            }
            
            response = requests.post(url, headers=self.headers, json=data, timeout=10)
            response.raise_for_status()
            
            issue = response.json()
            return {
                "success": True,
                "issue_number": issue["number"],
                "url": issue["html_url"],
                "title": title
            }
        except Exception as e:
            return {"error": str(e)}
    
    def list_repos(self, username: Optional[str] = None) -> List[Dict]:
        """List GitHub repositories"""
        if not self.token:
            return []
        
        try:
            if username:
                url = f"{self.base_url}/users/{username}/repos"
            else:
                url = f"{self.base_url}/user/repos"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            repos = response.json()
            return [{
                "name": repo["name"],
                "full_name": repo["full_name"],
                "url": repo["html_url"],
                "private": repo["private"]
            } for repo in repos]
        except Exception as e:
            return [{"error": str(e)}]
    
    def create_repo(self, name: str, description: str = "",
                   private: bool = False) -> Dict:
        """Create a new GitHub repository"""
        if not self.token:
            return {"error": "GitHub token not configured"}
        
        try:
            url = f"{self.base_url}/user/repos"
            data = {
                "name": name,
                "description": description,
                "private": private
            }
            
            response = requests.post(url, headers=self.headers, json=data, timeout=10)
            response.raise_for_status()
            
            repo = response.json()
            return {
                "success": True,
                "name": repo["name"],
                "url": repo["html_url"]
            }
        except Exception as e:
            return {"error": str(e)}
