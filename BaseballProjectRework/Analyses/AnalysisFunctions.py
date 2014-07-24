from pymongo import Connection
import csv
from AnalysisFunctions import *
import numpy as np

def get_data(curs, stat_str, min_AB):
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
			if float(c_car[key]['AB']) > min_AB:
				stat_list.append((int(key),float(c_car[key][stat_str])/float(c_car[key]['AB'])))
		except:
			pass
		
	stat_list = sorted(stat_list)
	return stat_list

def write_normalized_stats_to_file(player_type, stat_str, min_AB, file_str):
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
		stat_list = get_data(curs, stat_str, min_AB)
		to_file = []
		for stat in stat_list:
			# stat = (year, stat)
			to_file.append(stat[1])
		
		with open(file_str,'a') as file:
			wr = csv.writer(file)
			wr.writerow(to_file)
			
def find_min_seasons(in_file, out_file, min_seasons):

	with open(in_file,'r') as file:
		lines = file.readlines()
		
	new_data = []
	
	for line in lines:
		data = line.strip('\r\n').split(',')
		if len(data) > min_seasons - 1:
			new_data.append([float(x) for x in data])
			
	with open(out_file,'w') as file:
		wr = csv.writer(file)
		for row in new_data:
			wr.writerow(row)
			
def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result[result.size/2:]





