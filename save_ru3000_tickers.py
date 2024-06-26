'''
This script is heavily inspired by a work of Mr. Franklin Schram - description of his program is available here: 
https://medium.com/@franklin.schram/hissing-the-python-way-scraping-ishares-com-to-get-index-constituents-w00t-7505746dcf0c
I applied some minor changes to it in order to get a simple list of ticker symbols - components of the Russell 3000 index
in tls format, which I then process by AmiQuote program for downloading actual stock prices from sites such as Yahoo, Quandl etc.
'''
import requests
import pandas as pd
from bs4 import BeautifulSoup


def getProductLink(etfString):
    '''
    Takes name of the index its components we are looking for and returns a hyperlink to the ETF webpage storing a csv file with
    the index components.

    Args:
        etfString (str): Should contain name of the index in the following format: 'russell-3000'
    '''
    url = 'https://www.ishares.com/uk/professional/en/products/etf-investments'
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
    par = {
        'switchLocale': 'y',
        'siteEntryPassthrough': 'true',
        'productView': 'all',
        'sortColumn': 'totalFundSizeInMillions',
        'sortDirection': 'desc',
        'dataView': 'keyFacts',
        'keyFacts': 'all',
        'search': 'russell%203000'
    }
    resp = requests.get(url, headers=head, params=par)
    dataList = []
    soup = BeautifulSoup(resp.content, 'html.parser')
    tableRows = soup.find_all('tr')
    for row in tableRows:
        dataDict = {}
        tdLink = row.find_all('td', class_='links')
        link = ''
        if len(tdLink) >= 1:
            link = tdLink[0].a['href']
        # Links are stripped from first part of URL -> we add it back
        dataDict['link'] = 'http://www.ishares.com' + link
        for value in dataDict.values():
            if etfString in value:
                dataList.append(value)
                break
    return dataList[0]


def getProductFileLink(productLink):
    '''
    Takes a hyperlink of a webpage dedicated to the ETF and returns a new hyperlink that leads directly to our desireable csv file.

    Args: 
        productLink (str): Hyperlink as a product of the preceding function. 
    '''
    # pretending we're a webbrowser
    head = {
        'User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
    # skipping the cookies stuff
    par = {'switchLocale': 'y', 'siteEntryPassthrough': 'true'}
    # response object and parsing
    response = requests.get(productLink, headers=head, params=par)
    soup = BeautifulSoup(response.content, 'html.parser')
    partOfTheLink = soup.find('a', class_='icon-xls-export',
                              attrs={'data-link-event': 'holdings:holdings'}).get('href')
    return 'http://www.ishares.com' + partOfTheLink


def getHeaderRowIndex(link, keyWord):
    '''
    Gets index (int) of a row that will be a header of the new data object.

    Args:
        link (str): Is referencing to the http address from which I can download the whole file with ETF constituents.
        keyWord (str): Is referencing to a string which I expect to be present somewhere in the header row. 'Ticker' is the keyword by default as
        my aim is to get stocks symbols only.
    '''
    df = pd.read_csv(link, sep=';', header=None, on_bad_lines='skip')
    headerRow = df.index[df.iloc[:, 0].str.contains(
        keyWord, na=False)].tolist()
    return headerRow[0]


def prepareTickers(link, headRowIndex, keyWord):
    '''
    Create a new instance of Pandas-reading object while skipping all the rows above the header-row, that are mainly blank and specifically narrow the
    reading to a column with stock symbols by applying a keyWord arg. 

    Args:
        link (str): Is referencing to the http address from which I can download the whole file with ETF constituents.
        headRowIndex (str): Contains number of the header row returned from the function named getHeaderRowIndex.
        keyWord (str): 'Ticker' by default. Depends on what are you looking for. Can be multiple str values.
    '''
    df = pd.read_csv(link, sep=',', header=headRowIndex, on_bad_lines='skip')
    tickers = df[keyWord]
    return tickers


def getTickers(rawTickers, fileName):
    '''
    1) Add hyphen (-) before last character of selected stock symbol. Data providers differentiate in marking stock classes. While raw data from 
    ishares.com have no symbols to mark them, some data providers like Google Finance are using dot (.) to distinguish between different classes 
    (e.g. Berkshire Hathaway Class B has symbol BKR.B). My primary provider Yahoo Finance is using hyphen (Berkshire Hathaway Class B has symbol BKR-B).
    Without modifying some symbols with hyphen, AmiQuote would not be able to retrieve data for those stocks from Yahoo Finance. This applies for 
    multiple symbols and I recommend from time to time to manually check if any new symbol might need to undergo this modification and eventually add
    the symbol (just add string of capitals like 'LGFA', no 'LGF.A' or 'LGF-A') to a list named dashTickers nested in this function.

    2) Save file.

    Args:
        rawTickers (): Contains a returned object from the function named prepareTickers.
        fileName (str): Contains a whole path of a newly created file with stocks symbols.
    '''
    dashTickers = ['BFA', 'BFB', 'LGFA', 'LGFB', 'BRKB',
                   'HEIA', 'UHALB', 'LENB', 'CWENA', 'GEFB']
    tickersList = []
    for ticker in rawTickers:
        if not ticker.isalnum():
            continue
        elif ticker in dashTickers:
            # Adding '-' before last letter of a ticker
            tickersList.append('-'.join([ticker[:len(ticker)-1], ticker[-1:]]))
        else:
            tickersList.append(ticker)
    with open(fileName, 'w') as file:
        for item in tickersList:
            file.write("%s\n" % item)


def main():

    etfString = 'russell-3000'
    productLink = getProductLink(etfString)
    link = getProductFileLink(productLink)
    keyWord = 'Ticker'
    headerIndex = getHeaderRowIndex(link, keyWord)
    print(type(headerIndex))
    rawTickers = prepareTickers(link, headerIndex, keyWord)
    fileName = r'C:\ru3000.tls'
    getTickers(rawTickers, fileName)

if __name__ == '__main__':
    main()
