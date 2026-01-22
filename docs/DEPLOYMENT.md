# Deployment Guide

## Quick Deployment

### Local Deployment
```bash
# 1. Clone repository
git clone https://github.com/Deme-Banks/jarvis.git
cd jarvis

# 2. Install dependencies
pip install -r requirements_pi.txt

# 3. Run setup
python scripts/quick_start.py

# 4. Start JARVIS
python jarvis_pi.py
```

### Docker Deployment (Coming Soon)
```bash
docker build -t jarvis .
docker run -p 5000:5000 -p 8080:8080 jarvis
```

## Production Deployment

### System Requirements
- **CPU**: 2+ cores recommended
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 10GB free space
- **OS**: Linux, Windows, or macOS
- **Python**: 3.8 or higher

### Installation Steps

1. **System Preparation**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and pip
   sudo apt install python3 python3-pip python3-venv
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements_pi.txt
   ```

4. **Configure System**
   ```bash
   python scripts/quick_start.py
   python scripts/health_check.py
   ```

5. **Setup Ollama** (Optional)
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull model
   ollama pull llama2
   
   # Start Ollama service
   ollama serve
   ```

## Service Configuration

### Systemd Service (Linux)

Create `/etc/systemd/system/jarvis.service`:
```ini
[Unit]
Description=JARVIS Voice Assistant
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/jarvis-voice-system
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python jarvis_pi.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable jarvis
sudo systemctl start jarvis
sudo systemctl status jarvis
```

### Windows Service

Use NSSM (Non-Sucking Service Manager):
```bash
nssm install JARVIS "C:\path\to\venv\Scripts\python.exe" "C:\path\to\jarvis_pi.py"
nssm start JARVIS
```

## Configuration

### Environment Variables
Create `.env` file:
```env
JARVIS_WAKE_WORD=jarvis
JARVIS_MODEL=llama2
JARVIS_TEMPERATURE=0.7
JARVIS_CACHE_ENABLED=true
JARVIS_ANALYTICS_ENABLED=true
```

### Configuration File
Edit `config/user_config.json`:
```json
{
  "voice": {
    "wake_word": "jarvis",
    "sensitivity": 0.5
  },
  "llm": {
    "model": "llama2",
    "temperature": 0.7
  },
  "features": {
    "enable_learning": true,
    "enable_analytics": true
  }
}
```

## Security Considerations

### Firewall
```bash
# Allow API port
sudo ufw allow 5000/tcp
sudo ufw allow 8080/tcp
```

### User Permissions
- Run as non-root user
- Limit file permissions
- Use isolated mode for cybersecurity features

### Network Security
- Use HTTPS in production
- Implement authentication
- Restrict API access

## Monitoring

### Health Checks
```bash
# Manual check
python scripts/health_check.py

# Automated monitoring
watch -n 60 'python scripts/health_check.py'
```

### Logs
```bash
# View logs
tail -f logs/jarvis.log

# Rotate logs (automatic with RotatingFileHandler)
```

### Metrics
- Access dashboard: `http://localhost:8080`
- API status: `http://localhost:5000/api/status`

## Backup

### Automated Backup
```python
from utils.backup_restore import BackupRestore

backup = BackupRestore()
backup_path = backup.create_backup()
print(f"Backup created: {backup_path}")
```

### Scheduled Backups
Add to crontab:
```bash
0 2 * * * cd /path/to/jarvis && python -c "from utils.backup_restore import BackupRestore; BackupRestore().create_backup()"
```

## Updates

### Update Process
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements_pi.txt --upgrade

# Restart service
sudo systemctl restart jarvis
```

## Scaling

### Multiple Instances
- Use load balancer
- Share database (if using external)
- Configure different ports

### Resource Limits
- Set CPU limits
- Set memory limits
- Monitor resource usage

## Troubleshooting

See `TROUBLESHOOTING.md` for common issues and solutions.
