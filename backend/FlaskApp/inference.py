import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import keras
import argparse
import keras.backend as K
from keras.models import load_model
import cv2
import h5py


def get_prediction(preds, classes):

    preds = preds.ravel()
    y = len(classes)

    top_prediction = -1.0
    top_prediction_class = "None"
    for i in range(y):
        if (preds[i] > top_prediction):
            top_prediction = preds[i]
            top_prediction_class = classes[i]
    
    x = ""
    for i in range(y):
        preds_rounded = np.around(preds, decimals=4)
        x = x + classes[i] + ": " + str(preds_rounded[i]) + "%"
        if i != (y - 1):
            x = x + ", "        
        else:
            None
    
    print(preds)
    print(x)
    print("top_prediction_class = " + top_prediction_class)
    
    return top_prediction_class

def image_preprocessing(img):
    img = cv2.imread(img)
    img = cv2.resize(img, (224,224))
    img = np.reshape(img, [1, 224, 224, 3])
    img = 1.0 * img/255

    return img

def inference():

    # img,weights,dataset

    #filename = '/static/test_images/CNV-1016042-1.jpeg'
    filename = '/static/test_images/DME-1081406-1.jpeg'
    # filename = '/static/test_images/DRUSEN-1083159-1.jpeg'
    # filename = '/static/test_images/NORMAL-1017237-1.jpeg'
    weights = '/static/model/Optic_net-4_classes-Kermany2018.hdf5'
    dataset = 'Kermany2018'

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    img = path = os.path.join(ROOT_DIR + filename)
    weights = h5py.File(os.path.join(ROOT_DIR + weights), 'r')

    if dataset == 'Srinivasan2014':
        classes = ['AMD', 'DME', 'NORMAL']
    else:
        classes = ['CNV', 'DME', 'DRUSEN', 'NORMAL']

    processsed_img = image_preprocessing(img)
    K.clear_session()
    model = load_model(weights)
    
    preds = model.predict(processsed_img, batch_size = None, steps = 1)  
   
    category = get_prediction(preds, classes)

    return category
