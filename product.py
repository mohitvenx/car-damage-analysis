from pyrsistent import freeze



import json
import urllib.request
import numpy as np
import pickle as pk
import tensorflow as tf
from keras.models import load_model
from keras.applications.vgg16 import VGG16
from keras.applications.imagenet_utils import preprocess_input
from keras.utils import img_to_array, load_img, array_to_img
import keras.utils.data_utils
import cv2
import os
import json
import h5py
import urllib.request
import numpy as np
import pickle as pk
import keras
from IPython.display import Image, display, clear_output
from keras.models import Sequential, load_model
from keras.utils.data_utils import get_file
from keras.applications.vgg16 import VGG16
from keras.applications.resnet import ResNet50
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.data_utils import get_file
from damagearea_bbox import *
from damagearea_bbox import bounding_box






model1 = VGG16(weights = 'imagenet')
model2 = load_model("C:/Users/Admin/OneDrive/Desktop/damaged_cars/h5_files/ft_model_data1a.h5")
model3 = load_model("C:/Users/Admin/OneDrive/Desktop/damaged_cars/h5_files/ft_model_data2a.h5")
model4 = load_model("C:/Users/Admin/OneDrive/Desktop/damaged_cars/h5_files/ft_model_data3a.h5")
with open("C:/Users/Admin/OneDrive/Desktop/damaged_cars/h5_files/vgg16_cat_list.pk", 'rb') as f:
    cat_list = pk.load(f)

CLASS_INDEX = None
CLASS_INDEX_PATH = 'https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json'


def get_predictions(preds, top=5):
    global CLASS_INDEX
    if len(preds.shape) != 2 or preds.shape[1] != 1000:
        raise ValueError('`decode_predictions` expects '
                         'a batch of predictions '
                         '(i.e. a 2D array of shape (samples, 1000)). '
                         'Found array with shape: ' + str(preds.shape))
    if CLASS_INDEX is None:
        fpath = keras.utils.data_utils.get_file('imagenet_class_index.json', CLASS_INDEX_PATH, cache_subdir='models')
        CLASS_INDEX = json.load(open(fpath))
    arr = []
    for pred in preds:
        top_indices = pred.argsort()[-top:][::-1]
        indexes = [tuple(CLASS_INDEX[str(i)]) + (pred[i],) for i in top_indices]
        indexes.sort(key=lambda x: x[2], reverse=True)
        arr.append(indexes)
    return arr


def prepare_image_224(img_path):
    # urllib.request.urlretrieve(img_path, 'save.jpg')
    img = load_img(img_path, target_size=(224, 224))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x


def pipe1(img_224, model):
    print("Ensuring entered picture is a car...")
    out = model.predict(img_224)
    preds = get_predictions(out, top=5)
    for pred in preds[0]:
        if pred[0:2] in cat_list:
            return True  # "Successful. Proceeding to damage assessment..."
        return False  # "The entered image is a not a car. Please try again. Consider a different angle or lighting."


def prepare_img_256(img_path):
    # urllib.request.urlretrieve(img_path, 'save.jpg')
    img = load_img(img_path, target_size=(256, 256))
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape) / 255
    return x


def pipe2(img_256, model):
    print("Validating that damage exists....")
    pred = model.predict(img_256)
    if pred[0][0]<=0.5:
        return True #print("Validation complete - proceed to location and severity determination")
    else:
        return False #print ("Are you sure that your car is damaged? Please submit another picture of the damage.\nHint: Try zooming in/out, using a different angle or different lighting")  


def pipe3_loc(img_256, model):
    print("Determining location of damage...")
    pred = model.predict(img_256)
    pred_labels = np.argmax(pred, axis=1)
    d = {0: 'front', 1: 'rear', 2: 'side'}
    for key in d.keys():
        if pred_labels[0] == key:
            # print("Result: damage to {} of vehicle".format(d[key]))
            return d[key]
    # print("Location assessment complete.")


def pipe3_sev(img_256, model):
    print("Determining severity of damage...")
    pred = model.predict(img_256)
    pred_labels = np.argmax(pred, axis=1)
    d = {0: 'minor', 1: 'moderate', 2: 'severe'}
    for key in d.keys():
        if pred_labels[0] == key:
            # print("Result:{} damage".format(d[key]))
            return d[key]
    # print("Severity assessment complete.")




def pipe(img_path):
    img_224 = prepare_image_224(img_path)
    p1 = pipe1(img_224, model1)

    if p1 is False:
        result = {'pipe1': 'Car validation check: ',
                  'pipe1_result': 0,
                  'pipe1_message': {0: 'The entered image is a not a car. Please try again. ',
                                    1: 'Hint: Consider a different angle or lighting.'},
                  'pipe2': None,
                  'pipe2_result': None,
                  'pipe2_message': {0: None, 1: None},
                  'location': None,
                  'severity': None,
                  'final': 'Damage assessment unsuccessful!'}
        return result

    img_256 = prepare_img_256(img_path)
    p2 = pipe2(img_256, model2)

    if p2 is False:
        result = {'pipe1': 'Car validation check: ',
                  'pipe1_result': 1,
                  'pipe1_message': {0: None, 1: None},
                  'pipe2': 'Damage validation check: ',
                  'pipe2_result': 0,
                  'pipe2_message': {0: 'Are you sure that your car is damaged? Please try again.',
                                    1: 'Hint: Consider a different angle or lighting.'},
                  'location': None,
                  'severity': None,
                  'final': 'Damage assessment unsuccessful!'}
        return result

    
    x = pipe3_loc(img_256, model3)
    y = pipe3_sev(img_256, model4)
    
    result = {'pipe1': 'Car validation check: ',
              'pipe1_result': 1,
              'pipe1_message': {0: None, 1: None},
              'pipe2': 'Damage validation check: ',
              'pipe2_result': 1,
              'pipe2_message': {0: None, 1: None},
              'location': x,
              'severity': y,
              'final': 'Damage assessment complete!'}
    return result
