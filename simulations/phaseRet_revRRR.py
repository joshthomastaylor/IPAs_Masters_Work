#!/usr/bin.env python

'''
phaseRet_revRRR.py
Created by: joshthomastaylor

'''
import sys
sys.path.append('..')

import numpy as np 
import matplotlib.pyplot as plt 
import random 
import ncp_params
import ncp_funcs
import time

#external parameters
ncp_params.folderName = "phaseRet_revRRR"
ncp_params.suppSelect = []

#initialise
startT = time.perf_counter()
Ox, Op, Px, Sn = ncp_params.Ox, ncp_params.Op, ncp_params.Px, ncp_params.Sn

#create true object and addtional supports
trueObj = ncp_funcs.genObj(Ox, Op, Px)
conSupp = ncp_funcs.genSupps(Ox, Op, Px, Sn)

#define true support constraint
trueSupp = trueObj.copy()
trueSupp[trueSupp > 0] = 1
conSupp.insert(0, trueSupp)

#select one support
index = random.sample(range(0,len(conSupp)), 1)

#detemrine initial object
initObj = conSupp[index[0]].copy()
for i in range(Px):
	for j in range(Px):
		if initObj[i,j] == 1:
			initObj[i,j] = np.random.rand(1)
itr = initObj.copy()

#define Fourier constraint
conFour = np.abs(np.fft.fftn(trueObj))

#error metrics
errFour = np.zeros(ncp_params.N)
errReal = np.zeros(ncp_params.N)


#iterate!
for i in range(ncp_params.N):
	itr, itrSoln = ncp_funcs.alg_revRRR(ncp_funcs.projFour, ncp_funcs.projSupp, itr, ncp_params.beta, conFour, conSupp)
	errFour[i], errReal[i] = ncp_funcs.errMetrics(trueObj, conFour, itrSoln)

#save run
endT = time.perf_counter()
elapsedT = endT - startT

suppIndex = ncp_params.suppSelect
suppIndex.insert(0, index[0])

arrAll = ncp_funcs.arrMerge(initObj, itrSoln, trueObj, errFour, errReal, suppIndex, conSupp)
ncp_funcs.arrSave(arrAll, elapsedT)






