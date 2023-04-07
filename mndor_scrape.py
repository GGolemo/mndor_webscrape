#!/usr/bin/env python3
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import date, timedelta
import os

excel = False

def make_hyperlink(ecrvId, countyFinal='false'):
    url = 'https://www.mndor.state.mn.us/ecrv_search/app/openPublicEcrvView?ecrvId=' + ecrvId + '&countyFinal=' + countyFinal + '&title=View+Summary+for+Preliminary+eCRV+ID'
    return '=HYPERLINK("%s", "%s")' % (url, 'eCRV')

def extract(counties='Dakota, Hennepin, Ramsey', search_type='Preliminary', property_use_group='RESID', begin_date=date.today()-timedelta(days=7), end_date=date.today()):
    county_ids = {
        'Aitkin': '01',
        'Anoka': '02',
        'Becker': '03',
        'Beltrami': '04',
        'Benton': '05',
        'Big Stone': '06',
        'Blue Earth': '07',
        'Brown': '08',
        'Carlton': '09',
        'Carver': 10,
        'Cass': 11,
        'Chippewa': 12,
        'Chisago': 13,
        'Clay': 14,
        'Clearwater': 15,
        'Cook': 16,
        'Cottonwood': 17,
        'Crow Wing': 18,
        'Dakota': 19,
        'Dodge': 20,
        'Douglas': 21,
        'Faribault': 22,
        'Fillmore': 23,
        'Freeborn': 24,
        'Goodhue': 25,
        'Grant': 26,
        'Hennepin': 27,
        'Houston': 28,
        'Hubbard': 29,
        'Isanti': 30,
        'Itasca': 31,
        'Jackson': 32,
        'Kanabec': 33,
        'Kandiyohi': 34,
        'Kittson': 35,
        'Koochiching': 36,
        'Lac qui Parle': 37,
        'Lake of the Woods': 38,
        'Lake': 39,
        'Le Sueur': 40,
        'Lincoln': 41,
        'Lyon': 42,
        'Mahnomen': 43,
        'Marshall': 44,
        'Martin': 45,
        'McLeod': 46,
        'Meeker': 47,
        'Mille Lacs': 48,
        'Morrison': 49,
        'Mower': 50,
        'Murray': 51,
        'Nicollet': 52,
        'Nobles': 53,
        'Norman': 54,
        'Olmsted': 55,
        'Otter Tail': 56,
        'Pennington': 57,
        'Pine': 58,
        'Pipestone': 59,
        'Polk': 60,
        'Pope': 61,
        'Ramsey': 62,
        'Red Lake': 63,
        'Redwood': 64,
        'Renville': 65,
        'Rice': 66,
        'Rock': 67,
        'Roseau': 68,
        'Saint Louis': 69,
        'Scott': 70,
        'Sherburne': 71,
        'Sibley': 72,
        'Stearns': 73,
        'Steele': 74,
        'Stevens': 75,
        'Swift': 76,
        'Todd': 77,
        'Traverse': 78,
        'Wabasha': 79,
        'Wadena': 80,
        'Waseca': 81,
        'Washington': 82,
        'Watonwan': 83,
        'Wilkin': 84,
        'Winona': 85,
        'Wright': 86,
        'Yellow Medicine': 87
    }

    search_type_dict = {
        'Preliminary': False,
        'Completed': True,
        'P': False,
        'C': True
    }

    property_use_group_dict = {
        'Residential': 'RESID',
        'R': 'RESID',
        'RESID': 'RESID'
    }

    url = f'https://www.mndor.state.mn.us/ecrv_search/app/performPublicSearch?'
    for county in counties.replace(',', '').split(' '):
        url += '&counties=' + str(county_ids[county])

    url += '&_counties=1'
    url += '&_cities=1'
    url += '&countyFinal=' + str(search_type_dict[search_type])
    url += '&propertyUseCodeCodeLevel1=' + \
        str(property_use_group_dict[property_use_group])
    url += '&propertyUseCodeCodeLevel2='
    url += '&propertyUseCodeCodeLevel3='
    url += '&begDate=' + str(begin_date.strftime("%m/%d/%Y")
                             ).replace('/', '%2F').replace('-', '%2F')
    url += '&endDate=' + str(end_date.strftime("%m/%d/%Y")
                             ).replace('/', '%2F').replace('-', '%2F')
    url += '&searchOption=isCustomSearch'

    proxies = {
        "http": "",
        "https": "",
    }
    response = requests.post(url, proxies=proxies)
    soup = BeautifulSoup(response.content, 'lxml')
    return soup


def transform(soup):
    all_records = []
    table = soup.find('table', id='searchReultTable')
    try:
        tbody = table.find('tbody')
    except:
        print("Data doesn't exist, check your input")
        return False

    rows = tbody.find_all('tr')
    for record in rows:
        cols = record.find_all('td')
        cols = [element.text.strip() for element in cols]
        cols.append(make_hyperlink(cols[0]))
        all_records.append(cols)
    return all_records


def main():
    ########################### IF INPUT IS DESIRED ########################
    # counties = input('Please enter the list of counties: ')
    # search_type = input(
    #     'Please enter the search type([P]reliminary/[C]ompleted): ')
    # property_use_group = input(
    #     'Please select the Property Use Group([R]esidential): ')
    # begin_date = input('Please enter the begin date(MM/DD/YYYY): ')
    # end_date = input('Please enter the end date(MM/DD/YYYY): ')
    # all_records = transform(
    #     extract(counties, search_type, property_use_group, begin_date, end_date))

    all_records = transform(extract())
    if all_records:
        listings_csv = pd.DataFrame(all_records, columns=[
                                    'eCRV ID', 'Sale Date', 'County', 'Jurisdiction', 'Deed Acres', 'Buyer', 'Seller', 'Gross Sale', 'hyperlink'])
        listings_csv.to_csv(f'eCRV_filings_{date.today()}.csv', index=False, columns=['eCRV ID', 'Jurisdiction', 'Buyer', 'Seller', 'Gross Sale', 'hyperlink'])
        if excel:
            listings_excel = pd.DataFrame(all_records)
            listings_excel.to_excel(
                f'eCRV_filings_{date.today()}.excel', index=False, columns=['eCRV ID', 'Jurisdiction', 'Buyer', 'Seller', 'Gross Sale', 'hyperlink'])


if __name__ == '__main__':
    main()
