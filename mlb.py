# Program to read MLB JSON

import requests
import json
from bs4 import BeautifulSoup

def get_play_data():
	'''
	This function combines the component parts of MLB Gameday's URL
	'''
	url = 'http://gd2.mlb.com/components/game/mlb/'
	year = '/year_2017'
	month = '/month_05'
	day = '/day_08'
	game = '/gid_2017_05_08_clemlb_tormlb_1'
	xml = '/game_events.xml'
	r = requests.get(url + year + month + day + game + xml)
	soup = BeautifulSoup(r.text, features='lxml-xml') 
	return soup

def find_atbat(xml):
	atbat_num = 1
	atbat_data = xml.find('atbat', {'num' : atbat_num})
	print(atbat_data)
	return

xml = get_play_data()
find_atbat(xml)

