import numpy as np

from model.slides_model import load_data
from video.img_utils import resize_img_list
from tensorflow.keras.applications.vgg19 import preprocess_input


def get_text_data(base_model, test_mapping):
    test_x, test_y = load_data(test_mapping, False)
    test_x = resize_img_list(test_x, 224, 224)
    test_x = preprocess_input(test_x)
    test_x = base_model.predict(test_x)
    test_x = test_x.reshape(len(test_x), 7 * 7 * 512)
    test_x = test_x / test_x.max()
    return test_x, test_y


def get_scores(model, test_x, test_y):
    scores = model.evaluate(test_x, test_y)
    return scores


def get_predictions(model, test_x):
    predictions = np.argmax(model.predict(test_x), axis=-1)
    return predictions
