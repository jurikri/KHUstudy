# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 09:54:07 2020

@author: msbak
"""

import numpy as np
import random
import matplotlib.pyplot as plt
from scipy import stats

population1 = []
for epoch in range(100000):
    sum1 = 0
    for i in range(10):
        sum1 += random.randrange(1,7)
    population1.append(sum1)
plt.figure(0) 
plt.hist(population1, bins=42)
print('population1 mean', np.mean(population1))

population2 = []
for epoch in range(100000):
    sum1 = 0
    for i in range(10):
        sum1 += random.randrange(1,7)
    population2.append(sum1 + 1)
plt.figure(0)    
plt.hist(population2, bins=42)
print('population2 mean', np.mean(population2))

# In[]
for n in range(10,1000,10):
    
    meansave = []
    for epoch in range(1000):
        a = random.sample(population1, n)
        b = random.sample(population2, n)
        meansave.append(stats.ttest_ind(a, b)[1])

    print(n, np.mean(meansave))


















    
    
    
