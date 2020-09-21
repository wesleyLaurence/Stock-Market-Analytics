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
from data_model import Data_Model

class Dashboard:
    
    def __init__(self, watch_list=[]):
        
        self.watch_list = watch_list
        self.model = Data_Model(self.watch_list)
    
    def live_data(self, symbol, time_filter=0):
        
        """ Visualize stock prices in real time """
        
        # create plot figure and axis
        fig1 = plt.figure(figsize=(12,5))
        ax1 = fig1.add_subplot(111)

        # Main loop
        while True:
            
            # get most recent stock price data from MongoDB
            live_prices_data = self.model.get_live_price(symbol)
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
        
        fig2, axs = plt.subplots(len(self.watch_list),figsize=(8,5))
        fig2.tight_layout(pad=2.0)
        

        # Main loop
        while True:
            
            i = 0
            for symbol in self.watch_list:
                
                # get most recent stock price data from MongoDB
                live_prices_data = self.model.get_live_price(symbol)
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
                
                if i == 2:
                    axs[2].set_xticklabels(x_axis_labels)
                
                fig2.canvas.draw() 
                                
                i += 1
                
                # wait
                time.sleep(1)
