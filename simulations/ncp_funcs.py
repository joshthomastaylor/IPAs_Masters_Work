#!/usr/bin.env python

'''
ncp_funcs.py
Created by: joshthomastaylor
On: 06/04/2021

'''

import numpy as np 
import matplotlib.pyplot as plt 
import random
import ncp_params
import datetime
import time
import os

#Generate Objects and Supports.
def genObj(Ox, Op, Px):
	obj = np.zeros([Ox, Ox])
	randPos = random.sample(range(0, np.square(Ox)), int(np.square(Ox)*Op))

	for i in randPos:
 		x, y = divmod(i, Ox)
 		obj[x, y] = np.random.rand(1)

	padObj = np.zeros([Px, Px])
	padObj[Ox//2:Px-Ox//2, Ox//2:Px-Ox//2] = obj
	return(padObj)

def genSupps(Ox, Op, Px, Sn):
	supps = []
	for i in range(Sn):
		newObj = genObj(Ox, Op, Px)
		newObj[newObj > 0] = 1
		supps.append(newObj)
	return(supps)

def genObjNoSym(Ox, Op, Px):
	obj = np.zeros([Ox, Ox])
	sampleArr = []
	while len(sampleArr) < (np.square(Ox)*Op):
		randPos = random.sample(range(0, np.square(Ox)), int(1))
		if randPos[0] not in sampleArr:
			if (np.mod(randPos[0], Ox) != 0):
				oppPos = (np.square(Ox)-1)-randPos[0]+(Ox)+1
				if oppPos not in sampleArr:
					sampleArr.append(randPos[0])
				else:
					continue
			else:
				sampleArr.append(randPos[0])
				continue
		else:
			continue

	for i in sampleArr:
 		x, y = divmod(i, Ox)
 		obj[x, y] = np.random.rand(1)

	padObj = np.zeros([Px, Px])
	padObj[Ox//2:Px-Ox//2, Ox//2:Px-Ox//2] = obj
	return(padObj)

def genSuppsNoSym(Ox, Op, Px, Sn):
	supps = []
	for i in range(Sn):
		newObj = genObjNoSym(Ox, Op, Px)
		newObj[newObj > 0] = 1
		supps.append(newObj)
	return(supps)



#Projections.
def projFour(itr, conFour):
	mag = conFour
	phase = np.angle(np.fft.fftn(itr))
	z = mag*np.exp(1j*phase)
	return(np.real(np.fft.ifftn(z)))

def projFourImag(itr, conFour):
	z = conFour + np.imag(np.fft.fftn(itr))*1j
	return(np.real(np.fft.ifftn(z)))

def projFourAmp(itr, conFour, conDC):
	Px = ncp_params.Px
	mag = np.zeros([Px, Px])
	itrAmps = np.abs(np.fft.fftn(itr))
	itrAngles = np.mod(np.angle(np.fft.fftn(itr)), 2*np.pi)
	for i in range(Px):
		for j in range(Px):
			diffAngle = np.abs(itrAngles[i,j] - conFour[i,j])
			if (diffAngle > np.pi):
				diffAngle = np.pi*2 - diffAngle

			if (diffAngle < (np.pi/2)):
				mag[i,j] = np.cos(diffAngle) * itrAmps[i,j]	
			else:
				mag[i,j] = 0

			x = mag * np.cos(conFour)
			y = mag * np.sin(conFour)
	newitrFour = x+y*1j
	newitrFour[0,0] = conDC
	return(np.real(np.fft.ifftn(newitrFour)))

def projSupp(itr, conSupp):
	errArr = []
	for i in conSupp:
		test = itr*i
		error = errRMS(itr, test)
		errArr.append(error)

		test2 = np.rot90(itr, 2)*i
		error2 = errRMS(itr, test2)
		errArr.append(error2)

	errMin = errArr.index(min(errArr))

	if errMin%2 == 0:
		newIndex = errMin//2
		ncp_params.suppSelect.append(newIndex)
		suppedItr = itr*conSupp[newIndex]
	else:
		newIndex = (errMin - 1)//2
		ncp_params.suppSelect.append(newIndex)
		suppedItr = np.rot90(itr, 2)*conSupp[newIndex]

	return(suppedItr)



#Relaxed Projections.
def r_projFour(itr, beta, conFour):
	gamA = -1/beta
	pA = projFour(itr, conFour)
	return(pA+gamA*(pA-itr))

def r_projFourImag(itr, beta, conFour):
	gamA = -1/beta
	pA = projFourImag(itr, conFour)
	return(pA+gamA*(pA-itr))

def r_projFourAmp(itr, beta, conFour, conDC):
	gamA = -1/beta
	pA = projFourAmp(itr, conFour, conDC)
	return(pA+gamA*(pA-itr))

def r_projSupp(itr, beta, conSupp):
	gamB = 1/beta
	pB = projSupp(itr, conSupp)
	return(pB+gamB*(pB-itr))



#DM Algorithms.
def alg_DM(funcFour, funcSupp, r_funcFour, r_funcSupp, itr, beta, conFour, conSupp):
	x1 = funcFour(r_funcSupp(itr, beta, conSupp), conFour)
	x2 = funcSupp(r_funcFour(itr, beta, conFour), conSupp)
	itr = itr + beta * (x1 - x2)
	return(itr, x2)

def alg_DM_amp(funcFour, funcSupp, r_funcFour, r_funcSupp, itr, beta, conFour, conSupp, conDC):
	x1 = funcFour(r_funcSupp(itr, beta, conSupp), conFour, conDC)
	x2 = funcSupp(r_funcFour(itr, beta, conFour, conDC), conSupp)
	itr = itr + beta * (x1 - x2)
	return(itr, x2)



#RRR Algorithms.
def alg_RRR(funcFour, funcSupp, itr, beta, conFour, conSupp):
	x1 = funcSupp(itr, conSupp)
	y1 = x1 + (x1 - itr)

	x2 = funcFour(y1, conFour)
	itr = itr + beta*(x2 - x1)
	return(itr, x1)

def alg_revRRR(funcFour, funcSupp, itr, beta, conFour, conSupp):
	x1 = funcFour(itr, conFour)
	y1 = x1 + (x1 - itr)

	x2 = funcSupp(y1, conSupp)
	itr = itr + beta*(x2 - x1)
	return(itr, x2)

def alg_RRR_amp(funcFour, funcSupp, itr, beta, conFour, conSupp, conDC):
	x1 = funcSupp(itr, conSupp)
	y1 = x1 + (x1 - itr)

	x2 = funcFour(y1, conFour, conDC)
	itr = itr + beta*(x2 - x1)
	return(itr, x1)

def alg_revRRR_amp(funcFour, funcSupp, itr, beta, conFour, conSupp, conDC):
	x1 = funcFour(itr, conFour, conDC)
	y1 = x1 + (x1 - itr)

	x2 = funcSupp(y1, conSupp)
	itr = itr + beta*(x2 - x1)
	return(itr, x2)



def errRMS(arg1, arg2):
	N = len(arg1) * len(arg1[1])

	a = (np.sum(np.square(arg2 - arg1)))/N
	b = (np.sum(np.square(arg1)))/N
	return(np.sqrt(a/b))

def errRMSphase(arg1, arg2):
	N = len(arg1) * len(arg1[1])
	diffAngle = []
	Px = ncp_params.Px

	for i in range(Px):
		for j in range(Px):
			diffAngle = np.abs(arg2[i,j] - arg1[i,j])
			if (diffAngle > np.pi):
				diffAngle = np.pi*2 - diffAngle

	a = (np.sum(np.square(diffAngle)))/N
	return(np.sqrt(a))



def errMetrics(trueObj, conFour, itrSoln):
	errFour = errRMS(conFour, np.abs(np.fft.fftn(itrSoln)))
	errReal = errRMS(trueObj, itrSoln)
	return(errFour, errReal)

def errMetricsREF(trueObj, conFour, itrSoln):
	errFour = errRMS(conFour, np.real(np.fft.fftn(itrSoln)))
	errReal = errRMS(trueObj, itrSoln)
	return(errFour, errReal)


def errMetricsAmp(trueObj, conFour, itrSoln):
	errFour = errRMSphase(conFour, np.mod(np.angle(np.fft.fftn(itrSoln)), 2*np.pi))
	errReal = errRMS(trueObj, itrSoln)
	return(errFour, errReal)





def arrMerge(a, b, c, d, e, f, g):
	m = [a, b, c, d, e, f]
	return(m+g)

def arrSave(arrAll, elapsedT):
	directory = "../../results/"+str(ncp_params.folderName)
	if not os.path.exists(directory):
		os.mkdir(directory)

	if not os.path.exists(directory+"/beta"+str(ncp_params.beta)):
		os.mkdir(directory+"/beta"+str(ncp_params.beta))

	if not os.path.exists(directory+"/beta"+str(ncp_params.beta)+"/suppMask"+str(ncp_params.Sn)):
		os.mkdir(directory+"/beta"+str(ncp_params.beta)+"/suppMask"+str(ncp_params.Sn))

	nameRun = str(datetime.datetime.now())
	nameRun = nameRun.replace(':', '')

	nameFolder = directory+"/beta"+str(ncp_params.beta)+"/suppMask"+str(ncp_params.Sn)+"/"+nameRun
	os.mkdir(nameFolder)

	arrIds =  ["%.2d" % i for i in range(len(arrAll))]
	for i in range(len(arrAll)):
		nameFile = nameFolder+"/"+arrIds[i]+".csv"
		np.savetxt(nameFile, arrAll[i], delimiter = ',')

	#create .txt file with extra details
	txtTitle = np.array(['Iterations:', 'Beta:', 'Time:', 'Supports:'])
	txtData = np.array([ncp_params.N, ncp_params.beta, elapsedT, ncp_params.Sn])
	txtArr = np.zeros(txtTitle.size, dtype=[('var1', 'U6'), ('var2', float)])
	txtArr['var1'] = txtTitle
	txtArr['var2'] = txtData
	np.savetxt(nameFolder+"/"+'info.txt', txtArr, fmt="%s %10.3f")

	return()

def arrSaveShort(arrAll):
	if not os.path.exists(directory):
		os.mkdir(directory)

	if not os.path.exists(directory+"/beta"+str(ncp_params.beta)):
		os.mkdir(directory+"/beta"+str(ncp_params.beta))

	if not os.path.exists(directory+"/beta"+str(ncp_params.beta)+"/suppMask"+str(ncp_params.Sn)):
		os.mkdir(directory+"/beta"+str(ncp_params.beta)+"/suppMask"+str(ncp_params.Sn))

	nameRun = str(datetime.datetime.now())
	nameRun = nameRun.replace(':', '')

	nameFolder = directory+"/beta"+str(ncp_params.beta)+"/suppMask"+str(ncp_params.Sn)+"/"+nameRun
	os.mkdir(nameFolder)

	arrIds =  ["%.2d" % i for i in range(len(arrAll))]
	for i in range(len(arrAll)):
		nameFile = nameFolder+"/"+arrIds[i]+".csv"
		np.savetxt(nameFile, arrAll[i], delimiter = ',')

	return()



def dispObj(itrSoln, trueObj):
	objects = [itrSoln, trueObj, trueObj - itrSoln ]
	cnt = 0
	fig, axes = plt.subplots(nrows=1, ncols=3)
	for ax in axes.flat:
		plt.gray()
		im = ax.imshow(objects[cnt], vmin=-1, vmax=1)
		cnt+=1

	fig.subplots_adjust(right=0.8)
	cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
	fig.colorbar(im, cax=cbar_ax)

	plt.show()


def dispErr(errFour, errReal):
	fig, ax1 = plt.subplots()

	ax1.set_xlabel('Iterations')
	ax1.set_ylabel('Error')
	ax1.plot(range(0, ncp_params.N), errFour, color='tab:blue')
	ax1.plot(range(0, ncp_params.N), errReal, color='tab:red')
	plt.yscale('log')
	plt.gca().legend(('four', 'real'))

	fig.tight_layout()
	plt.show()

def loadSupps(directory):
	supps = []
	suppList = os.listdir(directory)
	for i in suppList:
		supp = np.loadtxt(directory+str(i), delimiter = ',')
		supps.append(supp)
	return(supps)
