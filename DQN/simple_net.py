import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten
from generate_dataset import *

# as first layer in a sequential model:
model = Sequential()
model.add(Dense(10, input_shape=(3,)))
# now the model will take as input arrays of shape (*, 16)
# and output arrays of shape (*, 32)

# after the first layer, you don't need to specify
# the size of the input anymore:
model.add(Dense(10))
model.add(Activation('relu'))
model.add(Dense(2))
model.add(Activation('softmax'))

# For a binary classification problem
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

import numpy as np
# data = np.random.random((1000, 100))
# labels = np.random.randint(2, size=(1000, 1))

data = []
labels = []

for i in range(len(samples)):
    if samples[i].hit_num + samples[i].stand_num < 100:
        continue
    a, b, c = samples[i].state
    data.append([a, b, c])
    t = [0, 0]
    t[samples[i].action] = 1
    labels.append(t)

print('Training Data Size:', len(data))

print(labels)

model.fit(np.array(data), np.array(labels), epochs=10, batch_size=16)

test_data = np.array(data)
print('ndim = ', test_data[0:3].ndim, test_data[0:3].shape)
print('ndim = ', test_data[0:1], test_data[0:1].ndim, test_data[0:1].shape)
print('ndim = ', test_data[0:1].ndim, test_data[0:1].transpose().shape)

def act(a):
    if a[0] > a[1]:
        return 0
    else:
        return 1
model.predict(test_data[0:1])
num_right = 0
for i,s in enumerate(data):
    ss = np.array([s])
    a = model.predict(ss)
    print(s, a[0], act(a[0]))
    if act(a[0]) == act(labels[i]):
        num_right += 1

print(num_right, '/', len(data))

