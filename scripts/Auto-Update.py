"""
This program records live stock prices from Yahoo Finance API and stores the data in a MongoDB Atlas database.
"""

from StockMarket import Stock_Model

# set list of stocks for live dashboard
sm = Stock_Model(['MSFT','AAPL'])

print("Updating database...")

# run data-update loop
sm.data_capture()
