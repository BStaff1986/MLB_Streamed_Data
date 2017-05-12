# Program to read MLB XML Data

# TODO: Fix issue where only final pitch of atbat appears.

import requests
import json
import subprocess as sp
from time import sleep 
from bs4 import BeautifulSoup

class MLB_Scrape():
	def __init__(self):
		self.inning = 0
		self.ab_num = 0
		self.pitch_id = 0
		self.xml = ''

	def get_game_events(self):
		'''
		This function combines the component parts of MLB Gameday's URL
		'''
		url = 'http://gd2.mlb.com/components/game/mlb/'
		year = '/year_2017'
		month = '/month_05'
		day = '/day_11'
		game = '/gid_2017_05_11_seamlb_tormlb_1' 
		xml_link = '/game_events.xml'

		r = requests.get(url + year + month + day + game + xml_link)
		self.xml = BeautifulSoup(r.text, features='lxml-xml') 
		
	def get_atbat_info(self):
		'''
		This function parses the XML data and prints the desired data
		'''
		self.ab_num = len(self.xml.find_all('atbat'))

	def get_last_pitch_info(self):
		all_pitch = self.xml.find_all('pitch')
		last_pitch_num = len(all_pitch) - 1
		
		last_pitch = all_pitch[last_pitch_num]
		pitch_id = int(last_pitch['sv_id'].replace("_",""))

		if pitch_id > self.pitch_id:
			self.pitch_id = pitch_id
			pitch_speed = last_pitch['start_speed']
			pitch_type = last_pitch['pitch_type']
			return (pitch_speed, pitch_type)
		else:
			return (None, None)

	def pitch_update(self):
		'''
		This is the executive function which obtains all desired data
		and prints it to the command line.
		'''
		self.get_game_events()
		ab_info = self.get_atbat_info()
		speed, pitch_type = self.get_last_pitch_info()
		
		if speed and pitch_type:
			print('Pitch Speed: {} Pitch Type: {}'.format(speed, pitch_type))
			return
		else:
			return
		
sp.call('clear',shell=True)
mlb = MLB_Scrape()
while True:
	sleep(3)
	mlb.pitch_update()
