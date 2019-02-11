import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten

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

model.fit(data, labels, epochs=10, batch_size=32)


