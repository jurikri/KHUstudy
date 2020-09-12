# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 17:27:16 2020

@author: MSBak
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


# In[] data load, 정리

filepath =  'C:\\Users\\msbak\\Downloads\\과제6-20200906T080030Z-001\\과제6\\'
filename = 'sample_data.csv'
df = pd.read_csv(filepath+filename)
data = np.array(df)


X = []; Y = []
for i in range(len(data)):
    X.append([data[i,0]])
    Y.append([data[i,1]])
        
X = np.array(X) # data num x feature num
Y = np.array(Y) # data num x class num
# 모든것은 data size(shape)으로 이해되곤 합니다. data size를 눈여겨 보세요.

feature_num = 1 # 현재 데이터의 feature의 갯수는 1개 입니다.

graph_1 = tf.Graph()
with graph_1.as_default():
    Xtf = tf.placeholder(tf.float32, [None, feature_num]) # None for data num
    Ytf = tf.placeholder(tf.float32, [None, 1]) # 1 for Y shape
    
    W = tf.Variable(tf.random_normal([feature_num, 1]))
    b = tf.Variable(tf.random_normal([1]))

    Yhat = tf.matmul(Xtf, W)+b
    loss = tf.reduce_mean(tf.square(Ytf - Yhat))
    optimizer = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(loss)
    

losssave=[]
with tf.Session(graph = graph_1) as sess1:
    sess1.run(tf.global_variables_initializer())
    for epoch in range(30000):
        _, loss_var, yhat_var = sess1.run([optimizer, loss, Yhat], feed_dict = {Xtf: X, Ytf: Y})
        losssave.append(loss_var)
        if epoch % 200 == 0:
            print(epoch, 'loss :', loss_var)
            
    # 예측값 출력
    Yhat_var, W_var, b_var = sess1.run([Yhat, W, b], feed_dict = {Xtf: X})
plt.figure(); plt.plot(losssave) 
print('W_var, b_var', W_var, b_var)
























