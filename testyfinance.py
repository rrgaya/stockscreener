import yfinance as yf


msft = yf.Ticker("msft")

#get stock info
print(msft.info)