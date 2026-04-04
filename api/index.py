import json
import requests
from datetime import datetime
import time

def handler(request):
    FINNHUB_API_KEY = "d788dehr01qsamsjbb70d788dehr01qsamsjbb7g"
    
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
        
        time.sleep(0.8)
        
        try:
            finnhub_ticker = ticker.replace('.TO', ':TSX')
            url = f"https://finnhub.io/api/v1/quote?symbol={finnhub_ticker}&token={FINNHUB_API_KEY}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                current_price = data.get('c')
                prev_close = data.get('pc')
                
                if current_price and prev_close and current_price > 0:
                    daily_change = current_price - prev_close
                    daily_change_pct = (daily_change / prev_close) * 100 if prev_close != 0 else 0
                    position_value = shares * current_price
                    
                    positions.append({
                        "ticker": ticker,
                        "shares": shares,
                        "price": round(current_price, 2),
                        "previous_close": round(prev_close, 2),
                        "daily_change": round(daily_change, 2),
                        "daily_change_pct": round(daily_change_pct, 2),
                        "position_value": round(position_value, 2),
                        "status": "success"
                    })
                else:
                    positions.append({
                        "ticker": ticker,
                        "shares": shares,
                        "error": "No data",
                        "status": "failed"
                    })
            else:
                positions.append({
                    "ticker": ticker,
                    "shares": shares,
                    "error": "API error",
                    "status": "error"
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
    
    response_data = {
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
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(response_data, indent=2)
    }

