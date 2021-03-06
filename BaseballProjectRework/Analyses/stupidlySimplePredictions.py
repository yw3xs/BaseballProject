import csv, sys
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import pearsonr
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
from math import sqrt

## call these functions on files created using AnalysisFunctions.py

def get_data_from_file(file_str, num_years):
	'''
	Read in some time series data; the last value in each row
	is the value we want to predict, the preceding values are
	the data to be used in making the prediction.  The last
	values will be returned in y, the usable data will be 
	returned in X
	'''
	data = []
	with open(file_str,'r') as csvfile:
		all_data = csv.reader(csvfile)
		for row in all_data:
			data.append([float(x) for x in row[:num_years]])
	row_length = len(data[0])
	X = np.zeros([len(data),row_length-1])
	y = np.zeros([len(data),1])
	
	for i in range(len(data)):
		X[i,:] = data[i][0:row_length-1]
		y[i] = data[i][-1]
	
	return X, y
	
def predict_y(X, y):
	'''
	Use some values, X, to predict some values y using averages.
	Returns	predicted values of y and prediction errors.  X can 
	have any number of columns.
	'''
	
	# initialize arrays
	predicted_y = np.zeros([len(y),1])
	prediction_errors = np.zeros([len(y),1])
	
	# calculate averages and prediction errors
	#predicted_y = np.mean(X,1) # mean of each row
	for i in range(len(y)):
		predicted_y[i] = np.mean(X[i])
	prediction_errors = y - predicted_y
		
	return predicted_y, prediction_errors
	
def compare_predictions(y, pred_y1, pred_errors1, pred1_disc, pred_y2, pred_errors2, pred2_disc):
	'''
	Compare some predictions. Include predictions, prediction errors, and a 
	description of each prediction to be used as a label
	'''
	
	# calculate R squared
	ssr1 = sum(pred_errors1**2)
	ssr2 = sum(pred_errors2**2)
	sst = sum((y-np.mean(y))**2)
	R21 = 1-ssr1/sst
	R22 = 1-ssr2/sst
	
	
	# make histogram
	maxim = max(max(pred_errors1), max(pred_errors2))
	minim = min(min(pred_errors1), min(pred_errors2))
	bin_size = (maxim - minim)/50
	bins = np.arange(minim, maxim, bin_size)
	
	values1 = (pred_errors1, pred_errors2)
	colors = ('blue', 'green')
	labels = (pred1_disc, pred2_disc)
	zipper1 = zip(values1, colors, labels)
	
	fig1 = plt.figure(1)
	for i in range(2):
		plt.hist(zipper1[i][0],
				bins=bins,
				color=zipper1[i][1],
				alpha=0.4,
				label=zipper1[i][2])
		
	plt.legend(loc='upper left')
	plt.xlabel('Prediction error')
	plt.title('Prediction Error Histogram')
	
	# make scatter plot
	values2 = (pred_y1, pred_y2)
	rmse = (sqrt(np.mean(pred_errors1**2)), sqrt(np.mean(pred_errors2**2)))
	r = (pearsonr(y,pred_y1)[0], pearsonr(y,pred_y2)[0])
	R2 = (R21, R22)
	zipper2 = zip(values2, colors, labels, r, rmse, R2)
	
	fig2 = plt.figure(2)
	for i in range(2):
		plt.plot(zipper2[i][0], y, 'o',
			color=zipper2[i][1],
			alpha=0.4,
			label='%(label)s \nr = %(r).2f\nRMSE = %(rmse).3f \nR Squared = %(R2).03f' % 
					{'label':zipper2[i][2], 'r':zipper2[i][3], 'rmse':zipper2[i][4], 'R2':zipper2[i][5]}
					)
	
	goal = np.arange(0,.2,.001)
	plt.plot(goal,goal,'g-')
	plt.legend(loc='upper left')
	plt.title('Actual Values vs. Predicted Values Using Averages')
	plt.xlabel('Predicted values')
	plt.ylabel('Actual values')
	
def regression_fun(X,y):
	'''Run linear regression on linear and quadratic input data'''
	
	# linear regression with linear input parameters
	X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.3,random_state=123)
	
	clf1 = linear_model.LinearRegression(normalize=True)
	#clf1 = linear_model.Ridge(alpha=.25)
	clf1.fit(X_train, y_train)
	
	R2_train = clf1.score(X_train, y_train)
	R2_test = clf1.score(X_test, y_test)
	
	y_pred = clf1.predict(X_test)
	r = pearsonr(y_pred, y_test)[0]
	rmse = sqrt(np.mean((y_pred-y_test)**2))
	
	goal = np.arange(0,.2,.001)
	label_str = 'Linear inputs \nr = %(r).2f \nRMSE = %(rmse).3f \nR squared = %(R2_test).2f' % {
				'r':r, 'rmse':rmse, 'R2_test':R2_test}
	fig3 = plt.figure(3)
	plt.plot(y_pred, y_test, 'bo', alpha=.3, label=label_str)
	
	print 'Linear regression coefficients using sklearn: '
	print clf1.coef_
	
	plt.plot(goal, goal, 'g-')
	plt.title('Actual Values vs. Predicted Values using Regression')
	plt.xlabel('Predicted value')
	plt.ylabel('Actual value')
	plt.legend(loc='upper left')
		
	
def main():
	
	command = sys.argv[1]
	f_string, num_years = command.split()
	num_years = int(num_years)
		
	X, y = get_data_from_file(f_string, num_years)
	
	# use all past data
	pred_y1, pred_errors1 = predict_y(X, y)
	pred1_disc = 'Prediction using all previous seasons'
	
	# use only previous year
	pred_y2, pred_errors2 = predict_y(X[:,np.size(X,1)-1], y)
	pred2_disc = 'Prediction using only most recent season'
	
	compare_predictions(y, pred_y1, pred_errors1, pred1_disc, pred_y2, pred_errors2, pred2_disc)
	
	# use regression models
	regression_fun(X,y)
	
	# plot stuff
	plt.show()
	
if __name__ == '__main__':
	main()


## next will be making prediction based on time forecasting methods
	
	
	
	
	
	
	
	
	

	
