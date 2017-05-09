# Program to read MLB JSON

import requests
import json


def get_play_data():
    url = 'http://gd2.mlb.com/components/game/mlb/'
    year = '/year_2017'
    month = '/month_05'
    day = '/day_08'
    game = '/gid_2017_05_08_clemlb_tormlb_1/plays.json'
    r = requests.get(url + year + month + day + game)
    data = json.loads(r.text)
    return data	


def print_count(json):
    print('Balls: {data[b]} Strikes: {data[s]} Outs: {data[o]}'.format\
    (data=json['data']['game']))

data  = get_play_data()

print_count(data)
