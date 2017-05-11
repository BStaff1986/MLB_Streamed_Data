# Program to read MLB JSON

import requests
import json
from time import sleep 
from bs4 import BeautifulSoup

class MLB_Scrape():
	def __init__(self):
		self.inning = 0
		self.ab_num = 0

	def get_play_data(self):
		'''
		This function combines the component parts of MLB Gameday's URL
		'''
		url = 'http://gd2.mlb.com/components/game/mlb/'
		year = '/year_2017'
		month = '/month_05'
		day = '/day_10'
		game = '/gid_2017_05_10_pitmlb_lanmlb_1/'
		xml = '/game_events.xml'

		r = requests.get(url + year + month + day + game + xml)
		soup = BeautifulSoup(r.text, features='lxml-xml') 
		return soup

	def get_atbat_num(self):
		xml = self.get_play_data()
		atbat_num = len(xml.find_all('atbat'))
		return atbat_num

	def atbat_info(self):
		current_ab = self.get_atbat_num()
		if current_ab  > self.ab_num:
			self.ab_num = current_ab
			print('New Batter')
		else:
			print('Same Batter')

mlb = MLB_Scrape()
while True:
	sleep(3)
	mlb.atbat_info()
