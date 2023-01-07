# TD Ameritrade Data Scraping

![Contributors](https://img.shields.io/github/contributors/jakebyford/TD_Ameritrade_Financial_Scraping?style=plastic)
![Forks](https://img.shields.io/github/forks/jakebyford/TD_Ameritrade_Financial_Scraping)
![Stars](https://img.shields.io/github/stars/jakebyford/TD_Ameritrade_Financial_Scraping)
![Licence](https://img.shields.io/github/license/jakebyford/TD_Ameritrade_Financial_Scraping)
![Issues](https://img.shields.io/github/issues/jakebyford/TD_Ameritrade_Financial_Scraping)

## Description

The primary focus of this project is to scrape the fundamental reporting data from the 30 stocks of the Dow Jones and their respective competitors. This leads us to use the data for further analysis to make better investment decisions. For example, implementing ratio analysis on a specific Dow Jones stock and its competitors can show which company is more financially leveraged.

This project was built on the Python programming language. The packages used for this project were BeautifulSoup4, Pandas, Selenium, Splinter, and Webdriver_Manager.

BeautifulSoup4 and Pandas were used interchangeably to take the data from HTML and transform it into a DataFrame.

WebDriverManager is used to initialize the web browser and Selenium directs the webdriver to different stock pages on TD Ameritrade and Wall Street Journal. Selenium also navigated between the annual and quarterly reports of the balance sheet, income statement, and cash flow statements of the 30 stocks aas well as their respective competitors.

Some challenges faced:

- Getting the webdriver to switch between quarterly and annually using the radio buttons on TD Ameritrade.
- Implementing a recursive function to
  - save 2 hours of runtime copying competitor directories already created
- Sometimes when the program ran it wouldn't scrape all the data. Needed to add more seconds to the `time.sleep` function

Features being implemented in the future:

- Create a SQL or NoSQL database to store all the data
- Set up an automated monthly schedule this program runs to save time manually
- Create jupyter notebooks to analyze the data

## ✨ Demo

Below we can see the automation of the program switching between the reports and their annual/quarterly data.

## ![](images/td_ameritrade_scrape.gif) <br />

Below we can see the program automatically creating a directory for Apple's stock and also creating a CSV for the respective report.

## ![](images/demo_aapl.gif)

# How to Install and Run the Project

## System Requirements

- Python Version 3.9.7
- VS Code (or any text editor that runs Python)

## Installation

- Fork this repository
- Clone your forked repository
- Create a config.py and a git_ignore file to respectively declare and hide your directory variables
- Add your scripts
- Commit and push
- Create a pull request
- Star this repository
- Wait for pull request to merge
- Celebrate your first step into the open source world and contribute more

Use 'pip' to install necessary modules in environment.

- The command below installs all necessary requirements need be.

```bash
$ pip install -r requirements.txt
```

For help check this stackoverflow <a href = "https://stackoverflow.com/questions/7225900/how-can-i-install-packages-using-pip-according-to-the-requirements-txt-file-from">link</a>.

## Additional tools to help you get Started with Open-Source Contribution

- [How to Contribute to Open Source Projects – A Beginner's Guide](https://www.freecodecamp.org/news/how-to-contribute-to-open-source-projects-beginners-guide/)

# How to Use the Project

There are two main Python files in this project. `td_ameritrade_scrape.py` is the class that was created and is imported into `financial_scrape_test.py` (which is considered the<strong>"</strong>`main`<strong>"</strong> file) and is the program that collects all the data of the stocks (and their competitors) of the Dow Jones.

## Important

To see the step by step process of the data collection with this app you must delete the `all_competitors` and `dow_jones_stocks` directories to start running from stratch. The runtime on my computer takes about 3 and 1/2 hours and will range from computer to computer. You will also need to set up your screen display to stay awake for at least 3 and 1/2 hours after running this program. My suggestion is to schedule this app to run on an automated schedule once a month.

## Author

👤 **Jake Byford**

- Github: [@jakebyford](https://github.com/jakebyford)
- LinkedIn: [@JakeByford](https://www.linkedin.com/in/jake-byford)

## References

https://www.tdameritrade.com/ <br />
https://www.wsj.com/ <br />
https://beautiful-soup-4.readthedocs.io/en/latest/#parsing-only-part-of-a-document <br />
https://www.selenium.dev/documentation/ <br />
https://stackoverflow.com/ <br />
https://stockmarketmba.com/stocksinthedjia.php <br />
https://www.slickcharts.com/dowjones <br />

## 📝 License

Copyright © 2023 [Jake Byford](https://github.com/jakebyford).<br />
This project is [Apache](https://github.com/jakebyford/td_ameritrade_scraping/blob/master/LICENSE) licensed.
