from http.server import BaseHTTPRequestHandler
import json
import yfinance as yf
from datetime import datetime
import time

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Simple test response
        response = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "message": "Portfolio API is working!",
            "test_data": {
                "total_value_usd": 130527.56,
                "total_positions": 21,
                "sample_ticker": "VFV.TO"
            }
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
        return
