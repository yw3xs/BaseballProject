from bs4 import BeautifulSoup
import urllib2
import pymongo
import re, string

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

def generateURLS(url):
    """Generate urls appropriate to player type"""
    return urls

def getTableData(table):
    """Get title, column heads, and data from table"""
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


def dbInsert(base_url):
	"""Insert data into a mongodb instance
	
	this will take the base_url and creat the url where the stats are contained,
	it will get the stats and create a document for mongodb
	"""
	
	url = base_url.replace('player/','player/stats/') # stats are here
	clean_url = re.sub('[%s]' % re.escape(string.punctuation), '', base_url) # use as _id
	
	# get the tables containing stats using beautiful soup
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html)
	tables = soup('table', {'class' : 'tablehead'})

	
	

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
	base_response = urllib2.urlopen(base_url)
	base_html = base_response.read()
	base_soup = BeautifulSoup(base_html)
	header_stat_table = base_soup.find('table', {'class' : 'header-stats'})
	player_type = playerType(str(header_stat_table))

	# create the rest of the player_dict entries
	player_dict['player_type'] = player_type
	player_dict['base_url'] = base_url
	player_dict['_id'] = clean_url
	player_dict['name'] = base_url.split('/')[-1].replace('-', ' ') # get player name from end of url
    	
    	
    # put document in mongodb instance	
	conn = pymongo.MongoClient()
	db = conn.PlayerStats
	db.Players.insert(player_dict)


# loop over all players in urlset

with open('UrlSet.txt', 'r') as file:
	lines = file.readlines()

num_lines = len(lines)
line_num = 1

for line in lines:	
	# print out progress
	print 'processing url ' + str(line_num) + ' out of ' + str(num_lines)
	dbInsert(line.strip('\n').strip('"'))	
	line_num += 1

#dbInsert('http://espn.go.com/mlb/player/_/id/30836/mike-trout')
#dbInsert('http://espn.go.com/mlb/player/_/id/6194/felix-hernandez')
#dbInsert('http://espn.go.com/mlb/player/_/id/1720/ruben-sierra')



	
