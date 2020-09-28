""" 

    Dashboard
        
        Visual - visualize live stock prices and more
        Market- stock market and crypto trends
        Company - analyze company information and financials
    
"""

from .security import Security
from .company import Company
from .market import Market
from .visualize import Visualize
import getpass

class Dashboard:

    def __init__(self, watch_list=[]):
        
        # encrypted password
        s = Security()
        _admin = s.encrypt()
        
        # user watch list
        self.watch_list = watch_list
        
        # custom classes
        self.company = Company(_admin)
        self.market = Market(_admin)
        self.visual = Visualize(_admin, watch_list)