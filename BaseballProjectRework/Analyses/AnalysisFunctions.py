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
			stat_list.append((int(key),float(c_car[key][stat_str])/float(c_car[key]['AB'])))
		except:
			pass
		
	stat_list = sorted(stat_list)
	return stat_list
