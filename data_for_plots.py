#! usr/bin/env python3.6
# coding: utf-8

import csv
import numpy
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import requests
import re
import os, sys

def get_data_about_smb(input_file, name, *parameters):
	with open(input_file, mode = 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		data = []
		for row in reader:
			if (row['Mark'] == name):
				d = {}
				for par in parameters:
					if par[1] == 'int':
						d[par[0]] = int(row[par[0]].replace(' ', ''))
					else:
						d[par[1]] = str(row[par[0]])
				data.append(d)
	
	return data

def get_color(url: str) -> str:
	page = requests.get(url=url)

	soup = BeautifulSoup(page.text, 'html.parser')
	data = soup.find('div', class_='card-info')
	if data is not None:
		link = data.find_all('dl')[5]
		encoded_color = link.dd.text
		if encoded_color.find('ÑÐµÑÐ½ÑÐ¹') != -1:
			color = 'Black'
		elif encoded_color.find('ÑÐµÑÑÐ¹') != -1:
			color = 'Grey'
		elif encoded_color.find('ÐºÐ¾ÑÐ¸ÑÐ½ÐµÐ²ÑÐ¹') != -1:
			color = 'Brown'
		elif encoded_color.find('Ð·ÐµÐ»ÐµÐ½ÑÐ¹') != -1:
			color = 'Green'
		elif encoded_color.find('ÑÐ¸Ð½Ð¸Ð¹') != -1:
			color = 'Blue'
		elif encoded_color.find('Ð±ÐµÐ»ÑÐ¹') != -1:
			color = 'White'
		elif encoded_color.find('ÑÐµÑÐµÐ±ÑÐ¸ÑÑÑÐ¹') != -1:
			color = 'Silver'
		elif encoded_color.find('Ð¸Ð¾Ð»ÐµÑÐ¾Ð²ÑÐ¹') != -1:
			color = 'Violet'
		else:
			color = 'Other'
		return color

	

if __name__ == "__main__":
	with open('DATA.csv', mode = 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		data = []
		for row in reader:
			if (row['Mark'] == 'Polo'):
				print(get_color(row['Hlink']))