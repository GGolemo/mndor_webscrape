from bs4 import BeautifulSoup
import pandas as pd
import requests

url = f'https://www.mndor.state.mn.us/ecrv_search/app/performPublicSearch'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}
search_settings = {'_counties': 1,
'_cities': 1,
'countyFinal': 'false',
'propertyUseCodeCodeLevel1': 'RESID',
'propertyUseCodeCodeLevel2': 'SINGLEFAM',
'propertyUseCodeCodeLevel3': '',
'begDate': '03/30/2023',
'endDate': '03/31/2023',
'searchOption': 'isCustomSearch'}

response = requests.post(url, data=search_settings)
soup = BeautifulSoup(response.content, 'lxml')

print(soup)


# requests.post(url, data={key: value}, json={key: value}, args)