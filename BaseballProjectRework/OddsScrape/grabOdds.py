from bs4 import BeautifulSoup
import urllib2
from datetime import datetime

def saveOdds():
	'''
	This function will grab the html containing the daily odds from
	bovada's website
	'''
	
	# get the relevant html
	url = 'http://sports.bovada.lv/sports-betting/mlb-baseball-lines.jsp'
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html)
	odds_html = soup.find('div', {'id' : 'event-schedule'})

	# save file
	f_str = datetime.today().strftime('%m%d%Y') + 'odds.html'
	with open(f_str, 'w') as file:
		file.write(str(odds_html))	
		
if __name__ == '__main__':
	saveOdds()
