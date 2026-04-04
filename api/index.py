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
        
        portfolio_holdings = [
            {"ticker": "ARKQ", "shares": 30},
            {"ticker": "BE", "shares": 20},
            {"ticker": "CGL.TO", "shares": 150},
            {"ticker": "GRID", "shares": 65},
            {"ticker": "HURA.TO", "shares": 65},
            {"ticker": "ICLN", "shares": 380},
            {"ticker": "IXN", "shares": 53},
            {"ticker": "LIT", "shares": 45},
            {"ticker": "MAGS", "shares": 42},
            {"ticker": "MGK", "shares": 10},
            {"ticker": "SMH", "shares": 25},
            {"ticker": "TAN", "shares": 70},
            {"ticker": "THNQ", "shares": 166},
            {"ticker": "URA", "shares": 161},
            {"ticker": "VFV.TO", "shares": 109},
            {"ticker": "VXC.TO", "shares": 139},
            {"ticker": "XAR", "shares": 31},
            {"ticker": "XEM.TO", "shares": 120},
            {"ticker": "XETM.TO", "shares": 90},
            {"ticker": "XQQ.TO", "shares": 80},
            {"ticker": "ZEB.TO", "shares": 285}
        ]
        
        start_time = time.time()
        positions = []
        
        # Fetch prices with rate limiting (1 second delay)
        for holding in portfolio_holdings:
            ticker = holding['ticker']
            shares = holding['shares']
            
            # Rate limit - wait between requests
            time.sleep(1)
            
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period='1d')
                
                if not hist.empty and len(hist) > 0:
                    current_price = hist['Close'].iloc[-1]
                    previous_close = hist['Close'].iloc[0] if len(hist) > 1 else current_price
                    
                    daily_change = current_price - previous_close
                    daily_change_pct = (daily_change / previous_close) * 100 if previous_close != 0 else 0
                    position_value = shares * current_price
                    
                    positions.append({
                        "ticker": ticker,
                        "shares": shares,
                        "price": round(current_price, 2),
                        "previous_close": round(previous_close, 2),
                        "daily_change": round(daily_change, 2),
                        "daily_change_pct": round(daily_change_pct, 2),
                        "position_value": round(position_value, 2),
                        "status": "success"
                    })
                else:
                    positions.append({
                        "ticker": ticker,
                        "shares": shares,
                        "error": "No price data",
                        "status": "failed"
                    })
            except Exception as e:
                positions.append({
                    "ticker": ticker,
                    "shares": shares,
                    "error": str(e)[:100],
                    "status": "error"
                })
        
        # Calculate totals
        total_value_usd = sum(p.get('position_value', 0) for p in positions if p.get('status') == 'success')
        usd_to_cad_rate = 1.35
        total_value_cad = total_value_usd * usd_to_cad_rate
        
        success_count = sum(1 for p in positions if p.get('status') == 'success')
        
        response = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "elapsed_time": round(time.time() - start_time, 2),
            "summary": {
"total_value_usd": round(total_value_usd, 2),
                "total_value_cad": round(total_value_cad, 2),
                "usd_to_cad_rate": usd_to_cad_rate,
                "total_positions": len(portfolio_holdings),
                "successful_updates": success_count,
                "failed_updates": len(portfolio_holdings) - success_count,
                "total_shares": sum(h['shares'] for h in portfolio_holdings)
            },
            "positions": positions
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
        return
