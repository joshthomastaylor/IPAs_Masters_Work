#!/usr/bin.env python

'''
errPlot.py
Created by: joshthomastaylor
On: 04/10/2021

'''
import numpy as np 
import matplotlib.pyplot as plt
import random 

import time
import os
from collections import Counter


def checkCon(x):
	n = len(x) - 1
	return(sum(np.diff(x) == 1) == n)


mainFolder = '../../results/'
algFolder = 'imagRet_revRRR/'
betaValue = 'beta0.5/'


alg_type = mainFolder+algFolder+betaValue
j = 'suppMask10'
threshold = 1/1000000 


fig, ax1 = plt.subplots()
ax1.set_xlabel('Iteration')
ax1.set_ylabel('Support')
length = 70
step_size = 10
iterns = range(0, length+1)

runs = os.listdir(alg_type+j)
runs = runs[0:100]

conv_count = 0
first_stack = []
for i in runs:

	errFour = np.loadtxt(str(alg_type)+str(j)+"/"+str(i)+"/03.csv", delimiter = ',')
		
	indices = np.argwhere(errFour < threshold)
	if indices.any():
		conv_count +=1
	else:
		continue

	lin = np.loadtxt(str(alg_type)+str(j)+"/"+str(i)+"/05.csv", delimiter = ',')+1


	ax1.plot(iterns, lin[0:length+1])

plt.yticks([1,2,3,4,5,6,7,8,9,10,11])
plt.xticks(np.arange(0, length+1, step_size))


fig.tight_layout()
plt.savefig('../../figures/'+algFolder[:-1]+betaValue[:-1]+'_negSUPP.png', format = 'png', bbox_inches='tight')
plt.show()
print("Converged:", conv_count)