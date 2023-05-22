import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import numpy as np
import config
import logging

# Create logging settings
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

url_login = 'https://wpos.walts.com/pos/index.php?action=login'
url_download = 'https://wpos.walts.com/pos/on_hand_download.php'

# Create Persistent Session
s = requests.Session()
#==============================================================================
#==============================================================================
#==============================================================================
# Function for webscraping the token hidden in HTML (USED FOR THE LEGACY WPOS2 SYSTEM)
# Not currently implemented in working code
def tScraper(url):
    r = s.get(url)
    logging.debug(r)
    soup = BeautifulSoup(r.content, 'html.parser')
    token = soup.find('input')['value']
    logging.debug(token)
    return token
#==============================================================================
#==============================================================================
#==============================================================================
# Login into WPOS System
def login(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': 97,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'wpos2_session=eyJpdiI6InI4RkxxR3R0djBFUEdnREVHSFJMU2c9PSIsInZhbHVlIjoiZFY5QnR5WEVSRlcxTjFpNkp4TmV1SlRqYTNxMnZiZTNuMERjSTlwNVhTQ0QrNnVublMrZGZla3BBWmVKYURwalBPaSszUUFkdWVHMVwvMWs3ZE1jaThnPT0iLCJtYWMiOiJlODVhMTg2ZmRmMWFmMjViMGQxNTcyNWIwYzc4YmRkMWQwZjk1YTNlMDY3NjY3NjRmZmRlYTE3MjZkOGFmMGM5In0%3D',
        'Host': 'wpos2.walts.com',
        'Origin': 'https://wpos2.walts.com',
        'Referer': 'https://wpos2.walts.com/admin/login',
        'sec-ch-ua-mobile' : '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
  
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': 97,
        'Content-Type': 'application/x-www-form-urlencoded',
        'sec-ch-ua-mobile' : '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
  
    payload = {
        'email': config.WALTS_EMAIL,
        'password': config.WALTS_PASSWORD,
        'location': config.WALTS_LOCATION,
        'Sign In': 'Sign In'
    }
    response = s.post(url,data=payload)
    logging.info('Login() request Status Code: '+str(response.status_code))
    return response

#==============================================================================
#==============================================================================
#==============================================================================
# *Click* the Inventory On Hand Download link located on inventory page
def download_file(url):
    # Set User-Agent key to a user-agent value of a home device (prevents webscraper blocking safeguard detection)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    response = s.get(url, headers=headers)
    
    logging.info('Download link status code: ' + str(response.status_code))
    logging.debug('Response Head:\n' + str(response.text[:300]))
    return response.text

#==============================================================================
#==============================================================================
#==============================================================================
# Function for Flow Control that returns raw pandas DataFrame
def raw_df():
    # login (no need to assign return value)
    login(url_login)    # creates session object to manage and persist settings across requests from different functions
    inventory_report = download_file(url_download)

    # Convert response to pandas DataFrame
    inventory_report = pd.read_csv(StringIO(inventory_report))
    logging.info('Pandas DataFrame Created')
    logging.debug('FIRST 20 ROWS:\n' + str(inventory_report.head(20)) + '\n END OF FIRST 20 ROWS')
    s.close()
    return inventory_report

#==============================================================================
#==============================================================================
#==============================================================================
# returns a cleaned version of the raw pandas DataFrame
def df():
    # Get raw DataFrame
    inventory_report = raw_df()
    logging.info('Inventory On Hand raw DataFrame pulled')
    # Clean DataFrame
    inventory_report['UPC'] = inventory_report['UPC'].fillna(-1)
    inventory_report['UPC'] = inventory_report['UPC'].astype(np.int64)
    inventory_report['Model'] = inventory_report['Model'].str.strip()
    inventory_report['Brand'] = inventory_report['Brand'].str.strip()
    inventory_report = inventory_report.sort_values(by='Model')
    logging.debug('Is UPC column still scientific notation?\n' + str(inventory_report.loc[:,['Model','UPC','Brand','MPN']]) + '\n END OF SCIENTIFIC NOTATION LOGGING CHECK')

    logging.info('Inventory On Hand raw DataFrame cleaned. Returning Pandas DataFrame...')
    return inventory_report



