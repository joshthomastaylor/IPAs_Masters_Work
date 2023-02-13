#!/usr/bin.env python

'''
convPropPlot.py
Created by: joshthomastaylor

'''
import numpy as np 
import matplotlib.pyplot as plt
import random 
import time
import os

divisor = 100

mainFolder = '../../extracted_data/'
algFolder = 'phaseRet/'
alg = 'phaseRet_RRR'


#import data and scale
lin1 = np.load(mainFolder+algFolder+alg+'-05conv.npy')/divisor
lin2 = np.load(mainFolder+algFolder+alg+'-10conv.npy')/divisor
lin3 = np.load(mainFolder+algFolder+alg+'-15conv.npy')/divisor
overN = 1/(np.arange(1,16))

#begin figure
fig, ax1 = plt.subplots()
ax1.set_xlabel('N')
ax1.set_ylabel('Converged Proportion')

ax1.plot(np.arange(1,16), lin1, label = r'DM, $\beta = -0.5$')
ax1.plot(np.arange(1,16), lin2, label = r'DM, $\beta = -1.0$')
ax1.plot(np.arange(1,16), lin3, label = r'DM, $\beta = -1.5$')

ax1.plot(np.arange(1,16), overN, label = "1/N", color='r')


fig.tight_layout()
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])

plt.legend(loc = 'center left', bbox_to_anchor=(1,0.5))
# plt.savefig('../../figures/'+alg+'_negCONV.png', format = 'png', bbox_inches='tight')
plt.show()
