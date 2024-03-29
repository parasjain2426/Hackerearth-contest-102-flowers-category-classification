# -*- coding: utf-8 -*-
"""CNNwithPretrained.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MG1jp5BHFnnXGDqAfvvcHPd95SZlmo2g
"""

import numpy as np
xtrain=np.load('/content/drive/My Drive/Datasets/traindata.npy')

import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.layers import Dense,Dropout,Activation,Conv2D,MaxPooling2D,Flatten
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.models import Sequential

xtrain=tf.keras.utils.normalize(xtrain)

import pandas as pd
ytrain=pd.read_csv('/content/drive/My Drive/Datasets/trainfinal.csv')
#ytrain.shape

from tensorflow.keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
from keras import backend as K

from keras.layers import Input
IMG_SHAPE = (250, 250, 3) # used 250x250 pixel size of image and got 80% accuracy.
VGG16_MODEL=tf.keras.applications.VGG16(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet')
VGG16_MODEL.trainable=False
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
prediction_layer = tf.keras.layers.Dense(103,activation='softmax')

model = tf.keras.Sequential([
  VGG16_MODEL,
  global_average_layer,
  prediction_layer
])

model.compile(optimizer=tf.train.AdamOptimizer(), 
              loss=tf.keras.losses.sparse_categorical_crossentropy,
              metrics=["accuracy"])

# model=Sequential()
# model.add(Conv2D(64,(3,3),activation='relu',input_shape=(40,40,3)))
# model.add(Conv2D(64,(3,3),activation='relu'))
# model.add(Dropout(0.7))
# model.add(MaxPooling2D(pool_size=(2,2)))

# model.add(Conv2D(64,3,3,activation='relu'))
# model.add(Conv2D(64,3,3,activation='relu'))
# model.add(Dropout(0.7))
# model.add(MaxPooling2D(pool_size=(2,2)))


# model.add(Flatten())

# model.add(Dense(128))
# model.add(Dense(128))
          
# model.add(Dense(103))
# model.add(Activation('softmax'))
# model.compile(loss='sparse_categorical_crossentropy',optimizer='rmsprop', metrics=['accuracy'])

model.fit(xtrain,ytrain,epochs=20,validation_split=0.3)

import cv2
data=[]
predicted=[]
data1=[]
for i in range(18540,20549):
  dim=(250,250)
  img=cv2.imread('/content/drive/My Drive/Datasets/test/'+str(i)+'.jpg')
  resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
  data.append(resized)
  data1 = np.stack(data)
  features=model.predict(data1)
  predicted.append(np.argmax(features))
  data1=[]
  data=[]

predicted=np.stack(predicted)
predicted.shape
#predicted=np.stack(predicted)
c = np.savetxt('/content/drive/My Drive/Datasets/testnew.csv', predicted,fmt='%.2f', delimiter =', ')

from google.colab import drive
drive.mount('/content/drive')
