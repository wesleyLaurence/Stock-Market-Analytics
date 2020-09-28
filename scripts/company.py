""" 

    Company - GET methods, access to MongoDB Atlas databases: Company Info and Stocks

"""
    
# import libraries
from .security import Security
import pymongo
from pymongo import MongoClient
from datetime import datetime
import json
import time
from datetime import datetime
import pandas as pd
import numpy as np
import pkg_resources

class Company:
    """ 
    Pull company and stock data from MongoDB Atlas database. 
    """
    
    def __init__(self, _admin):
        
        self._admin = _admin
    
        # ticker--> company data
        stream = pkg_resources.resource_stream(__name__, 'data/stock_symbols.csv')
        ticker_df = pd.read_csv(stream, encoding='latin-1')
        ticker_list = list(ticker_df['Symbol'])
        ticker_companies = list(ticker_df['CompanyName'])
        self.company_tickers = dict(zip(ticker_list,ticker_companies))

    
    def data_bundle(self, data, data_type):
        """ Convert input data into JSON, Dictionary or DataFrame """
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
        
        
    def get(self, key, database, collection):
        s = Security()
        client_connect = "mongodb+srv://wesley:{}@stock-analytics.vmxv5.mongodb.net/{}?retryWrites=true&w=majority".format(s.decrypt(self._admin), collection)
        cluster = MongoClient(client_connect)
        db = cluster[database]
        collection = db[collection]
        
        # FIND
        results = collection.find_one({"_id" : key})
        
        return results
        
    def historic(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Historic')
        return self.data_bundle(data, data_type) 
    
    def live_prices(self, symbol):
        return self.get(symbol, 'Stocks','Live_Price')
    
    def analyst_info(self ,symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Analyst_Info')
        return self.data_bundle(data, data_type) 
    
    def yearly_balance_sheet(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Yearly_Balance_Sheet')
        return self.data_bundle(data, data_type) 
    
    def cashflow(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Cashflow')
        return self.data_bundle(data, data_type)    
        
    def quote_table(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Quote_Table')
        return self.data_bundle(data, data_type)
    
    def stats(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Stats')
        return self.data_bundle(data, data_type)
    
    def stats_valuation(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Stats_Valuation')
        return self.data_bundle(data, data_type)
    
    def income_statement(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Income_Statement')
        return self.data_bundle(data, data_type)
    
    def holders(self, symbol, data_type='dict'):
        data = self.get(symbol, 'Stocks','Holders')
        return self.data_bundle(data, data_type)
    
    