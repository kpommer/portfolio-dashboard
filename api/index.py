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
        
        for holding in portfolio_holdings:
            ticker = holding['ticker']
            shares = holding['shares']
            
            # Rate limit
            time.sleep(0.5)
            
            try:
                stock = yf.Ticker(ticker)
                
                price = None
                prev_close = None
                
                # Method 1: fast_info
                try:
                    fast_info = stock.fast_info
                    price = fast_info.last_price
                    prev_close = fast_info.previous_close
                except:
                    pass
                
                # Method 2: info
                if not price:
                    info = stock.info
                    price = info.get('regularMarketPrice') or info.get('currentPrice')
                    prev_close = info.get('regularMarketPreviousClose') or info.get('previousClose')
                
                # Method 3: history
                if not price:
                    hist = stock.history(period='2d')
                    if not hist.empty:
                        price = hist['Close'].iloc[-1]
                        prev_close = hist['Close'].iloc[0] if len(hist) > 1 else price
                
                if price and prev_close:
                    daily_change = price - prev_close
                    daily_change_pct = (daily_change / prev_close) * 100 if prev_close != 0 else 0
                    position_value = shares * price
                    
                    positions.append({
                        "ticker": ticker,
                        "shares": shares,
                        "price": round(float(price), 2),
                        "previous_close": round(float(prev_close), 2),
                        "daily_change": round(float(daily_change), 2),
                        "daily_change_pct": round(float(daily_change_pct), 2),
                        "position_value": round(float(position_value), 2),
                        "status": "success"
                    })
                else:
positions.append({
                        "ticker": ticker,
                        "shares": shares,
                        "error": "No price",
                        "status": "failed"
                    })
                    
            except Exception as e:
                positions.append({
                    "ticker": ticker,
                    "shares": shares,
                    "error": str(e)[:80],
                    "status": "error"
                })
        
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

            "positions": positions
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
        return
