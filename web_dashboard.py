#!/usr/bin/env python3
"""
Simple web dashboard for HK Smart Factory
Minimal HTTP server to view production status
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path
from datetime import datetime


class FactoryDashboardHandler(BaseHTTPRequestHandler):
    """Handles HTTP requests for factory dashboard"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.serve_dashboard()
        elif self.path == '/api/status':
            self.serve_status_api()
        elif self.path == '/api/reports':
            self.serve_reports_list()
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
        """Serve main HTML dashboard"""
        html = """<!DOCTYPE html>
<html>
<head>
    <title>HK Smart Factory Dashboard</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f0f0f0;
        }
        .header {
            background: #2c3e50;
            color: white;
            padding: 20px;
            margin: -20px -20px 20px -20px;
        }
        .card {
            background: white;
            padding: 20px;
            margin: 10px 0;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .status-good { color: #27ae60; font-weight: bold; }
        .status-warn { color: #f39c12; font-weight: bold; }
        h1 { margin: 0; }
        h2 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        .metric { font-size: 24px; color: #3498db; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏭 HK Smart Factory Dashboard</h1>
        <p>Real-time Production Monitoring</p>
    </div>
    
    <div class="card">
        <h2>System Status</h2>
        <p>Status: <span class="status-good">OPERATIONAL</span></p>
        <p>Last Update: <span id="update-time"></span></p>
    </div>
    
    <div class="card">
        <h2>Production Lines</h2>
        <p><strong>Assembly Line A:</strong> <span class="status-good">Running</span></p>
        <p class="metric" id="line-a-output">--- units/hour</p>
        <p><strong>Packaging Line B:</strong> <span class="status-good">Running</span></p>
        <p class="metric" id="line-b-output">--- units/hour</p>
    </div>
    
    <div class="card">
        <h2>Recent Reports</h2>
        <div id="reports-list">Loading...</div>
    </div>
    
    <script>
        function updateDashboard() {
            document.getElementById('update-time').textContent = new Date().toLocaleString();
            
            fetch('/api/reports')
                .then(r => r.json())
                .then(data => {
                    const list = document.getElementById('reports-list');
                    if (data.reports && data.reports.length > 0) {
                        list.innerHTML = '<ul>' + 
                            data.reports.slice(0, 5).map(r => 
                                `<li>${r}</li>`
                            ).join('') + 
                            '</ul>';
                    } else {
                        list.innerHTML = '<p>No reports available</p>';
                    }
                });
        }
        
        updateDashboard();
        setInterval(updateDashboard, 5000);
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_status_api(self):
        """Serve status API endpoint"""
        status = {
            "factory": "HK Manufacturing Facility",
            "timestamp": datetime.now().isoformat(),
            "status": "operational",
            "lines": {
                "line_a": {"running": True, "rate": 450},
                "line_b": {"running": True, "rate": 280}
            }
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(status).encode())
    
    def serve_reports_list(self):
        """Serve list of available reports"""
        reports_dir = Path('production_data')
        reports = []
        
        if reports_dir.exists():
            reports = [f.name for f in reports_dir.glob('*.json')]
        
        response = {"reports": sorted(reports, reverse=True)}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, fmt, *args):
        """Suppress request logging"""
        pass


def start_dashboard(port=8080):
    """Start the dashboard server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, FactoryDashboardHandler)
    print(f"\n{'='*60}")
    print(f"HK Smart Factory Dashboard")
    print(f"{'='*60}")
    print(f"\nDashboard running at: http://localhost:{port}")
    print("Press Ctrl+C to stop\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nDashboard stopped")
        httpd.shutdown()


if __name__ == "__main__":
    start_dashboard()
