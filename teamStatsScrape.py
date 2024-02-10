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

teamStatsURL = 'https://www.basketball-reference.com/leagues/NBA_{}_standings.html'

for year in years:
    sleep(2)
    url = teamStatsURL.format(year)
    data = requests.get(url)
    
    with open('teamStats/{}.html'.format(year), 'w+', encoding='utf-8') as file:
        file.write(data.text)
        
dfTeamStats = []        
for year in years:
    with open('teamStats/{}.html'.format(year), encoding='utf-8') as file:
        page = file.read()
        soup = bs(page, 'html.parser')
        soup.find('tr', class_="thead").decompose()
        teamStatsTable = soup.find(id='divs_standings_E')
        teamStat = pd.read_html(str(teamStatsTable))[0]
        teamStat['Year'] = year
        teamStat['Team'] = teamStat['Eastern Conference']
        del teamStat['Eastern Conference']
        dfTeamStats.append(teamStat)
        
        soup = bs(page, 'html.parser')
        soup.find('tr', class_="thead").decompose()
        teamStatsTable = soup.find(id='divs_standings_W')
        teamStat = pd.read_html(str(teamStatsTable))[0]
        teamStat['Year'] = year
        teamStat['Team'] = teamStat['Western Conference']
        del teamStat['Western Conference']
        dfTeamStats.append(teamStat)

#Generate csv file for mvps        
teamStats = pd.concat(dfTeamStats)
teamStats.to_csv('teams.csv')