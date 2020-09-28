"""

    Wiki
    
    This class provides access to the Wikipedia API to pull company data.
    
"""

import wikipedia
import pandas as pd

class Wiki:
    
    def __init__(self):
        
        # ticker--> company data
        stream = pkg_resources.resource_stream(__name__, 'data/stock_symbols.csv')
        ticker_df = pd.read_csv(stream, encoding='latin-1')
        ticker_list = list(ticker_df['Symbol'])
        ticker_companies = list(ticker_df['CompanyName'])
        self.company_tickers = dict(zip(ticker_list,ticker_companies))
    
    def get_wiki(self, symbol):
        
        """ Get company wikipedia data """ 
        
        company_name = self.company_tickers[symbol]
        page = wikipedia.page(company_name)
        summary = wikipedia.summary(company_name)
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