"""

    Update
    
    This program records live stock prices from Yahoo Finance API and stores the data in a MongoDB Atlas database.

    This is the data updating mechanism for the entire database.
    
"""

from .security import Security
from yahoo_fin import stock_info as si
import pymongo
from pymongo import MongoClient
from datetime import datetime
import wikipedia
import getpass
import json
import time
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pkg_resources

class Update:
    
    def __init__(self, watch_list=[]):

        self.s = Security()
        self._admin = self.s.encrypt()
        
        self.watch_list = watch_list
        
        # ticker--> company data
        stream = pkg_resources.resource_stream(__name__, 'data/stock_symbols.csv')
        ticker_df = pd.read_csv(stream, encoding='latin-1')
        ticker_list = list(ticker_df['Symbol'])
        ticker_companies = list(ticker_df['CompanyName'])
        self.company_tickers = dict(zip(ticker_list,ticker_companies))
    
    def db_update_daily(self):
        
        # stock market closes
        self.post_market()
        
        
    
    def data_capture(self):
        
        """ Primary database update loop """
        print('Recording live data...')
        now =  datetime.now()
        current_hour = now.hour
        current_minute = now.minute
        
        # Live Prices Update Loop
        self.watch_list_update()

        # update company info and wiki info every 7 days
        if int(now.day) % 7 == 0:
            self.update_wiki(stock_symbol)
            self.update_company_info(stock_symbol)
            
    
    def new_stock_entry(self, stock_symbol):

        """ Add new stock symbol and data to MongoDB database """
        
        # Initialize new stock
        for collection_title in ['Analyst_Info','Cashflow','Historic','Holders',
                                 'Income_Statement','Live_Price','Quote_Table',
                                 'Stats','Stats_Valuation','Twitter','Wiki',
                                 'Yearly_Balance_Sheet']:         

            client_connect = "mongodb+srv://wesley:{}@stock-analytics.vmxv5.mongodb.net/{}?retryWrites=true&w=majority".format(self.s.decrypt(self._admin), collection_title)
            cluster = MongoClient(client_connect)
            db = cluster['Stocks']
            collection = db[collection_title]
            
            try:
                # insert one post to database
                post = {"_id" : stock_symbol, }
                collection.insert_one(post)
            except:
                pass
        
        # update database
        self.update_wiki(stock_symbol)
        self.update_company_info(stock_symbol)
    
    
    """ 
    **************
    UPDATE METHODS 
    **************
    """    
        
    def update(self, key, value, database, collection_title):
        
        # connect to MongoDB
        client_connect = "mongodb+srv://wesley:{}@stock-analytics.vmxv5.mongodb.net/{}?retryWrites=true&w=majority".format(self.s.decrypt(self._admin), collection_title)
        cluster = MongoClient(client_connect)
        
        # Convert to JSON
        if isinstance(value, dict):
            data = json.dumps(value)
        else:
            data = value
        
        # set database and collection
        db = cluster[database]
        collection = db[collection_title]

        now = str(datetime.date(datetime.now()))
        collection.update_one({"_id" : key}, {"$set":{now : data}})
    
    
    def watch_list_update(self):
        
        """ Loop for recording live stock prices in real time and storing that data in MongoDB database """
        
        current_time =  datetime.now().time()
        current_hour = current_time.hour
        current_minute = current_time.minute
        
        # while stock market is open
        while (current_hour < 16):
            
            new_time = datetime.now().time()
            current_hour = new_time.hour
            current_minute = new_time.minute
            
            for symbol in self.watch_list:
                self.update_live_price(symbol)
                
            time.sleep(3)
    
    
    def update_wiki(self, symbol):
        
        """ Pull company data from the Wikipedia API and store it in MongoDB collection """ 
        
        w = Wiki()
        data = w.get_wiki(symbol)
        self.update(symbol, data, 'Stocks', 'Wiki')
        
        
    def update_twitter(self,symbol):
        
        """ 
        (In development)
        
        Connect to Twitter API and extract tweets based on keyword search for stock ticker or company name
        
        """
        
        twitter_streamer = TwitterStreamer()
        twitter_streamer.stream_tweets([symbol])
        
    
    def update_live_price(self, symbol):
        
        # info
        database_title = 'Stocks'
        collection_title = 'Live_Price'
        
        # connect to MongoDB
        client_connect = "mongodb+srv://wesley:{}@stock-analytics.vmxv5.mongodb.net/{}?retryWrites=true&w=majority".format(self.s.decrypt(self._admin), collection_title)
        cluster = MongoClient(client_connect)
        db = cluster[database_title]
        collection = db[collection_title]
        
        now = str(datetime.now()).replace('.','_')
        live_price = si.get_live_price(symbol)

        # update database
        collection.update_one({"_id" : symbol}, {"$set":{now : live_price}})  
        
        
    def update_company_info(self, symbol):
        
        # Once a day
        self.update_historic(symbol)
        
        # Once a week
        self.update_quote_table(symbol)
        
        # Once every 3 months
        self.update_analyst_info(symbol)
        self.update_cashflow(symbol)
        self.update_stats(symbol)
        self.update_stats_valuation(symbol)
        self.update_income_statement(symbol)
        self.update_holders(symbol)
        
        # Once a year
        self.update_yearly_balance_sheet(symbol)
    
        
    def update_historic(self, symbol):
        historic = si.get_data(symbol)
        historic.index = historic.index.astype(str)
        historic = historic.to_dict(orient="dict")
        self.update(symbol, historic, 'Stocks', 'Historic')
       
        
    def update_analyst_info(self, symbol):
        analysts_info = si.get_analysts_info(symbol)
        analysts_info = {'Earnings Estimate' : analysts_info['Earnings Estimate'].to_dict(orient="dict"),
                         'Revenue Estimate'  : analysts_info['Revenue Estimate'].to_dict(orient="dict"),
                         'Earnings History'  : analysts_info['Earnings History'].to_dict(orient="dict"),
                         'EPS Trend'         : analysts_info['EPS Trend'].to_dict(orient="dict"),
                         'EPS Revisions'     : analysts_info['EPS Revisions'].to_dict(orient="dict"),
                         'Growth Estimates'  : analysts_info['Growth Estimates'].to_dict(orient="dict")}

        self.update(symbol, analysts_info, 'Stocks', 'Analyst_Info')
     
    
    def update_yearly_balance_sheet(self, symbol):
        
        yearly_balance_sheet = si.get_balance_sheet(symbol).to_dict(orient="dict")
        self.update(symbol, yearly_balance_sheet, 'Stocks', 'Yearly_Balance_Sheet')
        
        
    def update_cashflow(self, symbol):
        cashflow = si.get_cash_flow(symbol).to_dict(orient="dict")
        self.update(symbol, cashflow, 'Stocks', 'Cashflow')
        
        
    def update_quote_table(self, symbol):
        quote_table = si.get_quote_table(symbol)
        self.update(symbol, quote_table, 'Stocks', 'Quote_Table')
        
        
    def update_stats(self, symbol):
        stats = si.get_stats(symbol).to_dict(orient="dict")
        self.update(symbol, stats, 'Stocks', 'Stats')
        
        
    def update_stats_valuation(self, symbol):
        stats_valuation = si.get_stats_valuation(symbol).to_dict(orient="dict")
        self.update(symbol, stats_valuation, 'Stocks', 'Stats_Valuation')
        
        
    def update_income_statement(self, symbol):
        income_statement = si.get_income_statement(symbol).to_dict(orient="dict")
        self.update(symbol, income_statement, 'Stocks', 'Income_Statement')
        
        
    def update_holders(self, symbol):
        holders = si.get_holders(symbol)
        
        for key_value_ in holders.keys():
            if type(holders[key_value_]) == dict:
                pass
            else:
                holders[key_value_] = holders[key_value_].to_dict(orient='dict')
        

        self.update(symbol, holders, 'Stocks', 'Holders')         

        
    """ Market Database Update """
    
    def update_day_gainers(self):
        self.update(symbol, data, 'Market', 'Day_Gainers') 
        
        
    def update_day_losers(self):
        self.update(symbol, data, 'Market', 'Day_Losers') 
        
        
    def update_top_crypto(self):
        self.update(symbol, data, 'Market', 'Top_Crypto') 
        
        
    def update_most_active(self):
        self.update(symbol, data, 'Market', 'Most_Active') 
        
        
    """ 
    ************
    POST METHODS
    ************
    """
    
    def post(self, key, value, database, collection):
        
        # connect to MongoDB
        client_connect = "mongodb+srv://wesley:{}@stock-analytics.vmxv5.mongodb.net/{}?retryWrites=true&w=majority".format(self.s.decrypt(self._admin), collection)
        cluster = MongoClient(client_connect)
        
        # Convert to JSON
        if isinstance(value, dict):
            data = json.dumps(value)
        else:
            data = value
        
        # set database and collection
        db = cluster[database]
        collection = db[collection]

        # insert one post to database
        post = {"_id" : key, "data" : data}
        collection.insert_one(post)
        
       
    # MARKET
    def post_market(self):
        
        root = {}
        root["market"] = {}

        """ Market Node """
        
        day_gainers = si.get_day_gainers().to_dict(orient="dict")
        day_losers = si.get_day_losers().to_dict(orient="dict")
        top_crypto = si.get_top_crypto().to_dict(orient="dict")
        most_active = si.get_day_most_active().to_dict(orient="dict")

        new_node = {"Day_Gainers" : day_gainers,
                        "Day_Losers"  : day_losers,
                        "Top_Crypto"  : top_crypto,
                        "Most_Active" : most_active}

        for node_key in new_node.keys():
            now = str(datetime.date(datetime.now()))
            key_var = now
            self.post(key_var, new_node[node_key], "Market", node_key)
            
            time.sleep(.5)
        
        print('Sucess\n')           