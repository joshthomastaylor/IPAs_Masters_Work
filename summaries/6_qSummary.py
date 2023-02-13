#!/usr/bin.env python

'''
2q_summary.py
Created by: joshthomastaylor
On: 07/04/2021

'''

import numpy as np 
import os
import ncp_params
import matplotlib.pyplot as plt

#[suppMask0, suppMask1 ...]
folderSupp = os.listdir(ncp_params.arrDir)

iterations = 10
runs = ncp_params.R 
SC = []
q1Prep = []
cnt = 0

print(folderSupp)

for i in folderSupp:
	cnt += 1
	#[2021-04-07 xxx.xxx, 2021-04-07 xxx.xxx, ...]
	folderIds = os.listdir(ncp_params.arrDir+i+'/')
	for j in folderIds:
		#[05.csv - suppSelect csv file]
		suppArr = np.loadtxt(ncp_params.arrDir+i+'/'+j+'/05.csv', delimiter=',')
		suppArr = suppArr[0:iterations]
		stateChanges = 0
		uniqSupp = []
		for k in range(iterations-1):
			if suppArr[k] != suppArr[k+1]:
				stateChanges+=1
		SC.append(stateChanges)

		suppArr+=1
		for m in range(1,16):
			suppOcc = 0
			suppOcc = np.sum(suppArr == m)
			uniqSupp.append(suppOcc)

		sqPrep = np.array(uniqSupp[0:14])**2
		sumPrep = np.sum(sqPrep)
		# print(sumPrep)
		q1Prep.append(iterations**2/sumPrep)





		
q1 = []
for p in range(15):
	q1.append(np.mean(q1Prep[0+p*len(folderIds):(runs-1)+p*len(folderIds)]))


q2 = []
for l in range(15):
	q2.append(np.mean(SC[0+l*len(folderIds):(runs-1)+l*len(folderIds)]))

suppsGraph = range(1,16)
q2 = np.array(q2)/iterations




fig = plt.figure()
ax = fig.add_subplot(111)

ax.set_xlabel("Number of supports (N)")
ax.set_ylabel(r"q1", rotation='0', labelpad=20)
# ax.set_ylim([1, 3])

lns1 = ax.plot(suppsGraph, q1, marker='o', color='tab:blue', label='q1')

ax2 = ax.twinx()

ax2.set_ylabel(r"q2", rotation='0', labelpad=20)
ax2.set_ylim([0, 1])

lns2 = ax2.plot(suppsGraph, q2, marker='o', color='tab:purple', label='q2')

lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)


plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

# plt.title(ncp_params.arrDir)
# plt.savefig('../../results/3108figures/ampRRR0.5Q.png', format = 'png', bbox_inches='tight')
plt.show()
