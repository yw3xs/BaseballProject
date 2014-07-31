from getGameInfo import *
from createHitterInputValues import *
from createPitcherInputValues import *
from pymongo import Connection
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
import matplotlib.pyplot as plt
import csv

c = Connection()
box_db = c.BoxScores
player_db = c.PlayerStats




## make datasets containing the stats for each game in each year
## the year in each line that it appears in can be changed

def make_data():
	'''This will create a text file of data to be used in logistic regression'''

	box_score_dicts = box_db.BoxScores2012.find()
	with open('logistic_games_2012_data.txt','w') as file:
		wr = csv.writer(file)
		
		for box_dict in box_score_dicts:
			try:
				home_hitters, away_hitters = get_hitters(box_dict)
				home_pitcher, away_pitcher = get_pitchers(box_dict)
				winner = get_winner(box_dict)

				hh_stats = []
				ah_stats = []
	
				for h_hitter, a_hitter in zip(home_hitters, away_hitters):
					hh = get_hitter(h_hitter, 2012, 'Home')
					ah = get_hitter(a_hitter, 2012, 'Away')

					hh_stats.extend(list(project_hitter(hh)))
					ah_stats.extend(list(project_hitter(ah)))
	
				hp = get_pitcher(home_pitcher, 2012, 'Home')
				ap = get_pitcher(away_pitcher, 2012, 'Away')
	
				hp_stats = list(project_pitcher(hp))
				ap_stats = list(project_pitcher(ap))
	
	
				# w=0 -> away win, w=1 -> home win
				w = 0 
				if winner == 'Home':
					w = 1
			
				data = []
				data.extend(hh_stats)
				data.extend(ah_stats)
				data.extend(hp_stats)
				data.extend(ap_stats)
				data.extend([w])
				wr.writerow(data)
			except: 
				print 'darn it'
	
			
def regress(X,y):
	
	model = linear_model.LogisticRegression(penalty='l2')
	model.fit(X,y)
	return model


if __name__ == '__main__':

	# make model
	data = np.loadtxt('logistic_training_data.txt', dtype='float', delimiter=',')
	X = data[:,:-1]
	y = data[:,-1]
					
	X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.5,random_state=123)
	model = regress(X_train,y_train)
	
	print 'Training set accuracy: {}'.format(model.score(X_train,y_train))
	print 'Test set accuracy: {}'.format(model.score(X_test,y_test))
	
	
	file_list = ['logistic_games_2008_data.txt','logistic_games_2009_data.txt',
				'logistic_games_2010_data.txt', 'logistic_games_2011_data.txt',
				'logistic_games_2012_data.txt']
			
	# get all the data in the files listed above - this got a bit messy because
	# the make_data function put in some data that was incomplete in each file
	# so this code will deal with that.  
	all_data = []
	for file_str in file_list:
		with open(file_str,'r') as file:
			for line in file:
				sp_line = line.split(',')
				if len(sp_line) == 321:
					all_data.append([float(x) for x in sp_line])
	
	# make arrays to be input to the model created above
	all_data_array = np.array(all_data)
	X_all = all_data_array[:,:-1]
	y_all = all_data_array[:,-1]
	
	
	# make predictions
	y_pred = model.predict(X_all)
	predicted_probs_pair = model.predict_proba(X_all)
	test_size = np.size(y_pred)
	
	# find correct predictions
	correct_prediction = y_pred == y_all
	
	# reduce predicted_probs_pair to a single value containing
	# the maximum of each pair - corresponds to the probability
	# assigned to either a 0 or 1 for a given game.
	predicted_probs = np.zeros(test_size)
	for i in range(test_size):
		predicted_probs[i] = max(predicted_probs_pair[i,:])
		
		
	# bin the probabilities in increments of a specified percent
	bins = np.arange(.5,1,.025) # last argument is the specified percent
	bin_index = np.digitize(predicted_probs, bins)
	pred_probs_dig = np.zeros(np.size(bin_index))
	for i in range(test_size):
		pred_probs_dig[i] = bins[bin_index[i]]
		
	# create array of predicted probabilities and success or not (1 or 0)
	pred_data = np.array([pred_probs_dig, correct_prediction]).transpose()
	
	# calculate the percent of successes as a function of predicted percent
	calib_probs = np.zeros(np.shape(bins))
	weights = np.zeros(np.shape(bins))
	for i in range(np.size(bins)):
		subset = pred_data[pred_data[:,0]==bins[i]]
		weights[i] = np.size(subset,0)
		if weights[i] > 0:
			calib_probs[i] = float(sum(subset[:,1]))/weights[i]
		
	# non zero values for calib_probs
	nz_weights = weights[calib_probs!=0]
	nz_bins = bins[calib_probs!=0]
	nz_calib_probs = calib_probs[calib_probs!=0]

	## nz_bins are the predicted probabilities and nz_calib_probs are the
	## observed probabilities.  if multiplied by nz_weights, this interpretation
	## is transformed to predicted number of games won, and observed number of
	## games won.  this will more properly account for the number of calculations
	## involved in each data point when using pearsonr, for example
		
	## a bit of visualization
	
	fig1 = plt.figure(1)
	plt.plot(nz_weights*nz_bins,nz_weights*nz_calib_probs,'o')
	plt.xlabel('Predicted number of games won')
	plt.ylabel('Actual number of games won')
	plt.title('Number of games won per probability bin')
	plt.show()
	


		
	

















	

