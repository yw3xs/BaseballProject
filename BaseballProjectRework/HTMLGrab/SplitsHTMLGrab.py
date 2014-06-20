'''

This file gets each players splits page's stats
from ESPN

'''

# still debugging, it isn't quite processing the
# html correctly

from Functions import *

conn = Connection()
db = conn.PlayerStats

player = db.Players.find({'name': 'mike trout'})
url = player[0]['base_url'].replace('player/','player/splits/')

print str(url)

response = urllib2.urlopen(url)
html = response.read()
soup = BeautifulSoup(html)
options = soup('option')

splits = []

for option in options:
	if option.has_attr('value'):
		if (option['value'].find('splits') > 0) & (option['value'].find('year') > 0):
			print option['value']
			splits.append(str(option['value']))

splits_dict = {}
			
for split in splits:
	split_response = urllib2.urlopen(split)
	split_html = split_response.read()
	split_soup = BeautifulSoup(split_html)
	tables = split_soup('table', {'class' : 'tablehead'})
	
	season_dict = {}
	
	for table in tables:    
	
		title, col_heads, data_rows = getTableData(table)
    
		for row in data_rows:
			data_dict = {}
			for col in range(len(row)):
				data_dict[col_heads[col]] = row[col]
    		key = re.sub('[%s]' % re.escape(string.punctuation), '', str(row[0]))
    		season_dict[key] = data_dict
		
	splits_dict[title.strip('\n')] = season_dict
	splits_dict[title.strip('\n')]['url'] = split
	
	
db.TestCollection.insert(splits_dict)
    	