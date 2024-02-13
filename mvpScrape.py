import requests
from time import sleep
from bs4 import BeautifulSoup as bs
import pandas as pd


#Getting MVP Votes from 99 - 23

years = list(range(1999, 2024)) 

#Download Pages neseccary for MVP
mvpsURL = "https://www.basketball-reference.com/awards/awards_{}.html" 

for year in years:
    sleep(2)
    url = mvpsURL.format(year)
    data = requests.get(url)
    
    with open('mvp/{}.html'.format(year), 'w+', encoding='utf-8') as file:
        file.write(data.text)

#Parse data and add it to panda data frames
dfMVP = []        
for year in years:
    with open('mvp/{}.html'.format(year), encoding='utf-8') as file:
        page = file.read()
        soup = bs(page, 'html.parser')
        soup.find('tr', class_="over_header").decompose()
        mvpTable = soup.find(id='mvp')
        mvp = pd.read_html(str(mvpTable))[0]
        mvp['Year'] = year
        dfMVP.append(mvp)

#Generate csv file for mvps        
mvps = pd.concat(dfMVP)
mvps.to_csv('mvps.csv')