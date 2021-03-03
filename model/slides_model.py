import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

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


def compare_screens(slides_csv):
    data = pd.read_csv(slides_csv)
    changes_logs = []
   
    screen1 = None
    screen2 = None
    img_name1 = None
    img_name2 = None
    for i, c in data.iterrows():
        
        img = c['Image_ID']  
        c = c['Class']
        if c == 1 or c == 2:
            if i != 0:
                img_name2 = img
                screen2 = cv2.imread('data/frames/slides_frames/test/frame'+str(img_name2)+'.jpg')
                diff_img=cv2.subtract(screen1,screen2)
                w,h,c=diff_img.shape
                total_pixel_value_count=w*h*c*255
                percentage_match=(total_pixel_value_count -np.sum(diff_img))/total_pixel_value_count*100

                if percentage_match < 98.5:
                    changes_logs.append([img_name2, percentage_match])
                    print("Changed ======> ", percentage_match, img_name1, img_name2)
                screen1 = screen2
                img_name1 = img_name2
            else:
                img_name1 = img
                screen1 = cv2.imread('data/frames/slides_frames/test/frame'+str(img_name1)+'.jpg')
    return changes_logs



def are_screens_similar2(screen1, screen2):
    comparations = intersection(screen1, screen2) # Intersection of pixels between the one being processed and the one in dictionary
    return comparations > 1000


def are_screens_similar(lst1, lst2): 
    """
        A pixel is in lst2 if its colors are similar to any pixel in lst2 and color is not purple
    """
    count = 0
    for i in range(0, len(lst1)):
        for j in range(0, len(lst1[0])):
            if are_near_pixel_colors(lst1[i][j], lst2[i][j]):
                count += 1
                if count > 400000:
                    return True
            j += 2
        i += 1
    return False 


def are_near_pixel_colors(color_a, color_b):
    return are_near_single_colors(color_a[0], color_b[0]) and are_near_single_colors(color_a[1], color_b[1]) and are_near_single_colors(color_a[2], color_b[2])


def are_near_single_colors(color_a, color_b):
    return color_b -2 <= color_a <= color_b +2