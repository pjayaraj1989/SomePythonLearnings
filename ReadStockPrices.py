import yfinance as yf
import sys

#FIXME
# read if symbol exists
# read currency
# if possible convert currency

def Error_Exit(msg):
    input(msg)
    exit(1)

def GetStockPrice(symbol):
    price=0.0
    data=yf.Ticker(symbol)
    price = data.info['open']
    return price

if len(sys.argv) != 2:
    Error_Exit ('Error! Give the symbol as an arg')
symbol=sys.argv[1]
if symbol is None or '':
    Error_Exit ('Error! Enter valid symbol!')

print (GetStockPrice(symbol))
