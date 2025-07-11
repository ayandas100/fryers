from fyers_apiv3 import fyersModel
# from fyers_api import fyersModel
import json
from datetime import date
from datetime import datetime

# Replace with your actual access token
# ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCb1pLdzliaGlOMTNTdTVoeEVzXzQwOVIxX3ZUVFJaUlYtUjkzSkNPd196OF91UzNZZkRUS3hQck82ZWhYRHJ1TlBYblVUMGQwMm1EWldmcUpIbkNMS2VuY01JeGpBUWgzc0dJR2xLV3hhWTZCOU13cz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjYTU5M2UwOTRmZmIyMzBmZTNkMjdiNGY5NDA1Y2ZmOWM5ZmI2YzEzNjBmMDRjYTExMjY4OGMxMyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEE2NjkxMCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzUxNTAyNjAwLCJpYXQiOjE3NTE0MjgxNTcsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc1MTQyODE1Nywic3ViIjoiYWNjZXNzX3Rva2VuIn0.eU3k4Ue0kgj_2gPprDtaFb4Dj1lPbqPY4Qh66cdkv_k"

# Initialize Fyers API
# fyers = fyersModel.FyersModel(client_id="15YI17TORX-100",token=ACCESS_TOKEN, log_path="")
# fyers.access_token = ACCESS_TOKEN
# --- Order Config ---

# Bracket Order (BO) configuration
# order_data = {
#     "symbol": symbol,
#     "qty": qty,
#     "type": 2,                      
#     "side": 1,
#     "productType": "BO",            # Bracket Order
#     "stopLoss": stoploss_points,   # Points away from entry
#     "takeProfit": target_points,   # Points away from entry
#     "disclosedQty": 0,
#     "validity": "DAY",
#     "offlineOrder": False
    
# }



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
        print(start_time,now,end_time)
        return {"status": "closed", "message": " No trades allowed before 9.20 am or after 3:00 PM."}
    
    if order_state["active"]:
        print("Order already active. Skipping.")
        return {"status": "active", "message": "Order already running."}

    if order_state["count"] >= 2:
        print("Daily order limit reached.")
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
        s = response.get("message")
        return s
    except Exception as e:
        print("Order Error:", e)
        return {"status": "error", "message": str(e)}


# Place the order
# response = fyers.place_order(order_data)
# print("Order Response:", json.dumps(response, indent=2))


if __name__ == '__main__':
    # Replace with your actual access token
    ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCb2NNdG94YUNENThvYnhUQ1pMTXBFSzZMVnlFR0FodTFvY0ZIOXkwQmE2WG9qSW9xUm1nUldQR05feWxIOXNKT0U1ZGNiM2t4b1U5YWI1dkg2LXJuSWo1dEJFaWRJLV9ZNXctRzBFTnBydmU0RERrMD0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjYTU5M2UwOTRmZmIyMzBmZTNkMjdiNGY5NDA1Y2ZmOWM5ZmI2YzEzNjBmMDRjYTExMjY4OGMxMyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEE2NjkxMCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzUyMjgwMjAwLCJpYXQiOjE3NTIyMjI1NjgsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc1MjIyMjU2OCwic3ViIjoiYWNjZXNzX3Rva2VuIn0.3vBfSMLVEJRMKT2jeEPGR0EDuNs6ZkL2fRjmpCPZc88"

    # Initialize Fyers API
    fyers = fyersModel.FyersModel(client_id="15YI17TORX-100",token=ACCESS_TOKEN, log_path="")
    symbol = "NSE:NIFTY2571725350PE"     # Change to your desired symbol

    qty = 75
    atr = 13
    target = 10                    # 1 lot (75 quantity)
    # target = 10                  # 10-point target
    stop_loss = 3                 # 7-point stoploss

    orSt = place_bo_order(fyers, symbol, qty, stop_loss, target)
    print(orSt)
    print(order_state)