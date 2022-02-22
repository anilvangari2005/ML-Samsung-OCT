import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import keras.backend as K
from keras.models import load_model
import cv2
import h5py
from .vizgradcam.gradcam import create_grad_cam_viz, VizGradCAM, grad_image_preprocessing

def load_opticnet_model():
    print("load_opticnet_model: Begin")
    
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # path_weights = '/home/ubuntu/source/dev-anil/ML-Samsung-OCT/backend/FlaskApp/static/model/Optic_net-4_classes-Kermany2018.hdf5'
    path_weights = os.path.join(ROOT_DIR, "static/model/Optic_net-4_classes-Kermany2018.hdf5")
    print("Loading model from " + path_weights)

    weights = h5py.File(path_weights, 'r')
    
    print("load_opticnet_model: End")
    
    return load_model(weights)

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

def inference(imgFullPath):

    # img,weights,dataset

    #filename = '/static/test_images/CNV-1016042-1.jpeg'
    #filename = '/static/test_images/DME-1081406-1.jpeg'
    #filename = '/static/test_images/DRUSEN-1083159-1.jpeg'
    #filename = '/static/test_images/NORMAL-1017237-1.jpeg'
    weights = '/static/model/Optic_net-4_classes-Kermany2018.hdf5'
    dataset = 'Kermany2018'

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    #imgFullPath = path = os.path.join(ROOT_DIR + filename)
    weights = h5py.File(os.path.join(ROOT_DIR + weights), 'r')

    if dataset == 'Srinivasan2014':
        classes = ['AMD', 'DME', 'NORMAL']
    else:
        classes = ['CNV', 'DME', 'DRUSEN', 'NORMAL']

    processsed_img = image_preprocessing(imgFullPath)
    K.clear_session()
    #model = load_model(weights)
    
    preds = model.predict(processsed_img, batch_size = None, steps = 1)
   
    category = get_prediction(preds, classes)

    input_img, overlay, heatmap = create_grad_cam_viz(model, imgFullPath)

    cv2.imwrite('/home/ubuntu/source/dev-anil/ML-Samsung-OCT/backend/FlaskApp/static/output/overlay.jpeg', overlay)

    return category, input_img, overlay


model = load_opticnet_model()
