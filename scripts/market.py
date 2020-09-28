""" 

    Market

    This class is a stock market data model with GET method to access to MongoDB Atlas databases: Company Info and Stocks

"""

from .security import Security
import pymongo
from pymongo import MongoClient
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from datetime import datetime
import time
import pkg_resources

class Market:

    def __init__(self, _admin):
    
        self._admin = _admin
        
        # ticker--> company data
        stream = pkg_resources.resource_stream(__name__, 'data/stock_symbols.csv')
        ticker_df = pd.read_csv(stream, encoding='latin-1')
        ticker_list = list(ticker_df['Symbol'])
        ticker_companies = list(ticker_df['CompanyName'])
        self.company_tickers = dict(zip(ticker_list,ticker_companies))

    
    def data_bundle(self, data, data_type):
        
        # convert json to python dict
        if isinstance(data, str):
            data = json.loads(data)
            
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
        s = Security()
        client_connect = "mongodb+srv://wesley:{}@stock-analytics.vmxv5.mongodb.net/{}?retryWrites=true&w=majority".format(s.decrypt(self._admin), collection)
        cluster = MongoClient(client_connect)
        db = cluster[database]
        collection = db[collection]
        
        # FIND
        results = collection.find_one({"_id" : key})
        
        return results
    
    def day_gainers(self, date, data_type='dict'):
        data = self.get(date, 'Market','Day_Gainers')
        return self.data_bundle(data, data_type)
    
    def day_losers(self, date, data_type='dict'):
        data = self.get(date, 'Market','Day_Losers')
        return self.data_bundle(data, data_type)
    
    def top_crypto(self, date, data_type='dict'):
        data = self.get(date, 'Market','Top_Crypto')
        return self.data_bundle(data, data_type)
    
    def most_active(self, date, data_type='dict'):
        data = self.get(date, 'Market','Most_Active')
        return self.data_bundle(data, data_type)