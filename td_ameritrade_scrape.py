# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from pprint import pprint
from os import path
import os
from selenium.common.exceptions import NoSuchElementException
import shutil
from config import *

# Create class


class td_ameritrade_scrape:
    """
    A class used to get data from TD Ameritrade.

    ...

    Attributes
    ----------
    driver : WebDriver
            Creates a new instance of the chrome driver. Starts the service and then creates new instance of chrome driver

    Methods
    -------
    dow_jones_symbols():
        Returns a list of the 30 stocks in the Dow Jones.

    set_url(url):
        Sets the url .

    get_url(url):
        Returns the current webpage with the associated url.

    get_ticker(ticker):
        Returns the current stock ticker.

    switch_to_balance_sheet():
        Changes webpage to the stocks balance sheet.

    switch_to_income_statement():
        Changes webpage to the stocks income statement.

    switch_to_cash_flow_statement():
        Changes webpage to the stocks cash flow statement.

    quarter_data(competitor=""):
        Scrapes the quarterly data of stocks on TD Ameritrade because each stock has same format.

    annual_data(competitor=""):
        Scrapes the annual data of stocks on TD Ameritrade because each stock has same format.

    get_data(ticker, financial_statement):
        Makes use navigating the HTML radio buttons between annual and quarterly data on each stock reports webpage.
        After identifying which page the driver is currently on this method makes use of the quarter_data() 
        and annual_data() methods to create a new directory with a csv of the page's data.

    get_competitors(ticker):
        Returns the competitors associated with the current company.

    get_competitor_data(ticker, competitor, financial_statement):
        Makes use navigating the HTML radio buttons between annual and quarterly data on each competitor reports webpage.
        After identifying which page the driver is currently on this method makes use of the quarter_data() 
        and annual_data() methods to create a new directory with a csv of the page's data.

    close_driver():
        Closes the driver.
    """
    # print(td_ameritrade_scrape.td_ameritrade_scrape.__doc__) ### this works to view the docstring

    def __init__(self,
                 service=ChromeService(
                     executable_path=ChromeDriverManager().install())
                 ):
        """
        Constructs the webdriver to be activated.

        Parameters
        ----------
        service : class

                  Creates a new instance of Service.

                  :Args:

                    executable_path : str
                        Path to the ChromeDriver
                    port : int, optional
                        Port the service is running on 
                    service_args : list, optional
                        List of args to pass to the chromedriver service
                    log_path : str, optional
                        Path for the chromedriver service to log to
        """
        self.driver = webdriver.Chrome(service=service)

    def dow_jones_symbols(self):
        """
        Returns a list of the 30 stocks in the Dow Jones.

        Returns
        -------
        list
            a list of strings that are stock symbols which make up the Dow Jones Industrial Average
        """
        dow_jones_url = 'https://stockmarketmba.com/stocksinthedjia.php'
        # dow_jones_url = 'https://www.slickcharts.com/dowjones' // another site to get the stock tickers
        dow_jones = pd.read_html(dow_jones_url)
        dow_jones = dow_jones[0]
        dow_jones = dow_jones.sort_values(by=['Symbol'])
        dow_jones = dow_jones.rename(columns={'GICS Sector': 'Sector'})
        dow_jones = dow_jones[['Symbol', 'Sector']].dropna()
        dow_jones_list = []
        for i in dow_jones['Symbol']:
            dow_jones_list.append(i)

        return dow_jones_list

    def set_url(self, url):
        """
        Sets the param url.

        Parameters
        ----------
        url : str
            The url of the website
        """
        self.url = url

    def get_url(self):
        """
        Returns the current webpage with the associated url.

        Returns
        -------
        driver : webdriver
                Loads a web page in the current browser session
        """
        return self.driver.get(self.url)

    def get_ticker(self, ticker):
        """
        Returns the current stock ticker.

        Parameters
        ----------
        ticker : str
                The current stock ticker being processed

        Returns
        -------
        str
            The current stock ticker
        """
        self.ticker = ticker
        return self.ticker

    def switch_to_balance_sheet(self):
        """
        Changes webpage to the stocks balance sheet.

        Returns
        -------
        driver : WebDriver
                webpage to the stocks balance sheet
        """
        time.sleep(7)
        return self.driver.find_element(By.XPATH, "//a[@href='https://research.tdameritrade.com/grid/public/research/stocks/fundamentals/statement/balancesheet']").send_keys(Keys.ENTER)

    def switch_to_income_statement(self):
        """
        Changes webpage to the stocks income statement.

        Returns
        -------
        driver : WebDriver
                webpage to the stocks income statement
        """
        time.sleep(7)
        return self.driver.find_element(By.XPATH, "//a[@href='https://research.tdameritrade.com/grid/public/research/stocks/fundamentals/statement/incomestatement']").send_keys(Keys.ENTER)

    def switch_to_cash_flow_statement(self):
        """
        Changes webpage to the stocks cash flow statement.

        Returns
        -------
        driver : WebDriver
                webpage to the stocks cash flow statement
        """
        time.sleep(7)
        return self.driver.find_element(By.XPATH, "//a[@href='https://research.tdameritrade.com/grid/public/research/stocks/fundamentals/statement/cashflow']").send_keys(Keys.ENTER)

    def quarter_data(self, competitor=""):
        """
        Scrapes the quarterly data of stocks on TD Ameritrade because each stock has same format.

        Parameters
        ----------
        competitor : str, optional
            the current competitor
        Returns
        -------
        df: (DataFrame)
            Dataframe of the quarterly data 

        """
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        my_labels = []
        labels = soup.find_all('label')
        for label in labels[-3:]:
            my_labels.append(label.text)

        my_theads = []
        theads = soup.find_all('thead')

        # Gets all the dates used as column headers that are used for reporting when data is released
        for thead in theads:
            my_text = thead.tr.text
            first_th = my_text.replace(my_text, my_text[:7])
            second_th = my_text.replace(my_text, my_text[15:22])
            third_th = my_text.replace(my_text, my_text[30:37])
            fourth_th = my_text.replace(my_text, my_text[45:52])
        #     fifth_th = my_text.replace(my_text, my_text[60:67])
            my_theads.append(first_th)
            my_theads.append(second_th)
            my_theads.append(third_th)
            my_theads.append(fourth_th)
        #     my_theads.append(fifth_th)

        my_theads = my_theads[0:4]

        # print(my_theads)

        data = []
        first_column = []
        tables = soup.find_all('table', attrs={'class': 'section-content'})
        for table in tables:
            table_body = table.find('tbody')

            rows = table_body.find_all('tr')
            for row in rows:
                first_col = row.find_all('th')
                cols = row.find_all('td')
                first_cols = [ele.text.strip() for ele in first_col]
                cols = [ele.text.strip() for ele in cols]

                first_column.append(first_cols)
                data.append(cols)

        first_column = [item for sublist in first_column for item in sublist]

        # Create the pandas DataFrame
        df = pd.DataFrame(data, columns=my_theads)
        first_column = pd.Series(first_column)
        # print dataframe.
        df['items'] = first_column
        df = df.set_index('items')
        df = df.reset_index()

        ticker_name = []
        length = len(df.index)
        for i in range(length):
            if competitor != "":
                ticker_name.append(str(competitor))
            else:
                ticker_name.append(str(self.ticker))
        df['ticker'] = ticker_name
        return df

    def annual_data(self, competitor=""):
        """
        Scrapes the annual data of stocks on TD Ameritrade because each stock has same format.

        Parameters
        ----------
        competitor : str, optional
            the current competitor

        Returns
        -------
        df: (DataFrame)
            Dataframe of the annual data 

        """
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        my_labels = []
        labels = soup.find_all('label')
        for label in labels[-3:]:
            my_labels.append(label.text)

        my_theads = []
        theads = soup.find_all('thead')
        for thead in theads:
            my_text = thead.tr.text
            if len(my_text) == 48:
                first_th = my_text.replace(my_text, my_text[:4])
                second_th = my_text.replace(my_text, my_text[12:16])
                third_th = my_text.replace(my_text, my_text[24:28])
                fourth_th = my_text.replace(my_text, my_text[36:40])
                my_theads.append(first_th)
                my_theads.append(second_th)
                my_theads.append(third_th)
                my_theads.append(fourth_th)
                my_theads = my_theads[0:4]
            else:
                first_th = my_text.replace(my_text, my_text[:4])
                second_th = my_text.replace(my_text, my_text[12:16])
                third_th = my_text.replace(my_text, my_text[24:28])
                fourth_th = my_text.replace(my_text, my_text[36:40])
                fifth_th = my_text.replace(my_text, my_text[48:52])
                my_theads.append(first_th)
                my_theads.append(second_th)
                my_theads.append(third_th)
                my_theads.append(fourth_th)
                my_theads.append(fifth_th)
                my_theads = my_theads[0:5]

        data = []
        first_column = []
        tables = soup.find_all('table', attrs={'class': 'section-content'})
        for table in tables:
            table_body = table.find('tbody')

            rows = table_body.find_all('tr')
            for row in rows:
                first_col = row.find_all('th')
                cols = row.find_all('td')
                first_cols = [ele.text.strip() for ele in first_col]
                cols = [ele.text.strip() for ele in cols]

                first_column.append(first_cols)
                data.append(cols)

        first_column = [item for sublist in first_column for item in sublist]

        # Create the pandas DataFrame
        df = pd.DataFrame(data, columns=my_theads)
        first_column = pd.Series(first_column)
        # print dataframe.
        df['items'] = first_column
        df = df.set_index('items')
        df = df.reset_index()

        ticker_name = []
        length = len(df.index)
        for i in range(length):
            if competitor != "":
                ticker_name.append(str(competitor))
            else:
                ticker_name.append(str(self.ticker))
        df['ticker'] = ticker_name
        return df

    def get_data(self, ticker, financial_statement):
        """
        Makes use navigating the HTML radio buttons between annual and quarterly data on each stock reports webpage.
        After identifying which page the driver is currently on this method makes use of the quarter_data() 
        and annual_data() methods to create a new directory with a csv of the page's data.

        Parameters
        ----------
        ticker : str
                The current stock ticker
        financial_statement : str
                The current report (balance sheet, income statement, cash flow statement)
        """
        self.ticker = ticker
        self.financial_statement = financial_statement

        # instead of having two try/catches you can have an f string where Annual is during for loop
        periods = ["Annual", "Quarter"]
        quarter = 'Quarter'
        annual = 'Annual'
        DOW_JONES_DIR = dow_jones_directory

        for i in periods:
            try:
                radio_button = self.driver.find_element(
                    By.XPATH, "//input[@checked='checked']")
                period = self.driver.find_element(
                    By.XPATH, f"//label[@class='ui-radio-button checked']/span[text()='{i}']")
                if (radio_button):
                    if (i == annual):
                        wait = WebDriverWait(self.driver, 10)
                        wait.until(EC.element_to_be_clickable(
                            (By.XPATH, "//span[text()='Quarter']"))).click()
                        time.sleep(5)
                        quarter_data_df = self.quarter_data()

                        my_path = DOW_JONES_DIR + self.ticker
                        isExist = os.path.exists(my_path)

                        if isExist:
                            quarter_data_df.to_csv(path.join(
                                my_path, f"{self.ticker}{quarter.lower()+'ly'}{self.financial_statement}.csv"), index=False)
                        else:
                            os.mkdir(my_path)
                            quarter_data_df.to_csv(path.join(
                                my_path, f"{self.ticker}{quarter.lower()+'ly'}{self.financial_statement}.csv"), index=False)

                        break
                    else:
                        wait = WebDriverWait(self.driver, 10)
                        wait.until(EC.element_to_be_clickable(
                            (By.XPATH, "//span[text()='Annual']"))).click()
                        time.sleep(5)
                        annual_data_df = self.annual_data()

                        my_path = DOW_JONES_DIR + self.ticker
                        isExist = os.path.exists(my_path)

                        if isExist:
                            annual_data_df.to_csv(path.join(
                                my_path, f"{self.ticker}{annual.lower()}{self.financial_statement}.csv"), index=False)
                        else:
                            os.mkdir(my_path)
                            annual_data_df.to_csv(path.join(
                                my_path, f"{self.ticker}{annual.lower()}{self.financial_statement}.csv"), index=False)

                        break
            except NoSuchElementException:
                pass

    def get_competitors(self, ticker):
        """
        Returns the competitors associated with the current company.

        Parameters
        ----------
        ticker : str
                The current company stock ticker

        Returns
        -------
        list
                The competitors associated with the current company documented on Wall Street Journal (WSJ).
                [Not all competitors from WSJ are documented. These competitors are flagged because they are 
                not listed on TD Ameritrade.]
        """
        dow_jones_list = self.dow_jones_symbols()
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        competitors = []

        tables = soup.find_all('table', id='cr_competitors_table')
        for table in tables:

            table_body = table.find('tbody')
            rows = table_body.find_all('tr')

            for row in rows:
                a_tag = row.find('a')
                if (a_tag != None):
                    text = a_tag.text
                    result = any(i.isdigit() for i in text)
                    if (result != True):
                        competitors.append(text)

        other_competitors = []

        for competitor in competitors:
            COMPETITORS_DIR = all_competitors_dir
            my_path = COMPETITORS_DIR + competitor
            isExist = os.path.exists(my_path)

            if (competitor in dow_jones_list) & (competitor != ticker):
                src = dow_jones_directory + competitor
                dest = dow_jones_directory + \
                    ticker + "/competitors/" + competitor
                shutil.copytree(src, dest)

            if (competitor not in dow_jones_list) & (competitor.__contains__(".") == False) & (isExist == False):
                other_competitors.append(competitor)

            if isExist:
                src = my_path
                dest = dow_jones_directory + \
                    ticker + "/competitors/" + competitor
                shutil.copytree(src, dest)
                isExist = False

        return other_competitors

    def get_competitor_data(self, ticker, competitor, financial_statement):
        """
        Makes use navigating the HTML radio buttons between annual and quarterly data on each stock reports webpage.
        After identifying which page the driver is currently on this method makes use of the quarter_data() 
        and annual_data() methods to create a new directory with a csv of the page's data.

        Parameters
        ----------
        ticker : str
                The current stock ticker
        competitor : str
                The current competitor of the associated stock ticker
        financial_statement : str
                The current report (balance sheet, income statement, cash flow statement)
        """
        self.ticker = ticker
        self.competitor = competitor
        self.financial_statement = financial_statement

        # instead of having two try/catches you can have an f string where Annual is during for loop
        periods = ["Annual", "Quarter"]
        quarter = 'Quarter'
        annual = 'Annual'
        DATA_DIR = dow_jones_directory + f"{ticker}/competitors/"
        ALL_COMPETITOR_DIR = all_competitors_dir

        for i in periods:
            try:
                radio_button = self.driver.find_element(
                    By.XPATH, "//input[@checked='checked']")
                period = self.driver.find_element(
                    By.XPATH, f"//label[@class='ui-radio-button checked']/span[text()='{i}']")
                if (radio_button):
                    if (i == annual):
                        wait = WebDriverWait(self.driver, 10)
                        wait.until(EC.element_to_be_clickable(
                            (By.XPATH, "//span[text()='Quarter']"))).click()
                        time.sleep(5)
                        quarter_data_df = self.quarter_data(
                            competitor=self.competitor)

                        my_path = DATA_DIR + self.competitor
                        competitor_path = ALL_COMPETITOR_DIR + self.competitor

                        competitorDirExist = os.path.exists(DATA_DIR)
                        isExist = os.path.exists(my_path)
                        allCompetitorDataExist = os.path.exists(
                            competitor_path)

                        if competitorDirExist:
                            pass
                        else:
                            os.mkdir(DATA_DIR)

                        if isExist:
                            quarter_data_df.to_csv(path.join(
                                my_path, f"{self.competitor}{quarter.lower()+'ly'}{self.financial_statement}.csv"), index=False)
                        else:
                            os.mkdir(my_path)
                            quarter_data_df.to_csv(path.join(
                                my_path, f"{self.competitor}{quarter.lower()+'ly'}{self.financial_statement}.csv"), index=False)

                        if allCompetitorDataExist:
                            quarter_data_df.to_csv(path.join(
                                competitor_path, f"{self.competitor}{quarter.lower()+'ly'}{self.financial_statement}.csv"), index=False)
                        else:
                            os.mkdir(competitor_path)
                            quarter_data_df.to_csv(path.join(
                                competitor_path, f"{self.competitor}{quarter.lower()+'ly'}{self.financial_statement}.csv"), index=False)

                        # return quarter_data_df
                        break
                    else:
                        wait = WebDriverWait(self.driver, 10)
                        wait.until(EC.element_to_be_clickable(
                            (By.XPATH, "//span[text()='Annual']"))).click()
                        time.sleep(5)
                        annual_data_df = self.annual_data(
                            competitor=self.competitor)

                        my_path = DATA_DIR + self.competitor
                        competitor_path = ALL_COMPETITOR_DIR + self.competitor

                        competitorDirExist = os.path.exists(DATA_DIR)
                        isExist = os.path.exists(my_path)
                        allCompetitorDataExist = os.path.exists(
                            competitor_path)

                        if competitorDirExist:
                            pass
                        else:
                            os.mkdir(DATA_DIR)

                        if isExist:
                            annual_data_df.to_csv(path.join(
                                my_path, f"{self.competitor}{annual.lower()}{self.financial_statement}.csv"), index=False)
                        else:
                            os.mkdir(my_path)
                            annual_data_df.to_csv(path.join(
                                my_path, f"{self.competitor}{annual.lower()}{self.financial_statement}.csv"), index=False)

                        if allCompetitorDataExist:
                            annual_data_df.to_csv(path.join(
                                competitor_path, f"{self.competitor}{annual.lower()}{self.financial_statement}.csv"), index=False)
                        else:
                            os.mkdir(competitor_path)
                            annual_data_df.to_csv(path.join(
                                competitor_path, f"{self.competitor}{annual.lower()}{self.financial_statement}.csv"), index=False)

                        # return annual_data_df
                        break
            except NoSuchElementException:
                pass

    def close_browser(self):
        """
        Closes the driver.

        Returns
        -------
        None
        """
        return self.driver.quit()
