# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 17:24:51 2020

@author: MSBak
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(font_scale=1.2)
import scipy.stats as stats
import random


x = np.arange(-10, 10, 0.0001)

y = stats.norm(0, 1).pdf(x)
plt.figure(); plt.plot(x, y, label='y')

y2 = stats.norm(1, 1.5).pdf(x)
plt.plot(x, y2, label='y2')

y3 = stats.norm(0, 2.085).pdf(x)
plt.plot(x, y3, label='y3')

y4 = stats.norm(-2, 3).pdf(x)
plt.plot(x, y4, label='y4')
plt.legend()


def KLD(p, q):
    return np.mean(p * np.log(p/q))

print('y', KLD(y, y))
print('y2', KLD(y, y2))
print('y3', KLD(y, y3))
print('y4', KLD(y, y4))

#%%
samples = np.random.normal(size=10000)
tlen = len(samples)
ix1 = random.sample(range(tlen), 10)
#ix2 = list(set(range(tlen)) - set(ix1))
ix2 = random.sample(range(tlen), 10)

group1 = np.sort(samples[ix1])
group2 = np.sort(samples[ix2])

#plt.figure()
#plt.hist(samples, bins=50)
#plt.hist(group1, bins=50)
#plt.hist(group2, bins=50)

plt.figure()
plt.hist(group1, bins=50)
plt.hist(group2, bins=50)

print('mean diff', np.mean(group1) - np.mean(group2))
print('std diff', np.std(group1, ddof=1) - np.std(group2, ddof=1))
















