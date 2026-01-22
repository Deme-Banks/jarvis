"""
Email Notification System
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
import os


class EmailNotifications:
    """Email notification system"""
    
    def __init__(self, smtp_server: str = None, smtp_port: int = 587,
                 username: str = None, password: str = None):
        self.smtp_server = smtp_server or os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = smtp_port or int(os.getenv('SMTP_PORT', '587'))
        self.username = username or os.getenv('EMAIL_USERNAME')
        self.password = password or os.getenv('EMAIL_PASSWORD')
        self.from_email = username
    
    def send_email(self, to_email: str, subject: str, body: str,
                  html_body: Optional[str] = None) -> Dict:
        """Send email"""
        if not self.username or not self.password:
            return {
                'success': False,
                'error': 'Email credentials not configured. Set EMAIL_USERNAME and EMAIL_PASSWORD'
            }
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add text and HTML parts
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            return {
                'success': True,
                'to': to_email,
                'subject': subject
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_notification_email(self, to_email: str, notification_type: str,
                               message: str) -> Dict:
        """Send notification email"""
        subject = f"JARVIS Notification: {notification_type.title()}"
        
        html_body = f'''
        <html>
        <body>
            <h2>JARVIS Notification</h2>
            <p><strong>Type:</strong> {notification_type}</p>
            <p><strong>Message:</strong></p>
            <p>{message}</p>
            <hr>
            <p><small>This is an automated message from JARVIS</small></p>
        </body>
        </html>
        '''
        
        return self.send_email(to_email, subject, message, html_body)
    
    def send_report_email(self, to_email: str, report_type: str,
                         report_path: str) -> Dict:
        """Send report via email"""
        subject = f"JARVIS {report_type.title()} Report"
        body = f"Please find the {report_type} report attached."
        
        # In real implementation, would attach file
        return self.send_email(to_email, subject, body)
