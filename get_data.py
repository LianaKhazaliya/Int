from bs4 import BeautifulSoup
import requests
import re
import os, sys


AV_URL = 'https://cars.av.by'
def get_brands_list(url: str) -> list:
    
    page = requests.get(url=url)
    soup = BeautifulSoup(page.text, 'html.parser')
    cars_list = list()
    data = soup.find('ul', class_='brandslist')
    data.find_all('li')
    for link in data.find_all('li'):
        link_class = link.get('class')
        if link_class is not None:
            if link_class[0] != 'bransditem brandsitem--primary':
                cars_list.append(brand(link))
    
    return cars_list


def write_brands(cars_list, name):
    with open(name+'brands_list.txt', mode = 'w') as brands_file:
        for car in cars_list:
            print(car, file=brands_file)

def write_smth(smth_list, name):
    with open(name+'.txt', mode = 'w') as Outfile:
        for smth in smth_list:
            print(smth, file=Outfile)

def append_smth(brand, mark, smth_list, name):
    with open(name+'.csv', mode = 'a+') as Outfile:
        for smth in smth_list:
            print(','.join([brand, mark]+smth), file=Outfile)

def brand(link):
    
    data = link.span
    if data is not None:
        brand = data.text
        number = link.small.text
        hlink = link.a.get('href')
        return [brand, number, hlink]

def get_pages_links(url: str) -> list:

    page = requests.get(url=url)
    soup = BeautifulSoup(page.text, 'html.parser')
    data = soup.find_all('li', class_='pages-numbers-item')
    pages_list = list()

    for link in data:
        if link.a is not None:
            pages_list.append(link.a.get('href'))

    return pages_list

def encoding_crutch(description):
    decoding = {
        'Ð°Ð½Ð¸ÐºÐ°' : 'механика',
        'Ð±ÐµÐ½Ð·Ð¸Ð½' : 'бензин',
        'ÑÐµÐ´Ð°Ð½' : 'седан',
        'Ð°Ð²Ñ' : 'автомат',
        'Ð´Ð¸Ð·ÐµÐ»Ñ' : 'дизель',
        'ÑÐ½Ð¸Ð²ÐµÑÑÐ°Ð»' : 'универсал',
        'Ð²Ð½ÐµÐ´Ð¾ÑÐ¾Ð¶Ð½Ð¸Ðº' : 'внедорожник',
        'ÐºÑÐ¿Ðµ' : 'купе',
        'ÑÑÐ±ÐµÐº' : 'хэтчбек',
        'Ð½' : 'минивэн'
    }

    m = description.split(',')
    c = 1
    if len(m) == 6:
        
        if m[1].strip().find('Ð°Ð²ÑÐ¾Ð¼Ð°Ñ')  != -1 :
            dv_type = 'автомат'
        elif m[1].strip().find('Ð¼ÐµÑ') + m[1].strip().find('Ð°Ð½Ð¸ÐºÐ°') != -2:
            dv_type = 'механика'
        else:
            c = 0
        if m[3].strip().find('Ð±ÐµÐ½Ð·Ð¸Ð½')  != -1 :
            toplivo = 'бензин'
        elif m[3].strip().find('Ð´Ð¸Ð·ÐµÐ»Ñ') != -1:
            toplivo = 'дизель'
        else:
            c = 0
        
        a = m[4].strip()
        if a.find('Ð²Ð½ÐµÐ´Ð¾ÑÐ¾Ð¶Ð½Ð¸Ðº') + a.find('ÑÐµÑÑÐ°Ð¹Ð»Ð¸Ð½Ð³') != -2:
            car_type = 'внедорожник'
        elif a.find('ÑÑÐ±ÐµÐº') != -1:
            car_type = 'хэтчбэк'
        elif a.find('ÑÐµÐ´Ð°Ð½') != -1:
            car_type = 'седан'
        elif a.find('ÑÐ½Ð¸Ð²ÐµÑÑÐ°Ð»') != -1:
            car_type = 'универсал'
        elif a.find('ÐºÑÐ¿Ðµ') != -1:
            car_type = 'купе'
        else:
            c = 0
        
        probeg = re.findall(r'\d+', m[5].strip())[0]   

        if c:
            return [dv_type, toplivo, car_type, probeg]
        else:
            return None
    else:
        return None

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
            description = encoding_crutch(description_block.text)

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
    pages_links = get_pages_links(url = url)
    data = get_data_cars(url = url)
    
    for link in pages_links:
        data+=get_data_cars(url = link)
        
    return data
    


if __name__ == "__main__":
    
    AV_URL = 'https://cars.av.by'
    brands_list = get_brands_list(AV_URL)
    
    with open('DATA.csv', mode = 'w') as Outfile:
        print('Brand,Mark,Title,Hlink,Year,Transmission,Fuel,Type,Run,Cost', file=Outfile)
    for i in brands_list: 
        brand_list2 = get_brands_list(str(i[2]))
        for j in brand_list2:
            data = get_all_data(str(j[2]))
            append_smth(i[0], j[0], data, 'DATA')
            print(i[0], j[0])
            
    
    
    """write_brands(get_brands_list(AV_URL), 'Init')
    with open('Initbrands_list.txt', mode = 'r') as brands_file:
        lines = brands_file.readlines()
        for line in lines:
            a, b, c = map(str, line[2:-3].split('\', \''))
            write_brands(get_brands_list(c), a)"""

    #for i in get_data_cars('https://cars.av.by/audi/a4'):
    #    print('\n'.join(i))
    #print(get_pages_links('https://cars.av.by/audi/a4'))

    #for i in get_data_cars('https://cars.av.by/audi/a4'):
    #    print(" ".join(i))
    
    """page = requests.get(url='https://advent.compscicenter.ru/')
    soup = BeautifulSoup(page.text, 'html.parser')
    cars_list = list()
    data = soup.find('div', class_='col-12')

    print(data.h2.text)"""


