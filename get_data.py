from bs4 import BeautifulSoup
import requests

AV_URL = 'https://cars.av.by'
def get_brands_list(url: str) -> list:
    
    page = requests.get(url=url)
    soup = BeautifulSoup(page.text, 'html.parser')
    cars_list = list()
    data = soup.find('ul', class_='brandslist')

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


def brand(link):
    
    data = link.span
    if data is not None:
        brand = data.text
        number = link.small.text
        hlink = link.a.get('href')
        return [brand, number, hlink]


if __name__ == "__main__":
    
    write_brands(get_brands_list(AV_URL), 'Init')
    with open('Initbrands_list.txt', mode = 'r') as brands_file:
        lines = brands_file.readlines()
        for line in lines:
            a, b, c = map(str, line[2:-3].split('\', \''))
            write_brands(get_brands_list(c), a)