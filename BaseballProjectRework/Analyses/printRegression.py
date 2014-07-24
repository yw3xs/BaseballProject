import sys
import numpy as np
from pandas import DataFrame
from ast import literal_eval
import statsmodels.formula.api as sm
from sklearn.cross_validation import train_test_split
from stupidlySimplePredictions import get_data_from_file


command = sys.argv[1]
f_string, num_years = command.split()
num_years = int(num_years)

X,y = get_data_from_file(f_string, num_years)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.3,random_state=123)
	
X1_train = np.concatenate((np.ones((len(y_train),1)),X_train), axis=1)

result = sm.OLS(y_train,X1_train).fit()
print result.summary()
