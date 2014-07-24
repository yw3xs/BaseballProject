
def get_hitters(box_dict):
	'''Get the list of hitters for the game'''
	home_hitters = [str(url) for url in box_dict['home hitters']]
	away_hitters = [str(url) for url in box_dict['away hitters']]
	return home_hitters, away_hitters
	
def get_pitchers(box_dict):
	'''Get the pitchers of the game'''
	home_pitcher = str(box_dict['home pitcher'])
	away_pitcher = str(box_dict['away pitcher'])
	return home_pitcher, away_pitcher
	
def get_winner(box_dict):
	'''Get the winner of the game'''
	home_score = int(box_dict['home scoring']['R'])
	away_score = int(box_dict['away scoring']['R'])
	if home_score > away_score:
		winner = 'Home'
	else:
		winner = 'Away'
	return winner
	

	

