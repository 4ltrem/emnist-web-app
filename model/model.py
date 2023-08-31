import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt
from emnist import extract_training_samples
from emnist import list_datasets
from emnist import extract_test_samples
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.datasets import mnist
from keras.utils import np_utils as np
import tensorflowjs as tfjs

""" Obtaining the data """
(x_train, y_train) = extract_training_samples('byclass') 
(x_test, y_test) = extract_test_samples('byclass')

""" Preprocessing """
# reshape in the format [samples][width][height][channels]
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1).astype("float32")
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1).astype("float32")
# normalize inputs from 0-255 to 0-1
x_train /= 255
x_test /= 255
# one hot encoding categorical outputs
y_train = np.to_categorical(y_train)
y_test = np.to_categorical(y_test)

""" Creating the model """
classifier = Sequential()
# convolution layer 1
classifier.add(Conv2D(32, (3, 3), input_shape=(28, 28, 1), activation="relu"))
# max pooling layer 1
classifier.add(MaxPooling2D(pool_size=(2, 2)))
# convolution layer 2
classifier.add(Conv2D(32, (3, 3), activation="relu"))
# max pooling layer 2
classifier.add(MaxPooling2D(pool_size=(2, 2)))
# flattening
classifier.add(Flatten())
# add the ANN
classifier.add(Dense(units=128, activation="relu"))
classifier.add(Dense(units=62, activation="softmax"))
# compiling
classifier.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

classifier.summary()

# fit the model
history = classifier.fit(x_train, y_train, validation_data=(x_test, y_test), batch_size=32, epochs=10)

# model evaluation
scores = classifier.evaluate(x_test, y_test, verbose=0)
print("Error: {:.2f}%".format((1-scores[1])*100))

# save the model
tfjs.converters.save_keras_model(classifier, "model")

print(history.history.keys())

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.grid()
plt.show()

# summarize history for loss
plt.plot(classifier.history['loss'])
plt.plot(classifier.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.grid()
plt.show()