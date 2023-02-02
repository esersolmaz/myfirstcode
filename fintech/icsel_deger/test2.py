from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pandas_datareader as dr
import datetime
'''---------- // Hard-coded variables below // ----------'''

company_ticker = 'AAPL'
timespan = 100 #timespan for the equity beta calculation
market_risk_premium = 0.0523
long_term_growth = 0.01
debt_return = 0.01
tax_rate = 0.3
'''---------- // Hard-coded variables above // ----------'''
'''----- // I. Financial Information from Yahoo Finance // -----'''

income_statement_url = '<https://finance.yahoo.com/quote/>' + company_ticker + '/financials?p=' + company_ticker

income_statement_html = requests.get(income_statement_url)
income_statement_soup = bs(income_statement_html.text, 'html.parser')

income_statement_table = income_statement_soup.find('div', class_='M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)')
income_statement_header = income_statement_table.find('div', class_='D(tbr) C($primaryColor)')
header_lst = []
for i in income_statement_header.find_all('div'):
    if len(i) != 0:
       header_lst.append(i.text)
header_lst = header_lst[::-1]
del header_lst[len(header_lst)-1]
header_lst.insert(0,'Breakdown')
income_statement_df = pd.DataFrame(columns = header_lst)

revenue_row = income_statement_table.find('div', class_='D(tbr) fi-row Bgc($hoverBgColor):h')
revenue_lst = []
for i in revenue_row.find_all('div', attrs={'data-test':'fin-col'}):
    i = i.text
    i = i.replace(",","")
    revenue_lst.append(int(i))
revenue_lst = revenue_lst[::-1]
revenue_lst.insert(0,'Total Revenue')
income_statement_df.loc[0] = revenue_lst

EBIT_row = income_statement_table.find('div', attrs={'title':'EBIT'}).parent.parent
EBIT_lst = []
for i in EBIT_row.find_all('div', attrs={'data-test':'fin-col'}):
    i = i.text
    i = i.replace(",","")
    EBIT_lst.append(int(i))
EBIT_lst = EBIT_lst[::-1]
EBIT_lst.insert(0,'EBIT')
income_statement_df.loc[1] = EBIT_lst

income_statement_df = income_statement_df.drop('ttm', axis=1)
'''---------- // II. Forecasting Revenues and EBIT // ----------'''

latest_rev = income_statement_df.iloc[0,len(income_statement_df.columns)-1]
earliest_rev = income_statement_df.iloc[0,1]
rev_CAGR = (latest_rev/earliest_rev)**(float(1/(len(income_statement_df.columns)-2)))-1

EBIT_margin_lst = []
for year in range(1,len(income_statement_df.columns)):
    EBIT_margin = income_statement_df.iloc[1,year]/income_statement_df.iloc[0,year]
    EBIT_margin_lst.append(EBIT_margin)
avg_EBIT_margin = sum(EBIT_margin_lst)/len(EBIT_margin_lst)

forecast_df = pd.DataFrame(columns=['Year ' + str(i) for i in range(1,7)])

rev_forecast_lst = []
for i in range(1,7):
    if i != 6:
        rev_forecast = latest_rev*(1+rev_CAGR)**i
    else:
        rev_forecast = latest_rev*(1+rev_CAGR)**(i-1)*(1+long_term_growth)
    rev_forecast_lst.append(int(rev_forecast))
forecast_df.loc[0] = rev_forecast_lst

EBIT_forecast_lst = []
for i in range(0,6):
    EBIT_forecast = rev_forecast_lst[i]*avg_EBIT_margin
    EBIT_forecast_lst.append(int(EBIT_forecast))
forecast_df.loc[1] = EBIT_forecast_lst

'''---------- // III. Calculating the WACC // ----------'''

current_date = datetime.date.today()
past_date = current_date-datetime.timedelta(days=timespan)

risk_free_rate_df = dr.DataReader('^TNX', 'yahoo', past_date, current_date)
risk_free_rate_float = (risk_free_rate_df.iloc[len(risk_free_rate_df)-1,5])/100

