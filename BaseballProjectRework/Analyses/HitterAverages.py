'''

just playing around with some of the data obtained already

'''



from pymongo import Connection
from pylab import *

conn = Connection()
db = conn.PlayerStats
hitters = db.Players.find({'player_type':'hitter'})


for hitter in hitters:

	dat = hitter['CAREER BATTING STATISTICS']
	avgs = [float(dat[x]['AVG']) for x in dat.keys()
			if (float(dat[x]['AB']) > 150) & (str(x) != 'Season Averages') &
			(str(x) != 'Total')]
			# this should be modified to have something like a NaN if 
			# the condition is false
	
	figure(1)
	plot(avgs)
	


show()


