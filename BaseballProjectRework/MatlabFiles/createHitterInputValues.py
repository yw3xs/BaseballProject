import numpy as np
import pymongo
from pymongo import Connection

## define global variables

# database stuff
c = Connection()
hitter_db = c.PlayerStats

# keys for needed stats
ab_key = 'AB' # everything will be divided by this
stat_keys = ['BB', '2B', '3B', 'HR', 'SO', 'H'] # CAREER (or Home/Away)
mi_stat_keys = ['GB', 'FB'] # MISCELLANEOUS

# minimum number of at bats
threshold = 50

# average seasons; use if ab < threshold 
avg_career = np.zeros([1,8])
avg_home = np.zeros([1,8])
avg_away = np.zeros([1,8])

# rookie stats
rookie_stats = np.array([0.0756507847, 0.1612630392, 0.0483305812, 0.0071690362,	
							0.0241384403, 0.2034180461,	0.2230187818, 0.2570112906])

## define functions

def get_season(season_dict, mi_season_dict):
	'''This will get all of the relevant stats from a given season.'''
	
	season = np.zeros(8)
		
	stats = [float(season_dict[stat_key]) for stat_key in stat_keys]
	# seasons prior to 04 dont' have groundball flyball stats
	try:
		mi_stats = [float(mi_season_dict[mi_key]) for mi_key in mi_stat_keys]
	except:
		mi_stats= [100.0, 100.0]
		
	ab = float(season_dict[ab_key]) + stats[0] # total of listed at bats and walks
	
	if ab < threshold:
		season = rookie_stats
	else:
		# calculate singles
		singles = stats[5] - (stats[1] + stats[2] + stats[3])
	
		# calculate ground outs and fly outs
		outs = ab - (stats[5] + stats[0] + stats[4])
		GOs = mi_stats[0]*outs/sum(mi_stats)
		FOs = mi_stats[1]*outs/sum(mi_stats)
	
		season = np.array([stats[0], singles, stats[1], stats[2], stats[3], 
						stats[4], GOs, FOs])/ab
	
	return season

def get_season_keys(potential_keys, current_year):
	'''
	Get the list of years available up to current_year.  This function
	must separate out the entries corresponding to 'Totals' and 'Averages'.
	It returns a list of integers.
	'''
	key_list = []
	for potential_key in potential_keys:
		# try/except to avoid aggregate entries such as totals or averages
		try:
			year = int(potential_key)
			if year < current_year:
				key_list.append(year)
		except:
			pass
	
	return key_list

def get_hitter(player_url, current_year, location):
	'''
	This function will get all of the stats needed for a given hitter.  It
	will get stats through the years prior to 'current_year'.  It will return
	an array of years as rows and 16 columns corresponding to the 8 career 
	statistics and 8 home or away statistics as determined by 'location', which
	is either 'Home' or 'Away'.
	'''
	
	player = hitter_db.Stats.find_one({'base_url':player_url})
	
	
	ca_potential_keys = player['CAREER BATTING STATISTICS'].keys()
	# get list of years player has played - these keys are currently ints
	ca_keys = get_season_keys(ca_potential_keys, current_year)
	# make list of keys for getting home/away stats
	split_keys = [str(key) + ' Batting Splits' for key in ca_keys]
		
	
	num_years = len(ca_keys)
	stat_array = np.zeros([num_years, 16])
	
	for i in range(len(ca_keys)):
		try:
			# Career
			ca_key = str(ca_keys[i]) # make key str again
			sp_key = split_keys[i]
			ca_season_dict = player['CAREER BATTING STATISTICS'][ca_key] 
			mi_season_dict = player['MISCELLANEOUS BATTING'][ca_key]
			ca_season = get_season(ca_season_dict, mi_season_dict)
		except:
			ca_season = rookie_stats
			
		stat_array[i,:8] = ca_season
			
		try:
			# Home/Away
			sp_season_dict = player['Splits'][sp_key][location]
			sp_season = get_season(sp_season_dict, mi_season_dict)
		except:
			sp_season = rookie_stats
			
		stat_array[i,8:] = sp_season
		
	return stat_array

def project_hitter(stat_array):
	
	# this can be modified based on results of regression analysis
	averager = np.array([[.2],[.3],[.5]])
	
	num_rows = np.size(stat_array,0)
	if num_rows >= 3:
		projected_hitter = np.sum(stat_array[(num_rows-3):,:]*averager,0)
	else:
		pad = np.tile(rookie_stats,(3-num_rows,2))
		padded_hitter = np.concatenate((pad, stat_array), axis=0)
		projected_hitter = np.sum(padded_hitter*averager,0)
		
	return projected_hitter
		
		
		
		
		
		
		
		
		
		
	
	
