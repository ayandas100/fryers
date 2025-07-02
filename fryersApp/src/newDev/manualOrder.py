from fyers_apiv3 import fyersModel
# from fyers_api import fyersModel
import json

# Replace with your actual access token
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCb1pLdzliaGlOMTNTdTVoeEVzXzQwOVIxX3ZUVFJaUlYtUjkzSkNPd196OF91UzNZZkRUS3hQck82ZWhYRHJ1TlBYblVUMGQwMm1EWldmcUpIbkNMS2VuY01JeGpBUWgzc0dJR2xLV3hhWTZCOU13cz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjYTU5M2UwOTRmZmIyMzBmZTNkMjdiNGY5NDA1Y2ZmOWM5ZmI2YzEzNjBmMDRjYTExMjY4OGMxMyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEE2NjkxMCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzUxNTAyNjAwLCJpYXQiOjE3NTE0MjgxNTcsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc1MTQyODE1Nywic3ViIjoiYWNjZXNzX3Rva2VuIn0.eU3k4Ue0kgj_2gPprDtaFb4Dj1lPbqPY4Qh66cdkv_k"

# Initialize Fyers API
fyers = fyersModel.FyersModel(client_id="15YI17TORX-100",token=ACCESS_TOKEN, log_path="")
# fyers.access_token = ACCESS_TOKEN
# --- Order Config ---
symbol = "NSE:NIFTY2570325700PE"     # Change to your desired symbol

qty = 75                             # 1 lot (75 quantity)
target_points = 10                  # 10-point target
stoploss_points = 3                 # 7-point stoploss

# Bracket Order (BO) configuration
order_data = {
    "symbol": symbol,
    "qty": qty,
    "type": 2,                      
    "side": 1,
    "productType": "BO",            # Bracket Order
    "stopLoss": stoploss_points,   # Points away from entry
    "takeProfit": target_points,   # Points away from entry
    "disclosedQty": 0,
    "validity": "DAY",
    "offlineOrder": False
    
}

# Place the order
response = fyers.place_order(order_data)
print("Order Response:", json.dumps(response, indent=2))
