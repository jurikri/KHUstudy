# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 15:23:16 2020

@author: MSBak
"""

# https://www.tensorflow.org/tutorials/images/cnn?hl=ko

#1. 데이터 전처리, 시각화 - array data의 차원개념 이해하기
#2. CNN 모델의 원리, 딥러닝의 이해
#3. overfitting의 이해. validation의 중요성.

#%% data import
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

(train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()

train_images = train_images.reshape((60000, 28, 28, 1))
test_images = test_images.reshape((10000, 28, 28, 1))

#train_images, test_images = train_images / 1.0, test_images / 1.0
train_images, test_images = train_images / 255.0, test_images / 255.0
#%%

# sample 한개를 선택하여 시각화 하기
print('train_images', train_images.shape)
aimage = train_images[4,:,:,0]
plt.figure(); plt.imshow(aimage)
print('aimage.shape', aimage.shape)
train_labels[4]

aimage2 = aimage[0:15,0:15]
plt.figure(); plt.imshow(aimage2)
print(aimage2.shape)

arow = aimage[15:16,0:28]
plt.figure(); plt.imshow(arow)
print(arow.shape)

arow = aimage[15:16,:]
plt.figure(); plt.imshow(arow)
print(arow.shape)

arow = aimage[15,:]
plt.figure(); plt.plot(arow)
print(arow.shape)

#%% keras setup
    
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

model.summary()


#%% training
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=5)

#%% test

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
print(test_acc)

msresult = model.predict(test_images[0:1, :, :, :])
plt.imshow(test_images[0, :, :, 0])
print('msresult', msresult)





































