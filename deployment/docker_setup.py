"""
Docker Deployment Setup
"""
import os
from typing import Dict, Optional


class DockerSetup:
    """Docker deployment utilities"""
    
    def __init__(self):
        self.dockerfile_content = self._get_dockerfile()
        self.docker_compose_content = self._get_docker_compose()
    
    def _get_dockerfile(self) -> str:
        """Get Dockerfile content"""
        return '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    portaudio19-dev \\
    alsa-utils \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_pi.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_pi.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p memory logs backups config plugins

# Expose ports
EXPOSE 5000 8080

# Run JARVIS
CMD ["python", "jarvis_pi.py"]
'''
    
    def _get_docker_compose(self) -> str:
        """Get docker-compose.yml content"""
        return '''version: '3.8'

services:
  jarvis:
    build: .
    container_name: jarvis
    ports:
      - "5000:5000"  # API
      - "8080:8080"  # Dashboard
    volumes:
      - ./memory:/app/memory
      - ./logs:/app/logs
      - ./config:/app/config
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    restart: unless-stopped
'''
    
    def create_dockerfile(self, output_path: str = "./Dockerfile") -> Dict:
        """Create Dockerfile"""
        try:
            with open(output_path, 'w') as f:
                f.write(self.dockerfile_content)
            
            return {
                'success': True,
                'file': output_path
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_docker_compose(self, output_path: str = "./docker-compose.yml") -> Dict:
        """Create docker-compose.yml"""
        try:
            with open(output_path, 'w') as f:
                f.write(self.docker_compose_content)
            
            return {
                'success': True,
                'file': output_path
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_docker_setup(self) -> Dict:
        """Create complete Docker setup"""
        results = {
            'dockerfile': self.create_dockerfile(),
            'docker_compose': self.create_docker_compose()
        }
        
        return {
            'success': all(r.get('success') for r in results.values()),
            'files': results
        }
