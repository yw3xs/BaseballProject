from pymongo import Connection
import csv
from AnalysisFunctions import *


# connect to db
c = Connection()
db = c.PlayerStats
cursor = db.Stats.find({'player_type':'hitter'})

for curs in cursor:
	stat_list = getData(curs, 'HR')
	to_file = []
	for stat in stat_list:
		to_file.append(stat[1])
		
	with open('hrdata.txt','a') as file:
		wr = csv.writer(file)
		wr.writerow(to_file)


