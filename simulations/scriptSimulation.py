#!/usr/bin.env python

'''
scriptTemplate.py
Created by: joshthomastaylor
On: 07/04/2021


'''

import numpy as np 
import matplotlib.pyplot as plt
import runpy
import ncp_funcs
import ncp_params
import random 
import time

import sys
sys.path.append('..')

ncp_params.beta = 0.5
for i in np.arange(11,15,1):
	ncp_params.Sn = i
	print(i)
	for j in range(100):
		runpy.run_path('ampRet_revRRR.py')

