import yfinance as yf
import os


#f = open("/Users/esersolmaz/PycharmProjects/myfirstcode/fintech/hissekod", "r")
#print(f.read())

# Open the file for reading.
with open('hissekod', 'r') as infile:

    data = infile.read()  # Read the contents of the file into memory.

# Return a list of the lines, breaking at line boundaries.
my_list = data.splitlines()
print(my_list)



#data = yf.download("FROTO.IS")#, start="2021-05-28", end="2021-05-28")
#data = yf.Ticker("FROTO.IS")
#cashflow = datax.cashflow
#print(cashflow)
#print(datax.info)
#sonfiyat = datax.info['currentPrice']
#fkoarani = datax.info['trailingPE']
#pddd = datax.info['priceToBook']
#fdfavok = datax.info['enterpriseToEbitda']
#ozsermayakarliligi = datax.info['returnOnEquity']
#temettuorani = datax.info['dividendRate']
#evebitda = datax.info['']
#print('Son Fiyat: ',sonfiyat)
#print('F/K Oranı: ',fkoarani)
#print('PD/DD: ',pddd)
#print('PD/FAVOK :',fdfavok)
#print('Öz Sermaye Karlılığı: ', ozsermayakarliligi)
#print('Temettü Oranı :', temettuorani)


for hissekodu in my_list:
    try:
        #print(hissekodu)
        dataget = yf.Ticker(hissekodu)
        #print(dataget.info)
        fkorani = dataget.info['trailingPE']
        pddd = dataget.info['priceToBook']
        ozsermayakarliligi = dataget.info['returnOnEquity']

        if fkorani < 10 and pddd <2:
            if ozsermayakarliligi > 1.15:
                print (hissekodu,'- F/K :',fkorani,',',' PD/DD :',pddd,',', ' Öz Sermaye Karlılığı : ',ozsermayakarliligi)

    except Exception as e:
        #print(f'Error: {e}')
        pass