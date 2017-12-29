import numpy as np
import pandas as pd
#import sklearn as sk

def mean(array):
	return np.mean(array)

def median(array):
	return np.median(array)

def lowerQuartile(array):
	dataframe = pd.DataFrame(array)
	description = dataframe.describe()
	#print (description.25)
	print (description)

def topQuartile(array):
	dataframe = pd.DataFrame(array, columns=['col1'])
	description = dataframe.describe()
	print (description)