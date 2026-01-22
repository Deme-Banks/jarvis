"""
SSO Integration - Okta, Azure AD, Google SSO
"""
import os
import requests
from typing import Dict, Optional
from datetime import datetime, timedelta
import jwt


class SSOIntegration:
    """Base SSO integration"""
    
    def authenticate(self, username: str, password: str) -> Dict:
        """Authenticate user"""
        raise NotImplementedError
    
    def validate_token(self, token: str) -> Dict:
        """Validate SSO token"""
        raise NotImplementedError


class OktaSSO(SSOIntegration):
    """Okta SSO integration"""
    
    def __init__(self, domain: Optional[str] = None, client_id: Optional[str] = None):
        self.domain = domain or os.getenv("OKTA_DOMAIN")
        self.client_id = client_id or os.getenv("OKTA_CLIENT_ID")
        self.base_url = f"https://{self.domain}"
    
    def authenticate(self, username: str, password: str) -> Dict:
        """Authenticate with Okta"""
        if not self.domain:
            return {"error": "Okta domain not configured"}
        
        try:
            url = f"{self.base_url}/api/v1/authn"
            data = {
                "username": username,
                "password": password
            }
            
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get("status") == "SUCCESS":
                return {
                    "success": True,
                    "token": result.get("sessionToken"),
                    "user": result.get("_embedded", {}).get("user", {})
                }
            else:
                return {"error": "Authentication failed"}
        except Exception as e:
            return {"error": str(e)}
    
    def validate_token(self, token: str) -> Dict:
        """Validate Okta token"""
        try:
            url = f"{self.base_url}/oauth2/v1/introspect"
            data = {
                "token": token,
                "token_type_hint": "access_token"
            }
            
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return {
                "valid": result.get("active", False),
                "user": result.get("username"),
                "expires": result.get("exp")
            }
        except Exception as e:
            return {"error": str(e)}


class AzureADSSO(SSOIntegration):
    """Azure AD SSO integration"""
    
    def __init__(self, tenant_id: Optional[str] = None, client_id: Optional[str] = None):
        self.tenant_id = tenant_id or os.getenv("AZURE_TENANT_ID")
        self.client_id = client_id or os.getenv("AZURE_CLIENT_ID")
        self.base_url = f"https://login.microsoftonline.com/{self.tenant_id}"
    
    def authenticate(self, username: str, password: str) -> Dict:
        """Authenticate with Azure AD"""
        if not self.tenant_id or not self.client_id:
            return {"error": "Azure AD credentials not configured"}
        
        try:
            url = f"{self.base_url}/oauth2/v2.0/token"
            data = {
                "client_id": self.client_id,
                "scope": "https://graph.microsoft.com/.default",
                "username": username,
                "password": password,
                "grant_type": "password"
            }
            
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "access_token": result.get("access_token"),
                "expires_in": result.get("expires_in")
            }
        except Exception as e:
            return {"error": str(e)}
    
    def validate_token(self, token: str) -> Dict:
        """Validate Azure AD token"""
        try:
            # Decode JWT token
            decoded = jwt.decode(token, options={"verify_signature": False})
            return {
                "valid": True,
                "user": decoded.get("upn") or decoded.get("preferred_username"),
                "expires": decoded.get("exp")
            }
        except Exception as e:
            return {"error": str(e)}


class GoogleSSO(SSOIntegration):
    """Google SSO integration"""
    
    def __init__(self, client_id: Optional[str] = None):
        self.client_id = client_id or os.getenv("GOOGLE_CLIENT_ID")
    
    def get_auth_url(self, redirect_uri: str) -> str:
        """Get Google OAuth URL"""
        scope = "openid email profile"
        url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={self.client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"
        return url
    
    def authenticate(self, code: str, redirect_uri: str) -> Dict:
        """Authenticate with Google using authorization code"""
        if not self.client_id:
            return {"error": "Google client ID not configured"}
        
        try:
            client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
            url = "https://oauth2.googleapis.com/token"
            data = {
                "code": code,
                "client_id": self.client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code"
            }
            
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "access_token": result.get("access_token"),
                "id_token": result.get("id_token")
            }
        except Exception as e:
            return {"error": str(e)}
    
    def validate_token(self, token: str) -> Dict:
        """Validate Google token"""
        try:
            url = f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return {
                "valid": True,
                "user": result.get("email"),
                "expires": result.get("expires_in")
            }
        except Exception as e:
            return {"error": str(e)}
