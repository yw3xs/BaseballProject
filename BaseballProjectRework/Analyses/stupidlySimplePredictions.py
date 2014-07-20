import csv
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import pearsonr

## call these functions on files created using AnalysisFunctions.py

def getSomeDataFromFile(file_str):
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
			data.append([float(x) for x in row[:5]])
			
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
	mse = (np.mean(pred_errors1**2), np.mean(pred_errors2**2))
	R = (pearsonr(y,pred_y1)[0], pearsonr(y,pred_y2)[0])
	zipper2 = zip(values2, colors, labels, R, mse)
	
	fig2 = plt.figure(2)
	for i in range(2):
		plt.plot(zipper2[i][0], y, 'o',
			color=zipper2[i][1],
			alpha=0.4,
			label='%(label)s, R = %(r).2f, MSE = %(mse).6f' % 
					{'label':zipper2[i][2], 'r':zipper2[i][3], 'mse':zipper2[i][4]}
					)
	
	plt.legend(loc='upper left')
	plt.title('Actual Values vs. Predicted Values')
	plt.xlabel('Predicted values')
	plt.ylabel('Actual values')

	plt.show()
	
def main():
	X, y = getSomeDataFromFile('fiver_year_guys.txt')
	
	pred_y1, pred_errors1 = predict_y(X, y)
	pred1_disc = 'Prediction using all previous seasons'
	pred_y2, pred_errors2 = predict_y(X[:,np.size(X,1)-1], y)
	pred2_disc = 'Prediction using only most recent season'
	
	compare_predictions(y, pred_y1, pred_errors1, pred1_disc, pred_y2, pred_errors2, pred2_disc)
	
if __name__ == '__main__':
	main()


## next will be to make one prediction using regression with training and test set,
## and one prediction using time series forcasting methods
	
	
	
	
	
	
	
	
	

	
