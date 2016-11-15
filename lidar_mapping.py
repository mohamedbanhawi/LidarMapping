#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyurg
import matplotlib.pyplot as plt
import matplotlib.lines as ln
import numpy as np
from math import *
import time


# For initializing.
urg = pyurg.UrgDevice()

# Connect to the URG device.
# If could not conncet it, get False from urg.connect()
if not urg.connect():
    print 'Could not connect.'
    exit()


# Get length datas and timestamp.
# If missed, get [] and -1 from urg.capture()
startT = time.time()

scan_range = []
scan_bearing = []
scan_x = []
scan_y = []


#number of scans - n 
n = 10


for i in range(n):

	data, timestamp = urg.capture()
	theta = np.linspace(-120, 120, len(data))
	x=[]
	y=[]
	
	scan_range.append(data)
	scan_bearing.append(theta)
	
	#plot cartesian
	for j in range(len(data)):
		x.append(data[j]*cos(theta[j]*pi/180))
		y.append(data[j]*sin(theta[j]*pi/180))
	scan_x.append(x)
	scan_y.append(y)
	
	#plt.plot(x,y,'.',markersize=2)
	plt.show()

#plot range	
plt.plot(0,0,'r+',markersize=10)
plt.plot([-5000,-5000,5000,5000,-5000],[-5000,5000,5000,-5000,-5000],'0.45',lw=0.5)


# probabilistic mapping
cell_size_factor =100

#create grid with hits, probabilities & updates
cells_hit = np.zeros((cell_size_factor+1,cell_size_factor+1))
cells_prob = np.zeros((cell_size_factor+1,cell_size_factor+1))
cells_update = np.zeros((n,cell_size_factor+1,cell_size_factor+1))

#update hits per cell

for i in range(n):
	
	for j in range(len(scan_x[i])):
		#find cell indices
		ix  = int(floor(scan_x[i][j]/cell_size_factor))
		ix = ix+cell_size_factor/2
		#bound x
		if ix<0: ix =0
		elif ix>cell_size_factor: ix =cell_size_factor
		iy  = int(floor(scan_y[i][j]/cell_size_factor))
		iy = iy+cell_size_factor/2
		#bound y
		if iy<0: iy =0
		elif iy>cell_size_factor: iy =cell_size_factor
		
		
		if cells_update[i][ix][iy] == 0: #if cell not updated
			cells_update[i][ix][iy] = 1
			cells_hit[ix][iy] = cells_hit[ix][iy]+1

#calculate probability
p_thres = 0.3
p_collide = 0.5		
for i in range (cells_hit.shape[0]):
	for j in range (cells_hit.shape[1]):
		cells_prob[i][j] = cells_hit[i][j] / n 
		#if cells_prob[i][j] < p_thres: cells_prob[i][j] = 0.0
		#if cells_prob[i][j] > p_collide: cells_prob[i][j] = 1.0


		
fig = plt.figure(2)

ax = fig.add_subplot(111)
ax.set_title('colorMap')
plt.imshow(cells_prob)
ax.set_aspect('equal')
plt.colorbar(orientation='vertical')
plt.show()

			
			
		


	




	


