#!/usr/bin.env python

'''
2_convIterPlot.py
Created by: joshthomastaylor
'''
import sys
sys.path.append('..')

import numpy as np 
import matplotlib.pyplot as plt
import random 
import time
import os

mainFolder = "../../extracted_data/important/"
alg = "imagRet_RRR" 

lin1 = np.load(mainFolder+alg+"-05mean.npy")
lin2 = np.load(mainFolder+alg+"-05std.npy")

#begin figure
fig, ax1 = plt.subplots()

ax1.set_xlabel('Number of Supports (N)')
ax1.set_ylabel('Iterations to Converge')

ax1.errorbar(np.arange(1,16), lin1, yerr=2*lin2, label = r'revRRR, $\beta = 0.5$, mean', capthick =2)

fig.tight_layout()
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])

plt.legend(loc = 'center left', bbox_to_anchor=(1,0.5))
# plt.savefig('../../figures/'+alg+'_negITER.png', format = 'png', bbox_inches='tight')
plt.show()
