""" 
Stock Market Analytics 

- Data Model for Company & Stock data
- Extract Data From:
      - Yahoo_Finance
      - Wikipedia 
      - Twitter
- Load into MongoDB Atlas cloud database
- Visualize stock prices in real time


FEATURES IN DEVELOPMENT:
- Twitter sentiment analysis
- Power BI & Tableau dashboards
- Flask REST API


Author: Wesley Laurence
Date: 9/17/2020

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

class Stock_Model:
    
    """ 
    Stock_Model helps you:
    - extract company info from outside APIs
    - perform real time data visualization of stock prices.
    - interact with the MongoDB database (Get, Set, Update)
    
    """
    
    def __init__(self, watch_list=[]):
        
        # mongo db atlas password
        self.password = getpass.getpass('Password: ')
        
        # user selected stocks
        self.watch_list = watch_list
        
        # ticker--> company data
        ticker_df = pd.read_csv("stock symbols_companies.csv", encoding="latin1")
        ticker_list = list(ticker_df['CompanyTicker'])
        ticker_companies = list(ticker_df['CompanyName'])
        self.company_tickers = dict(zip(ticker_list,ticker_companies))
        
        # add watch list items to mongodb database
        for stock_symbol in watch_list:
            
            # if stock symbol is already in database, pass
            if stock_symbol in list(self.company_tickers.keys()):
                pass
            
            # add new stock to database
            else:
                self.new_stock_entry(stock_symbol)
            
    
    def new_stock_entry(self, stock_symbol):
        
        """ Add new stock symbol and data to MongoDB database """
        
        # Initialize new stock
        for collection_title in ['Wiki','Live_Prices','Company_Info','Twitter']:
            database_title = 'Stocks'

            client_connect = "mongodb+srv://wesley:{}@stock-analytics.vmxv5.mongodb.net/{}?retryWrites=true&w=majority".format(self.password, collection_title)
            cluster = MongoClient(client_connect)
            db = cluster[database_title]
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
    
    
    def watch_list_update(self):
        
        """ Loop for recording live stock prices in real time and storing that data in MongoDB database """
        
        current_time =  datetime.now().time()
        current_hour = current_time.hour
        current_minute = current_time.minute
        
        # while stock market is open
        while (current_hour >= 9) and current_hour < 16:
            
            new_time = datetime.now().time()
            current_hour = new_time.hour
            current_minute = new_time.minute
            
            for symbol in self.watch_list:
                self.update_live_price(symbol)
                
    
    def data_capture(self):
        
        """ Main database update loop """
        
        now =  datetime.now()
        current_hour = now.hour
        current_minute = now.minute

        # while stock market is open
        while (current_hour >= 9) and current_hour < 16:
            self.watch_list_update()
            
            now =  datetime.now()
            current_hour = now.hour
            current_minute = now.minute

        # stock market closes
        self.post_market()

        # update company info and wiki info every 7 days
        if int(now.day) % 7 == 0:
            self.update_wiki(stock_symbol)
            self.update_company_info(stock_symbol)
        
    
    def live_data(self, symbol, time_filter=0):
        
        """ Visualize stock prices in real time """
        
        # create plot figure and axis
        fig1 = plt.figure(figsize=(12,5))
        ax1 = fig.add_subplot(111)

        # Main loop
        while True:
            
            # get most recent stock price data from MongoDB
            live_prices_data = self.get_live_price(symbol)
            data = list(live_prices_data.values())[1:][time_filter:]
            
            # format x axis labels for plot
            x_axis_labels = [] 
            x_axis_labels_real = []
            for item in list(live_prices_data.keys())[1:][time_filter:]:
                
                # convert string to datetime
                item = item.replace('_','.')
                item = pd.to_datetime(item)
                
                x_axis_labels_real.append(item)
                
                # AM / PM
                time_am = True
                if item.hour >= 12:
                    time_am = False
                if time_am:
                    am_pm = 'AM'
                else:
                    am_pm = 'PM'
                
                # add 0 to time (ie 9:03)
                minute_val = str(item.minute)
                if len(minute_val) == 1:
                    minute_val = "0"+ minute_val
                
                # append new x_axis time labels
                str_value = str(item.hour) + ":" + minute_val + am_pm    
                x_axis_labels.append(str_value)
            
            # data for plot
            x = x_axis_labels_real
            y = data
            
            # generate plot
            ax1.set_xticklabels(x_axis_labels)
            ax1.cla()
            ax1.plot_date(x, y, color='mediumblue', linestyle='solid', marker='None')
            ax1.set_title(symbol.upper())
            ax1.set_xlabel('Time')
            ax1.set_ylabel("Share Price ($)")
            fig1.canvas.draw() 
            
            # wait
            time.sleep(1)
              
            
    def live_dashboard(self, time_filter=0):

        """ Visualize all watch list stock prices in real time """
        
        """
        # create plot figure and axis
        fig = plt.figure(figsize=(12,5))
        ax = fig.add_subplot(111)
        """
        
        fig2, axs = plt.subplots(len(self.watch_list),figsize=(6,5))
        fig2.tight_layout(pad=3.0)
        

        # Main loop
        while True:
            
            i = 0
            for symbol in self.watch_list:
                
                # get most recent stock price data from MongoDB
                live_prices_data = self.get_live_price(symbol)
                data = list(live_prices_data.values())[1:][time_filter:]

                # format x axis labels for plot
                x_axis_labels = [] 
                x_axis_labels_real = []
                for item in list(live_prices_data.keys())[1:][time_filter:]:

                    # convert string to datetime
                    item = item.replace('_','.')
                    item = pd.to_datetime(item)

                    x_axis_labels_real.append(item)

                    # AM / PM
                    time_am = True
                    if item.hour >= 12:
                        time_am = False
                    if time_am:
                        am_pm = 'AM'
                    else:
                        am_pm = 'PM'

                    # add 0 to time (ie 9:03)
                    minute_val = str(item.minute)
                    if len(minute_val) == 1:
                        minute_val = "0"+ minute_val

                    # append new x_axis time labels
                    str_value = str(item.hour) + ":" + minute_val + am_pm    
                    x_axis_labels.append(str_value)

                # data for plot
                x = x_axis_labels_real
                y = data
                
                # generate plot
                axs[i].cla()
                axs[i].set_facecolor('whitesmoke')
                axs[i].plot_date(x, y, color='mediumblue', linestyle='solid', marker='None')
                axs[i].set_title(symbol.upper())
                
                axs[0].xaxis.set_visible(False)
                axs[1].xaxis.set_visible(False)
                axs[1].set_ylabel("Share Price ($)")
                axs[2].set_xlabel('Time')
                axs[2].set_xticklabels(x_axis_labels)
                
                fig2.canvas.draw() 
                                
                i += 1
                
                # wait
                time.sleep(1)    
        

    """
    ********************
    DATA EXTRACT METHODS
    ********************
    """
    
    def extract_wiki_data(self, symbol):
        
        """ Pull company data from the Wikipedia API and store it in dictionary """
        
        key_word = self.company_tickers[symbol]
        page = wikipedia.page(key_word)
        summary = wikipedia.summary(key_word)
        title = page.title
        url = page.url
        content = page.content
        links = page.links
        data = {"title" : title,
                "summary" : summary,
                "url" : url,
                "content" : content,
                "links" : links}
        return data
    
    
    def extract_company(self, symbol):
        """ 
        
        Pull company data from the Yahoo Finance API and store it in dictionary
        
        """

        # Company Info Node
        analysts_info = si.get_analysts_info(symbol)
        analysts_info = {'Earnings Estimate' : analysts_info['Earnings Estimate'].to_dict(orient="dict"),
                         'Revenue Estimate'  : analysts_info['Revenue Estimate'].to_dict(orient="dict"),
                         'Earnings History'  : analysts_info['Earnings History'].to_dict(orient="dict"),
                         'EPS Trend'         : analysts_info['EPS Trend'].to_dict(orient="dict"),
                         'EPS Revisions'     : analysts_info['EPS Revisions'].to_dict(orient="dict"),
                         'Growth Estimates'  : analysts_info['Growth Estimates'].to_dict(orient="dict")}

        yearly_balance_sheet = si.get_balance_sheet(symbol).to_dict(orient="dict")
        cashflow = si.get_cash_flow(symbol).to_dict(orient="dict")
        
        historic = si.get_data(symbol)
        historic.index = historic.index.astype(str)
        historic = historic.to_dict(orient="dict")
        
        quote_table = si.get_quote_table(symbol)
        stats = si.get_stats(symbol).to_dict(orient="dict")
        stats_valuation = si.get_stats_valuation(symbol).to_dict(orient="dict")
        holders = si.get_holders(symbol)
        income_statement = si.get_income_statement(symbol).to_dict(orient="dict")
        info_node = {'analysts_info'        : analysts_info,
                     'yearly_balance_sheet' : yearly_balance_sheet,
                     'cashflow'             : cashflow,
                     'historic'             : historic,
                     'quote_table'          : quote_table,
                     'stats'                : stats,
                     'stats_valuation'      : stats_valuation,
                     'holders'              : holders,
                     'income_statement'     : income_statement}
        
        
        for key_value_ in info_node['holders'].keys():
            if type(info_node['holders'][key_value_]) == dict:
                pass
            else:
                info_node['holders'][key_value_] = info_node['holders'][key_value_].to_dict(orient='dict')
        
        return info_node  
    

    def extract_twitter(self):
        
        """ 
        (In development)
        
        Connect to Twitter API and extract tweets based on keyword search for stock ticker or company name
        
        """

        tweet = {"tweet_id" : 0,
                        "content" : "I love stackoverflow.com",
                        "author" : "wesley_laurence",
                        "event_datetime" : str(datetime.now()),
                        "hashtags" : ["Rad"],
                        "links" : ["www.stackoverflow.com"] }
        
        return tweet

    
    
    """ 
    **************
    UPDATE METHODS 
    **************
    """    
        
    def update(self, key, value, database, collection_title):
        
        # connect to MongoDB
        client_connect = "mongodb+srv://wesley:{}@stock-analytics.vmxv5.mongodb.net/{}?retryWrites=true&w=majority".format(self.password, collection_title)
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
        
    
    # WIKI
    def update_wiki(self, symbol):
        data = self.extract_wiki_data(symbol)
        self.update(symbol, data, 'Stocks', 'Wiki')
            
    # COMPANY INFO
    def update_company_info(self, symbol):
        data = self.extract_company(symbol)
        self.update(symbol, data, 'Stocks', 'Company_Info')
                    
    
    def update_live_price(self, symbol):
        
        # info
        database_title = 'Stocks'
        collection_title = 'Live_Prices'
        
        # connect to MongoDB
        client_connect = "mongodb+srv://wesley:{}@stock-analytics.vmxv5.mongodb.net/{}?retryWrites=true&w=majority".format(self.password, collection_title)
        cluster = MongoClient(client_connect)
        db = cluster[database_title]
        collection = db[collection_title]
        
        now = str(datetime.now()).replace('.','_')
        live_price = si.get_live_price(symbol)

        # update database
        collection.update_one({"_id" : symbol}, {"$set":{now : live_price}})
        
        
    
    
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
    
    
    def get_live_price(self, symbol):
        return self.get(symbol, 'Stocks','Live_Prices')
    
    
    def get_wiki(self, symbol):
        return self.get(symbol, 'Stocks','Wiki')
    
    
    def get_company_info(self, symbol):
        return self.get(symbol, 'Stocks','Company_Info')
    
    
    def get_historic_prices(self, symbol):

        data = json.loads(self.get_company_info(symbol)['2020-09-16'])

        column_names = list(data['historic'].keys())
        historic_df = pd.DataFrame((data['historic'].values())).T
        historic_df.columns = column_names
        
        return historic_df
    
    
    def get_twitter(self):
        return self.get(symbol, 'Stocks','Twitter')
    
    
    def get_day_gainers(self):
        return self.get(symbol, 'Market','Day_Gainers')
    
    
    def get_day_losers(self):
        return self.get(symbol, 'Market','Day_Losers')
    
    
    def get_top_crypto(self):
        return self.get(symbol, 'Market','Top_Crypto')
    
    
    def get_most_active(self):
        return self.get(symbol, 'Market','Most_Active')
    
    
    
    
    """ 
    ************
    POST METHODS
    ************
    """
    
    def post(self, key, value, database, collection):
        
        # connect to MongoDB
        client_connect = "mongodb+srv://wesley:{}@stock-analytics.vmxv5.mongodb.net/{}?retryWrites=true&w=majority".format(self.password, collection)
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
        
        print("Add market node")
        
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
        
""" For questions about this code, please email wesleylaurencetech@gmail.com """
