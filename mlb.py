# Program to read MLB JSON Data

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
		self.ab_num = 0
		self.pitch_id = 0
		self.json_events = ''
		self.roster = {}

		self.url = 'http://gd2.mlb.com/components/game/mlb/'
		self.year = '/year_2017'
		self.month = '/month_05'
		self.day = '/day_11'
		self.game = '/gid_2017_05_11_detmlb_anamlb_1' 
		self.game_url = (self.url + self.year + self.month +
						self.day + self.game)
		print(self.game_url)

	def get_game_events(self):
		'''
		This function gets the game events JSON data from MLB.com	
		'''

		json_link = '/game_events.json'
		r = requests.get(self.game_url + json_link)
		self.json_events = json.loads(r.text) 

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
		rosters = {}
		p_info = {}
		for team in teams:
			team_name = team.get('id')
			for player in team.find_all('player'):
				id_num = player.get('id')
				f_name = player.get('first')
				l_name = player.get('last')
				p_info[id_num] = f_name + ' ' + l_name

				rosters[team_name] = p_info

		return soup, home, away, rosters

	def get_inning(self):
		'''
		This function parses the XML data finds the current inning
		'''
		inning = self.json_events['data']['game']['inning']
		inning_num = len(inning) - 1
		
		if not inning[inning_num]: 
			top_or_bottom = 'top'
		else:
			top_or_bottom = 'bottom'
		
		return (top_or_bottom, inning_num)

	def get_current_atbat(self):
		'''
		This function gets the data from the last pitch
		'''
		t_or_b, inn_num = self.get_inning()
		try:
			atbat = self.json_events['data']['game']['inning'][inn_num][t_or_b]['atbat']
		except: # Find the name of the error and make this stronger!
			return None
		
		current_atbat = atbat[len(atbat) -1]
		
		return current_atbat
	
	def get_last_pitch(self):
		'''
		This function gets the pitch speed and type from the most
		recent pitch
		'''
		current_ab = self.get_current_atbat()

		pitches = current_ab['pitch']
		last_pitch = pitches[len(pitches) -1]
		
		pitch_speed = last_pitch['start_speed']
		pitch_type = last_pitch['pitch_type']

		return pitch_speed, pitch_type

	def pitch_update(self):
		'''
		This is the executive function that gets refreshed continuously
		'''
		self.get_game_events()
		speed, p_type = self.get_last_pitch()

		print('Pitch Speed: {} Pitch Type: {}'.format(speed, p_type))



sp.call('clear',shell=True)
mlb = MLB_Scrape()
mlb.pitch_update()

ros, away, home, dic = mlb.get_rosters()
