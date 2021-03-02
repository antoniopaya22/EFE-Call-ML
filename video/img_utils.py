import numpy as np

from skimage.transform import resize


def resize_img_list(img_list, x, y):
    image = []
    for i in range(0, img_list.shape[0]):
        a = resize(img_list[i], preserve_range=True, output_shape=(x, y, 3)).astype(int)
        image.append(a)
    return np.array(image)
