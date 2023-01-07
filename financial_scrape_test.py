import os
from td_ameritrade_scrape import *
from config import directory

# Directory where your project lives
my_directory = directory
os.chdir(my_directory)

DOW_JONES_DIR = my_directory + "/dow_jones_stocks"
ALL_COMPETITORS_DIR = my_directory + "/all_competitors"

dow_jones_path_Exist = os.path.exists(DOW_JONES_DIR)
all_competitors_path_Exist = os.path.exists(ALL_COMPETITORS_DIR)

if dow_jones_path_Exist == True:
    pass
else:
    os.mkdir(DOW_JONES_DIR)


if all_competitors_path_Exist == True:
    pass
else:
    os.mkdir(ALL_COMPETITORS_DIR)

# Initializes the class and opens the web browser
scraper = td_ameritrade_scrape()

# Type of data we're after from the list of Dow Jones stock ticker we're going to loop through
reports = ['quarterly', 'annual']
dow_jones_list = scraper.dow_jones_symbols()

#**************************** First Loop ****************************#

for ticker in dow_jones_list:
    scraper.set_url(
        f"https://research.tdameritrade.com/grid/public/research/stocks/fundamentals?symbol={ticker}")
    scraper.get_url()

    # Balance Sheet Data
    scraper.switch_to_balance_sheet()
    for report in reports:
        # returns a df
        balance_sheet = scraper.get_data(ticker, "balance-sheet")

    # Income Statement Data
    scraper.switch_to_income_statement()
    for report in reports:
        income_statement = scraper.get_data(ticker, "income-statement")

    # Cash Flow Statement Data
    scraper.switch_to_cash_flow_statement()
    for report in reports:
        cash_flow_statement = scraper.get_data(ticker, "cash-flow")

#**************************** Second Loop ****************************#

for ticker in dow_jones_list:
    scraper.set_url(
        f"https://www.wsj.com/market-data/quotes/{ticker}")
    scraper.get_url()

    # List of competitors per Dow Jones stock
    competitors = scraper.get_competitors(ticker)
    for competitor in competitors:
        try:
            scraper.set_url(
                f"https://research.tdameritrade.com/grid/public/research/stocks/fundamentals?symbol={competitor}")
            scraper.get_url()

            # Competitor Balance Sheet Data
            scraper.switch_to_balance_sheet()
            for report in reports:
                # returns a df
                balance_sheet = scraper.get_competitor_data(
                    ticker, competitor, "balance-sheet")

            # Competitor Income Statement Data
            scraper.switch_to_income_statement()
            for report in reports:
                income_statement = scraper.get_competitor_data(
                    ticker, competitor, "income-statement")

            # Competitor Cash Flow Statement Data
            scraper.switch_to_cash_flow_statement()
            for report in reports:
                cash_flow_statement = scraper.get_competitor_data(
                    ticker, competitor, "cash-flow")
        except NoSuchElementException:
            pass


scraper.close_browser()
