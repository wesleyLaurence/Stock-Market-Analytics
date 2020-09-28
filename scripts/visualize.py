"""

    Visualize
    
    This class generates company and stock market visualizations using matplotlib.
    
"""

from .company import Company
from .market import Market
from .security import Security
from pymongo import MongoClient
import pymongo
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns
import time
from datetime import datetime


class Visualize:
    
    def __init__(self, _admin, watch_list=[]):
  
        # user watch list
        self.watch_list = watch_list
        
        # custom classes
        self.company = Company(_admin)
        self.market = Market(_admin)
    
    def live_data(self, symbol, time_filter=0):
        
        """ Visualize stock prices in real time """
        
        # create plot figure and axis
        fig1 = plt.figure(figsize=(12,5))
        ax1 = fig1.add_subplot(111)

        # Main loop
        while True:
            
            # get most recent stock price data from MongoDB
            live_prices_data = self.company.live_prices(symbol)
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
            ax1.set_xticks(np.arange(len(x_axis_labels)))
            ax1.set_xticklabels(x_axis_labels)
            ax1.cla()
            ax1.plot_date(x, y, color='springgreen', linestyle='solid', marker='None')
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
        
        fig2, axs = plt.subplots(len(self.watch_list),figsize=(8,5))
        fig2.tight_layout(pad=3.0)
        

        # Main loop
        while True:
            
            i = 0
            for symbol in self.watch_list:
                
                # get most recent stock price data from MongoDB
                live_prices_data = self.company.live_prices(symbol)
                keys = list(live_prices_data.keys())[1:][time_filter:]
                data = list(live_prices_data.values())[1:][time_filter:]
                
                num_elements = len(data)
                halfway = int(num_elements/2)
   
                X = np.arange(num_elements)
                x_tick_pos = [0, halfway, num_elements-1] 
        
                x_tick_labels = []
                for tickpos in x_tick_pos:
                    xticklabel = keys[tickpos]
                    xticklabel = xticklabel.replace('_','.')
                    xticklabel = pd.to_datetime(xticklabel)
                    
                    # AM / PM
                    time_am = True
                    if xticklabel.hour >= 12:
                        time_am = False
                    
                    # convert military to normal time
                    if xticklabel.hour > 12:
                        hour_value = xticklabel.hour - 12
                    else:
                        hour_value = xticklabel.hour
                
                    if time_am:
                        am_pm = 'AM'
                    else:
                        am_pm = 'PM'

                    # add 0 to time (ie 9:03)
                    minute_val = str(xticklabel.minute)
                    if len(minute_val) == 1:
                        minute_val = "0"+ minute_val

                    # append new x_axis time labels
                    
                    str_value = str(hour_value) + ":" + minute_val + am_pm    
                    x_tick_labels.append(str_value)
                    
                
                """
                for item in keys:

                    # convert string to datetime
                    item = item.replace('_','.')
                    item = 
                    

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
                    x_axis_labels_str.append(str_value)"""

                # data for plot
                x = X
                y = data
                
                # generate plot
                axs[i].cla()
                axs[i].set_facecolor('whitesmoke')
                axs[i].plot(x, y, color='springgreen', linestyle='solid', marker='None')
                axs[i].set_title(symbol.upper())
                
                axs[0].xaxis.set_visible(False)
                axs[1].xaxis.set_visible(False)
                axs[1].set_ylabel("Share Price ($)")
                
                date_today = str(datetime.date(datetime.now()))
                axs[2].set_xlabel(date_today)

                
                if i == 2:
                    
                    axs[2].set_xticks(x_tick_pos)
                    axs[2].set_xticklabels(x_tick_labels)
                
                fig2.canvas.draw() 
                                
                i += 1
                
                # wait
                time.sleep(1)
                

    def stock_history(self, symbol, zoom_level='1 year'):

        zoom_dict = { '1 month' : 22,
                      '3 month' : 65,
                      '1 year'  : 260,
                      '5 year'  : 1304 }

        stock_historic = self.company.historic(symbol, data_type='df')
        close_prices = stock_historic['close'].dropna()
        close_prices = close_prices[-zoom_dict[zoom_level]:]

        X_labels = list(close_prices.index)
        X_values = list(np.arange(len(X_labels)))
        Y = list(close_prices)

        # Create just a figure and only one subplot
        fig, ax = plt.subplots(figsize=(10,5))

        # X axis
        quarter_len = int(len(X_labels)/4)
        xticklabels = [0, quarter_len, quarter_len*2, quarter_len*3, quarter_len*4-1]
        xlabels_ = []

        if zoom_level == '5 year':
            for index_label in xticklabels:
                value = int(X_labels[index_label].split('-')[0])
                xlabels_.append(value)
                
            ax.set_xlabel('Year')

        elif zoom_level == '1 year' or zoom_level == '3 month':
            for index_label in xticklabels:
                year = int(X_labels[index_label].split('-')[0])
                month = int(X_labels[index_label].split('-')[1])
                label = str(month) + '/' + str(year)[2:]
                xlabels_.append(label)
                
            ax.set_xlabel('Month')
      
        ax.set_facecolor('whitesmoke')
        ax.set_xticks(xticklabels)
        ax.set_xticklabels(xlabels_)

        # plot
        ax.plot(X_values, Y, color='springgreen')

        # set
        ax.set_title(symbol.upper())
        ax.set_ylabel('Share Price $')
        
        
    def plot_income_statement(self, symbol, metric):
        """
        METRICS
        
        Total Revenue, 
        Cost of Revenue, 
        Gross Profit, 
        Operating Expense,
        Operating Income, 
        Net Non Operating Interest Income Expense,
        Other Income Expense, 
        Pretax Income, 
        Tax Provision,
        Net Income Common Stockholders,
        Diluted NI Available to Com Stockholders, 
        Basic EPS, 
        Diluted EPS,
        Basic Average Shares, 
        Diluted Average Shares,
        Total Operating Income as Reported, 
        Total Expenses,
        Net Income from Continuing & Discontinued Operation,
        Normalized Income, 
        Interest Income, 
        Interest Expense,
        Net Interest Income, 
        Reconciled Cost of Revenue,
        Reconciled Depreciation,
        Net Income from Continuing Operation Net Minority Interest,
        Total Unusual Items Excluding Goodwill, 
        Total Unusual Items,
        Normalized EBITDA, 
        Tax Rate for Calcs,
        Tax Effect of Unusual Items
        
        """
        
        # get data
        income_statement = self.company.income_statement(symbol, 'df')

        # transpose
        income_statement = income_statement.T

        # set header 
        income_statement.columns = income_statement.iloc[0]
        income_statement.drop(income_statement.index[0], inplace=True)

        primary_table = income_statement[metric][1:]

        # create X labels
        X_labs = []
        for date_str in list(primary_table.index):
            year = int(date_str.split('/')[-1])
            X_labs.append(year)

        # create numerical X values
        X_vals = np.arange(len(X_labs))

        # convert Y values to integer
        Y = [ int(value)*1000 for value in list(primary_table) ]

        # reverse X and Y to make graph chronological from left to right
        X_labs.reverse()
        Y.reverse()

        fig, ax = plt.subplots(figsize=(10,5))

        ax.plot(X_vals, Y, color='springgreen')

        # plot settings
        ax.set_xticks(X_vals)
        ax.set_xticklabels(X_labs)

        title = symbol.upper() + ' ' + metric
        ax.set_title(title)
        ax.set_ylabel(metric+' $')
        ax.set_xlabel('Year')
        ax.set_facecolor('whitesmoke')