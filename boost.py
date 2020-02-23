import requests

AV = 'https://cars.av.by/volkswagen/touareg/16417217'
while True:
    page = requests.get(url=AV)