'''
This file is meant to retrieve box scores and relevant information
to be used in testing of various models for predicting the outcomes
of baseball games

'''


from Functions import *
from pymongo import Connection
import sys, traceback

def getStarters(table):
	'''
	This function gets urls of all the starting hitters which are used
	as identifiers in the database
	'''
	
	starters = []
	rows=table('tr')
	for row in rows:
		rurl = re.search(r'href="([\S]+)"', str(row))
		
		# these strings indicate that this isn't a starter
		bad_str_1 = str(row).find('padding')
		bad_str_2 = str(row).find(chr(160))
		
		# get starters
		if (rurl) and (bad_str_1 <= 0) and (bad_str_2 <= 0):
			starters.append(rurl.group(1))
	return starters


def boxScoreUnwrap(tr):
	'''This function gets the box score information'''
	
	score = []
	for i in range(len(tr('td'))):
		td = tr('td')[i]
		if i == 0:
			# this should contain the team name
			score.append(td.find('a').renderContents())
		else:
			# this should contain the score for each inning
			s = re.search(r'([\d-]+)', td.renderContents())
			score.append(s.group(1))
			
	return score

def boxScoreGrabber(url):
	'''
	This function creates a dictionary with all the information
	needed to compile the information for the simulation
	'''
	
	doc = {}
	id_str = removePunct(url)
	doc['_id'] = id_str
	doc['url'] = url
	
	
	# get the tables containing info on what players to use
	tables = makeSoup(url, 'table', css_class = 'mod-data mlb-box')

	# store tables in doc
	doc['away hitters'] = getStarters(tables[0])
	doc['home hitters'] = getStarters(tables[2])
	doc['away pitcher'] = getStarters(tables[1])[0]
	doc['home pitcher'] = getStarters(tables[3])[0]
	
	# get table with boxscore in it
	line_score = makeSoup(url, 'table', css_class = 'linescore')

	# get column heads of boxscore table
	col_heads = []
	head_row = line_score[0].find('tr', {'class' : 'periods'})
	for td in head_row('td'):
		col_heads.extend([td.renderContents()])
	col_heads[0] = 'Team'
	scores = line_score[0]('tr')[1:]

	# unwrap away and home boxscore entries
	away_score = boxScoreUnwrap(scores[0])
	home_score = boxScoreUnwrap(scores[1])	
	
	away_score_dict = {}
	home_score_dict = {}
	
	for col in range(len(col_heads)):
		away_score_dict[col_heads[col]] = away_score[col]
		home_score_dict[col_heads[col]] = home_score[col]
		
	doc['away scoring'] = away_score_dict
	doc['home scoring'] = home_score_dict

	return doc
	
	
# run everything and stick it in mongodb
# this was run one year at a time and the year
# appearing below was updated each time manually
	
if __name__ == '__main__':
	c = Connection()
	db = c.BoxScores	

	with open('Urls2013.txt','r') as file:
		lines = file.readlines()

	i = 1
	for line in lines:
		print 'processing url ' + str(i) + ' out of ' + str(len(lines))
		i += 1
		url = line.strip('\n').strip('"')
		try:
			doc = boxScoreGrabber(url)
			db.BoxScores2013.insert(doc)
		except:
			# record errors
			print 'error with ' + url
			exc_type, exc_value, exc_traceback = sys.exc_info()
			with open('box score errors 2013.txt','a') as f:
				f.write(url + '\n')
				traceback.print_tb(exc_traceback, file=f)
			pass
		


