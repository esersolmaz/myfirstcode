import yfinance as yf
data = yf.download("FROTO.IS")#, start="2021-05-28", end="2021-05-28")
datax = yf.Ticker("FROTO.IS")
print(datax.info)
print(type(datax))
#print(type(data))
#print(data)


#data2 = datax.values.tolist()
#print(data2)