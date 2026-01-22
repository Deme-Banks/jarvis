"""
Cloud Storage Integration - Dropbox, Google Drive, OneDrive
"""
import os
import requests
from typing import Dict, List, Optional
from datetime import datetime


class DropboxIntegration:
    """Dropbox integration"""
    
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or os.getenv("DROPBOX_ACCESS_TOKEN")
        self.base_url = "https://api.dropboxapi.com/2"
    
    def upload_file(self, local_path: str, remote_path: str) -> Dict:
        """Upload file to Dropbox"""
        if not self.access_token:
            return {"error": "Dropbox access token not configured"}
        
        try:
            url = f"{self.base_url}/files/upload"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/octet-stream",
                "Dropbox-API-Arg": f'{{"path": "{remote_path}", "mode": "add", "autorename": true}}'
            }
            
            with open(local_path, 'rb') as f:
                response = requests.post(url, headers=headers, data=f, timeout=30)
                response.raise_for_status()
            
            return {"success": True, "path": remote_path}
        except Exception as e:
            return {"error": str(e)}
    
    def download_file(self, remote_path: str, local_path: str) -> Dict:
        """Download file from Dropbox"""
        if not self.access_token:
            return {"error": "Dropbox access token not configured"}
        
        try:
            url = f"{self.base_url}/files/download"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Dropbox-API-Arg": f'{{"path": "{remote_path}"}}'
            }
            
            response = requests.post(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            return {"success": True, "local_path": local_path}
        except Exception as e:
            return {"error": str(e)}
    
    def list_files(self, path: str = "") -> List[Dict]:
        """List files in Dropbox"""
        if not self.access_token:
            return [{"error": "Dropbox access token not configured"}]
        
        try:
            url = f"{self.base_url}/files/list_folder"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            data = {"path": path}
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return [
                {
                    "name": entry["name"],
                    "path": entry["path_lower"],
                    "type": entry[".tag"]
                }
                for entry in result.get("entries", [])
            ]
        except Exception as e:
            return [{"error": str(e)}]


class GoogleDriveIntegration:
    """Google Drive integration"""
    
    def __init__(self, credentials_file: Optional[str] = None):
        self.credentials_file = credentials_file or "credentials.json"
        self.service = None
        self._setup_service()
    
    def _setup_service(self):
        """Setup Google Drive service"""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
            from googleapiclient.errors import HttpError
            
            SCOPES = ['https://www.googleapis.com/auth/drive']
            
            creds = None
            token_file = "token.json"
            
            if os.path.exists(token_file):
                creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(requests.Request())
                else:
                    if os.path.exists(self.credentials_file):
                        flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
                        creds = flow.run_local_server(port=0)
                
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
            
            if creds:
                self.service = build('drive', 'v3', credentials=creds)
        except Exception as e:
            print(f"Google Drive setup error: {e}")
    
    def upload_file(self, local_path: str, remote_name: str) -> Dict:
        """Upload file to Google Drive"""
        if not self.service:
            return {"error": "Google Drive service not configured"}
        
        try:
            from googleapiclient.http import MediaFileUpload
            
            file_metadata = {'name': remote_name}
            media = MediaFileUpload(local_path, resumable=True)
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            return {"success": True, "file_id": file.get('id')}
        except Exception as e:
            return {"error": str(e)}
    
    def list_files(self, max_results: int = 10) -> List[Dict]:
        """List files in Google Drive"""
        if not self.service:
            return [{"error": "Google Drive service not configured"}]
        
        try:
            results = self.service.files().list(
                pageSize=max_results,
                fields="nextPageToken, files(id, name)"
            ).execute()
            
            return [
                {
                    "name": item["name"],
                    "id": item["id"]
                }
                for item in results.get('files', [])
            ]
        except Exception as e:
            return [{"error": str(e)}]


class OneDriveIntegration:
    """OneDrive integration"""
    
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or os.getenv("ONEDRIVE_ACCESS_TOKEN")
        self.base_url = "https://graph.microsoft.com/v1.0/me/drive"
    
    def upload_file(self, local_path: str, remote_path: str) -> Dict:
        """Upload file to OneDrive"""
        if not self.access_token:
            return {"error": "OneDrive access token not configured"}
        
        try:
            url = f"{self.base_url}/root:{remote_path}:/content"
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            
            with open(local_path, 'rb') as f:
                response = requests.put(url, headers=headers, data=f, timeout=30)
                response.raise_for_status()
            
            return {"success": True, "path": remote_path}
        except Exception as e:
            return {"error": str(e)}
    
    def list_files(self, path: str = "/") -> List[Dict]:
        """List files in OneDrive"""
        if not self.access_token:
            return [{"error": "OneDrive access token not configured"}]
        
        try:
            url = f"{self.base_url}/root:{path}:/children"
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return [
                {
                    "name": item["name"],
                    "id": item["id"],
                    "type": item.get("file", {}).get("mimeType", "folder")
                }
                for item in result.get("value", [])
            ]
        except Exception as e:
            return [{"error": str(e)}]
