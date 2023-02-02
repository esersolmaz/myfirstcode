import yfinance as yf
import pandas as pd

msft = yf.Ticker("FROTO.IS")
print(msft.info)
x = msft.info
zip = x["zip"]
print("Posta Kodu :",zip)

#print(x)
xxx = msft.quarterly_financials
print(type(xxx))
print(xxx.head())
print(xxx)
print(xxx[["2021-03-31"]])
x2= xxx[["2021-03-31"]]

test = pd.DataFrame(x2)
test2 = test.values.tolist()
print(type(test2))
print(test2[0])

#hist = msft.history(period="max")
#print(hist)

#xx=msft.financials
#print(xx)