price_information_df = pd.DataFrame(columns=['Stock Prices', 'Market Prices'])

stock_price_df = dr.DataReader(company_ticker, 'yahoo', past_date, current_date)
price_information_df['Stock Prices'] = stock_price_df['Adj Close']

market_price_df = dr.DataReader('^GSPC', 'yahoo', past_date, current_date)
price_information_df['Market Prices'] = market_price_df['Adj Close']

returns_information_df = pd.DataFrame(columns =['Stock Returns', 'Market Returns'])

stock_return_lst = []
for i in range(1,len(price_information_df)):
    open_price = price_information_df.iloc[i-1,0]
    close_price = price_information_df.iloc[i,0]
    stock_return = (close_price-open_price)/open_price
    stock_return_lst.append(stock_return)
returns_information_df['Stock Returns'] = stock_return_lst

market_return_lst = []
for i in range(1,len(price_information_df)):
    open_price = price_information_df.iloc[i-1,1]
    close_price = price_information_df.iloc[i,1]
    market_return = (close_price-open_price)/open_price
    market_return_lst.append(market_return)
returns_information_df['Market Returns'] = market_return_lst

covariance_df = returns_information_df.cov()
covariance_float = covariance_df.iloc[1,0]
variance_df = returns_information_df.var()
market_variance_float = variance_df.iloc[1]

equity_beta = covariance_float/market_variance_float
equity_return = risk_free_rate_float+equity_beta*(market_risk_premium)

balance_sheet_url = '<https://finance.yahoo.com/quote/>' + company_ticker + '/balance-sheet?p=' + company_ticker

balance_sheet_html = requests.get(balance_sheet_url)
balance_sheet_soup = bs(balance_sheet_html.text, 'html.parser')

balance_sheet_table = balance_sheet_soup.find('div', class_='D(tbrg)')

net_debt_lst = []

net_debt_row = balance_sheet_table.find('div', attrs={'title':'Net Debt'}).parent.parent
for value in net_debt_row.find_all('div'):
    value = value.text
    value = value.replace(',','')
    net_debt_lst.append(value)
net_debt_int = int(net_debt_lst[3])

market_cap_url = '<https://finance.yahoo.com/quote/>' + company_ticker + '?p=' + company_ticker
market_cap_html = requests.get(market_cap_url)
market_cap_soup = bs(market_cap_html.text, 'html.parser')

market_cap_int = 0

market_cap_row = market_cap_soup.find('td', attrs={'data-test':'MARKET_CAP-value'})
market_cap_str = market_cap_row.text
market_cap_lst = market_cap_str.split('.')

if market_cap_str[len(market_cap_str)-1] == 'T':
    market_cap_length = len(market_cap_lst[1])-1
    market_cap_lst[1] = market_cap_lst[1].replace('T',(9-market_cap_length)*'0')
    market_cap_int = int(''.join(market_cap_lst))

if market_cap_str[len(market_cap_str)-1] == 'B':
    market_cap_length = len(market_cap_lst[1])-1
    market_cap_lst[1] = market_cap_lst[1].replace('B',(6-market_cap_length)*'0')
    market_cap_int = int(''.join(market_cap_lst))

company_value = market_cap_int + net_debt_int

WACC = market_cap_int/company_value * equity_return + net_debt_int/company_value * debt_return * (1-tax_rate)

'''-------- // IV. Discounting the Forecasted EBIT // --------'''

discounted_EBIT_lst = []

for year in range(0,5):
    discounted_EBIT = forecast_df.iloc[1,year]/(1+WACC)**(year+1)
    discounted_EBIT_lst.append(int(discounted_EBIT))

terminal_value = forecast_df.iloc[1,5]/(WACC-long_term_growth)
PV_terminal_value = int(terminal_value/(1+WACC)**5)

enterprise_value = sum(discounted_EBIT_lst)+PV_terminal_value
equity_value = enterprise_value-net_debt_int