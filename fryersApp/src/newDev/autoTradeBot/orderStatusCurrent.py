from fyers_api import fyersModel

def get_current_order_details(fyers):
    try:
        orders = fyers.get_orders()
        positions = fyers.positions()
        
        active_orders = []
        
        for order in orders['orders']:
            if order['status'] in ['OPEN', 'TRIGGER PENDING', 'PARTIALLY FILLED', 'TRADE']:  # Active orders
                symbol = order['symbol']
                qty = order['qty']
                status = order['status']
                order_id = order['id']
                
                # Look up P&L from positions API
                pnl = 0
                for pos in positions['netPositions']:
                    if pos['symbol'] == symbol:
                        pnl = pos['pnl']
                        break
                
                active_orders.append({
                    "order_id": order_id,
                    "symbol": symbol,
                    "qty": qty,
                    "status": status,
                    "pnl": round(pnl, 2)
                })
        
        return active_orders if active_orders else [{"message": "No active orders"}]
    
    except Exception as e:
        return [{"error": str(e)}]
