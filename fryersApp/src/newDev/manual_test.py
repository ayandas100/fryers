from datetime import datetime

today = datetime.now().weekday()



# # Global state
# order_state = {
#     "active": False,
#     "count": 1,
#     "last_order_id": None
# }



# max_orders = 1 if today == 3 else 2
# if order_state["count"] >= max_orders:
#     print("Done")
# else:
#     print("None")


A = True
B = False
if not A == B:
    print("ok")
