# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:52:00 2019

@author: MSBak
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


filepath = 'C:\\Users\\MSBak\\Desktop\\새 폴더\\' + 'Image4_time_series_256-256_zoom1.5_1step_normal_speed7.xlsx'
df1 = pd.read_excel(filepath, header=None, sheet_name=0)
df2 = pd.read_excel(filepath, header=None, sheet_name=1)
df3 = pd.read_excel(filepath, header=None, sheet_name=2)

df1 = np.array(df1)
roiNum = int(df1.shape[1]/4)

df1_roi = np.zeros((roiNum, df1.shape[0]))
for i in range(roiNum):
    ci = (i*4+1)
    print(ci)
    
    
    df1_roi[i,:] = df1[:,ci]
#    plt.plot(df1[:,ci])
    

# 평균값 구하기 F0
    # 평균값 저장'
meansave = np.zeros(df1_roi.shape[0])

for i in range(df1_roi.shape[0]):
    df1_roi[i,:]
    
    meanrange = int(round(df1_roi[i,:].shape[0] * 0.3))
    
    mssort = np.sort(df1_roi[i,:])[0:meanrange]
    
    meansave[i] = np.mean(mssort)
    

# df 구하기
i = 0 

df1_df = np.zeros((roiNum, df1.shape[0]))
for i in range(df1_roi.shape[0]):
    dfdf = (df1_roi[i,:] - meansave[i])/meansave[i]
    
    df1_df[i,:] = dfdf
    


















