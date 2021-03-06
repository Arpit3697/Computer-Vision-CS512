import keras
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score
from keras import optimizers
from keras.models import Sequential
from keras.datasets import mnist
from keras.utils import np_utils
from keras.layers import Dense, Dropout,Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Activation
from tensorflow.keras.callbacks import LambdaCallback
from keras import backend as K
import tensorflow as tf
import time
import functools


    
def changeLabel(input):
  # We are using enumerate so we get index for each item
   for index, data in enumerate(input):
     # If the item is even we classify it as 0
     if data % 2 == 0:
       input[index] = 0
     # If the item is odd we classify it as 1
     else:
       input[index] = 1
   return input

def as_keras_metric(method):
     
     @functools.wraps(method)
     def wrapper(self, args, **kwargs):
         """ Wrapper for turning tensorflow metrics into keras metrics """
         value, update_op = method(self, args, **kwargs)
         K.get_session().run(tf.local_variables_initializer())
         with tf.control_dependencies([update_op]):
             value = tf.identity(value)
         return value
     return wrapper


img_rows = 28
img_cols = 28
precision = as_keras_metric(tf.metrics.precision)
recall = as_keras_metric(tf.metrics.recall)

# split data between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train[:55000]
y_train = y_train[:55000]

y_train = changeLabel(y_train)
y_test = changeLabel(y_test)

x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
input_shape = (img_rows, img_cols, 1)
  
#Trainig for 5 epochs
epochs = 5
 
# building a linear stack of layers with the sequential model
model = Sequential()
model.add(Conv2D(32, kernel_size=(5,5),input_shape=(28, 28, 1), activation = 'relu')) #Layer 1 consist of 32 filters of kernal size 5 X 5
model.add(MaxPooling2D(pool_size=(2, 2))) #pooling and downsample by a factor of 2
model.add(Conv2D(64, kernel_size=(5,5), activation = 'relu')) #Layer 2 consist of 64 filters of kernal size 5 X 5
model.add(MaxPooling2D(pool_size=(2, 2))) #pooling and downsample by a factor of 2
model.add(Dropout(0.4)) #droupout rate is 40%

# Flatten Layer
model.add(Flatten())

model.add(Dense(1))

#using sigmoid activation 
model.add(Activation("sigmoid"))

#using gradient descent optimizer and a learning rate of 0.001
sgd = optimizers.SGD(lr=0.001) 

# compile the sequential model
model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy', precision, recall])

# training the model and saving metrics in history
history = model.fit(x_train, y_train, epochs= epochs , validation_data=(x_test, y_test))


# plot for training accuracy 
figure1 = plt.figure()
plt.plot(history.history['acc'])
plt.title('Training model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train'])
figure1

# plot for training loss
figure2 = plt.figure()
plt.plot(history.history['loss'])
plt.title('Training model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train'])
figure2

# plot for testing set accuracy
figure3 = plt.figure()
plt.plot(history.history['val_acc'])
plt.title('Test set model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Test'])
figure3 

# plot for testing set loss
figure4 = plt.figure()
plt.plot(history.history['val_loss'])
plt.title('Test set model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Test'])
figure4

# plot for testing set precision
figure5 = plt.figure()
plt.plot(history.history['val_precision'])
plt.title('Test set model precision')
plt.ylabel('Precision')
plt.xlabel('Epoch')
plt.legend(['Test'])
figure5 

# plot for testing set recall
figure6 = plt.figure()
plt.plot(history.history['val_recall'])
plt.title('Test set model recall')
plt.ylabel('Recall')
plt.xlabel('Epoch')
plt.legend(['Test'])
figure6
#Evaluating model's performance
scores = model.evaluate(x_train, y_train, verbose = 1)
print("\n\n Loss and accuracy of final training step")
print('Train loss:', scores[0])
print('Train accuracy:', scores[1])

print("\n\n")
print("Evaluation of Testing set:\n\n")
eval_results = model.evaluate(x_test, y_test, steps=None)
print("Test Loss:" + str(eval_results[0]) + "\t"+"Test Accuracy:" + str(eval_results[1])+ "\t"+"Test Precision:" + str(eval_results[2])+"\t"+"Test Recall:" + str(eval_results[3]))
