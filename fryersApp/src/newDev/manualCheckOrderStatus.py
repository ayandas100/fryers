from fyers_apiv3 import fyersModel
from datetime import date
import json


# Global state
order_state = {
    "active": False,
    "count": 0,
    "last_order_id": "25070200221029-BO-3"
}



# def check_order_status(fyers):
#     """
#     Checks the status of the last order. If completed or exited, resets order_state.
#     """
#     try:
#         if not order_state["last_order_id"]:
#             return {"status": "idle", "message": "No order placed yet."}

        
#         orders = fyers.orderbook({})
#         for order in orders["orders"]:
#             if order.get("id") == order_state["last_order_id"]:
#                 print("yes")
#                 if order["status"] in ["TRADE", "CANCELLED", "REJECTED"]:
#                     order_state["active"] = False
                    
#                     return {"status": "done", "message": f"Order {order['status']}"}
#                 else:
#                     return {"status": "pending", "message": f"Order still active: {order['status']}"}

#         # return {"status": "not_found", "message": "Order ID not found in orderbook."}
#         return od
#     except Exception as e:
#         print("⚠️ Error checking order status:", e)
#         return {"status": "error", "message": str(e)}


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
            if  order.get("status") ==2:
                order_state["active"] = False
                break  

        # return {"status": "not_found", "message": "Order not found in orderbook"}
        return order





if __name__ == '__main__':
    # Replace with your actual access token
    ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCb2IwS1hBc1pRa2Ftb3psUGhZX1M0S2x1RklJMWx3dmpxd2xRcXU5Y0JXRDVqTHNxOXRaUV9yanhrekRlOEFIeENFSE90a1ZxYWFFc2RLOVd5SU5fYTlSLVR3TVR1ZHByblAwSUFvY1BNMUpXSnQ2bz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjYTU5M2UwOTRmZmIyMzBmZTNkMjdiNGY5NDA1Y2ZmOWM5ZmI2YzEzNjBmMDRjYTExMjY4OGMxMyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEE2NjkxMCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzUyMTkzODAwLCJpYXQiOjE3NTIxMjIwMDcsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc1MjEyMjAwNywic3ViIjoiYWNjZXNzX3Rva2VuIn0.aTfEWjfWjJeCJSKXbXuFh8XTv_NIchtUX2yMIlMreww"

    # Initialize Fyers API
    fyers = fyersModel.FyersModel(client_id="15YI17TORX-100",token=ACCESS_TOKEN, log_path="")

    orSt = check_order_status(fyers)
    print(orSt)
    print(order_state)