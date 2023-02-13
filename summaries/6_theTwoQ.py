#!/usr/bin.env python

'''
theTwoQ.py
Created by: joshthomastaylor

'''
import numpy as np 
import os
import matplotlib.pyplot as plt

algorithm = 'phaseRet_RRR/'
beta = 'beta0.5/'

results = '../../results/'+algorithm+beta+'/'
supports = os.listdir(results) #suppMask0 etc.

threshold = 1/1000000

order = [0,1,7,8,9,10,11,12,13,14,2,3,4,5,6]
#[suppMask0, suppMask1, suppMask2 ...]
supports = [supports[i] for i in order] #folderSupp
print(supports)
conv_count = 0

Q1Values = []
Q2Values = []
Q1Final = []
Q2Final = []

for i in supports:
	# i = 'suppMask0'
	folderIds = os.listdir(results+str(i)+'/')
	if i == 'suppMask10':
		folderIds = folderIds[0:100]
	for j in folderIds:
		errFour = np.loadtxt(str(results)+str(i)+"/"+str(j)+"/03.csv", delimiter = ',')

		indices = np.argwhere(errFour < threshold)
		if indices.any():
			conv_count +=1
		else:
			continue
		suppSelect = np.loadtxt(str(results)+str(i)+"/"+str(j)+"/05.csv", delimiter = ',')+1

		suppIndices = np.argwhere(suppSelect == 1)
		firstSelect = suppIndices[0][0]
		#resize suppSelect array up to correct support selection
		suppArr = suppSelect[0:firstSelect+1]

		#Q1
		suppOcc = []
		for k in np.arange(1,16,1):
			cnt = 0
			cnt = np.sum(suppArr == k)
			suppOcc.append(cnt)
		Q1Values.append((len(suppArr)**2)/np.sum(np.array(suppOcc[:])**2))


		#Q2
		stateC = 0
		for m in np.arange(0, firstSelect, 1):
			if suppArr[m] != suppArr[m+1]:
				stateC += 1
		Q2Values.append(stateC/(firstSelect+1))

	Q1Final.append(np.mean(Q1Values))
	Q2Final.append(np.mean(Q2Values))


print("Converged:"+str(conv_count))

#create figure
supports = range(1,16)

fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.set_xlabel("N")
ax1.set_ylabel(r"q1", rotation='0', labelpad=20)
ax1.set_ylim([1, 2])

lns1 = ax1.plot(supports, Q1Final, marker='o', color='tab:blue', label='q1')

ax2 = ax1.twinx()
ax2.set_ylabel(r"q2", rotation='0', labelpad=20)
ax2.set_ylim([0, 1])

lns2 = ax2.plot(supports, Q2Final, marker='o', color='tab:purple', label='q2')

lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0)

plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
# plt.savefig('../../figures/'+algorithm[:-1]+'_negQ.png', format = 'png', bbox_inches='tight')
plt.show()

