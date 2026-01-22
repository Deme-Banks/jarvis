"""
Enhanced Backup Manager
"""
import os
import shutil
import zipfile
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class BackupManager:
    """Enhanced backup management"""
    
    def __init__(self, backup_dir: str = "./backups"):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def create_full_backup(self, name: Optional[str] = None) -> Dict:
        """Create full system backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = name or f"jarvis_full_backup_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        os.makedirs(backup_path, exist_ok=True)
        
        # Backup directories
        dirs_to_backup = [
            './memory',
            './logs',
            './config',
            './plugins'
        ]
        
        backed_up = []
        for dir_path in dirs_to_backup:
            if os.path.exists(dir_path):
                dest = os.path.join(backup_path, os.path.basename(dir_path))
                try:
                    shutil.copytree(dir_path, dest, dirs_exist_ok=True)
                    backed_up.append(dir_path)
                except Exception as e:
                    print(f"Error backing up {dir_path}: {e}")
        
        # Create metadata
        metadata = {
            'name': backup_name,
            'timestamp': timestamp,
            'type': 'full',
            'directories': backed_up,
            'created': datetime.now().isoformat()
        }
        
        with open(os.path.join(backup_path, 'metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Create zip
        zip_path = f"{backup_path}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, backup_path)
                    zipf.write(file_path, arcname)
        
        # Remove uncompressed
        shutil.rmtree(backup_path)
        
        return {
            'success': True,
            'backup_path': zip_path,
            'name': backup_name,
            'size_mb': os.path.getsize(zip_path) / (1024 * 1024),
            'directories': backed_up
        }
    
    def create_incremental_backup(self, last_backup_time: Optional[datetime] = None) -> Dict:
        """Create incremental backup (only changed files)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"jarvis_incremental_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        os.makedirs(backup_path, exist_ok=True)
        
        changed_files = []
        
        # Check for changed files since last backup
        for root, dirs, files in os.walk('./memory'):
            for file in files:
                file_path = os.path.join(root, file)
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if not last_backup_time or file_time > last_backup_time:
                    rel_path = os.path.relpath(file_path, '.')
                    dest = os.path.join(backup_path, rel_path)
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    shutil.copy2(file_path, dest)
                    changed_files.append(rel_path)
        
        if not changed_files:
            shutil.rmtree(backup_path)
            return {
                'success': True,
                'message': 'No changes since last backup',
                'files': []
            }
        
        # Create zip
        zip_path = f"{backup_path}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in changed_files:
                file_path = os.path.join(backup_path, file)
                zipf.write(file_path, file)
        
        shutil.rmtree(backup_path)
        
        return {
            'success': True,
            'backup_path': zip_path,
            'files': changed_files,
            'count': len(changed_files)
        }
    
    def list_backups(self) -> List[Dict]:
        """List all backups"""
        backups = []
        
        for filename in os.listdir(self.backup_dir):
            if filename.endswith('.zip'):
                filepath = os.path.join(self.backup_dir, filename)
                stat = os.stat(filepath)
                
                # Try to read metadata
                metadata = {}
                try:
                    with zipfile.ZipFile(filepath, 'r') as zipf:
                        if 'metadata.json' in zipf.namelist():
                            metadata_data = zipf.read('metadata.json')
                            metadata = json.loads(metadata_data)
                except:
                    pass
                
                backups.append({
                    'name': filename,
                    'path': filepath,
                    'size_mb': stat.st_size / (1024 * 1024),
                    'created': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'type': metadata.get('type', 'unknown'),
                    'metadata': metadata
                })
        
        return sorted(backups, key=lambda x: x['created'], reverse=True)
    
    def cleanup_old_backups(self, keep_days: int = 30) -> Dict:
        """Clean up old backups"""
        cutoff = datetime.now().timestamp() - (keep_days * 24 * 3600)
        deleted = []
        
        for filename in os.listdir(self.backup_dir):
            if filename.endswith('.zip'):
                filepath = os.path.join(self.backup_dir, filename)
                if os.path.getmtime(filepath) < cutoff:
                    try:
                        os.remove(filepath)
                        deleted.append(filename)
                    except:
                        pass
        
        return {
            'success': True,
            'deleted_count': len(deleted),
            'deleted': deleted
        }
