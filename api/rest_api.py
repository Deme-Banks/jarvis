"""
REST API for JARVIS Integration
"""
from flask import Flask, request, jsonify
from typing import Dict, Optional
import threading
from agents.orchestrator_pi import PiOrchestrator
from llm.local_llm import LocalLLM
from cybersecurity.enhanced_integration import EnhancedCybersecurityOrchestrator


class JARVISAPI:
    """REST API for JARVIS"""
    
    def __init__(self, orchestrator: Optional[PiOrchestrator] = None,
                 cybersec_orchestrator: Optional[EnhancedCybersecurityOrchestrator] = None):
        self.app = Flask(__name__)
        self.orchestrator = orchestrator or PiOrchestrator()
        self.cybersec = cybersec_orchestrator
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            """Chat endpoint"""
            data = request.json
            message = data.get('message', '')
            context = data.get('context', {})
            
            response = self.orchestrator.process(message, context)
            
            return jsonify({
                'response': response,
                'success': True
            })
        
        @self.app.route('/api/security', methods=['POST'])
        def security():
            """Security endpoint"""
            if not self.cybersec:
                return jsonify({'error': 'Security module not available'}), 400
            
            data = request.json
            command = data.get('command', '')
            
            response = self.cybersec.handle_security_request(command)
            
            return jsonify({
                'response': response,
                'success': True
            })
        
        @self.app.route('/api/status', methods=['GET'])
        def status():
            """Status endpoint"""
            return jsonify({
                'status': 'operational',
                'version': '1.0',
                'features': {
                    'voice': True,
                    'security': self.cybersec is not None,
                    'learning': True
                }
            })
        
        @self.app.route('/api/history', methods=['GET'])
        def history():
            """Get command history"""
            from features.command_history import CommandHistory
            history = CommandHistory()
            limit = request.args.get('limit', 10, type=int)
            
            return jsonify({
                'history': history.get_recent(limit),
                'stats': history.get_stats()
            })
    
    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
        """Run API server"""
        self.app.run(host=host, port=port, debug=debug)
