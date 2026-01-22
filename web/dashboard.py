"""
Web Dashboard for JARVIS
"""
from flask import Flask, render_template_string, jsonify, request
from typing import Dict, Optional
from agents.orchestrator_pi import PiOrchestrator
from cybersecurity.enhanced_integration import EnhancedCybersecurityOrchestrator
from learning.memory import MemorySystem
from features.command_history import CommandHistory
from optimization.cache import ResponseCache


class JARVISDashboard:
    """Web dashboard for JARVIS"""
    
    def __init__(self, orchestrator: Optional[PiOrchestrator] = None,
                 cybersec: Optional[EnhancedCybersecurityOrchestrator] = None):
        self.app = Flask(__name__)
        self.orchestrator = orchestrator
        self.cybersec = cybersec
        self.memory = MemorySystem()
        self.history = CommandHistory()
        self.cache = ResponseCache() if orchestrator and hasattr(orchestrator, 'cache') else None
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup dashboard routes"""
        
        @self.app.route('/')
        def index():
            """Main dashboard"""
            return render_template_string(self._get_dashboard_html())
        
        @self.app.route('/api/stats')
        def stats():
            """Get statistics"""
            memory_stats = self.memory.analyze_user_style()
            history_stats = self.history.get_stats()
            cache_stats = self.cache.get_stats() if self.cache else {}
            
            return jsonify({
                'memory': memory_stats,
                'history': history_stats,
                'cache': cache_stats
            })
        
        @self.app.route('/api/commands', methods=['POST'])
        def execute_command():
            """Execute command via API"""
            data = request.json
            command = data.get('command', '')
            
            if self.cybersec:
                response = self.cybersec.handle_security_request(command)
            elif self.orchestrator:
                response = self.orchestrator.process(command)
            else:
                response = "Orchestrator not available"
            
            return jsonify({
                'command': command,
                'response': response,
                'success': True
            })
    
    def _get_dashboard_html(self) -> str:
        """Get dashboard HTML"""
        return '''
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: #fff; }
        .container { max-width: 1200px; margin: 0 auto; }
        .card { background: #2a2a2a; padding: 20px; margin: 10px 0; border-radius: 8px; }
        .stat { display: inline-block; margin: 10px; padding: 15px; background: #3a3a3a; border-radius: 5px; }
        .stat-value { font-size: 24px; font-weight: bold; color: #4CAF50; }
        .stat-label { font-size: 12px; color: #aaa; }
        button { background: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
        input { padding: 10px; width: 300px; border-radius: 5px; border: 1px solid #555; background: #333; color: #fff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>JARVIS Dashboard</h1>
        
        <div class="card">
            <h2>Statistics</h2>
            <div id="stats"></div>
        </div>
        
        <div class="card">
            <h2>Command Interface</h2>
            <input type="text" id="command" placeholder="Enter command...">
            <button onclick="executeCommand()">Execute</button>
            <div id="response" style="margin-top: 20px;"></div>
        </div>
        
        <div class="card">
            <h2>Recent Commands</h2>
            <div id="history"></div>
        </div>
    </div>
    
    <script>
        function loadStats() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('stats').innerHTML = `
                        <div class="stat">
                            <div class="stat-value">${data.history.total_commands || 0}</div>
                            <div class="stat-label">Total Commands</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">${data.cache.total_entries || 0}</div>
                            <div class="stat-label">Cached Responses</div>
                        </div>
                    `;
                });
        }
        
        function executeCommand() {
            const command = document.getElementById('command').value;
            fetch('/api/commands', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({command: command})
            })
            .then(r => r.json())
            .then(data => {
                document.getElementById('response').innerHTML = 
                    `<strong>Response:</strong> ${data.response}`;
            });
        }
        
        // Load stats on page load
        loadStats();
        setInterval(loadStats, 5000);
    </script>
</body>
</html>
'''
    
    def run(self, host: str = '0.0.0.0', port: int = 8080, debug: bool = False):
        """Run dashboard server"""
        self.app.run(host=host, port=port, debug=debug)
