""" 
    
    Unit tests to ensure system components are working properly.

    Test Categories:
        - Company
        - Market
        - Visual
        
"""

# intialize dashboard and connect to database
from dashboard import Dashboard
d = Dashboard(['msft'])

# keep track of failed components
failed = []


"""

    Company Tests
    
"""

print('\nRunning unit tests...\n')

for data_type in ['json','dict','df']:
    for symbol in ['msft']:
        
        # analyst_info
        try:
            d.company.analyst_info(symbol, data_type)
        
        except:
            error_details = "FAILED: {} - {} - analyst_info".format(symbol, data_type)
            failed.append(error_details)
            print(error_details)

        
        # cashflow
        try:
            d.company.cashflow(symbol, data_type)
        
        except:
            error_details = "FAILED: {} - {} - cashflow".format(symbol, data_type)
            failed.append(error_details)
            print(error_details)
            
            
        # historic
        try:
            d.company.historic(symbol, data_type)
        
        except:
            error_details = "FAILED: {} - {} - historic".format(symbol, data_type)
            failed.append(error_details)
            print(error_details)
            
            
        # holders
        try:
            d.company.holders(symbol, data_type)
        
        except:
            error_details = "FAILED: {} - {} - holders".format(symbol, data_type)
            failed.append(error_details)
            print(error_details)
            
            
        # income_statement
        try:
            d.company.income_statement(symbol, data_type)
        
        except:
            error_details = "FAILED: {} - {} - income_statement".format(symbol, data_type)
            failed.append(error_details)
            print(error_details)
            
            
        # live_prices
        try:
            d.company.live_prices(symbol)
        
        except:
            error_details = "FAILED: {} - {} - live_prices".format(symbol)
            failed.append(error_details)
            print(error_details)
            
            
        # quote_table
        try:
            d.company.quote_table(symbol, data_type)
        
        except:
            error_details = "FAILED: {} - {} - quote_table".format(symbol, data_type)
            failed.append(error_details)
            print(error_details)
            
            
        # stats
        try:
            d.company.stats(symbol, data_type)
        
        except:
            error_details = "FAILED: {} - {} - stats".format(symbol, data_type)
            failed.append(error_details)
            print(error_details)
            
            
        # stats_valuation
        try:
            d.company.stats_valuation(symbol, data_type)
        
        except:
            error_details = "FAILED: {} - {} - stats_valuation".format(symbol, data_type)
            failed.append(error_details)
            print(error_details)
            
            
        # yearly_balance_sheet
        try:
            d.company.yearly_balance_sheet(symbol, data_type)
        
        except:
            error_details = "FAILED: {} - {} - yearly_balance_sheet".format(symbol, data_type)
            failed.append(error_details)
            print(error_details)
      
    
failures_so_far = len(failed)          
if failures_so_far == 0:
    print("Passed all company tests")           

    
"""

    Market Tests
    
"""

for data_type in ['json','dict','df']:
    for date in ['2020-09-16']:
        
        # day_gainers
        try:
            d.market.day_gainers(date, data_type)
        
        except:
            error_details = "FAILED: {} - {} - day_gainers".format(date, data_type)
            failed.append(error_details)
            print(error_details)

        
        # day_losers
        try:
            d.market.day_losers(date, data_type)
        
        except:
            error_details = "FAILED: {} - {} - day_losers".format(date, data_type)
            failed.append(error_details)
            print(error_details)
            
            
        # top_crypto
        try:
            d.market.top_crypto(date, data_type)
        
        except:
            error_details = "FAILED: {} - {} - top_crypto".format(date, data_type)
            failed.append(error_details)
            print(error_details)
            
            
        # most_active
        try:
            d.market.most_active(date, data_type)
        
        except:
            error_details = "FAILED: {} - {} - most_active".format(date, data_type)
            failed.append(error_details)
            print(error_details)
                             
if len(failed) == failures_so_far:
    print("Passed all market tests") 
    
failures_so_far = len(failed)



""" 

    Visual Tests

"""

try:
    for time_range in ['1 month','3 month','1 year','5 year']:
        d.visual.stock_history('msft', time_range)
except:
    error_details = "FAILED: {} - {} - visual.stock_history()".format(time_range, 'msft')
    failed.append(error_details)
    print(error_details)
    
    
for metric in [ 'Total Revenue', 
                'Cost of Revenue', 
                'Gross Profit', 
                'Operating Expense',
                'Operating Income', 
                'Net Non Operating Interest Income Expense',
                'Other Income Expense', 
                'Pretax Income', 
                'Tax Provision',
                'Net Income Common Stockholders',
                'Diluted NI Available to Com Stockholders', 
                'Basic EPS', 
                'Diluted EPS',
                ' Basic Average Shares', 
                'Diluted Average Shares',
                'Total Operating Income as Reported', 
                'Total Expenses', 
                'Net Income from Continuing & Discontinued Operation',
                'Normalized Income', 
                'Interest Income', 
                'Interest Expense',
                'Net Interest Income', 
                'Reconciled Cost of Revenue',
                'Reconciled Depreciation',
                'Net Income from Continuing Operation Net Minority Interest',
                'Total Unusual Items Excluding Goodwill', 
                'Total Unusual Items',
                'Normalized EBITDA', 
                'Tax Rate for Calcs',
                'Tax Effect of Unusual Items' ]:

    try:
        d.visual.plot_income_statement('msft', metric)
    except:
        error_details = "FAILED: {} - {} - visual.plot_income_statement()".format(metric, 'msft')
        failed.append(error_details)
        print(error_details)    
    

if len(failed) == failures_so_far:
    print("Passed all visual tests")         
                
        
if len(failed) == 0:
    print("\nAll test passed successfully!")
