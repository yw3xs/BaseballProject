from pymongo import Connection
import csv
from AnalysisFunctions import *

def getData(curs, stat_str):
	'''
	This function returns a list of  the statistic specified normalized 
	to the number of at bats in a given season (indexed by year)
	'''
	
	# find numeric keys and sort
	c_car = curs['CAREER BATTING STATISTICS']
	c_bat = c_car.keys()
	stat_list = []
	for key in c_bat:
		tup = ()
		# gather data in try/except loop because some keys represent
		# aggregate info already, i.e. 'Total' or 'Averages'
		try: 
			if float(c_car[key]['AB']) > 75:
				stat_list.append((int(key),float(c_car[key][stat_str])/float(c_car[key]['AB'])))
		except:
			pass
		
	stat_list = sorted(stat_list)
	return stat_list

def writeNormalizedStatsToFile(player_type, stat_str, file_str):
	'''
	Pass a player_type ('hitter' or 'pitcher'), and a stat_str such as HR 
	and this will write a csv file containing rows representing lists of 
	this players stat divided by the number of at bats in the season
	'''
	# connect to db
	c = Connection()
	db = c.PlayerStats
	cursor = db.Stats.find({'player_type':player_type})

	for curs in cursor:
		stat_list = getData(curs, stat_str)
		to_file = []
		for stat in stat_list:
			# stat = (year, stat)
			to_file.append(stat[1])
		
		with open(file_str,'a') as file:
			wr = csv.writer(file)
			wr.writerow(to_file)
			

