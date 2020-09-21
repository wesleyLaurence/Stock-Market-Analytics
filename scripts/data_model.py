""" 

Data_Model - GET methods, access to MongoDB Atlas databases: Stocks and Market 

"""
    
# import libraries
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
from matplotlib.animation import FuncAnimation

class Data_Model():

    def __init__(self, watch_list=[]):
        
        # mongo db atlas password
        self.password = getpass.getpass('Password: ')
        
        # user selected stocks
        self.watch_list = watch_list
        
        # ticker--> company data
        ticker_df = pd.read_csv("stock_symbols.csv", encoding="latin1")
        ticker_list = list(ticker_df['Symbol'])
        ticker_companies = list(ticker_df['CompanyName'])
        self.company_tickers = dict(zip(ticker_list,ticker_companies))

    
    def data_bundle(self, data, data_type):
        latest_entry = list(data.keys())[-1]
        user_data_json = data[latest_entry]
        user_data_dict = json.loads(user_data_json)
        
        try:
            user_data_df = pd.DataFrame(user_data_dict)
        except:
            keys = list(user_data_dict.keys())
            values = list(user_data_dict.values())
            user_data_df = pd.DataFrame([keys,values]).T
            user_data_df.columns = ['Feature','Value']
            user_data_df.set_index('Feature', inplace=True)
                
        data_stack = {'json' : user_data_json,
                      'dict' : user_data_dict,
                      'df'   : user_data_df}
        
        return data_stack[data_type]
    
    
    """ 
    ***********
    GET METHODS 
    ***********
    """
    
    def get(self, key, database, collection):
        client_connect = "mongodb+srv://wesley:{}@stock-analytics.vmxv5.mongodb.net/{}?retryWrites=true&w=majority".format(self.password, collection)
        cluster = MongoClient(client_connect)
        db = cluster[database]
        collection = db[collection]
        
        # FIND
        results = collection.find_one({"_id" : key})
        
        return results
    
    # Wikipedia
    def get_wiki(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Wiki')
        return self.data_bundle(data, data_type) 
    
    # Twitter
    def get_twitter(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Twitter')
        return self.data_bundle(data, data_type) 
           
    # Yahoo Finance
    def get_historic(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Historic')
        return self.data_bundle(data, data_type) 
    
    def get_live_price(self, symbol):
        return self.get(symbol, 'Stocks','Live_Price')
    
    def get_analyst_info(self ,symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Analyst_Info')
        return self.data_bundle(data, data_type) 
    
    def get_yearly_balance_sheet(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Yearly_Balance_Sheet')
        return self.data_bundle(data, data_type) 
    
    def get_cashflow(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Cashflow')
        return self.data_bundle(data, data_type)    
        
    def get_quote_table(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Quote_Table')
        return self.data_bundle(data, data_type)
    
    def get_stats(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Stats')
        return self.data_bundle(data, data_type)
    
    def get_stats_valuation(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Stats_Valuation')
        return self.data_bundle(data, data_type)
    
    def get_income_statement(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Income_Statement')
        return self.data_bundle(data, data_type)
    
    def get_holders(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Holders')
        return self.data_bundle(data, data_type)
    
    def get_day_gainers(self, data_type='dict'):
        data = self.get(symbol, 'Market','Day_Gainers')
        return self.data_bundle(data, data_type)
    
    def get_day_losers(self, data_type='dict'):
        data = self.get(symbol, 'Market','Day_Losers')
        return self.data_bundle(data, data_type)
    
    def get_top_crypto(self, data_type='dict'):
        data = self.get(symbol, 'Market','Top_Crypto')
        return self.data_bundle(data, data_type)
    
    def get_most_active(self, data_type='dict'):
        data = self.get(symbol, 'Market','Most_Active')
        return self.data_bundle(data, data_type)
        
        
""" For questions about this code, email wesleylaurencetech@gmail.com """