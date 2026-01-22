"""
Mobile API Endpoints - REST API for mobile apps
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Optional
from agents.orchestrator_pi import PiOrchestrator
from cybersecurity.enhanced_integration import EnhancedSecurityIntegration


app = Flask(__name__)
CORS(app)  # Enable CORS for mobile apps

# Initialize JARVIS components
orchestrator = PiOrchestrator()
cybersec = EnhancedSecurityIntegration()


@app.route('/api/mobile/status', methods=['GET'])
def get_status():
    """Get JARVIS status"""
    return jsonify({
        "status": "online",
        "version": "1.0.0",
        "features": 370,
        "uptime": "24h"
    })


@app.route('/api/mobile/command', methods=['POST'])
def execute_command():
    """Execute a command from mobile"""
    data = request.json
    command = data.get('command', '')
    user_id = data.get('user_id', 'mobile_user')
    
    try:
        # Process command
        if cybersec:
            response = cybersec.handle_security_request(command)
        else:
            response = orchestrator.process(command)
        
        return jsonify({
            "success": True,
            "response": response,
            "command": command
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/mobile/voice', methods=['POST'])
def process_voice():
    """Process voice command from mobile"""
    # In production, would handle audio file
    data = request.json
    transcript = data.get('transcript', '')
    
    try:
        response = orchestrator.process(transcript)
        return jsonify({
            "success": True,
            "response": response,
            "transcript": transcript
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/mobile/notifications', methods=['GET'])
def get_notifications():
    """Get notifications for mobile"""
    # In production, would fetch from notification system
    return jsonify({
        "notifications": [
            {
                "id": "1",
                "title": "System Update",
                "message": "JARVIS has been updated",
                "timestamp": "2024-01-22T00:00:00",
                "read": False
            }
        ]
    })


@app.route('/api/mobile/stats', methods=['GET'])
def get_stats():
    """Get statistics for mobile dashboard"""
    return jsonify({
        "total_commands": 1000,
        "success_rate": 0.95,
        "active_features": 370,
        "system_health": "good"
    })


@app.route('/api/mobile/history', methods=['GET'])
def get_history():
    """Get command history"""
    limit = request.args.get('limit', 50, type=int)
    # In production, would fetch from history system
    return jsonify({
        "history": [
            {
                "command": "create keylogger",
                "response": "Keylogger created",
                "timestamp": "2024-01-22T00:00:00"
            }
        ]
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
