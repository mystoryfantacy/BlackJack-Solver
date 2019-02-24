import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten
from generate_dataset import *

# as first layer in a sequential model:
model = Sequential()
model.add(Dense(16, input_shape=(3,)))
# now the model will take as input arrays of shape (*, 16)
# and output arrays of shape (*, 32)

# after the first layer, you don't need to specify
# the size of the input anymore:
model.add(Activation('relu'))
model.add(Dense(32))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(8))
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


data_set = []
for i in range(len(samples)):
    if samples[i].hit_num + samples[i].stand_num < 100:
        continue
    a, b, c = samples[i].state
    data_set.append([a, b, c])
    t = [0, 0]
    t[samples[i].action] = 1
    data_set[-1] += t

real_len = len(data_set)
data_set = np.array(data_set)
data_set_tmp0 = np.zeros(data_set.shape)
data_set_tmp0[:][:] = data_set[:][:]
np.random.shuffle(data_set_tmp0)

data_set = np.concatenate((data_set, data_set_tmp0), axis = 0)

data = data_set[:, 0:3]
labels = data_set[:, 3:5]

print('Training Data Size:', len(data))

print(labels)

model.fit(data, labels, epochs=200, batch_size=16)

#model.fit(data, labels, epochs=50, batch_size=16)

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
for i,s in enumerate(data[0:real_len]):
    ss = np.array([s])
    a = model.predict(ss)
    # print(s, a[0], act(a[0]))
    if act(a[0]) == act(labels[i]):
        num_right += 1

print(num_right, '/', real_len)

model.save('BlackJack_keras_v0.h5')

