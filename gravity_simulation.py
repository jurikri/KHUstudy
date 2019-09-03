# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 16:41:17 2019

@author: MSBak
"""

import numpy as np
import matplotlib.pyplot as plt
import random as rd

spacesize = 1000; initial_speed_range = 10; object_n = 3

ob = []
for n in range(object_n):
    position = np.array([rd.randrange(spacesize), rd.randrange(spacesize)])
    movement = np.array([rd.randrange(initial_speed_range), rd.randrange(initial_speed_range)])
    
    ob.append([position, movement])

space = np.zeros((spacesize,spacesize))
timebin = 1
mass = 1; g = 10000
plt.ion()
plt.figure(0)

# 20190903 : 탄성계수 추가해야할듯.. nan은 왜 나는거지?

i = 0
for i in range(1000):
    plt.axis([0, spacesize, 0, spacesize])
    
    # 속도 결정, 충돌 및 만유인력 고려
    record = np.zeros((len(ob),len(ob)))
    record2 = np.zeros((len(ob),len(ob)))
    for j in range(len(ob)):
        for k in range(len(ob)):
            if list(ob[j][0]) == list(ob[k][0]) \
            and not j == k and record[j,k] == 0:
                ob[k][1] = ob[k][1] + ob[j][1] # 작용
                ob[j][1] = ob[j][1] - ob[j][1] # 반작용
                
                record[j,k] = 1; record[k,j] = 1
            
            # 중력 적용
            if not j == k and record2[j,k] == 0:
                distance = np.sum(np.square(ob[j][0] - ob[k][0])) ** 0.5
                gravity_force = g * mass * mass / (distance * distance)
                
                x = np.abs(ob[j][0][0] - ob[k][0][0])
                y = np.abs(ob[j][0][1] - ob[k][0][1])               
                rad = np.arctan(y/x)
                x_force = np.cos(rad) * gravity_force
                y_force = np.sin(rad) * gravity_force
                
                if np.isnan(x_force) or np.isnan(y_force):
                    print(x_force, y_force)
                    break
                
                x_direction = (ob[k][0][0] - ob[j][0][0])/np.abs((ob[k][0][0] - ob[j][0][0]))
                y_direction = (ob[k][0][1] - ob[j][0][1])/np.abs((ob[k][0][1] - ob[j][0][1]))
     
                ob[j][1] = ob[j][1] + np.array([x_force * x_direction , y_force * y_direction])
                ob[k][1] = ob[k][1] + np.array([x_force * -x_direction , y_force * -y_direction])
                
                record2[j,k] = 1; record2[k,j] = 1
                
            
    for j in range(len(ob)):
        ob[j][0][0] = ob[j][0][0] + (ob[j][1][0] * timebin)
        ob[j][0][1] = ob[j][0][1] + (ob[j][1][1] * timebin)
        
        if j == 0:
            print(i, ob[j][0][0], ob[j][0][1])

        plt.scatter(int(round(ob[j][0][0])), int(round((ob[j][0][1]))))
        
    plt.pause(10e-5)
    plt.clf()


















