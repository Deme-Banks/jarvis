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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --bg-color: #1a1a1a;
            --fg-color: #fff;
            --card-bg: #2a2a2a;
            --primary: #4CAF50;
            --secondary: #3a3a3a;
        }
        
        body { 
            font-family: Arial, sans-serif; 
            margin: 0;
            padding: 20px; 
            background: var(--bg-color); 
            color: var(--fg-color); 
        }
        
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
        }
        
        .card { 
            background: var(--card-bg); 
            padding: 20px; 
            margin: 10px 0; 
            border-radius: 8px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .stat { 
            display: inline-block; 
            margin: 10px; 
            padding: 15px; 
            background: var(--secondary); 
            border-radius: 5px; 
            min-width: 120px;
        }
        
        .stat-value { 
            font-size: 24px; 
            font-weight: bold; 
            color: var(--primary); 
        }
        
        .stat-label { 
            font-size: 12px; 
            color: #aaa; 
        }
        
        button { 
            background: var(--primary); 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 5px; 
            cursor: pointer; 
            margin: 5px;
        }
        
        button:hover {
            opacity: 0.9;
        }
        
        input { 
            padding: 10px; 
            width: 100%;
            max-width: 400px;
            border-radius: 5px; 
            border: 1px solid #555; 
            background: #333; 
            color: #fff; 
            box-sizing: border-box;
        }
        
        .theme-selector {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 1000;
        }
        
        .theme-selector select {
            padding: 8px;
            border-radius: 5px;
            background: var(--card-bg);
            color: var(--fg-color);
            border: 1px solid #555;
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
            body { padding: 10px; }
            .card { padding: 15px; margin: 5px 0; }
            .stat { 
                display: block; 
                width: 100%; 
                margin: 5px 0; 
            }
            input { width: 100%; max-width: 100%; }
            button { width: 100%; margin: 5px 0; }
            .theme-selector {
                position: relative;
                top: 0;
                right: 0;
                margin-bottom: 10px;
            }
        }
        
        @media (max-width: 480px) {
            .stat-value { font-size: 20px; }
            .card h2 { font-size: 18px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="theme-selector">
            <select id="themeSelect" onchange="changeTheme()">
                <option value="dark">Dark Theme</option>
                <option value="light">Light Theme</option>
                <option value="cyber">Cyber Theme</option>
            </select>
        </div>
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
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + K: Focus command input
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                document.getElementById('command').focus();
            }
            // Ctrl/Cmd + Enter: Execute command
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                executeCommand();
            }
            // Escape: Clear response
            if (e.key === 'Escape') {
                document.getElementById('response').innerHTML = '';
            }
            // Ctrl/Cmd + /: Show shortcuts help
            if ((e.ctrlKey || e.metaKey) && e.key === '/') {
                e.preventDefault();
                alert('Keyboard Shortcuts:\\n\\nCtrl+K: Focus command\\nCtrl+Enter: Execute\\nEscape: Clear\\nCtrl+/: Show this help');
            }
        });
        
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
