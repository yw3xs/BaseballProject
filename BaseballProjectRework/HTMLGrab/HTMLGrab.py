'''

This file gets all the stats from ESPN's main stats
page for each player.  Later files will get other 
stats from different pages (splits, and batting
stats for pitchers)

'''


from Functions import *

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



	
