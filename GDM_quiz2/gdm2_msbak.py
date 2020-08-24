# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 15:13:40 2020

@author: MSBak
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

# In[] data load
filename = 'sample_data.csv'
df = pd.read_csv(filename)
df = np.array(df)

x = df[:,0] # slicing 으로 빼옴
y = df[:,1]

# In[] calc. pearsonr
xmean = np.mean(x) # 평균 구하여 저장
ymean = np.mean(y)

tmp1 = []; tmp2 = []; tmp3 = []
for i in range(df.shape[0]):
    tmp1.append((x[i] - xmean) * (y[i] - ymean))
    
    tmp2.append((x[i]-xmean)**2)
    
    tmp3.append((y[i]-ymean)**2)

pearsonr = np.sum(tmp1) / (np.sqrt(np.sum(tmp2)*np.sum(tmp3)))
print('pearsonr', pearsonr)

# In[] calc. regression using normal equation.

stdx = np.std(x, ddof=1)
stdy = np.std(y, ddof=1)

beta0 = pearsonr * (stdy/stdx)
beta1 = ymean - (xmean * beta0)

plt.figure()
plt.scatter(x, y)
xaxis = np.arange(np.max(x)*1.1)
plt.plot(xaxis, xaxis*beta0 + beta1)

cheolsoo = 13
cheolsoo_y = cheolsoo * beta0 + beta1
print('beta0', beta0, 'beta1', beta1)
print('철수의 코딩실력 예상', cheolsoo_y)

# In[] calc. regression using GDM

def loss(xdata, beta0, beta1):
    return np.mean(((beta0 * xdata + beta1) - y)**2) 
    
    # slide에는 /2 까지 하기로 되어있는데, 이건 미분을 편하게 하기 위한 임의 조작입니다.
    # 임의의 상수를 넣는것은 계산값들 사이의 관계에 전혀 영향을 주지 않기 때문에 가능한 것이죠.
    # 저는 따로 미분하지 않으므로 여기서 그냥 평균처리만 하겠습니다.

# loss function visualization
# 현재 parameter가 (beta) 두개 이므로, loss function의 시각화도 2차원으로 표현될 수 있습니다.
# 각 parameter에 대해서 1차원으로 각각, 그리고 함께 2차원으로 표현해 볼게요.

# beta1에 대한 시각화
beta0 = 1 # 임의 값으로 고정
msplot = []
forlist = np.arange(-100, 100, 1)
for beta1 in forlist:
    msplot.append(loss(x, beta0, beta1))
plt.figure(); plt.plot(forlist, msplot) # 아주 매끄럽네요. GDM이 잘 먹히게 생겼습니다.

# beta0에 대한 시각화
beta1 = 1 # 임의 값으로 고정
msplot = []
forlist = np.arange(-100, 100, 1)
for beta0 in forlist:
    msplot.append(loss(x, beta0, beta1))
plt.figure(); plt.plot(forlist, msplot)

# beta0, beta1에 대한 시각화 (꼭 이해할 필요는 없음)
forlist = np.arange(-100, 100, 1)
msplot=[]
for beta0 in forlist:
    msplot_tmp=[]
    for beta1 in forlist:
        msplot_tmp.append(loss(x, beta0, beta1))
    msplot.append(msplot_tmp)
msplot = np.array(msplot) 
# list 2개르 겹처서 생성한 후 array로 변환합니다. 
# 크기가 정형화 (일정함)되어 잇는 경우 list를 다차원 (이 경우 이차원 array) array로 변환 가능합니다.
plt.figure(); plt.imshow(msplot); plt.colorbar()
# 2차원 array는 보통 image이므로, imshow (image show)라느이름의 function이 사용될 수 있습니다.

# GDM
# 저번 이차 방정식에서 사용했던 미분 추정 공식을 그대로 써볼게요.
# 이 문제에서 매우 어려운 부분은 parameter가 2개이므로 편미분이 필요하다는 점입니다.
# 제가 문제를 내놓고도 이부분을 놓쳤네요.

# 사실 개념은 매우 직관적입니다.
# 우리는 parameter x를 구하기 위해서 x에 대해 미분을 했었습니다.
# parameter가 늘어남에 따라 식이 복잡해 졌지만, 여전히 parameter x에 대해서만 집중하면 됩니다.
# 따라서, parameter x에대해서만 미분(편미분)을 하여 GDM을 적용하면 됩니다.

def loss(xdata, beta0, beta1): # 이해를 위해 위에것을 그대로 가져왔습니다.
    return np.mean(((beta0 * xdata + beta1) - y)**2)

def partial_differentiation_beta0(fx, x, beta0, beta1):  # x 표기를 헷갈리지 마시길.. 여기선 x는 고정값입니다.
    s = 0.0000001 
    return (fx(x, beta0+s, beta1) - fx(x, beta0, beta1)) / s

def partial_differentiation_beta1(fx, x, beta0, beta1):
    s = 0.0000001 
    return (fx(x, beta0, beta1+s) - fx(x, beta0, beta1)) / s


beta0 = random.randrange(-100,100)  # 저번 이차 방정식에서 사용했던 랜덤 시작값을 그대로 써볼게요.
beta1 = random.randrange(-100,100)
lr = 0.0001; d0 = None; d1 = None 
# d0, d1를 선언해도되고 안해도 됩니다. 안하면 에러로 잘못 인식되서 거슬리므로 그냥 선언하겠습니다.
loss_save = []
for epoch in range(300000):
    if epoch != 0:
        beta0 = beta0 - d0 * lr 
        beta1 = beta1 - d1 * lr
        
    d0 = partial_differentiation_beta0(loss, x, beta0, beta1)
    d1 = partial_differentiation_beta1(loss, x, beta0, beta1)
    
    loss_save.append(loss(x, beta0, beta1))
    
#    if epoch % 10:
#        print(epoch, loss(x, beta0, beta1))

plt.figure(); plt.plot(loss_save[:])

print('loss', loss(x, beta0, beta1))
print('optimized parameters', beta0, beta1)
print('철수의 코딩실력 예상', cheolsoo_y)

























