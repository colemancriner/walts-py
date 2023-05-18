import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import numpy as np
import config

url_login = 'https://wpos.walts.com/pos/index.php?action=login'
url_download = 'https://wpos.walts.com/pos/on_hand_download.php'

# Create Session
s = requests.Session()
#==============================================================================
#==============================================================================
#==============================================================================
# Function for webscraping the token hidden in the HTML
def tScraper(url):
  r = s.get(url)
  print(r)
  soup = BeautifulSoup(r.content, 'html.parser')
  token = soup.find('input')['value']
  print(token)
  return token
#==============================================================================
#==============================================================================
#==============================================================================
# Logging in to WPOS System
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
  r = s.post(url,data=payload)
  print('DOES LOGIN WORK?')
  print(r)

#==============================================================================
#==============================================================================
#==============================================================================
# Click the Download link located on inventory page
def download_file(url):
  headers = {
    
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
  }
  r = s.get(url, headers=headers)
  print('DOES DOWNLOAD LINK WORK?')
  print(r)
  return r

inventory_report = pd.DataFrame({})

#==============================================================================
#==============================================================================
#==============================================================================
# Function for Flow Control
def main():

  login(url_login)
  inventory_report = download_file(url_download)
  
  print('RESPONSE TYPE:')
  print(type(inventory_report))

  print('RESPONSE.text TYPE:')
  print((inventory_report.text))

  print('FIRST 20 ROWS:')
  inventory_report = pd.read_csv(StringIO(inventory_report.text))
  print(inventory_report.head(20))
  s.close()
  return inventory_report


inventory_report = main()
invdf = inventory_report

invdf['UPC'] = invdf['UPC'].fillna(0)
invdf['UPC'] = invdf['UPC'].astype(np.int64)
invdf['Model'] = invdf['Model'].str.strip()
invdf['Brand'] = invdf['Brand'].str.strip()
invdf = invdf.sort_values(by = 'Model')





