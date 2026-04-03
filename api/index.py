from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "message": "Portfolio API working",
            "test": True
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
        return
