# Advanced Cybersecurity Tools Guide

## Overview

JARVIS includes advanced cybersecurity testing tools for authorized security testing and educational purposes.

⚠️ **WARNING**: For authorized testing and educational purposes only. Never use on systems you don't own or without proper authorization.

## New Tools

### 1. Webhook Grabber

Extract and test webhook URLs from various applications.

**Features:**
- Discord webhook extraction
- Slack webhook extraction
- Telegram bot token extraction
- Generic webhook discovery
- Webhook validation/testing

**Voice Commands:**
```
"Create webhook grabber"
"Grab Discord webhooks"
"Get Slack webhooks and test them"
"Create webhook grabber for all types"
```

**What It Finds:**
- Discord webhook URLs
- Slack webhook URLs
- Telegram bot tokens
- Generic webhook URLs in config files

### 2. Token Grabber

Extract authentication tokens from various applications and services.

**Features:**
- Discord token extraction
- GitHub token/SSH key extraction
- Steam token extraction
- Spotify token extraction
- Generic token discovery

**Voice Commands:**
```
"Create token grabber"
"Grab Discord tokens"
"Get GitHub tokens and SSH keys"
"Create token grabber for all services"
```

**What It Finds:**
- Discord authentication tokens
- GitHub personal access tokens
- SSH private keys
- Steam session tokens
- Spotify OAuth tokens
- Generic API keys and tokens

### 3. Network Analyzer

Analyze network traffic and detect suspicious activity.

**Features:**
- Packet capture (simplified)
- Traffic analysis
- Protocol analysis
- Suspicious activity detection
- Connection monitoring
- Port scanning

**Voice Commands:**
```
"Create network analyzer"
"Analyze network traffic for 5 minutes"
"Capture packets and analyze protocols"
"Detect suspicious network activity"
```

**What It Analyzes:**
- Active network connections
- Listening ports
- Established connections
- Protocol statistics
- Unusual ports
- Foreign connections
- High connection counts

### 4. Log Cleaner

Anti-forensics tool for cleaning logs and traces.

**Features:**
- System log cleaning
- Browser history cleaning
- Recent files cleaning
- Temp file cleaning
- Secure deletion (multiple passes)

**Voice Commands:**
```
"Create log cleaner"
"Clean system logs and browser history"
"Secure delete temp files"
"Clean all logs and traces"
```

**What It Cleans:**
- Windows/Linux system logs
- Browser history (Chrome, Firefox)
- Browser cookies
- Recent files list
- Temporary files
- Application logs

## Usage Examples

### Webhook Grabber
```python
from cybersecurity.webhook_grabber import WebhookGrabber

grabber = WebhookGrabber()
result = grabber.create_webhook_grabber(
    target_types=['discord', 'slack'],
    test_webhook=True
)
```

### Token Grabber
```python
from cybersecurity.token_grabber import TokenGrabber

grabber = TokenGrabber()
result = grabber.create_token_grabber(
    target_types=['discord', 'github', 'steam']
)
```

### Network Analyzer
```python
from cybersecurity.network_analyzer import NetworkAnalyzer

analyzer = NetworkAnalyzer()
result = analyzer.create_network_analyzer(
    analysis_types=['packet_capture', 'traffic_analysis'],
    capture_duration=300  # 5 minutes
)
```

### Log Cleaner
```python
from cybersecurity.log_cleaner import LogCleaner

cleaner = LogCleaner()
result = cleaner.create_log_cleaner(
    clean_types=['system_logs', 'browser_history'],
    clean_method='secure_delete'
)
```

## Security Notes

⚠️ **IMPORTANT**:
- All tools include warnings
- Use only in isolated VMs
- Get authorization before testing
- Never use on production systems
- Follow responsible disclosure
- This is for educational and authorized testing only

## Legal and Ethical

**ALLOWED**:
- ✅ Testing your own systems
- ✅ Authorized penetration testing
- ✅ Security research with permission
- ✅ Educational purposes
- ✅ Bug bounty programs (with authorization)

**NOT ALLOWED**:
- ❌ Testing without authorization
- ❌ Accessing others' tokens/webhooks
- ❌ Production systems without permission
- ❌ Violating terms of service
- ❌ Malicious purposes

## Best Practices

1. **Always get authorization** before testing
2. **Use isolated test environments** only
3. **Review generated code** before running
4. **Understand what the code does**
5. **Follow responsible disclosure** for vulnerabilities
6. **Document your testing** for authorized work
7. **Handle tokens/webhooks securely**
8. **Don't share extracted credentials**

## Tool Combinations

### Complete Reconnaissance
```
1. "Create IP grabber" - Get network info
2. "Create webhook grabber" - Find webhooks
3. "Create token grabber" - Extract tokens
4. "Analyze network traffic" - Monitor activity
```

### Post-Exploitation Cleanup
```
1. "Create log cleaner" - Remove traces
2. "Clean all logs and history" - Full cleanup
3. "Secure delete temp files" - Anti-forensics
```

### Network Analysis
```
1. "Create network analyzer" - Start monitoring
2. "Analyze network traffic for 10 minutes" - Capture data
3. "Detect suspicious activity" - Identify threats
```

## Troubleshooting

### "No webhooks found"
- Check application is installed
- Verify search paths are correct
- Review file permissions

### "Token extraction failed"
- Check application is running
- Verify database isn't locked
- Review error messages

### "Network analysis incomplete"
- Check admin/root permissions
- Verify network tools are installed
- Review firewall settings

### "Log cleaning failed"
- Check admin/root permissions
- Verify file paths are correct
- Review error messages

---

**Remember: Use responsibly and only for authorized security testing!**
