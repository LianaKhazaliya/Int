from bs4 import BeautifulSoup
import requests
import re
import os, sys


def get_data_cars(url: str) -> list:
    
    page = requests.get(url=url)
    soup = BeautifulSoup(page.text, 'html.parser')
    data = soup.find_all('div', class_='listing-item-wrap')

    cars = list()
    for car in data:
        if car is not None:
            block = car.find('div', class_='listing-item-main')
            title_block = block.find('div', class_='listing-item-title')
            title = title_block.a.text.strip()
            title_href = title_block.a.get('href')

            description_block = block.find('div', class_='listing-item-desc')
            year = re.findall(r'\d+', description_block.span.text.strip())[0]
            description = [i.strip() for i in description_block.text.split(',')]


            #message_block = block.find('div', class_='listing-item-message')
            #message = message_block.div.text

            #date = car.find('div', class_='listing-item-date').text    <-- does not work

            price_block = car.find('div', class_='listing-item-price')
            price = price_block.small.text

            if description is not None:
                res =[title, title_href, year]+description+[price]
                cars.append(res)
    
    return cars

def get_all_data(url: str):

    data = get_data_cars(url = url)

    return data

def write_smth(smth_list, name):
    with open(name+'.csv', mode = 'w') as Outfile:
        for smth in smth_list:
            print(','.join([get_decoded(i) for i in smth]), file=Outfile)

def get_decoded(s):
    return str(s.encode('iso-8859-1'), 'utf-8')

if __name__ == "__main__":
    
    AV_URL = 'https://cars.av.by/volkswagen/touareg'
    
    with open('ENCODING.csv', mode = 'w') as Outfile:
        print('Brand,Mark,Title,Hlink,Year,Transmission,Fuel,Type,Run,Cost', file=Outfile)

    data = get_all_data(AV_URL)
    print(data)
    write_smth(data, 'ENCODING')
    print()