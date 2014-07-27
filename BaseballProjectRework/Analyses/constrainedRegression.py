import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import leastsq, minimize
from stupidlySimplePredictions import get_data_from_file

# the 1.0 at the beginning will be for the intercept term
p0 = np.array([1.0, 0.0, 0.2, 0.3, 0.5])
#p0 = np.array([0.0, 0.2, 0.3, 0.5])

def pad(X):
	'''Add column of ones'''
	num_rows = np.size(X,0)
	eins = np.ones((num_rows,1))
	padded_X = np.concatenate((eins, X), axis=1)
	return padded_X

def residuals(p, y, X):
	'''Compute residual'''
	prod = p*X
	prodsum = prod.sum(axis=1)
	residual = np.zeros([np.size(y,0)])
	for i in range(np.size(residual,0)):
		residual[i] = y[i][0] - prodsum[i]
	return residual

def sum_sq_res(p, y, X):
	'''Compute sum of squared residuals'''
	prod = p*X
	prodsum = prod.sum(axis=1)
	residual = np.zeros([np.size(y,0)])
	for i in range(np.size(residual,0)):
		residual[i] = y[i][0] - prodsum[i]
	J = (residual**2).sum()
	return J
	
if __name__ == '__main__':
	X,y = get_data_from_file('HRminAB50minSeasons5.txt',5)
	#X = X[:,1:]
	X = pad(X)
	
	# unconstrained linear regression
	plsq = leastsq(residuals, p0, args=(y,X))
	
	# linear regression constrained to having coefficients sum
	# to one, so that the result is the optimal weighted average
	cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) -1})
	constrained = minimize(sum_sq_res, p0, args=(y,X), constraints=cons,
							method='SLSQP', options={'disp':True})
	
	# plot results
	unc_y = (X*plsq[0]).sum(axis=1)
	con_y = (X*constrained.x).sum(axis=1)
	goal = np.arange(0,.1,.01)
	plt.plot(unc_y,y,'ro',alpha=.5,label='Values predicted from unconstrained optimization')
	plt.plot(con_y,y,'bo',alpha=.5,label='Values predicted from constrained optimization')
	plt.plot(goal, goal, 'g-')
	plt.xlabel('Predicted values'); plt.xlim(0,.1)
	plt.ylabel('Actual values'); plt.ylim(0,.1)
	plt.legend(loc='upper left')
	plt.show()
	
	
	
