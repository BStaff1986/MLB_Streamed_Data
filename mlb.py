#!python3

# mlb.py :  Program to read and display MLB JSON Data

# TODO: Make a function that delays the printing of result
# 		in a way that the result appears on computer after Roku TV broadcast

# TODO: Future issue - Starting program before game and having program
# 		become unstable from get_game_events()

import requests
import json
import subprocess as sp
from time import sleep 
from pprint import pprint as pp
from bs4 import BeautifulSoup

class MLB_Scrape():
	def __init__(self):
		# Class variables
		self.inning = 0
		self.t_or_b = 'top'
		self.atbat = '' 
		self.plays_json = ''
		self.sv_id = 0
		self.roster = {}
		self.play_data = {}


		# Game of interest URL components
		self.url = 'http://gd2.mlb.com/components/game/mlb/'
		self.year = '/year_2017'
		self.month = '/month_05'
		self.day = '/day_13'
		self.game = '/gid_2017_05_13_seamlb_tormlb_1' 
		self.game_url = (self.url + self.year + self.month +
						self.day + self.game)
		# Start up functions
		self.get_rosters()
		self.init_play_data()
	
	def init_play_data(self):
		'''
		This function sets up a dictionary which will hold
		all the information of interest
		'''
		self.play_data = {
					'inning':0,
					't_or_b':0,
					'batter':0,
					'p_type':'',
					'p_speed':0,
					'p_result': '',		
		}

	def get_plays_json(self):
		'''
		This function gets the game events JSON data from MLB.com	
		'''

		json_link = '/plays.json'
		r = requests.get(self.game_url + json_link)
		self.plays_json = json.loads(r.text) 

	def get_rosters(self):			
		'''
		This function gets the XML roster data and returns a dictionary
		which contains data about the player
		'''
		xml_link = '/players.xml'
		r = requests.get (self.game_url + xml_link)
		soup = BeautifulSoup(r.text, features='lxml-xml')

		home = soup.team
		away = home.find_next('team')

		teams = [away, home]
		p_info = {}
		rosters = {}
		for team in teams:

			for player in team.find_all('player'):
				id_num = player.get('id')
				f_name = player.get('first')
				l_name = player.get('last')
				p_info[id_num] = f_name + ' ' + l_name

			rosters = p_info

		self.roster = rosters
		
	def get_play_data(self):
		'''
		This functions gets information from the last thrown pitch
		This function also checks whether the data needs updating
		'''
		game = self.plays_json['data']['game']
		current_ab = game['atbat']
		try:
			n_pitches = len(current_ab['p']) - 1 # Minus 1 for zero-index
		except KeyError:
			return None
		try:
			last_pitch = current_ab['p'][n_pitches]
		except KeyError:
			return None	

		sv_id = int(last_pitch['sv_id'].replace("_", ""))

		if sv_id > self.sv_id:
			self.sv_id = sv_id

			self.play_data['p_type'] = last_pitch['pitch_type']
			self.play_data['p_speed'] = last_pitch['start_speed']
			self.play_data['p_result' ]= last_pitch['type']
			
			self.play_data['batter'] = game['players']['batter']['pid']

			return 'Need Update'

			self.play_data['inning'] = game['inning']
			self.play_data['t_or_b'] = game['top_inning']
		else:
			return None

	def pitch_update(self):
		'''
		This is the executive function that gets refreshed continuously
		'''
		self.get_plays_json()
		
		update =  self.get_play_data() 

		if update:
			# Assign dict values to variables for readability
			p_speed = self.play_data['p_speed']
			p_type = self.play_data['p_type']
			p_result = self.play_data['p_result']

			bat_id = self.play_data['batter']
			batter = self.roster[bat_id]
			
			print('Batter: {}'.format(batter))
			print('Pitch Speed: {} Pitch Type: {}'.format(p_speed, p_type))
			print('Result: {}'.format(p_result))

sp.call('clear',shell=True)
mlb = MLB_Scrape()
while True:
	mlb.pitch_update()
	sleep(3)
