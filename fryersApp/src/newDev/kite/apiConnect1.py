import pandas  as pd
instrumentList = pd.read_csv("https://api.kite.trade/instruments")
print(instrumentList)