from fyers_apiv3 import fyersModel
from datetime import date
client_id = "15YI17TORX-100"
# today = date.today().strftime("%Y-%m-%d")
from datetime import datetime

# Global state
order_state = {
    "active": False,
    "count": 0,
    "last_order_id": None
}

def place_bo_order(fyers, symbol, qty, stop_loss, target):
    """
    Places a Bracket Order (BO) if no other active order and count < 3.
    """
    start_time = datetime.strptime("09:20", "%H:%M").time()
    end_time = datetime.strptime("15:00", "%H:%M").time()
    now = datetime.now().time()
    if not (start_time <= now < end_time):
        # print("No more trades after 3:00 PM.")
        return {"status": "closed", "message": " No trades allowed before 9.20 am or after 3:00 PM."}
    
    if order_state["active"]:
        # print("Order already active. Skipping.")
        return {"status": "active", "message": "Order already running."}

    if order_state["count"] >= 2:
        # print("Daily order limit reached.")
        return {"status": "limit", "message": "Max 2 orders reached."}

    payload = {
        "symbol": symbol,
        "qty": qty,
        "type": 2,               
        "side": 1,               
        "productType": "BO",
        "stopLoss": stop_loss,
        "takeProfit": target,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False
    }

    try:
        
        response = fyers.place_order(payload)
        order_state["active"] = True
        order_state["count"] += 1
        order_state["last_order_id"] = response.get("id")
        return response.get("message")
    except Exception as e:
        print("Order Error:", e)
        return {"status": "error", "message": str(e)}

def check_order_status(fyers):
    if not order_state["last_order_id"]:
        return {"status": "idle", "message": "No order placed yet."}
    
    orders = fyers.orderbook({})
    if "orderBook" in orders:
        
        sorted_orders = sorted(
                    orders["orderBook"],
                    key=lambda x: x.get("orderDateTime", ""),
                    reverse=True
                )
        for order in sorted_orders:
            if order.get("id") == order_state["last_order_id"]:
                if order.get("status") in [1,2,5]:
                    order_state["active"] = False
                  

        return {"status": "not_found", "message": "Order not found in orderbook"}



def get_order_state():
    """Returns the current order state."""
    return order_state
