import urllib3
import requests
import csv
import re
from bs4 import BeautifulSoup
import sys
from importlib import reload
import urllib.request as urllib

reload(sys)


url = "https://www.vl.ru/vladivostok/fun/extreme"

req = urllib.Request(url)
response = urllib.urlopen(req)
vlCookie = response.headers.get('Set-Cookie')

def TryGetNotVlRuUrl(vlRuUrl, cookie):
    url = 'http://vl.ru' + vlRuUrl
    print(url)
    req = urllib.Request(url)
    req.add_header('cookie', vlCookie)
    vlUrlSite = urllib.urlopen(req)

    vlSiteText = vlUrlSite.read()

    soup = BeautifulSoup(vlSiteText, 'html.parser')
    cafeMeta = soup.find('div', attrs={"class": "contacts-item website company-contacts__paragraph"})

    result = ""
    try:
        result = cafeMeta.find('a')['href']
    except:
        result = ""

    return result


with open('extreme.csv', 'w', newline='', encoding='utf8') as csvfile:
    fieldnames = ['Id', 'Name', 'FullName', 'Description', 'Type', 'MinCost', 'MaxCost', 'WordingHours', 'Location', 'Phone']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    id = 122
    writer.writeheader()

    for i in range(1, 32):
        url = "https://www.vl.ru/vladivostok/fun/extreme?page=" + str(i)
        req2 = urllib.Request(url)
        req2.add_header('cookie', vlCookie)
        vlUrlSite = urllib.urlopen(req2)

        vlSiteText = vlUrlSite.read()

        soup = BeautifulSoup(vlSiteText, 'html.parser')

        cafeContacts = soup.find_all('div', attrs={"class": "company-wrap"})


        for i in cafeContacts:
            name = re.sub('\s\s+|\t\t+', '', i.find('header', attrs={"class": "company__header"}).find('a').text).replace("\n", "").encode('utf-8')
            vlruurl = re.sub('\s\s+|\t\t+|//', '', i.find('header', attrs={"class": "company__header"}).find('a')['href']).replace("\n", "")
            
            print(vlruurl)
            url = TryGetNotVlRuUrl(vlruurl, vlCookie)
            try:
                address = re.sub('\s\s+|\t\t+', '', i.find('div', attrs={"class": "contacts__row address-row"}).text).replace("\n", "").encode('utf-8')
            except:
                address = "-"
            try:
                phone = re.sub('\s\s+|\t\t+', '', i.find('div', attrs={"class": "contacts__row phone-row"}).text).replace("\n", "").encode('utf-8')
            except:
                phone = "NaN"
            try:
            	description = re.sub('\s\s+|\t\t+', '', i.find('div', attrs={"class": "company__annotation"}).text).encode('utf-8')
            except:
            	description = "-"
            try:
            	type = re.sub('\s\s+|\t\t+', '', i.find('div', attrs={"class": "company__activity-type text-light is-advt-hide"}).text).encode('utf-8')
            except:
            	type = "-"
            writer.writerow({'Id': id,
            				'Name': str(name, 'utf-8'), 
                            'FullName': str(name, 'utf-8'),
                            'Description': str(description, 'utf-8'),
                            'Type': 'Активный отдых',
                            'MinCost': 0,
                            'MaxCost': 0,
                            'WordingHours': '09:00-21:00',
                            'Location': str(address, 'utf-8'),
                            'Phone': phone})
            id = id + 1
