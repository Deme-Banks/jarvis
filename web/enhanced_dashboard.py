"""
Enhanced Web Dashboard with Real-time Updates
"""
from flask import Flask, render_template_string, jsonify, request, Response
from typing import Dict, Optional
import json
import threading
import time
from agents.orchestrator_pi import PiOrchestrator
from analytics.performance_monitor import PerformanceMonitor
from analytics.usage_analytics import UsageAnalytics
from features.command_history import CommandHistory


class EnhancedDashboard:
    """Enhanced web dashboard with real-time features"""
    
    def __init__(self, orchestrator: Optional[PiOrchestrator] = None):
        self.app = Flask(__name__)
        self.orchestrator = orchestrator
        self.performance_monitor = PerformanceMonitor()
        self.usage_analytics = UsageAnalytics()
        self.command_history = CommandHistory()
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
            perf_stats = self.performance_monitor.get_summary()
            usage_stats = self.usage_analytics.get_insights()
            history_stats = self.command_history.get_stats()
            
            return jsonify({
                'performance': perf_stats,
                'usage': usage_stats,
                'history': history_stats,
                'timestamp': time.time()
            })
        
        @self.app.route('/api/commands', methods=['POST'])
        def execute_command():
            """Execute command via API"""
            data = request.json
            command = data.get('command', '')
            
            if self.orchestrator:
                response = self.orchestrator.process(command)
            else:
                response = "Orchestrator not available"
            
            return jsonify({
                'command': command,
                'response': response,
                'success': True
            })
        
        @self.app.route('/api/history')
        def history():
            """Get command history"""
            limit = request.args.get('limit', 20, type=int)
            return jsonify({
                'history': self.command_history.get_recent(limit)
            })
        
        @self.app.route('/api/stream')
        def stream():
            """Server-sent events stream"""
            def event_stream():
                while True:
                    stats = self.performance_monitor.get_summary()
                    yield f"data: {json.dumps(stats)}\n\n"
                    time.sleep(2)
            
            return Response(event_stream(), mimetype='text/event-stream')
    
    def _get_dashboard_html(self) -> str:
        """Get enhanced dashboard HTML"""
        return '''
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS Enhanced Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { opacity: 0.8; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .card { 
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3); }
        .card h2 { margin-bottom: 15px; color: #4CAF50; }
        .stat { display: flex; justify-content: space-between; margin: 10px 0; padding: 10px; background: rgba(255, 255, 255, 0.05); border-radius: 8px; }
        .stat-label { opacity: 0.8; }
        .stat-value { font-weight: bold; color: #4CAF50; }
        .command-input { 
            width: 100%;
            padding: 15px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: #fff;
            font-size: 16px;
            margin-bottom: 10px;
        }
        .command-input::placeholder { color: rgba(255, 255, 255, 0.5); }
        .btn { 
            padding: 12px 24px;
            background: #4CAF50;
            border: none;
            border-radius: 8px;
            color: white;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }
        .btn:hover { background: #45a049; }
        .response { 
            margin-top: 20px;
            padding: 15px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }
        .history-item { 
            padding: 10px;
            margin: 5px 0;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            border-left: 3px solid #4CAF50;
        }
        .status-indicator { 
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #4CAF50;
            margin-right: 10px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 JARVIS Enhanced Dashboard</h1>
            <p><span class="status-indicator"></span>System Operational</p>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>📊 Performance</h2>
                <div id="performance-stats"></div>
            </div>
            
            <div class="card">
                <h2>📈 Usage Analytics</h2>
                <div id="usage-stats"></div>
            </div>
            
            <div class="card">
                <h2>💬 Command Interface</h2>
                <input type="text" id="command" class="command-input" placeholder="Enter command...">
                <button class="btn" onclick="executeCommand()">Execute</button>
                <div id="response" class="response" style="display:none;"></div>
            </div>
        </div>
        
        <div class="card">
            <h2>📜 Recent Commands</h2>
            <div id="history"></div>
        </div>
    </div>
    
    <script>
        function loadStats() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    // Performance stats
                    const perf = data.performance || {};
                    document.getElementById('performance-stats').innerHTML = `
                        <div class="stat">
                            <span class="stat-label">Avg Response Time</span>
                            <span class="stat-value">${(perf.avg_response_time || 0).toFixed(2)}s</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Total Responses</span>
                            <span class="stat-value">${perf.total_responses || 0}</span>
                        </div>
                    `;
                    
                    // Usage stats
                    const usage = data.usage || {};
                    document.getElementById('usage-stats').innerHTML = `
                        <div class="stat">
                            <span class="stat-label">Total Commands</span>
                            <span class="stat-value">${usage.total_commands || 0}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Success Rate</span>
                            <span class="stat-value">${((usage.success_rate || 0) * 100).toFixed(1)}%</span>
                        </div>
                    `;
                });
        }
        
        function loadHistory() {
            fetch('/api/history?limit=10')
                .then(r => r.json())
                .then(data => {
                    const history = data.history || [];
                    document.getElementById('history').innerHTML = history.map(cmd => `
                        <div class="history-item">
                            <strong>${cmd.command}</strong><br>
                            <small>${cmd.timestamp}</small>
                        </div>
                    `).join('');
                });
        }
        
        function executeCommand() {
            const command = document.getElementById('command').value;
            if (!command) return;
            
            fetch('/api/commands', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({command: command})
            })
            .then(r => r.json())
            .then(data => {
                const responseDiv = document.getElementById('response');
                responseDiv.style.display = 'block';
                responseDiv.innerHTML = `<strong>Response:</strong> ${data.response}`;
                loadHistory();
                loadStats();
            });
        }
        
        // Auto-refresh
        setInterval(loadStats, 5000);
        setInterval(loadHistory, 10000);
        loadStats();
        loadHistory();
        
        // Enter key support
        document.getElementById('command').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                executeCommand();
            }
        });
    </script>
</body>
</html>
'''
    
    def run(self, host: str = '0.0.0.0', port: int = 8080, debug: bool = False):
        """Run dashboard server"""
        self.app.run(host=host, port=port, debug=debug)
