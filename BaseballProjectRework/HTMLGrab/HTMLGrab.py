"""
This file gets all the stats from ESPN's main stats
page for each player.  Later files will get other 
stats from different pages (splits, and batting
stats for pitchers)
"""

import pymongo
from pymongo import Connection
from Functions import *

# create db connection
conn = Connection()
db = conn.PlayerStats	

# read in data
with open('UrlSet.txt', 'r') as file:
	lines = file.readlines()

# use to print out progress
num_lines = len(lines)
line_num = 1

# loop over all players in urlset
for line in lines:	
	line_num += 1
	if line_num > 383:		
		try:
			# print out progress
			print 'processing url ' + str(line_num) + ' out of ' + str(num_lines)
			base_url = line.strip('\n').strip('"')
			player_dict = careerStats(base_url)
			player_dict = splits(player_dict, base_url)

			if player_dict['player_type'] == 'pitcher':
				player_dict = pitcherBatting(player_dict, base_url)
	
			db.Stats.insert(player_dict)
		except:
			pass
	





	
