import requests
from time import sleep

#Selenium 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as bs
import pandas as pd

years = list(range(1999, 2024)) 



#Getting Player Per Game Stats from 99 - 23

playerStatsURL = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("start-maximized")  
chrome_options.add_argument("disable-infobars")  
chrome_options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=chrome_options)

for year in years:
    url = playerStatsURL.format(year)
    driver.get(url)
    driver.execute_script('window.scrollTo(1,10000)')
    sleep(2)
    html = driver.page_source
    
    with open('playerStats/{}.html'.format(year), 'w+', encoding='utf-8') as file:
        file.write(html)
     


dfPlyrStats = []        
for year in years:
    with open('playerStats/{}.html'.format(year), encoding='utf-8') as file:
        page = file.read()
        soup = bs(page, 'html.parser')
        soup.find('tr', class_="thead").decompose()
        plyrTable = soup.find(id='per_game_stats')
        plyr = pd.read_html(str(plyrTable))[0]
        plyr['Year'] = year
        dfPlyrStats.append(plyr)


plyrs = pd.concat(dfPlyrStats)
plyrs.to_csv("players.csv")

