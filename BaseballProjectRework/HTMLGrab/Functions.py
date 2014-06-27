from bs4 import BeautifulSoup
import urllib2
import re, string


"""
These are the functions called by the files in this folder that are
being used to create the database (mongo) of player statistics
"""


def playerType(tablestring):
    """Hitter or pitcher?

    give this function the table with class 'header-stats' in order to
    determine whether the player is a hitter or pitcher
    """
    if tablestring.find('AVG') > 0:
		player_type = 'hitter'
    else:
		player_type = 'pitcher'
    return player_type
    

def getTableData(table):
    """Get title, column heads, and data from table with class 'tablehead'"""
    title = table.find('tr', {'class' : 'stathead'}).find('td').renderContents()
    header_row = table.find('tr', {'class' : 'colhead'})
    col_heads = []
    for td in header_row('td'):
    	col_heads.extend([td.renderContents()])
    
    data = table.findAll('tr', {'class' : ['evenrow', 'oddrow']})
    data_rows = []
    for tr in data:
    	row = []	
    	for td in tr('td'):
    		row.extend([td.renderContents()])
    	
    	data_rows.append(row)

    return title, col_heads, data_rows

def makeSoup(url, tag, css_class):
	"""
	This function takes a url and gets the elements specified by tag with an optional
	css class specified
	"""
	
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html)
	
	if css_class == None:
		element = soup(tag)
	else:
		element = soup(tag, {'class' : css_class})
		
	return element

def removePunct(dirty_string):
	"""This function removes punctuation from a string"""
	
	clean_string = re.sub('[%s]' % re.escape(string.punctuation), '', dirty_string)
	return clean_string


def careerStats(base_url):
	"""
	this will take the base_url and creat the url where the stats are contained,
	it will get the stats and create a document for later insertion into mongodb
	"""
	
	url = base_url.replace('player/','player/stats/') # stats are here
	clean_url = removePunct(base_url) # use as _id
	
	# get the tables containing stats using beautiful soup
	tables = makeSoup(url, 'table', 'tablehead')

	player_dict = {}

	for table in tables:    
    
		title, col_heads, data_rows = getTableData(table)
    
		season_dict = {}
		for row in data_rows:
			data_dict = {}
			for col in range(len(row)):
				data_dict[col_heads[col]] = row[col]
    	
			season_dict[str(data_dict[col_heads[0]])] = data_dict

    	# there are two tables called 'MISCELLANEOUS', this block makes sure
    	# the second one doesn't simply replace the first in the dict
		try: 
			for season in season_dict.keys():
				if ((season != 'Total') & (season != 'Season Averages')):
					player_dict[title][season].update(season_dict[season])
		except:
			player_dict[title] = season_dict
    

	# find out if player is a hitter or pitcher
	header_stat_table = makeSoup(base_url, 'table', 'header-stats')
	player_type = playerType(str(header_stat_table))

	# create the rest of the player_dict entries
	player_dict['player_type'] = player_type
	player_dict['base_url'] = base_url
	player_dict['_id'] = clean_url
	player_dict['name'] = base_url.split('/')[-1].replace('-', ' ') # get player name from end of url
	
	return player_dict
	
	
def splits(player_dict, base_url):
	"""
	This function is to be called after careerStats, it will take the previously 
	created player_dict and update it with each players splits, for pitchers, it
	will get both pitching and batting splits, but earlier years wont' have batting
	splits which will return an error that should be caught by the try/except
	"""
	
	# this url modification gets splits
	url = base_url.replace('player/','player/splits/')
	
	# get list of urls containing splits
	options = makeSoup(url, 'option', css_class = None)
	splits = []
	for option in options:
		if option.has_attr('value'):
			if (option['value'].find('splits') > 0) & (option['value'].find('year') > 0):
				splits.append(str(option['value']))


	split_dict = {}

	for split in splits:
	
		try:

			tables = makeSoup(split, 'table', 'tablehead')
		
			title, col_heads, data_rows = getTableData(tables[0])
			season_dict = {}
			season_dict['url'] = split
    
			for row in data_rows:
				data_dict = {}
				for col in range(len(row)):
					data_dict[col_heads[col]] = row[col]
				data_key = removePunct(row[0])
				season_dict[data_key] = data_dict
		
			split_dict[title.strip('\n')] = season_dict	
			
		except:
			print 'error with ' + split + ', printing url to file...'
			with open('split_errors.txt','a') as file:
				file.write(split + '\n')
	
	player_dict['Splits'] = split_dict
	return player_dict
	

def pitcherBatting(player_dict, base_url):
	"""
	This function will be called after splits and should be wrapped in an
	if statement to determine first whether or not the player is a pitcher.
	"""
	
	# this url modification gets pitchers batting stats page
	# http://espn.go.com/mlb/player/_/id/6194/felix-hernandez
	# http://espn.go.com/mlb/player/stats/_/id/6194/type/batting/felix-hernandez
	url = base_url.replace('player/','player/stats/')
	index = url.rfind('/') + 1
	url = url[0:index] + 'type/batting/' + url[index:]
	
	tables = makeSoup(url, 'table', 'tablehead')


	try:
		
		for table in tables:    
    
			title, col_heads, data_rows = getTableData(table)
    
			season_dict = {}
			for row in data_rows:
				data_dict = {}
				for col in range(len(row)):
					data_dict[col_heads[col]] = row[col]
    	
				season_dict[str(data_dict[col_heads[0]])] = data_dict

    		# there are two tables called 'MISCELLANEOUS', this block makes sure
	    	# the second one doesn't simply replace the first in the dict
			try: 
				for season in season_dict.keys():
					if ((season != 'Total') & (season != 'Season Averages')):
						player_dict[title][season].update(season_dict[season])
			except:
				player_dict[title] = season_dict
	
	except:
		print 'error with ' + url + ', print url to file...'
		with open('pitcher_hitting_errors.txt','a') as file:
			file.write(url + '\n')
	
	return player_dict
	
    	






