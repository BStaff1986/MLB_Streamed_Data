#!python3

# mlb.py :  Program to read and display MLB JSON Data

# TODO: BIGGEST ISSUE! - Only last pitch in atbat appears. MLB Json not quick enough?
#       Or better algo needs to be written?

# TODO: Future issue - Starting program before game and having program
# 		become unstable from get_game_events()
# TODO: Perhaps move current atbat function into pitch_update
#		and return it's value to class variables so multiple functions
# 		have access without needing to call it multiple times
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
		self.pitch_id = 0
		self.json_events = ''
		self.roster = {}

		# Game of interest URL components
		self.url = 'http://gd2.mlb.com/components/game/mlb/'
		self.year = '/year_2017'
		self.month = '/month_05'
		self.day = '/day_12'
		self.game = '/gid_2017_05_12_detmlb_anamlb_1' 
		self.game_url = (self.url + self.year + self.month +
						self.day + self.game)
		# Start up functions
		self.get_rosters()
		
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
		self.inning = len(inning) - 1
		
		if not inning[self.inning]: 
			self.t_or_b = 'top'
		else:
			self.t_or_b = 'bottom'

		
	def get_current_atbat(self):
		'''
		This function gets the data from the last pitch
		'''
		t_or_b, inn_num = self.t_or_b, self.inning
		try:
			atbat = self.json_events['data']['game']['inning'][inn_num][t_or_b]['atbat']
		except: # Find the name of the error and make this stronger!
			return None
		
		self.atbat = atbat[len(atbat) -1]
		
	def get_last_pitch(self):
		'''
		This function gets the pitch speed and type from the most
		recent pitch
		'''

		pitches = self.atbat['pitch']
		last_pitch = pitches[len(pitches) -1]
		
		sv_id = int(last_pitch['sv_id'].replace('_',""))
		
		if sv_id > self.pitch_id:
			pitch_speed = last_pitch['start_speed']
			pitch_type = last_pitch['pitch_type']
			self.pitch_id = sv_id
			return pitch_speed, pitch_type
		else:
			return None, None

		

	def pitch_update(self):
		'''
		This is the executive function that gets refreshed continuously
		'''
		self.get_game_events()
		# Get and check inning
		self.get_inning()
		# Get and check atbat event num
		self.get_current_atbat()
		# Get and check pitch sv_id num

		speed, p_type = self.get_last_pitch()
		if speed == None and p_type == None:
			print('No pitch thrown in this atbat')
		else:
			print('Pitch Speed: {} Pitch Type: {}'.format(speed, p_type))



sp.call('clear',shell=True)
mlb = MLB_Scrape()
while True:
	mlb.pitch_update()
	sleep(3)
