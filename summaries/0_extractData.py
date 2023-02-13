#!/usr/bin.env python

'''
extractData.py
Created by: joshthomastaylor

'''
import numpy as np 
import matplotlib.pyplot as plt
import random 
import time
import os


def convCheck(errFour, threshold, convCount):

	indices = np.argwhere(errFour < threshold)
	if indices.any():
		return(convCount+1, np.min(indices))
	else:
		return(convCount+0, 0)


algorithm = 'imagRet_revRRR/'
beta = 'beta0.5/'

results = '../../results/'+algorithm+beta
supports = os.listdir(results) #suppMask0 etc.

threshold = 1/1000000
totalConv = []
totalMean = []
totalStd = []

for i in supports:
	print(i)
	runs = os.listdir(os.path.join(results, i))
	convCount = 0
	convIterRun = []
	for j in runs:
		errFour = np.loadtxt(os.path.join(results,i,j)+"/03.csv", delimiter = ',')
		convCount, convIter = convCheck(errFour, threshold, convCount)
		if convIter != 0:
			convIterRun.append(convIter)
		else:
			continue
	totalConv.append(convCount)
	totalMean.append(np.mean(convIterRun))
	totalStd.append(np.std(convIterRun))

#adjust data for bad indexing
order = [0,1,7,8,9,10,11,12,13,14,2,3,4,5,6]
totalConv = [totalConv[i] for i in order]
totalMean = [totalMean[i] for i in order]
totalStd = [totalStd[i] for i in order]
print(totalConv)
print(totalMean)
print(totalStd)

# np.save('../../extracted_data/'+algorithm[:-1]+beta[4:-3]+beta[-2:-1]+'conv', totalConv)
# np.save('../../extracted_data/'+algorithm[:-1]+beta[4:-3]+beta[-2:-1]+'mean', totalMean)
# np.save('../../extracted_data/'+algorithm[:-1]+beta[4:-3]+beta[-2:-1]+'std', totalStd)
