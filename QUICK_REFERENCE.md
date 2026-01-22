# JARVIS Quick Reference

## 🚀 Quick Start

```bash
# 1. Setup
python scripts/quick_start.py

# 2. Health Check
python scripts/health_check.py

# 3. Start JARVIS
python jarvis_pi.py

# 4. Web Dashboard
python -m web.dashboard
# Visit http://localhost:8080

# 5. API
python -m api.rest_api
# API at http://localhost:5000
```

## 🎤 Voice Commands

### Shortcuts
- `kl` - Create keylogger
- `rs` - Create reverse shell
- `rat` - Create RAT
- `usb` - Detect USB drives
- `test` - Run TCP flood test
- `help` - What can you do
- `stats` - What have you learned
- `history` - Show command history
- `favs` - Show favorites

### Common Commands
```
"Create a keylogger"
"Create a reverse shell with obfuscation"
"Deploy keylogger to USB with autorun"
"Test TCP flood on localhost for 30 seconds"
"Add registry persistence for payload.py"
"Create stealth version of keylogger.py"
"Detect VM"
"Scan network 192.168.1.0/24"
"Show system stats"
"Backup system"
```

## 🔒 Cybersecurity Commands

### Malware Creation
```
"Create a keylogger"
"Create a reverse shell"
"Create a RAT"
"Create a credential harvester"
"Create a data exfiltrator"
"Create a cryptominer"
"Create a wiper"
"Create fileless malware"
```

### DDoS Testing
```
"Test TCP flood on localhost"
"Test UDP flood on 192.168.1.1"
"Test HTTP stress on example.com"
"Test Slowloris on target.com"
```

### Persistence
```
"Add registry persistence for payload.py"
"Add scheduled task for payload.py"
"Add startup folder persistence"
"Add service persistence"
"Add cron persistence"
```

### Evasion
```
"Create stealth version of keylogger.py"
"Obfuscate payload.py"
"Fully obfuscate keylogger.py"
"Create anti-detection payload"
```

## 🌐 API Endpoints

### Chat
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello JARVIS"}'
```

### Security
```bash
curl -X POST http://localhost:5000/api/security \
  -H "Content-Type: application/json" \
  -d '{"command": "create a keylogger"}'
```

### Status
```bash
curl http://localhost:5000/api/status
```

### History
```bash
curl http://localhost:5000/api/history?limit=10
```

## 🛠️ Utilities

### System Info
```python
from utils.system_info import SystemInfo
SystemInfo.print_summary()
```

### Backup
```python
from utils.backup_restore import BackupRestore
backup = BackupRestore()
backup_path = backup.create_backup()
```

### Configuration
```python
from config.configuration_manager import ConfigurationManager
config = ConfigurationManager()
config.set('voice.wake_word', 'jarvis')
value = config.get('voice.wake_word')
```

### Analytics
```python
from analytics.usage_analytics import UsageAnalytics
analytics = UsageAnalytics()
insights = analytics.get_insights()
```

## 📊 Monitoring

### Performance
```python
from analytics.performance_monitor import PerformanceMonitor
monitor = PerformanceMonitor()
stats = monitor.get_summary()
```

### Health Check
```bash
python scripts/health_check.py
```

### Logs
```bash
tail -f logs/jarvis.log
```

## 🔌 Plugins

### Create Plugin
```python
from plugins.plugin_system import Plugin

class MyPlugin(Plugin):
    def get_name(self):
        return "My Plugin"
    
    def get_version(self):
        return "1.0.0"
    
    def handle_command(self, command, context):
        if "my command" in command.lower():
            return "Response"
        return None
```

### Load Plugin
Place plugin file in `./plugins/` directory. It will be loaded automatically.

## 🌐 Networking

### Port Scan
```python
from network.advanced_networking import AdvancedNetworking
net = AdvancedNetworking()
results = net.scan_ports("localhost", [80, 443, 8080])
```

### Network Scan
```python
results = net.scan_network("192.168.1.0/24", [22, 80, 443])
```

## 🧪 Testing

### Run Tests
```bash
python -m testing.test_runner
```

### Specific Test
```python
from testing.test_runner import TestRunner
runner = TestRunner()
result = runner.run_specific_test('testing.test_cache', 'TestResponseCache')
```

## 📝 Configuration Files

### Main Config
- `config_pi.py` - Raspberry Pi configuration
- `config/user_config.json` - User configuration

### Directories
- `./memory/` - Learning data, history
- `./logs/` - Log files
- `./backups/` - Backup files
- `./plugins/` - Plugin files
- `./config/` - Configuration files

## 🚨 Troubleshooting

### Common Issues
1. **No audio**: Check microphone permissions
2. **LLM not working**: Start Ollama or enable cloud fallback
3. **Slow responses**: Enable caching, use smaller model
4. **Permission errors**: Check file permissions

### Get Help
- Check `docs/TROUBLESHOOTING.md`
- Run `python scripts/health_check.py`
- Check logs: `logs/jarvis.log`

## 📚 Documentation

- `README.md` - Main documentation
- `FINAL_FEATURE_LIST.md` - Complete feature list
- `docs/TROUBLESHOOTING.md` - Troubleshooting guide
- `docs/DEPLOYMENT.md` - Deployment guide
- `CYBERSECURITY_WARNING.md` - Security warnings

## ⚡ Performance Tips

1. **Use caching**: Already enabled
2. **Smaller models**: Use 7B instead of 13B
3. **Reduce agents**: Set `MAX_CONCURRENT_AGENTS = 2`
4. **Clear logs**: Periodically clean log files
5. **Use SSD**: For better I/O performance

## 🔐 Security Notes

- **Always use isolated VMs** for cybersecurity testing
- **Never test on production systems**
- **Get authorization** before testing
- **Review warnings** in `CYBERSECURITY_WARNING.md`

---

**For more details, see the full documentation files.**
