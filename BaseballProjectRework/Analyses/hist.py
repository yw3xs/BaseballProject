from pymongo import Connection
import csv
from AnalysisFunctions import *
import numpy as np
from matplotlib import pyplot as plt

# connect to db
c = Connection()
db = c.PlayerStats
cursor = db.Stats.find({'player_type':'hitter'})


len_list = []
for curs in cursor:
	stat_list = getData(curs, 'HR')
	len_list.append(len(stat_list))
	
	
bins = np.arange(min(len_list), max(len_list), 1)
plt.hist(len_list, bins=bins)
plt.show()
