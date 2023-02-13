#!/usr/bin.env python

'''
errPlot.py
Created by: joshthomastaylor
'''
import sys
sys.path.append('..')

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


mainFolder = '../../results/'
algFolder = 'imagRet_revRRR/'
betaValue = 'beta0.5/'


alg_type = mainFolder+algFolder+betaValue

j = 'suppMask10'
iterations = 1000

fig, ax1 = plt.subplots(1,1)
ax1.set_xlabel('Iteration')
ax1.set_ylabel('E', rotation=0)
ax1.set_ylim([1/10000000000000000, 1])

iterns = range(0, iterations)

threshold = 1/1000000
convCount = 0


runs = os.listdir(alg_type+j)
runs = runs[0:100]

count = 0
for i in runs:
	lin = np.loadtxt(str(alg_type)+str(j)+"/"+str(i)+"/03.csv", delimiter = ',') #03 - four, 04 - real
	convCount, convIter = convCheck(lin, threshold, convCount)
	ax1.plot(iterns, lin[0:iterations])



ax1.plot(iterns,threshold*np.ones(iterations), color = 'tab:red')

fig.tight_layout()
ax1.set_yscale('log')
ax1.set_ylim([None, 5])


# plt.savefig('../../figures/'+algFolder[:-1]+betaValue[:-1]+'_negREALERROR.png', format = 'png', bbox_inches='tight')
plt.show()
print(convCount)
