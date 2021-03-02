import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from keras.utils import np_utils
from tensorflow.keras.models import load_model as lm
from video.img_utils import resize_img_list
from tensorflow.keras.applications.vgg19 import preprocess_input
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.layers import Dense, InputLayer, Dropout
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split


def create_model(training_mapping):
    x, y = load_data(training_mapping)
    x = resize_img_list(x, 224, 224)

    # Preprocessing input data -> Mejora el rendimiento
    x = preprocess_input(x)

    # Dividir aleatoriamente imgs en entrenamiento y validacion
    x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=0.3, random_state=42)

    # Construccion del modelo -> usa VGG16 pretrained model
    base_model = VGG19(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

    x_train = base_model.predict(x_train)
    x_valid = base_model.predict(x_valid)

    x_train = x_train.reshape(560, 7 * 7 * 512)  # 206 -> 70%
    x_valid = x_valid.reshape(240, 7 * 7 * 512)  # 89 -> 30%

    x_train = x_train / x_train.max()
    x_valid = x_valid / x_train.max()
    model = train_model(x_train, x_valid, y_train, y_valid)
    return model, base_model


def train_model(x_train, x_valid, y_train, y_valid):
    model = Sequential()
    model.add(InputLayer((7 * 7 * 512,)))  # input layer
    model.add(Dense(units=500, activation='relu'))  # hidden layer
    model.add(Dropout(0.5))  # adding dropout
    model.add(Dense(units=300, activation='relu'))  # hidden layer
    model.add(Dropout(0.5))  # adding dropout
    model.add(Dense(units=100, activation='relu'))  # hidden layer
    model.add(Dropout(0.5))  # adding dropout
    model.add(Dense(4, activation='softmax'))  # output layer

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=100, validation_data=(x_valid, y_valid))
    return model


def load_data(mapping_csv, is_training=True):
    data_location = "test"
    if is_training:
        data_location = "training"
    # Load data
    data = pd.read_csv(mapping_csv)
    # Array de imagenes -> Cada img es una matriz de pixeles (R,G,B)
    x = []
    for img_name in data.Image_ID:
        img = plt.imread('data/frames/slides_frames/'+data_location+'/' + img_name)
        x.append(img)
    x = np.array(x)
    y = np_utils.to_categorical(data.Class)
    return x, y


def save_model(model, url):
    model.save(url)


def load_model(url):
    return lm(url)
