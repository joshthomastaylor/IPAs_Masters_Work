#!/usr/bin.env python

'''
4_histrogramSupport.py
Created by: joshthomastaylor

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
algFolder = 'phaseRet_DM/'
betaValue = 'beta-0.7/'


alg_type = mainFolder+algFolder+betaValue
j = 'suppMask10'
threshold = 1/1000000 

runs = os.listdir(alg_type+j)
# runs = runs[0:100]
runs = runs[0:80]+runs[81:89]+runs[91:100]+runs[102:]
conv_count = 0


bad_list =[]
good_list = []
converge_iter = []
for i in runs:

	#determine if run will converge
	errFour = np.loadtxt(str(alg_type)+str(j)+"/"+str(i)+"/03.csv", delimiter = ',')
	indices = np.argwhere(errFour < threshold)
	if indices.any():
		converge_iter.append(indices[0,0])
		conv_count +=1
	else:
		continue

	#find iteration/s when run selects correct support
	lin = np.loadtxt(str(alg_type)+str(j)+"/"+str(i)+"/05.csv", delimiter = ',')+1
	one_locate = np.where(lin == 1)

	print(one_locate[0][0])
	bad_list.append(one_locate[0][0])
	if (one_locate[0][1] == one_locate[0][0]+1):
		good_list.append(one_locate[0][0])
	else:
		good_list.append(one_locate[0][1])

#used for trimming arrays
good_list = [x for x in good_list if x < 20]

labels, counts = np.unique(good_list, return_counts=True)
plt.bar(labels, counts/conv_count, align="center")
# plt.gca().set_xticks(labels)
plt.yticks(np.arange(0, 0.21, 0.04)) 
plt.xticks(np.arange(0, 21, 4), fontsize=10)
plt.xlabel('Iteration')
plt.ylabel('Normalised Frequency')
# plt.savefig('../../figures/'+algFolder[:-1]+betaValue[:-1]+'_posHIST.png', format = 'png', bbox_inches='tight')
print("Converged:"+str(conv_count))
print("Shown:"+str(len(good_list)))
plt.show()

