"""
Backup and Restore System
"""
import os
import shutil
import json
import zipfile
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class BackupRestore:
    """Backup and restore JARVIS data"""
    
    def __init__(self, backup_dir: str = "./backups"):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def create_backup(self, include_data: bool = True, 
                     include_config: bool = True,
                     include_plugins: bool = True) -> str:
        """Create backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"jarvis_backup_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        os.makedirs(backup_path, exist_ok=True)
        
        # Backup data
        if include_data:
            data_dirs = ["./memory", "./logs"]
            for data_dir in data_dirs:
                if os.path.exists(data_dir):
                    dest = os.path.join(backup_path, os.path.basename(data_dir))
                    shutil.copytree(data_dir, dest, dirs_exist_ok=True)
        
        # Backup config
        if include_config:
            config_files = ["./config/user_config.json", "./config_pi.py"]
            config_backup_dir = os.path.join(backup_path, "config")
            os.makedirs(config_backup_dir, exist_ok=True)
            
            for config_file in config_files:
                if os.path.exists(config_file):
                    shutil.copy2(config_file, config_backup_dir)
        
        # Backup plugins
        if include_plugins:
            plugin_dir = "./plugins"
            if os.path.exists(plugin_dir):
                dest = os.path.join(backup_path, "plugins")
                shutil.copytree(plugin_dir, dest, dirs_exist_ok=True)
        
        # Create metadata
        metadata = {
            'timestamp': timestamp,
            'backup_name': backup_name,
            'includes': {
                'data': include_data,
                'config': include_config,
                'plugins': include_plugins
            }
        }
        
        with open(os.path.join(backup_path, "metadata.json"), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Create zip archive
        zip_path = f"{backup_path}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, backup_path)
                    zipf.write(file_path, arcname)
        
        # Remove uncompressed backup
        shutil.rmtree(backup_path)
        
        return zip_path
    
    def list_backups(self) -> List[Dict]:
        """List available backups"""
        backups = []
        
        for filename in os.listdir(self.backup_dir):
            if filename.endswith('.zip'):
                filepath = os.path.join(self.backup_dir, filename)
                stat = os.stat(filepath)
                
                backups.append({
                    'name': filename,
                    'path': filepath,
                    'size_mb': stat.st_size / (1024 * 1024),
                    'created': datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        return sorted(backups, key=lambda x: x['created'], reverse=True)
    
    def restore_backup(self, backup_path: str, 
                      restore_data: bool = True,
                      restore_config: bool = True,
                      restore_plugins: bool = True):
        """Restore from backup"""
        # Extract backup
        extract_dir = backup_path.replace('.zip', '_extracted')
        os.makedirs(extract_dir, exist_ok=True)
        
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            zipf.extractall(extract_dir)
        
        # Read metadata
        metadata_path = os.path.join(extract_dir, "metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
        else:
            metadata = {'includes': {'data': True, 'config': True, 'plugins': True}}
        
        # Restore data
        if restore_data and metadata['includes'].get('data', True):
            for item in os.listdir(extract_dir):
                item_path = os.path.join(extract_dir, item)
                if os.path.isdir(item_path) and item in ['memory', 'logs']:
                    dest = os.path.join('.', item)
                    if os.path.exists(dest):
                        shutil.rmtree(dest)
                    shutil.copytree(item_path, dest)
        
        # Restore config
        if restore_config and metadata['includes'].get('config', True):
            config_backup_dir = os.path.join(extract_dir, "config")
            if os.path.exists(config_backup_dir):
                for config_file in os.listdir(config_backup_dir):
                    src = os.path.join(config_backup_dir, config_file)
                    dest = os.path.join('.', 'config', config_file)
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    shutil.copy2(src, dest)
        
        # Restore plugins
        if restore_plugins and metadata['includes'].get('plugins', True):
            plugin_backup_dir = os.path.join(extract_dir, "plugins")
            if os.path.exists(plugin_backup_dir):
                dest = os.path.join('.', 'plugins')
                if os.path.exists(dest):
                    shutil.rmtree(dest)
                shutil.copytree(plugin_backup_dir, dest)
        
        # Cleanup
        shutil.rmtree(extract_dir)
        
        return True
