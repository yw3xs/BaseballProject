from bs4 import BeautifulSoup
import urllib2
import pymongo
import re

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



#url = 'http://espn.go.com/mlb/player/stats/_/id/30836/mike-trout'
url = 'http://espn.go.com/mlb/player/stats/_/id/6194/felix-hernandez'
response = urllib2.urlopen(url)
html = response.read()

soup = BeautifulSoup(html)

tables = soup('table', {'class' : 'tablehead'})
header_stat_table = soup.find('table', {'class' : 'header-stats'})

	
conn = pymongo.MongoClient()
db = conn[url.replace('.','').replace('/','').replace(':','')] # needs to be a better way to do this...

for table in tables:
    
    title, col_heads, data_rows = getTableData(table)
    
    for row in data_rows:
    	data_dict={}
    	for col in range(len(row)):
    		data_dict[col_heads[col]] = row[col]
    	db[title].insert(data_dict)




	
